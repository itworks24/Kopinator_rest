MONGO_URI = "mongodb://kopinator-test-user:zegdcPxztENMtlC@92.53.100.60:27017/kopinator-test"

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
    'users': {
        'schema': {
            'useremail': {
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
        'shema':{
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