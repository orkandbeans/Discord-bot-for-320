import json
import requests
import math

class chatGPT:
    def __init__(self, APIkey):
        self.APIkey=APIkey

    def generate(self, prompt, size):

        tokens = math.floor(1.3333 * size)
        ##if (self.checkAPI() < 1):
        ##    raise siteUnavailable()
        ##    return -1
        body = {
            "model": "text-babbage-001"
            "prompt": prompt,
            "max_tokens": tokens,
            "temperature": 1,
            "n": 1
        }

        response = requests.post('https://api.openai.com/v1/completions',
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + str(self.APIkey)
            },
            data = json.dumps(body))
        data = response.json()


        if "error" in data:
            raise parseFail()
            return -2
        if "data" not in data:
            raise noImages()
            return -3

        text = data['data'][0].text.trim())
        return text

    def checkAPI(self):
        try:
            r = requests.get('https://api.openai.com/v1/completions')
            r.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return 0
        except (requests.exceptions.HTTPError):
            return -1
        else:
            return 1

#Exceptions

class siteUnavailable(Exception):
    """
    Dalle API is unavailable
    """
    pass

class parseFail(Exception):
    """
    Dalle API returned an error
    """
    pass

class noImages(Exception):
    """
    Dalle API did not return an image
    """
    pass
