from flask import Blueprint
import hashlib
from flask import request, g, current_app
from bson.objectid import ObjectId
from eve.methods.post import post_internal
from eve.auth import TokenAuth
import json
import datetime
import random
import string
import datetime
import pytz

def get_hash(source):
    m = hashlib.md5()
    m.update(source.encode())
    return m.hexdigest()

class CurrentTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method): 
        account_id = request.headers.get('account-id')
        token = request.headers.get('token')
        if account_id == None or token == None:
            return None
        tokens = current_app.data.driver.db['tokens']
        token_found = tokens.find_one({'account_id' : ObjectId(account_id), 'token': token})
        if token_found != None:
            self.set_request_auth_value(ObjectId(account_id)) 
        return token_found

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods = ['POST'])
def register_account():
    email = request.json.get('email')
    password = request.json.get('password')
    accounts = current_app.data.driver.db['accounts']
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
    new_user = {
        'email' : email,
        'account_id' : ObjectId(insert_result.inserted_id)
    }
    post_internal('users', new_user)
    result_code = 200
    result = {'result' : 'ok', 'account-id' : str(insert_result.inserted_id)}

    return json.dumps(result), result_code

@auth_blueprint.route('/checktoken', methods = ['POST'])
def check_token():
    utc=pytz.UTC
    accountId = request.json.get('account-id')
    token = request.json.get('token')
    tokens = current_app.data.driver.db['tokens']
    filter = {'account_id' : ObjectId(accountId), 'token': token}
    token_found = tokens.find_one(filter)
    now = datetime.datetime.now()
    if token_found == None: 
        result_code = 406
        result = {'result' : 'no token found'}
    elif token_found['expires'].replace(tzinfo=utc) < now.replace(tzinfo=utc):
        result_code = 406
        result = {'result' : 'token expired'}
    else:
        result_code = 200
        result = {'result' : 'ok'}
    return json.dumps(result), result_code

@auth_blueprint.route('/updatetoken', methods = ['POST'])
def update_token():
    email = request.json.get('email')
    passwordhash = request.json.get('passwordhash')
    accounts = current_app.data.driver.db['accounts']
    found_account = accounts.find_one({'email' : email, 'passwordhash' : passwordhash})
    if found_account == None:
        result_code = 406
        result = {'result' : 'User email or password doesn\'t match', 'user_id' : '', 'token' : '', 'expires' : ''}
    else:
        tokens = current_app.data.driver.db['tokens']
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