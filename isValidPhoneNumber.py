import re

def isValidMZPhoneNumber(number):
    # Usa uma expressão regular para verificar o formato do número
    # O formato válido é '+258' seguido de 9 dígitos (total de 12 dígitos)
    pattern = r'^\+258\d{9}$'
    if re.match(pattern, number):
        return True
    else:
        return False