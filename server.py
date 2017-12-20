# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 23:39:16 2017

@author: prehawk
"""

import gevent
from gevent.pywsgi import WSGIServer
from datetime import datetime


def waitUntil(month, day, hour, minute):
    while True:
        now = datetime.now()
        if now.month >= month and now.day >= now.day and now.hour >= hour and now.minute >= minute:
            print('ok')
            break
        else:
            gevent.sleep(1)
        
        
        

def application(env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b"<b>hello world</b>"]

    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return [b'<h1>Not Found</h1>']


if __name__ == '__main__':
    print('Serving on 8088...')
    WSGIServer(('', 8088), application).serve_forever()