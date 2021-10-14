from flask import Flask
from flask import request, redirect, url_for, jsonify
import cv2
import numpy as np
import json
from text_extract10 import ocr_prsc
import time
import datetime


app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello, World!! ^^^^^'


def add_num(a1, a2):
    return (a1 + a2)

@app.route("/ping/", methods = ['GET'])
def ping():
    a = request.args.get('a',0)
    b = request.args.get('b',0)
    num = add_num(int(a), int(b))
    return 'pong'+ '  ' + str(num)



@app.route('/')
def user_juso():

    temp = request.args.get('name', "user01")
    temp1 = request.args.get('juso', '평택시')


    return temp + "-" + temp1 + '/'

@app.route('/prsc/', methods=['POST'])
def load_data():

    start_time = time.time()

    data = request.get_json()
    test_data = data["prsc"]
    s3_url = data["path"]
  #  print(test_data)
    output = ocr_prsc(test_data)

    end_time = time.time()
    sec = (end_time - start_time)
    print("Total_Process :", datetime.timedelta(seconds=sec))
    print(s3_url)
    return json.dumps({"result":output})
        #jsonify(test_data)


@app.route('/device/', methods=['POST'])
def load_data2():

    data = request.get_json()
    test_data = data['device']
    print(test_data)
    return json.dumps({"result":"success"})

@app.route('/diet/', methods=['POST'])
def load_data3():

    data = request.get_json()
    test_data = data['diet']
   # print(test_data)
    return json.dumps({"result":"success"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)