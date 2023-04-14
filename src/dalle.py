import json
import requests

class Dalle:
    def generate(self, prompt, APIkey, download):
        body = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        response = requests.post('https://api.openai.com/v1/images/generations',
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + str(APIkey)
            },
            data=json.dumps(body))
        data = response.json()

        if response.status_code == 401:
            #raise noValidAPI()
            return "ERROR CODE 1"
        elif response.status_code == 429:
            #raise rateLimited()
            return "ERROR CODE 2"
        elif response.status_code == 500:
            #raise siteUnavailable()
            return "ERROR CODE 3"
        elif "error" in data:
            if (data['error']['code'] == None):
                #raise TOSViolation()
                return "ERROR CODE 4"

        url = data['data'][0]['url']
        if (download):
            self.download_image(url)
        return url

    def download_image(self, url):
        response = requests.get(url)
        with open("temp/dalle.png", 'wb+') as f:
            f.write(response.content)

#Exceptions



class siteUnavailable(Exception):
    """
    Dalle API is unavailable
    """
    pass

class rateLimited(Exception):
    """
    Too many requests at a time
    """
    pass

class noValidAPI(Exception):
    """
    Server has no API Key
    """
    pass
class TOSViolation(Exception):
    """
    This prompt violates the TOS
    """
    pass
