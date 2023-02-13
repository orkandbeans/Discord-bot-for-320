#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 1: osrs_info --- Date: 02/05/2023

#DESCRIPTION:

import requests # API call package
import mwparserfromhell # Full Name - Media Wiki Parser from Hell

# main function for osrsinfo command, processes program flow for osrsinfo command
def osrsinfo(entity_name: str):

    control = controller(model(), View())
    control.set_entity_name(entity_name)
    control.set_base_url('https://oldschool.runescape.wiki/api.php?')
    control.set_custom_agent({ 'User-Agent': 'Arnoldbot_OSRS_lookup', 'From': 'john0893@gmail.com' })
    control.set_parameters('query')
    control.send_request()
    control.set_parsed_api_response()

    output = control.model.parsed_api_response

    if(len(output) < 2000):
        return output
    else:
        output = "page contents was too long for now"
        return output
    #control.set_constructed_url("https://oldschool.runescape.wiki/api.php?action=opensearch&search=abyssal&format=json&limit=20")
    # mod.constructed_url = "https://oldschool.runescape.wiki/api.php?action=opensearch&search=Abyssal_whip&format=json&limit=20"
    #mod.constructed_url = "https://oldschool.runescape.wiki/api.php?action=query&aclimit=500&list=allcategories&format=json"
    #mod.constructed_url = "https://oldschool.runescape.wiki/api.php?action=opensearch&search=abyssal&format=json&limit=20"
    # output = requests.get("https://oldschool.runescape.wiki/api.php?action=query&prop=revisions&rvprop=content&titles=Abyssal_whip")

    #output = requests.get(mod.constructed_url)
    #print(output.json())


#model: holds info on search query
class model:
    def __init__(self):
        #self.entity_type = entity_type
        #self.info_type = info_type
        self.entity_name = None
        self.base_url = None
        self.custom_agent = None
        self.parameters = None
        self.api_response = None
        self.parsed_api_response = None

    def construct_parameters(self, request_type: str):
        if (request_type == 'search'):
            return { 'action': 'opensearch', 'search': self.entity_name, 'format': 'json', 'limit': '20' }
        elif (request_type == 'query'):
            return { 'action': 'parse', 'prop': 'wikitext', 'page': self.entity_name, 'format': 'json'}

    def parse_api_response(self):
        data = self.api_response
        return mwparserfromhell.parse(data["parse"]["wikitext"]["*"])


#controller: 
class controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_entity_name(self, entity_name: str):
        self.model.entity_name = entity_name

    def set_base_url(self, base_url: str):
        self.model.base_url = base_url

    def set_custom_agent(self, custom_agent: dict[str, str]):
        self.model.custom_agent = custom_agent

    def set_parameters(self, request_type: str):
        self.model.parameters = self.model.construct_parameters(request_type)

    def send_request(self):
        self.model.api_response = requests.get(self.model.base_url, headers=self.model.custom_agent, params=self.model.parameters).json()

    def set_parsed_api_response(self):
        self.model.parsed_api_response = self.model.parse_api_response()
        # print(self.model.parsed_api_response)


#Defines how to send/recieve input/output for user
class View:
    def __init__(self):
        __user_selection: int
        pass

    def __get_user_selection(str) -> int:
        pass

    # result = "Searching for " + info_type + "s " + "of " + entity_type + ": " + name
    # return result
    
    # output = requests.get("https://api.osrsbox.com")
    # return(output.json())