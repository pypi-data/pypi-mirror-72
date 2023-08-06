import json
import requests


def get_lang_para(lang):
    d = {
        'C (GCC 9.2.1)': 'text/x-csrc',
        'C (Clang 10.0.0)': 'text/x-csrc',
        'C++ (GCC 9.2.1)': 'text/x-c++src',
        'C++ (Clang 10.0.0)': 'text/x-c++src',
        'Java (OpenJDK 11.0.6)': 'text/x-java',
        'Python (3.8.2)': 'python',
        'Ruby (2.7.1)': 'ruby',
        'C# (.NET Core 3.1.201)': 'text/x-csharp',
        'PyPy3 (7.3.0)': 'python',
        'Haskell (GHC 8.8.3)': 'haskell',
        'Rust (1.42.0)': 'rust',
    }
    if lang in d:
        return d[lang]
    else:
        return 'auto'


def get_carbon_image(code, lang):
    headers = {'Content-Type': 'application/json'}
    obj = {'code': code, 'language': lang}
    json_data = json.dumps(obj).encode('utf-8')
    carbon_url = 'https://carbonara.now.sh/api/cook'
    res = requests.post(carbon_url, json_data, headers=headers)
    image = res.content
    return image
