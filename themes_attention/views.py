from pyramid.view import view_config


@view_config(route_name='home', renderer='json')
def my_view(request):
    produto = request.db.produtos.find_one()
    print(produto)
    return {'project': {key:val for key, val in produto.items() if key != "_id"  }}
