import colander
import deform
from bson.objectid import ObjectId
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


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
            video = self.request.db.videos.insert_one({'name': appstruct['name'],
                                                       'theme': appstruct['theme'],
                                                       'thumbs_up': 0,
                                                       'thumbs_down': 0,
                                                       'thumbs_msg': 'Thumbs up'})
            self.create_theme_if_not_exists(appstruct['theme'])

        return dict(form=form, videos=self.videos)

    @property
    def videos(self):
        videos = []
        for video in self.request.db.videos.find():
            video['_id'] = str(video['_id'])
            videos.append(video)
        return videos

    @view_config(route_name='thumbs_attent', request_method="POST")
    def thumbs_attention(self):
        _id = self.request.POST['_id']
        video = self.request.db.videos.find_one({'_id': ObjectId(_id)})
        if 'thumbs_up' in self.request.POST:
            thumbs_up = int(self.request.POST['thumbs_up'])
            resp = self.request.db.videos.update_one({'_id': ObjectId(_id)},
                                                     {'$set': {'thumbs_up': video['thumbs_up'] + thumbs_up,
                                                               'thumbs_msg': 'Thumbs down'}})
        else:
            thumbs_down = int(self.request.POST['thumbs_down'])
            resp = self.request.db.videos.update_one({'_id': ObjectId(_id)},
                                                     {'$set': {'thumbs_down': video['thumbs_down'] + thumbs_down,
                                                               'thumbs_msg': 'Thumbs up'}})

        self.update_theme_score(video['theme'])

        url = self.request.route_url('home')
        return HTTPFound(url)

    def create_theme_if_not_exists(self, theme_name):
        """Theme is case sensitive"""
        theme = self.request.db.themes.find_one({'name': theme_name})
        if not theme:
            print("insering theme")
            self.request.db.themes.insert_one({'name': theme_name, 'score': 0})

    def update_theme_score(self, theme):
        videos = self.request.db.videos.find(
            {'theme': theme}, {'thumbs_up': 1, 'thumbs_down': 1})
        scores = [(video['thumbs_up'] - (video['thumbs_down']/2))
                  for video in videos]
        score = sum(scores)
        self.request.db.themes.update_one(
            {'name': theme}, {'$set': {'score': score}})

    @view_config(route_name='list_themes', renderer="templates/list_themes.jinja2")
    def list_themes(self):
        themes = self.request.db.themes.find(
            {'$query': {}, '$orderby': {'score': -1}})
        return {'themes': list(themes)}
