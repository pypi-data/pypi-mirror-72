#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sl.server import ThreadingWSGIServer
from wsocket import WebSocketHandler
import threading
import json
import logging
from .app import WSGIApp

logger = logging.getLogger(__name__)

app = WSGIApp()

def _get_random_port():
    while True:
        port = random.randint(1023, 65535)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('localhost', port))
            except OSError:
                logger.warning('Port %s is in use' % port)
                continue
            else:
                return port

class Server(ThreadingWSGIServer):
    def __init__(self, server_address=('',None)):
        if server_address[1]==None:
            server_address=(server_address[0], _get_random_port())
        ThreadingWSGIServer.__init__(self,server_address, WebSocketHandler)
        ThreadingWSGIServer.set_app(self, app)
    def serve_forever(self, Async=True):
        if Async:
            t = threading.Thread(target=ThreadingWSGIServer.serve_forever,args=[self])
            t.start()
        else:
            ThreadingWSGIServer.serve_forever(self)

class Hub:

    def __init__(
        self,
        url='/',
        _async=True
        ):
        self.readyState = 0
        self.chats = {}
        self._async = _async
        app.routes[url] = self.handle
        self._abort = False
        self.client_counter = 0

    def handle(self, environ, start_response):
        self.readyState = 1
        self.env = environ
        self.async_run(self.Open)
        wsock = environ.get('wsgi.websocket')
        if not wsock:
            if self.env['REQUEST_METHOD'] == 'GET' or 'POST':
                return self.GET_POST(start_response)
        else:
            self.client_counter += 1
            self.chats['ws' + str(self.client_counter)] = wsock
            return self.ws(wsock, 'ws'+str(self.client_counter))

    def reader(self):
        n_bytes = int(self.env.get('CONTENT_LENGTH'))
        content_bytes = self.env.get('wsgi.input').read(n_bytes)
        content_string = content_bytes.decode('ascii')
        d = json.loads(content_string)
        if d.get('id') and d.get('id') in self.chats:
            self.readyState = 4
            if d.get('id').startwith('ws'):
                self.client_counter += 1
                self.chats[str(self.client_counter)] = []
                self.async_run(self.Message, [d.get('message'),
                               str(self.client_counter)])
                return str(self.client_counter)
            self.async_run(self.Message, [d.get('message'), d.get('id'
                           )])
            return d.get('id')
        else:
            self.readyState = 4
            self.client_counter += 1
            self.chats[str(self.client_counter)] = []
            self.async_run(self.Message, [d.get('message'),
                           str(self.client_counter)])
            return str(self.client_counter)

    def GET_POST(self, start_response):
        self.readyState = 2
        if self._abort:
            return
        try:
            if self.env.get('CONTENT_LENGTH'):
                self.readyState = 3
                _id = self.reader()
            else:
                self.client_counter += 1
                self.chats[str(self.client_counter)] = []
                _id = str(self.client_counter)
            if len(self.chats.get(_id)) != 0:
                data = {}
                data['id'] = _id
                data['message'] = self.chats[_id]
                res = json.dumps(data)
                self.chats[_id] = []
                status = '200 OK'
                response_headers = []
                start_response(status, response_headers)
                self.async_run(self.Close)
                return res.encode()
            else:
                while len(self.chats[_id]) == 0:
                    if self._abort:
                        self.async_run(self.Close)
                        return
                else:
                    data = {}
                    data['id'] = _id
                    data['message'] = self.chats[_id]
                    res = json.dumps(data)
                    self.chats[_id] = []
                    status = '200 OK'
                    response_headers = []
                    start_response(status, response_headers)
                    self.async_run(self.Close)
                    return res.encode()
        except Exception as e:
            self.async_run(self.Error, [e])
        return

    def ws(self, wsock, _id):
        self.readyState = 2
        while True:
            if self._abort:
                return
            try:
                message = wsock.receive()
                self.readyState = 3
                if message:
                    self.readyState = 4
                    self.async_run(self.Message, [message,_id])
                else:
                    self.async_run(self.Close)
                    break
            except Exception as e:
                self.async_run(self.Error, [e])
                break
        self.async_run(self.Close)
        return

    def Open(self):
        logger.warning('Request Opened : ' + str(self.readyState))

    def Send(self, data, client=None):
        if client and client in self.chats:
            if client.startswith('ws'):
                try:
                    d = {}
                    d['id'] = client
                    d['message'] = data
                    res = json.dumps(d)
                    self.chats.get(client).send(res)
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    self.chats.get(client).append(data)
                except:
                    return False
        else:
            try:
                if list(self.chats.keys())[0].startswith('ws'):
                    d = {}
                    d['id'] = list(self.chats.keys())[0]
                    d['message'] = data
                    res = json.dumps(d)
                    self.chats.get(list(self.chats.keys())[0]).send(res)
                else:
                    self.chats.get(list(self.chats.keys())[0]).append(data)
            except Exception as e:
                print(e)
                return False

    def Close(self):
        logger.warning('Request Closed : ' + str(self.readyState))

    def Error(self, err):
        logger.warning('Request Error Happened (' + str(err) + ') : '
                       + str(self.readyState))

    def Abort(self):
        self._abort = True

    def Message(self, msg, client):
        logger.warning('Message Recived From Client '+ client +' (' + msg + ') : '
                       + str(self.readyState))

    def async_run(self, target, args=[]):
        if self._async:
            t = threading.Thread(target=target, args=args)
            t.start()
        else:
            target(*args)

