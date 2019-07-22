import datetime
from balance import income, expenses

MONGO_URI = "mongodb://kopinator-test-user:zegdcPxztENMtlC@127.0.0.1:27017/kopinator-test"

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

X_DOMAINS = ['http://localhost:8000',
             'http://editor.swagger.io',
             'http://petstore.swagger.io',
             'https://inspector.swagger.io']
X_HEADERS = ['Content-Type', 'If-Match']

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
        },
        'RESOURCE_METHODS':['GET'],
        'ITEM_METHODS':['GET', 'PATCH'],
    },
    'recordpatterns':{
        'schema':{
            'recordtype': {
                'type': 'string',
                'required': True,
                'allowed': [income, expenses],
                'default': 'income'
            }, 
            'amount': {
                'type': 'float',
                'required': True,
            },
            'fromdate':{
                'type': 'datetime',
                'default': datetime.datetime.utcnow()
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
                'allowed': [income, expenses],
                'default': 'income'
            }, 
            'amount': {
                'type': 'float',
                'required': True,
            },
            'date' : {
                'type': 'datetime',
                'required': True,
                'default': datetime.datetime.utcnow()
            },
            'pattern': {
                'type': 'objectid', 
                'data_relation': {
                    'resource': 'recordpatterns',
                    'field': '_id', 
                    'embeddable': True
                }    
            },
            'comment' : {
                'type': 'string'    
            }
        }
    },
    'balance': {
        'schema': {
            'date': {
                'type': 'datetime'
            }, 
            'income' : {
                'type': 'float'
            },
            'expenses' : {
                'type': 'float'
            },
            'balance': {
                'type': 'float'
            },
        },
        'RESOURCE_METHODS':['GET', 'POST'],
        'ITEM_METHODS':['GET'],
    }
}