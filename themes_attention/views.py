import colander
import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from bson.objectid import ObjectId
import pprint


class VideoPage(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    theme = colander.SchemaNode(colander.String())


class VideoViews:
    def __init__(self, request):
        self.request = request

    @property
    def home_form(self):
        schema = VideoPage()
        return deform.Form(schema, buttons=('submit',))
    
    @property
    def reqts(self):
        return self.home_form.get_widget_resources()

    @view_config(route_name='home', renderer='templates/home.jinja2')
    def home(self):
        form = self.home_form.render()
        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.home_form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(form=e.render())
            print(appstruct['name'], appstruct['theme'])
            video = self.request.db.videos.insert_one({'name': appstruct['name'], 
                                                       'theme': appstruct['theme'],
                                                       'thumbs_up': 0,
                                                       'thumbs_down': 0})
            
        return dict(form=form, videos=self.videos) 
    
    @property
    def videos(self):
        videos = []
        for video in self.request.db.videos.find():
            video['_id'] = str(video['_id'])
            videos.append(video)
            #print(str(video['_id']))
        return videos

    @view_config(route_name='thumbs_attent', request_method="POST")
    def thumbs_attention(self):
        print(self.request.POST)
        _id = self.request.POST['_id']
        video = self.request.db.videos.find_one({'_id': ObjectId(_id)})
        pprint.pprint(video)
        if 'thumbs_up' in self.request.POST:
            thumbs_up = int(self.request.POST['thumbs_up'])
            resp = self.request.db.videos.update_one({'_id': ObjectId(_id)}, {'$set': {'thumbs_up': video['thumbs_up'] + thumbs_up }})
            pprint.pprint(resp)
        else:
            thumbs_down = int(self.request.POST['thumbs_down'])
            resp = self.request.db.videos.update_one({'_id': ObjectId(_id)}, {'$set': {'thumbs_down': video['thumbs_down'] + thumbs_down }})
            pprint.pprint(resp)
    #    if 'submit' in self.request.params:
    #        controls = self.request.POST.items()
    #        try:
    #            appstruct = self.home_form.validate(controls)
    #        except deform.ValidationFailure as e:
    #            # Form is NOT valid
    #            return dict(form=e.render())
    #    print(appstruct['name'], appstruct['theme'])
        
        url = self.request.route_url('home')
        return HTTPFound(url)  

#@view_config(route_name='home', renderer='json')
#def my_view(request):
#    produto = request.db.produtos.find_one()
#    print(produto)
#    return {'project': {key:val for key, val in produto.items() if key != "_id"  }}
