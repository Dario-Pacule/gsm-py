from sim800l import SIM800L
import time
from apiRequest import *
from flask import Flask, jsonify, request
import threading
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
    if sim800l.is_registered():
        print("SIM is registered.")
    while True:
        # Lista todas as mensagens disponíveis
        result = sim800l.command('AT+CMGL="ALL"\n')
        sim800l.check_incoming()

        if result:
            messages = result.split('+CMGL:')
            for message_info in messages:
                if message_info.strip():
                    index_id = message_info.split(',')[0].strip()
                    message = sim800l.read_sms(index_id)
                    if message:
                        print(f"Index: {index_id}")
                        print(f"Number: {message[0]}")
                        print(f"Date: {message[1]}")
                        print(f"Time: {message[2]}")
                        print(f"Message: {message[3]}")
                        print("-------------------------")
        else:
            print("Nenhuma menssagem encontrada")
        
        time.sleep(5)


        """while True:
            message = sim800l.read_next_message(all_msg=False)
            if message is not None:
                print("Mensagem lida:", message)
            elif message is False:
                print("Erro de leitura da mensagem: ",message)
            else:
                print("Nenhuma mensagem para ler: ", message)
            time.sleep(1)
            
            
            result = sim800l.check_incoming()
            if result[0] == 'CMTI':
                index = result[1]
                msg = sim800l.read_sms(index_id=index)
                phoneNumber = msg[0]
                messageContent = msg[3].replace('\n', '')
                print("New message:", msg)
                post(phoneNumber, messageContent)
            """
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
