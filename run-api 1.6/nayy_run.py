#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, send_file
from tool import *
from datetime import timedelta
import re
app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(minutes=5)


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/sukebei', methods=['GET'])
def search_sukebei():
    if request.method == 'GET':
        name = request.args.get('search')
        category = request.args.get('category')
        user = request.args.get('user')

        nyaa_search = NyaaSearch('https://sukebei.nyaa.si/', search_time=1)
        nyaa_search.set_content(name)
        nyaa_search.set_user(user)
        if category:
            nyaa_search.set_category(category)
        nyaa_search.set_save()
        out = nyaa_search.running()
        if out == 4:
            return '(⊙﹏⊙)，没找到，换个关键词试试？'
        return app.send_static_file(f"{nyaa_search.return_save()}.xml")


@app.route('/nyaa', methods=['GET'])
def search_nyaa():
    if request.method == 'GET':
        name = request.args.get('search')
        category = request.args.get('category')
        user = request.args.get('user')

        nyaa_search = NyaaSearch('https://nyaa.si/', search_time=1)
        nyaa_search.set_content(name)
        nyaa_search.set_user(user)
        if category:
            nyaa_search.set_category(category)
        nyaa_search.set_save()
        out = nyaa_search.running()
        if out == 4:
            return '(⊙﹏⊙)，没找到，换个关键词试试？'
        return app.send_static_file(f"{nyaa_search.return_save()}.xml")


@app.route("/download", methods=['GET'])
def file_download():
    file_name = request.args.get("filename")
    if not file_name:
        return '文件名为空？'
    if re.match(r'^/download/[0-9]*\.torrent', file_name):
        re_ = requests.get('https://nyaa.si'+file_name)
        with open(f'static/{file_name}', 'wb+') as f:
            f.write(re_.content)
        response = make_response(send_file(f'static/{file_name}'))
        response.headers["Content-Disposition"] = "attachment; filename={};".format(f'static/{file_name}')
        return response
    return '格式匹配错误！'


@app.route("/download2", methods=['GET'])
def file_download2():
    file_name = request.args.get("filename")
    if not file_name:
        return '文件名为空？'
    if re.match(r'^/download/[0-9]*\.torrent', file_name):
        re_ = requests.get('https://sukebei.nyaa.si'+file_name)
        with open(f'static/{file_name}', 'wb+') as f:
            f.write(re_.content)
        response = make_response(send_file(f'static/{file_name}'))
        response.headers["Content-Disposition"] = "attachment; filename={};".format(f'static/{file_name}')
        return response
    return '格式匹配错误！'


@app.errorhandler(404)
def page_404(e):
    return '检查一下，未找到接口'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=80, debug=True)
