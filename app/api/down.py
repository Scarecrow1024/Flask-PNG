from flask import jsonify, session
from . import api
from task import down, getDownLink

def auth(func):
    def checkAuth(*args, **kwargs):
        if session.get('qq_token'):
            func()
        else:
            return jsonify({'status': 401, 'msg': 'permision deny'})
    return checkAuth

@api.route('/down/<bianhao>')
def dodown(bianhao):
    task = down.delay(bianhao)
    return jsonify({'jobid': task.id})

@api.route('/down/get-result/<bianhao>')
def getResult(bianhao):
    res = getDownLink(bianhao)
    if res is not None:
        response = {
            'status': 200,
            'state': 'Success',
            'data': res
        }
    else:
        response = {
            'status': 100,
            'data': [],
            'state': 'Pending...'
        }
    return jsonify(response)

@api.route('/down/status/<task_id>')
def taskstatus(task_id):
    task = down.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'status': 200,
            'state': task.state,
            'data': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'data': task.info,
            'status': 200
        }
        # if 'result' in task.info:
        #     response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'data': task.info,
            'status': '500',  # this is the exception raised
        }
    return jsonify(response)
