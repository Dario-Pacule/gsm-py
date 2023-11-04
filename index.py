from sim800l import SIM800L
import time
from checkHex import is_hex

sim800l = SIM800L('/dev/serial0')

sim800l.setup()

print("Date:",
    sim800l.get_date())
print("Operator:",
    sim800l.get_operator())
print("Service provider:",
    sim800l.get_service_provider())
print("Signal strength:",
    sim800l.get_signal_strength(), "%")
print("Temperature:",
    sim800l.get_temperature(), "degrees")
print("MSISDN:",
    sim800l.get_msisdn())
print("Battery Voltage:",
    sim800l.get_battery_voltage(), "V")
print("IMSI:",
    sim800l.get_imsi())
print("ICCID:",
    sim800l.get_ccid())
print("Unit Name:",
    sim800l.get_unit_name())

if sim800l.is_registered():
    print("SIM is registered.")
    while True:
      result = sim800l.check_incoming()
      if result[0] == 'CMTI':
       index = result[1]
       message = sim800l.read_sms(index)
       print("Nova mensagem recebida:", message)

       if is_hex(message):
        message_str = bytes.fromhex(message).decode('utf-16-be')
        print("Mensagem decodificada:", message_str)
      time.sleep(1)
else:
    print("SIM NOT registered.")
    sim800l.hard_reset(23)
