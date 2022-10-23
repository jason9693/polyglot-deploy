import logging

from flask import Flask, request, render_template
import traceback

import os
from queue import Queue, Empty
from threading import Thread
import time

import json
import requests
from functools import lru_cache


os.system('ls')
app = Flask(__name__)

requests_queue = Queue()    # request queue.
BATCH_SIZE = 100              # max request size.
CHECK_INTERVAL = 0.1

host_addr = os.environ['HOST_URL'] + '/generate' #


class EscapeSequenceAdapter:
    # \n => <|endoftext|>
    def encode(self, s):
        return s.replace('\n', '<|endoftext|>')
    
    def decode(self, s):
        return s.replace('<|endoftext|>', '\n')


adapter = EscapeSequenceAdapter()

##
# Request handler.
# GPU app can process only one request in one time.
def handle_requests_by_batch():
    while True:
        request_batch = []
        text_list = []

        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request = requests_queue.get(timeout=CHECK_INTERVAL)
                request_batch.append(request)
            except Empty:
                break

        if len(request_batch) == 0:
           continue
        # outputs = mk_predict(text_list)
        valid_requests = []
        for idx, request in enumerate(request_batch):
            valid_requests.append(request)
        request_batch = []
        
        for idx, request in enumerate(valid_requests):
            try:
                types = request["input"][0]
                txt = request["input"][1]
                outputs = send_req(txt, host_addr)
                outputs = json.loads(outputs)['output']
                if types != "original":
                    outputs = outputs[len(txt):]
                    pass
                
                outputs = adapter.decode(outputs)
                
                outputs = '<br>'.join(outputs.split('\n'))
                request["output"] = ({0: outputs}, 200)
                # {
                #     "result": outputs
                # }
            except Exception as e:
                request["output"] = e
    return


@lru_cache(maxsize=512)
def send_req(text, url):
    data = {
        "prompt": text,
        "max_length": 64 #TODO: to be fixed
    }
    # import pdb
    # pdb.set_trace()
    x = requests.post(url, json=data)
    return x.text


handler = Thread(target=handle_requests_by_batch).start()


##
# Get post request page.
@app.route('/generate/<types>', methods=['POST'])
def generate(types):
    if types not in ['original', 'generated']:
        return {'Error': 'Invalid types'}, 404

    # GPU app can process only one request in one time.
    if requests_queue.qsize() > BATCH_SIZE:
        return {'Error': 'Too Many Requests'}, 429

    try:
        args = []
        text = request.form['text'].replace('\r\n', '\n')

        text = adapter.encode(text)

        args.append(types)
        args.append(text)

    except Exception as e:
        return {'message': 'Invalid request'}, 500

    # input a request on queue
    req = {'input': args}
    requests_queue.put(req)

    # wait
    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)
    return req['output']


##
# Queue deadlock error debug page.
@app.route('/queue_clear')
def queue_clear():
    while not requests_queue.empty():
        requests_queue.get()

    return "Clear", 200


##
# Sever health checking page.
@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200


##
# Main page.
@app.route('/')
def main():
    return render_template('index.html'), 200


if __name__ == '__main__':
    from waitress import serve
    app.logger.info("server start")
    serve(app, port=19234, host='0.0.0.0')
