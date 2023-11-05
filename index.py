#from sim800l import SIM800L
#import time
#from apiRequest import *
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/send_sms', methods=['POST'])
def remotSendSMS():
    requestBody = request.get_json()
    
    print("Phone Number: ", requestBody["phoneNumber"])
    print("Message: ", requestBody["message"])

    res = { "message": "success" }
    return jsonify(res)

"""
sim800l = SIM800L('/dev/serial0')

sim800l.setup()

if sim800l.is_registered():
    print("SIM is registered.")
    while True:
      result = sim800l.check_incoming()
      if result[0] == 'CMTI':
       index = result[1]
       msg = sim800l.read_and_delete_all(index_id=1)
       phoneNumber = msg[0]
       messageContent =  msg[3].replace('\n', '')
       print("Nova mensagem recebida:", msg)
       print("Phone number: ",phoneNumber)
       print("messageContent: ",messageContent)
       post(phoneNumber,messageContent)
      time.sleep(1)
else:
    print("SIM NOT registered.")
    sim800l.hard_reset(23)
"""