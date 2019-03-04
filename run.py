from eve import Eve
from eve_swagger import swagger, add_documentation

app = Eve()
app.register_blueprint(swagger)

# required. See http://swagger.io/specification/#infoObject for details.
app.config['SWAGGER_INFO'] = {
    'title': 'Kopinator rest API',
    'version': '0.0.1',
    'description': 'an API description',
    'termsOfService': 'my terms of service',
    'contact': {
        'name': 'vladas',
        'url': 'https://github.com/vladasj'
    },
    'license': {
        'name': 'BSD',
        'url': 'https://github.com/pyeve/eve-swagger/blob/master/LICENSE',
    },
    'schemes': ['http', 'https'],
}

if __name__ == '__main__':
    app.run(host='0.0.0.0')