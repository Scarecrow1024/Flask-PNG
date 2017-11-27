from flask import jsonify, request, current_app
from elasticsearch import Elasticsearch
from . import api

@api.route('/search')
def search():
    app = current_app._get_current_object()
    ES_HOST = app.config['ES_HOST']
    ES_PORT = app.config['ES_PORT']
    """
    @page: 第几页
    @kw: 关键词
    @cat_1: 一级分类
    @cat_2: 二级分类
    @sort: 排序 1=>综合排序 2=>下载量排序 3=>最新排序
    :return: json
    """
    page = request.args.get('page', 1, type=int)
    kw = request.args.get('kw', None, type=str)
    cat_1 = request.args.get('cat_1', None, type=int)
    cat_2 = request.args.get('cat_2', None, type=int)
    sort = request.args.get('sort', 1, type=int)
    es = Elasticsearch(host=ES_HOST, port=ES_PORT)
    should = []
    if kw is not None:
        should.append({
            'match': {
                'title': kw
            }
        })
        should.append({
            'match': {
                'attr': kw
            }
        })
    if cat_1 is not None:
        should.append({
            'match': {
                'cat_1': cat_1
            }
        })
    if cat_2 is not None:
        should.append({
            'match': {
                'cat_1': cat_2
            }
        })
    # 根据sort字段排序
    _sort = {
        1: '_score',
        2: 'down',
        3: 'fav'
    }
    sortBy = {
        _sort.get(sort): {
            'order': 'desc'
        }
    }
    # 搜索条件
    body = {
        'query': {
            'bool': {
                'should': should
            }
        },
        'sort':sortBy,
        'from': (page-1)*10,
        'size': 10
    }
    filter_path = ['hits.total', 'hits.hits._source.bianhao', 'hits.hits._source.title', 'hits.hits._source.attr', 'hits.hits._source.url',
                   'hits.hits._source.format', 'hits.hits._source.width', 'hits.hits._source.height']
    res = es.search(index='png', doc_type='contact', body=body, filter_path=filter_path)
    data = {'msg':'ok','stats':200,'data':res['hits']['hits'],'total':res['hits']['total']}
    return jsonify(data)


@api.route('/detail/<int:id>')
def detail(id):
    app = current_app._get_current_object()
    ES_HOST = app.config['ES_HOST']
    ES_PORT = app.config['ES_PORT']
    es = Elasticsearch(host=ES_HOST, port=ES_PORT)
    body = {
        'query': {
            'ids': {
                'type': 'contact',
                'values': [
                    id
                ]
            }
        }
    }
    filter_path = ['hits.total', 'hits.hits._source.bianhao', 'hits.hits._source.title', 'hits.hits._source.attr',
                   'hits.hits._source.url',
                   'hits.hits._source.format', 'hits.hits._source.width', 'hits.hits._source.height']
    res = es.search(index='png', doc_type='contact', body=body, filter_path=filter_path)
    data = {'msg': 'ok', 'stats': 200, 'data': res['hits']['hits']}
    return jsonify(data)
