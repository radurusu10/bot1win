from flask import Flask,render_template, url_for, request, redirect, session
import sqlite3
import logging
import requests

import config
from config import *
app = Flask(__name__)

db = "DataBase.db"
logging.basicConfig(level=logging.INFO, filename="py_log_web.log", filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

@app.route('/postback',methods=['POST', 'GET'])
def get():
    if request.method == 'GET':
        sub1 = request.args.get('sub1')
        subid = request.args.get('subid')
        with sqlite3.connect(db) as cursor:
            cursor.execute("UPDATE user SET postbeck_id = ? WHERE user_id = ?", (subid,sub1,)).fetchall()
        text = 'Вы прошли регистрацию, теперь можете пользоваться сигналами'
        reque = f"https://api.telegram.org/bot{config.token}/sendMessage?chat_id={sub1}&text={text}&parse_mode=HTML"
        r = requests.get(reque)
        return "sub1 = {};subid = {};".format(sub1, subid)
    else:
        return "ожидание"
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

