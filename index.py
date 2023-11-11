from sim800l import SIM800L
from isValidPhoneNumber import isValidMZPhoneNumber
from apiRequest import *
from flask import Flask, jsonify, request
import threading
import time
import re
from removeAccents import replace_special_characters
from queue import Queue

app = Flask(__name__)
sim800l = SIM800L('/dev/serial0')
sim800l.setup()

message_queue = Queue()

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
        # Adicionar mensagem à fila para envio
        message_queue.put((phoneNumber, message))
        return jsonify({"message": "SMS sent successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def send_sms_worker():
    while True:
        phoneNumber, message = message_queue.get()
        try:
            cleanMessage = replace_special_characters(message)
            sim800l.send_sms(phoneNumber, cleanMessage)
            print(f"SMS sent to {phoneNumber} with message: {cleanMessage}")
        except Exception as e:
            print(f"Failed to send SMS to {phoneNumber}. Error: {str(e)}")
        finally:
            message_queue.task_done()


def message_check_loop():
    index_id = 0
    try:
        while True:
            index_id += 1
            try:
                msg = sim800l.read_sms(index_id)

                if msg:
                    print("Message: ", msg)
                    phoneNumber = msg[0]
                    messageContent = msg[3].replace('\n', '')
                    if isValidMZPhoneNumber(phoneNumber):
                        post(phoneNumber, messageContent)

                    sim800l.delete_sms(index_id)
                else:
                    print("Nenhuma mensagem encontrada: ", msg)
                    if index_id > 1:
                        index_id = 0
            except IndexError as e:
                print(f"Erro ao acessar a mensagem: {e}")
            except Exception as e:
                print(f"Erro desconhecido: {e}")
    except KeyboardInterrupt:
        print("Loop interrompido pelo usuário.")


if sim800l.is_registered():
    print("SIM is registered.")
else:
    print("SIM NOT registered.")
    sim800l.hard_reset(23)

if __name__ == '__main__':
    message_thread = threading.Thread(target=message_check_loop)
    sms_thread = threading.Thread(target=send_sms_worker)

    message_thread.daemon = True
    sms_thread.daemon = True
    
    message_thread.start()
    sms_thread.start()

    app.run(host='0.0.0.0', port=3001)
