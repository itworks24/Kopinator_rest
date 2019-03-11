import datetime

MONGO_URI = "mongodb://kopinator-test-user:zegdcPxztENMtlC@92.53.100.60:27017/kopinator-test"

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

X_DOMAINS = ['http://localhost:8000',  # The domain where Swagger UI is running
             'http://editor.swagger.io',
             'http://petstore.swagger.io',
             'https://inspector.swagger.io']
X_HEADERS = ['Content-Type', 'If-Match']  # Needed for the "Try it out" buttons

TRANSPARENT_SCHEMA_RULES = True

DEBUG = True

AUTH_FIELD = 'account_id'

DOMAIN = {
    'users': {
        'schema': {
            'email': {
                'type': 'string',
                'required': True,
                'unique_to_user': True,
                'regex': '\A[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}'
            },
            'firstname': {
                'type': 'string',
                'required': True,
                'default': 'Vasia'
            },
            'lastname': {
                'type': 'string',
                'required': False,
                'default': 'Petrov'
            },
            'account_id':{
                'type': 'objectid', 
                'required': True,    
            }
        }
    },
    'recordpatterns':{
        'schema':{
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
                'default': datetime.datetime.now()
            },
            'duetodate':{
                'type': 'datetime',
            },
        }
    },
    'records': {
        'schema': {
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
            'date':{
                'type': 'datetime',
                'required': True,
                'default': datetime.datetime.now()
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