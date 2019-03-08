MONGO_URI = "mongodb://kopinator-test-user:zegdcPxztENMtlC@92.53.100.60:27017/kopinator-test"

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

X_DOMAINS = ['http://localhost:8000',  # The domain where Swagger UI is running
             'http://editor.swagger.io',
             'http://petstore.swagger.io',
             'https://inspector.swagger.io']
X_HEADERS = ['Content-Type', 'If-Match']  # Needed for the "Try it out" buttons

TRANSPARENT_SCHEMA_RULES = True

DOMAIN = {
    'users': {
        'schema': {
            'email': {
                'type': 'string',
                'minlength': 5,
                'maxlength': 255,
                'required': True,
                'unique': True,
            },
            'firstname': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 50,
                'required': True,
            },
            'lastname': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 50,
                'required': False,
            },
            'active': {
                'type': 'boolean',
                'default': True
            }
        }
    },
    'recordpatterns':{
        'schema':{
            'user': {
                'type': 'objectid', 
                'required': True,
                'data_relation': {
                    'resource': 'users',
                    'field': '_id', 
                    'embeddable': True
                 }
            },
            'recordtype': {
                'type': 'string',
                'required': True,
                'allowed': ['income', 'expenses'],
                'default': 'income'
            }, 
            'amount': {
                'type': 'float',
                'required': True,
            },
            'fromdate':{
                'type': 'datetime',
            },
            'duetodate':{
                'type': 'datetime',
            },
        }
    },
    'records': {
        'schema': {
            'user': {
                'type': 'objectid', 
                'data_relation': {
                    'resource': 'users',
                    'field': '_id', 
                    'embeddable': True
                 }
            },
            'recordtype': {
                'type': 'string',
                'required': True,
                'allowed': ['income', 'expenses']
            }, 
            'amount': {
                'type': 'float',
                'required': True,
            },
            'date':{
                'type': 'datetime',
                'required': True,
            },
            'pattern':{
                'type': 'objectid', 
                'data_relation': {
                    'resource': 'recordpatterns',
                    'field': '_id', 
                    'embeddable': True
                }    
            }
        }
    }
}