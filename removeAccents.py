import unicodedata

def replace_special_characters(input_string):
    # Tabela de mapeamento para substituir caracteres especiais
    mapping = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
        # Adicione mais mapeamentos, se necessário
    }

    #unicodedata.normalize para remover acentos e diacríticos
    normalized_string = unicodedata.normalize('NFD', input_string)

    # Substitui caracteres especiais pelos equivalentes não especiais
    cleaned_string = ''.join([mapping.get(char, char) for char in normalized_string])

    return cleaned_string