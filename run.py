from eve import Eve
from eve.methods.post import post_internal
from eve_swagger import swagger, add_documentation
from eve.auth import TokenAuth, BasicAuth
from flask import request, g
import json
import hashlib
import random
import string
import datetime
from bson.objectid import ObjectId

def get_hash(source):
    m = hashlib.md5()
    m.update(source.encode())
    return m.hexdigest()

def get_db_prefix(source):
    return 'userdb_' + source.replace('.', '_')

class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method): 
        print(request.headers.get('account-id'), request.headers.get('token'))
        account_id = request.headers.get('account-id')
        token = request.headers.get('token')
        if account_id == None or token == None:
            return None
        tokens = app.data.driver.db['tokens']
        token_found = tokens.find_one({'account_id' : ObjectId(account_id), 'token': token})
        if token_found != None:
            self.set_request_auth_value(ObjectId(account_id)) 
        return token_found

app = Eve(auth = TokenAuth)
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
        return json.dumps(result), result_code

    new_account = {
        'email' : email,
        'passwordhash' : get_hash(password)
    }
    insert_result = accounts.insert_one(new_account)
    print(insert_result)
    new_user = {
        'email' : email,
        'account_id' : ObjectId(insert_result.inserted_id)
    }
    post_internal('users', new_user)
    result_code = 200
    result = {'result' : 'ok', 'account-id' : str(insert_result.inserted_id)}

    return json.dumps(result), result_code

@app.route('/updatetoken', methods = ['POST'])
def update_token():
    email = request.json.get('email')
    passwordhash = request.json.get('passwordhash')
    accounts = app.data.driver.db['accounts']
    found_account = accounts.find_one({'email' : email, 'passwordhash' : passwordhash})
    if found_account == None:
        result_code = 406
        result = {'result' : 'User email or password doesn\'t match', 'user_id' : '', 'token' : '', 'expires' : ''}
    else:
        tokens = app.data.driver.db['tokens']
        filter = {'account_id' : found_account['_id']}
        token_found = tokens.find_one(filter)
        expires = datetime.datetime.now() + datetime.timedelta(days=3)
        if token_found == None:
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(25))
            insert_result = tokens.insert_one({'account_id' : found_account['_id'], 
                                                'token' : token,
                                                'expires' : expires})
        else:
            token = token_found['token']
            insert_result = tokens.update_one(filter,
                                                {'$set': {'expires' : expires}})
        result_code = 200
        result = {'result' : 'ok', 'account-id' : str(found_account['_id']), 'token' : token, 'expires' : expires.strftime("%d.%m.%Y %H:%M:%S")}
        
    return json.dumps(result), result_code

@app.after_request
def after_request(response):
    del response.headers['www-authenticate']
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    