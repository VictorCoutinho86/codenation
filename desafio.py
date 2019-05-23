import os
import hashlib
import requests
import string
import time
import json
from dotenv import load_dotenv
from caesarCipher import decrypt


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

token = os.environ.get("TOKEN")
url_data = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=" + token
url_solution = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=" + token


def decifra(texto, n_casas):
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    frase = ""
    for t in texto.lower():
        if t in string.punctuation:
            new_t = t
        elif t in str(digits):
            new_t = t
        else:
            if (ord(t) + n_casas) > 122:
                new_t = chr(97 + ((ord(t) + n_casas) - 123))
            else:
                new_t = chr(ord(t) + n_casas)
        frase = frase + new_t
    print(frase)
    return frase.lower()


def resumo(texto):
    print(hashlib.sha1(texto.encode('utf-8')).hexdigest())
    print(hashlib.sha1(texto.encode('ascii')).hexdigest())
    return hashlib.sha1(texto.encode('utf-8')).hexdigest()


def getvalues():
    dados = requests.get(url_data)
    dados = dados.json()
    decoded = decrypt(dados['cifrado'], dados['numero_casas'])
    dados['decifrado'] = decoded
    dados['resumo_criptografico'] = resumo(decoded)

    with open('answer.json', 'w') as f:
        json.dump(dados, f)

    time.sleep(5)
    postvalues()


def postvalues():
    files = {'answer': open('answer.json', 'rb')}
    r = requests.post(url_solution, files=files)

    if r.status_code == 200:
        print("ORAY, funcionou")

    else:
        print("Deu alguma merda codigo {}".format(r.status_code))


if __name__ == "__main__":
    getvalues()
