from flask import jsonify, request, current_app, url_for, g, session, Response
from app.models import PngCollect
from . import api

def checkAuth(func):
    def checkAuth(*args, **kwargs):
        if session.get('qq_token'):
            return func(*args, **kwargs)
        else:
            return jsonify({'status': 401, 'msg': 'permision deny'})
    return checkAuth

@api.route('/user/user_info')
def user_info():
    if 'qq_token' in session:
        data = {'id':session['uid'],'nickname':session['nickname'],'avatar':session['avatar']}
        return jsonify({'status':200, 'data': data, 'msg':'ok'})
    else:
        return jsonify({'status': 401, 'data': [], 'msg': 'access deny'})


@api.route('/user/get_collect')
@checkAuth
def get_collect():
    pc = PngCollect()
    res = pc.getCollect(pc, session['uid'])
    data = []
    for item in res:
        data.append({'id':item.id, 'png_id':item.png_id})
    return jsonify({'status': 200, 'data': data, 'msg': 'ok'})

@api.route('/user/add_collect/<int:png_id>')
def add_collect(png_id):
    pc = PngCollect()
    res = pc.collectAdd(pc, png_id, session['uid'])
    if res:
        return jsonify({'status':200, 'data': res, 'msg':'ok'})
    else:
        return jsonify({'status':401, 'data': [], 'msg':'permision deny'})
    pass

@api.route('/user/del_collect/<int:png_id>')
def del_collect(png_id):
    pc = PngCollect()
    res = pc.delCollect(pc, png_id)
    if res:
        return jsonify({'status': 200, 'msg': 'delete success'})
    else:
        return jsonify({'status': 500, 'msg': 'delete field'})
    pass