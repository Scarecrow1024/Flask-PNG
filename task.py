import oss2, requests
from celery import Celery
from app import create_app
from flask import jsonify
import pymysql, json, hashlib, os, time

app = create_app('default')

celery = Celery('task', backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])

auth = oss2.Auth('*', '*')
service = oss2.Service(auth, 'http://oss-cn-hangzhou.aliyuncs.com')
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'demo-source')


def add_together(a, b):
    time.sleep(10)
    return jsonify({'data': a + b})


def getAccount():
    db = pymysql.connect("localhost", "root", "", "flaskpng")
    cursor = db.cursor()
    sql = "select cookie from account where current_down<max_down"
    cursor.execute(sql)
    res = cursor.fetchone()
    return res[0]

def getPng(bianhao):
    db = pymysql.connect("localhost", "root", "", "flaskpng")
    cursor = db.cursor()
    sql = "select cdn_url from png where bianhao='"+bianhao+"'"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

def getDownLink(bianhao):
    png = getPng(bianhao)
    if png is not None:
        return getOssLink(png)
    else:
        return None
    pass

@celery.task()
def down(bianhao):
    png = getPng(bianhao)
    if png is not None:
        return getOssLink(png)
    cookie = getAccount()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0)',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://www.51yuansu.com',
        'Cache-Control': 'no-cache',
        'Host': 'www.51yuansu.com',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Referer': 'http://www.51yuansu.com'
    }
    proxies = {
        'http': 'http://127.0.0.1:38251',
    }
    res = requests.get('http://www.51yuansu.com/index.php?m=ajax&a=down&id='+bianhao, headers=headers, proxies=proxies)
    url = json.loads(res.text)['url']
    localSave(url, bianhao)

def uploadOss(img, path):
    with open(img, 'rb') as fileobj:
        result = bucket.put_object(path, fileobj, headers={'Content-Type': 'application/octst-stream'})
        return result.status

def localSave(url, bianhao):
    res = requests.get(url)
    s = hashlib.md5()
    s.update(bianhao.encode('utf-8'))
    md5 = s.hexdigest()
    path = md5[0:2] + '/' + md5[2:4]
    content = res.content
    s = hashlib.md5()
    s.update(url.encode('utf-8'))
    name = s.hexdigest()
    if os.path.exists("D:/Python/demo/tmp/img/" + path) is not True:
        os.makedirs("D:/Python/demo/tmp/img/" + path)
    img_name = os.path.join("D:/Python/demo/tmp/img/" + path, name + '.jpg')
    with open(img_name, 'wb') as pic:
        pic.write(content)
    pathname = path+'/'+name+'.png'
    status = uploadOss(img_name, pathname)
    if status == 200:
        db = pymysql.connect("localhost", "root", "", "flaskpng")
        cursor = db.cursor()
        sql = "update png set cdn_url = '"+path+'/'+name+'.png'+"' where bianhao='"+bianhao+"'"
        cursor.execute(sql)
        db.commit()
        sing_url = bucket.sign_url('GET', pathname, 180)
        print({'down-link':'/api/down/get-result/'+bianhao,'sing_url':sing_url})
        return sing_url
    else:
        return {'status': 406, 'msg': '上传oss失败'}

def getOssLink(obj):
    sing_url = bucket.sign_url('GET', obj, 180)
    return sing_url

if __name__ == "__main__":
    print(down('lvrnwubifa'))
