import re
import emoji
from html.parser import HTMLParser
import string

__all__ = ["preprocess_text"]

def replace_slang(text):
    # Словарь замен: сленг и его нормальное представление
    slang_dict = {
        r'\bтг\b': ' телефон ',
        r'\bспс\b': ' спасибо ',
        r'\bплиз\b': ' пожалуйста ',
        r'\bчел\b': ' человек ',
        r'\bкек\b': ' смешно ',
        r'\bлол\b': ' смешно '
    }
    
    # Перебираем словарь и заменяем каждый сленг в тексте
    for slang, normal in slang_dict.items():
        text = re.sub(slang, normal, text, flags=re.IGNORECASE)
    
    return text

def replace_custom_text_emojis(text):
    # Словарь текстовых эмодзи и их словесных описаний
    emoji_dict = {
        r':\)': ' улыбка ',
        r':\(': ' грустное лицо ',
        r':D': ' смех ',
        r';\)': ' подмигивание '
    }
    
    # Перебираем словарь и заменяем каждый эмодзи в тексте
    for emoji, description in emoji_dict.items():
        text = re.sub(emoji, description, text, flags=re.IGNORECASE)
    
    return text

def replace_r_with_rubles(text):
    # Замена "р" после числа
    text = re.sub(r'(\d)р\b', r'\1 рублей ', text)
    # Замена "р" перед числом
    text = re.sub(r'\bр(\d)', r' рублей \1', text)
    return text

def replace_currency_symbols(text):
    # Словарь символов валют и их полных названий
    currency_symbols = {
        r'\$': ' долларов ',
        r'€': ' евро ',
        r'£': ' фунтов ',
        r'¥': ' йен ',
        r'₽': ' рублей '
    }
    
    # Перебираем словарь и заменяем каждый символ валюты в тексте
    for symbol, name in currency_symbols.items():
        text = re.sub(symbol, name, text)
    
    return text

def replace_identifiers(text):
    # Регулярное выражение, которое ищет шестнадцатеричные хеши, UUIDs и другие типичные идентификаторы
    pattern = r'\b([a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}|[a-f0-9-]{36}|[a-zA-Z0-9-]{7,})\b'
    
    # Заменяем найденные идентификаторы на слово "идентификатор"
    return re.sub(pattern, ' идентификатор ', text, flags=re.IGNORECASE)

def replace_phone_numbers_and_digits(text):
    # Регулярное выражение для номеров телефонов
    phone_pattern = r'\+?\d[\d\-\(\)\.\s]{8,}\d'
    
    # Заменить номера телефонов на "номер телефона"
    text = re.sub(phone_pattern, ' номер телефона ', text)

    text = replace_identifiers(text)
    
    # Заменить оставшиеся числа на "число"
    text = re.sub(r'\b\d+\b', ' число ', text)
    
    return text

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.extracted_data = []

    def handle_data(self, data):
        self.extracted_data.append(data)

    def get_data(self):
        return ''.join(self.extracted_data)

def expand_contractions(text, contractions_dict):
    for key, value in contractions_dict.items():
        text = text.replace(key, value)
    return text

contractions = {
    "и т.д.": " и так далее ",
    "и т.п.": " и тому подобное ",
    "ул.": " улица "
}

def remove_punctuation_list_comp(text):
    return re.sub(r'\s+', ' ', re.sub(r'[\s{}]+'.format(re.escape(string.punctuation)), ' ', text)).strip()


def replace_math_symbols_with_words(text):
    # Словарь замен: математический символ и его словесное представление
    math_symbols = {
        '+': ' плюс ',
        '*': ' умножить на ',
        '/': ' разделить на ',
        '=': ' равно ',
        '<': ' меньше ',
        '>': ' больше ',
        '≤': ' меньше или равно ',
        '≥': ' больше или равно '
    }
    
    # Перебираем словарь и заменяем каждый символ в тексте
    for symbol, word in math_symbols.items():
        text = text.replace(symbol, word)
    
    return text

def replace_units_with_full_names(text):
    # Словарь замен: сокращение единицы измерения и его полное словесное представление
    units = {
        'кг': 'килограмм',
        'г': 'грамм',
        'м': 'метр',
        'см': 'сантиметр',
        'мм': 'миллиметр',
        'л': 'литр',
        'мл': 'миллилитр',
        'ч': 'час',
        'мин': 'минута',
        'сек': 'секунда',
        'км': 'километр',
        'шт': 'штук'
    }
    
    for unit, full_name in units.items():
        text = text.replace(f' {unit} ', f' {full_name} ')
    return text

def remove_extra_spaces_regex(text):
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def remove_non_cyrillic(text):
    # Удаляем все, кроме русских букв
    return re.sub(r'[^а-яА-ЯёЁ]', ' ', text)


def preprocess_text(text):

    text = text.lower()

   # text = replace_hyphens(text)

    #print("hyphens ", text)

    text = replace_slang(text)

    #print("slang ", text)

    text = replace_custom_text_emojis(text)

    #print("emoji ", text)

    text = replace_r_with_rubles(text)

    #print("rubles ", text)

    text = replace_currency_symbols(text)

    #print("currency ", text)

    text = replace_phone_numbers_and_digits(text)

    #print("phone_numbers_and_digits ", text)

    # Перевод в нижний регистр

    
    # Раскрытие сокращений
    text = expand_contractions(text, contractions)

    """   url_pattern = re.compile(
    r'\b(?:https?|ftp|mailto|data|tel):\/\/'  # Расширенные схемы
    r'(?:(?:[a-z0-9-]+\.)+[a-z]{2,13})'  # Доменное имя
    r'(?:\/[\w\-\.~:+\/?#\[\]@!$&\'()*;,=]*)?'  # Путь
    r'(?:(?:\?[\w\-\.~:+\/?#\[\]@!$&\'()*;,=]*)?)'  # Параметры
    r'(?:(?:#[\w\-]*)?)\b',  # Якорь
    re.IGNORECASE)
    """


    url_pattern = re.compile(r'https?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}')

    # Удаление ссылок
    text = re.sub(url_pattern, '', text)

    #print("links ", text)

    # переводим эмоджи в текст вида :машет_рукой: , заменяем символы : и _ на пробелы
    text = emoji.demojize(text, language='ru').replace(':', ' ').replace('_', ' ')

    #print("emoji  ", text)
    
    # Обработка HTML
    parser = MyHTMLParser()
    parser.feed(text)
    extracted_text = parser.get_data()
    # Рекурсивно применяем функцию к извлеченному тексту
    if extracted_text != text:  # Проверяем, был ли HTML тег
        text = preprocess_text(extracted_text)
    
    #print("html  ", text)
    
    # убираем знаки пунктуации
    text = remove_punctuation_list_comp(replace_math_symbols_with_words(text))

    #print("remove_punctuation_list_comp  ", text)

    text = replace_units_with_full_names(text)

    #print("replace_units_with_full_names  ", text)

    text = remove_extra_spaces_regex(remove_non_cyrillic(text))
    
    return text