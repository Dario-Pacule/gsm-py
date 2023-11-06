from sim800l import SIM800L
import time
from apiRequest import *
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)
sim800l = SIM800L('/dev/serial0')
sim800l.setup()

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    phoneNumber = data.get('phoneNumber')
    message = data.get('message')

    print("phoneNumber: ",phoneNumber)
    print("message: ",message)

    if not phoneNumber or not message:
        return jsonify({"error": "Phone number and message are required."}), 400

    try:
        # Enviar a mensagem SMS
        time.sleep(2)
        sim800l.send_sms(phoneNumber, message)
        return jsonify({"message": "SMS sent successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def send_long_sms(destno, long_msg):
    max_msg_length = 120  # Tamanho máximo de uma mensagem SMS (para caracteres GSM 03.38)
    segments = [long_msg[i:i + max_msg_length] for i in range(0, len(long_msg), max_msg_length)]

    for i, segment in enumerate(segments):
        part_identifier = f"Part {i + 1}/{len(segments)}"
        full_msg = f"{segment} ({part_identifier})"
        sim800l.send_sms(destno, full_msg)


def message_check_loop():
    if sim800l.is_registered():
        print("SIM is registered.")
        while True:
            result = sim800l.check_incoming()
            if result[0] == 'CMTI':
                index = result[1]
                msg = sim800l.read_and_delete_all(index_id=index)
                phoneNumber = msg[0]
                messageContent = msg[3].replace('\n', '')
                print("New message:", msg)
                post(phoneNumber, messageContent)
            time.sleep(5)
    else:
        print("SIM NOT registered.")
        sim800l.hard_reset(23)

if __name__ == '__main__':
    message_thread = threading.Thread(target=message_check_loop)
    message_thread.daemon = True
    message_thread.start()

    app.run(host='0.0.0.0', port=3001)
