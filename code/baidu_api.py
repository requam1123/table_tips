# translate_service.py
import requests
import random
import hashlib
import json


BAIDU_APP_ID = '20250803002422632'
BAIDU_APP_KEY = 'ASW196H1RWMTY3S11bbL'
# ---------------------------------------------------------

ENDPOINT = 'http://api.fanyi.baidu.com'
PATH = '/api/trans/vip/translate'
URL = ENDPOINT + PATH

def make_md5(s, encoding='utf-8'):
    """Generate MD5 hash."""
    return hashlib.md5(s.encode(encoding)).hexdigest()

def translate_text(query: str, to_lang: str = 'en', from_lang: str = 'auto'):
    """
    Calls the Baidu Translate API to translate text using the official POST method.
    :param query: Text to be translated
    :param to_lang: Target language (e.g., 'en' for English)
    :param from_lang: Source language ('auto' for auto-detect)
    :return: Translated string on success, otherwise None
    """
    if not BAIDU_APP_ID or not BAIDU_APP_KEY:
        print("Error: Please set your Baidu Translate APP ID and Key in translate_service.py.")
        return "API not configured"
    
    salt = str(random.randint(32768, 65536))
    sign = make_md5(BAIDU_APP_ID + query + salt + BAIDU_APP_KEY)

    # The payload for the POST request
    payload = {
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'appid': BAIDU_APP_ID,
        'salt': salt,
        'sign': sign
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        response = requests.post(URL, params=payload, headers=headers, timeout=5)
        response.raise_for_status()  # Raises an exception for bad status codes
        result = response.json()

        if 'trans_result' in result:
            return result['trans_result'][0]['dst']
        else:
            # Provide a more helpful error message from the API
            error_code = result.get('error_code', 'N/A')
            error_msg = result.get('error_msg', 'Unknown error')
            print(f"Translation API Error: Code {error_code} - {error_msg}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network request failed: {e}")
        return None

# You can run this file directly to test the function
if __name__ == '__main__':
    # Test with a simple phrase
    test_query = "你好，世界！这是一个测试。"
    print(f"Translating: '{test_query}'")
    translated = translate_text(test_query, to_lang='en')
    
    if translated:
        print(f"Translation result: {translated}")
    else:
        print("Translation failed.")