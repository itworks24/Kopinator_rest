from eve import Eve
from eve_swagger import swagger, add_documentation
from eve.auth import TokenAuth
from flask import request, g
import json
import hashlib
import random
import string
import datetime

def get_hash(source):
    m = hashlib.md5()
    m.update(source.encode())
    return m.hexdigest()

def get_db_prefix(source):
    return 'userdb_' + source.replace('.', '_')

def get_current_user(token):
    pass

class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        print(token)
        email, token = token.split(':')
        tokens = app.data.driver.db['tokens']
        token_found = tokens.find_one({'email' : email, 'token': token})
        g.user_id = email
        return token_found

##app = Eve(auth = TokenAuth)
app = Eve()
app.register_blueprint(swagger)

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

@app.route('/register', methods = ['POST'])
def register_account():
    email = request.json.get('email')
    password = request.json.get('password')
    accounts = app.data.driver.db['accounts']
    accounts_found = accounts.find_one({'email' : email})
    if accounts_found != None:
        result_code = 406
        result = {'result' : 'User alredy exists'}
    else:
        try:
            insert_result = accounts.insert_one({'email' : email, 'passwordhash' : get_hash(password)})
            result_code = 200
            result = {'result' : 'Ok'}
        except:
            result_code = 501
            result = {'result' : 'Internal DB error'}
    return json.dumps(result), result_code

@app.route('/updatetoken', methods = ['POST'])
def update_token():
    email = request.json.get('email')
    passwordhash = request.json.get('passwordhash')
    accounts = app.data.driver.db['accounts']
    found_account = accounts.find_one({'email' : email, 'passwordhash' : passwordhash})
    if found_account == None:
        result_code = 406
        result = {'result' : 'User email or password doesn\'t match', 'token' : ''}
    else:
        tokens = app.data.driver.db['tokens']
        try:
            new_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
            insert_result = tokens.insert_one({'email' : email, 
                                                'token' : new_token,
                                                'expires' : datetime.datetime.now() + datetime.timedelta(days=3)})
            result_code = 200
            result = {'result' : 'Ok', 'token' : new_token}
        except Exception as e:
            print(str(e)) 
            result_code = 501
            result = {'result' : 'Internal DB error', 'token' : ''}
    return json.dumps(result), result_code

def pre_get_auth(resource, request, lookup):
    #print(g.user_id)
    #email = g.user_id
    email = 'zv@itworks24.ru'
    users = app.data.driver.db['users']
    user = users.find_one({'email': email})
    print(user)
    if resource == 'users':
        lookup.update({'email': email})
    else:
        lookup.update({'user': user['_id']})    

if __name__ == '__main__':
    app.on_pre_GET += pre_get_auth
    app.run(host='0.0.0.0')
    