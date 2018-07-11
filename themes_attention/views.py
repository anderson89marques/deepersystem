import colander
import deform
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
        videos = [{'name': "Pyramid", 'theme': 'DEV', 'id': 1}, 
                  {'name': "SOAD", 'theme': 'MUSIC',  'id': 2},
                  {'name': "IRON MAIDEN", 'theme': 'MUSIC', 'id': 3}]
        return dict(form=form, videos=videos)   

    def create_video(self):
        form = self.home_form.render()
        return dict(form=form)   

#@view_config(route_name='home', renderer='json')
#def my_view(request):
#    produto = request.db.produtos.find_one()
#    print(produto)
#    return {'project': {key:val for key, val in produto.items() if key != "_id"  }}
