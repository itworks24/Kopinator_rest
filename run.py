from eve import Eve
from eve_swagger import swagger, add_documentation
import auth
import balance

app = Eve(auth = auth.CurrentTokenAuth)
app.register_blueprint(swagger)
app.register_blueprint(auth.auth_blueprint, url_prefix='/auth')

app.on_inserted_records += balance.on_inserted_records
app.on_replaced_records += balance.on_replaced_records
app.on_updated_records += balance.on_updated_records
app.on_deleted_item_records += balance.on_deleted_item_records

# required. See http://swagger.io/specification/#infoObject for details.
app.config['SWAGGER_INFO'] = {
    'title': 'Kopinator rest API',
    'version': '0.0.1',
    'description': 'an API description',
    'termsOfService': 'my terms of service',
    'contact': {
        'name': 'vladas.j',
        'url': 'https://github.com/vladasj'
    },
    'license': {
        'name': 'BSD',
        'url': 'https://github.com/pyeve/eve-swagger/blob/master/LICENSE',
    },
    'schemes': ['http'],
}

@app.after_request
def after_request(response):
    del response.headers['www-authenticate']
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    