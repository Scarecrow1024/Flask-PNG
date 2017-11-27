from flask import jsonify, request, current_app, session, url_for, Markup, redirect, g
from flask_oauthlib.client import OAuth
from app.models import User, User_qq
from app import db
from . import api
import json

oauth = OAuth(current_app)
qq = oauth.remote_app(
    'qq',
    consumer_key='*',
    consumer_secret='*',
    base_url='https://graph.qq.com',
    request_token_url=None,
    request_token_params={'scope': 'get_user_info'},
    access_token_url='/oauth2.0/token',
    authorize_url='/oauth2.0/authorize',
)

def json_to_dict(x):
    '''OAuthResponse class can't not parse the JSON data with content-type
    text/html, so we need reload the JSON data manually'''
    if x.find('callback') > -1:
        pos_lb = x.find('{')
        pos_rb = x.find('}')
        x = x[pos_lb:pos_rb + 1]
    try:
        return json.loads(x, encoding='utf-8')
    except:
        return x

def update_qq_api_request_data(data={}):
    '''Update some required parameters for OAuth2.0 API calls'''
    defaults = {
        'openid': session['openid'],
        'access_token': session['qq_token'][0],
        'oauth_consumer_key': current_app.config['QQ_APP_ID'],
    }
    defaults.update(data)
    return defaults

@api.route('/')
def index():
    return Markup('''<meta property="qc:admins" '''
                  '''content="226526754150631611006375" />''')


@api.route('/user_info')
def get_user_info():
    if 'qq_token' in session:
        user = User_qq.query.filter_by(qq_openid=session['openid']).first()
        if user is None:
            data = update_qq_api_request_data()
            resp = qq.get('/user/get_user_info', data=data)
            userinfo = json.loads(resp.data.decode())
            user = User()
            user.username = userinfo['nickname']
            user.avatar = userinfo['figureurl_qq_2']
            user.access_token = session['qq_token'][0]
            user.reg_ip = request.remote_addr
            db.session.add(user)
            db.session.commit()
            if user.id:
                user_qq = User_qq()
                user_qq.qq_openid = session['openid']
                user_qq.uid = user.id
                db.session.add(user_qq)
                db.session.commit()
                data = {'msg': 'ok', 'stats': 0,
                        'data': {'id': user.id, 'nickname': userinfo['nickname'], 'avatar': userinfo['figureurl_qq_2']}}
                session['uid'] = user.id
                session['nickname'] = userinfo['nickname']
                session['avatar'] = userinfo['figureurl_qq_2']
                return jsonify(data)
        user = User.query.filter_by(access_token=session['qq_token'][0]).first()
        data = {'msg': 'ok', 'stats': 200, 'data': {'id':user.id,'nickname':user.username,'avatar':user.avatar}}
        session['uid'] = user.id
        session['nickname'] = user.username
        session['avatar'] = user.avatar
        return jsonify(data)
    return redirect('/api/login')


@api.route('/login')
def login():
    return qq.authorize(callback='http://127.0.0.1:5000/api/login/authorized')


@api.route('/logout')
def logout():
    session.pop('qq_token', None)
    session.pop('openid', None)
    session.pop('uid', None)
    session.pop('nickname', None)
    session.pop('avatar', None)
    return redirect('/api/user_info')

@api.route('/login/authorized')
def authorized():
    resp = qq.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['qq_token'] = (resp['access_token'], '')
    resp = qq.get('/oauth2.0/me', {'access_token': session['qq_token'][0]})
    resp = resp.data.decode()
    openid = resp.split(':')[2].split('}')[0]
    #return openid
    session['openid'] = openid.replace('"', "")
    return redirect('/api/user_info')


@qq.tokengetter
def get_qq_oauth_token():
    return session.get('qq_token')