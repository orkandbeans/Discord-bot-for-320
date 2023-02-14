#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 1: osrs_info --- Date: 02/05/2023

#DESCRIPTION:
import requests # API call package
import mwparserfromhell # Full Name - Media Wiki Parser from Hell

# main function for osrsinfo command, processes program flow
def osrsinfo(entity_name: str, search_option: int):
    BASE_URL = 'https://oldschool.runescape.wiki/api.php?'
    CUSTOM_AGENT = { 'User-Agent': 'Arnoldbot_OSRS_lookup', 'From': 'john0893@gmail.com' }

    control = controller(model(), View())

    #set request baselines
    control.set_entity_name(entity_name)
    control.set_base_url(BASE_URL)
    control.set_custom_agent(CUSTOM_AGENT)

    #send initial search request
    request_type = 'search'
    control.set_parameters(request_type)
    control.send_request()
    control.set_search_results()
    control.set_search_result_count()

    if (control.model.search_result_count == 1):                    #one search result, request page from api.
        request_type = 'parse'
        control.model.entity_name = control.model.search_results    #reset entity name to handle non-exact query matching
        control.set_parameters(request_type)
        control.send_request()
        control.set_wikicode()
        control.set_wiki_templates()
        control.set_wiki_headers()
        control.set_wiki_text()
        control.set_single_page_output()
        control.set_formatted_single_page_output()
    elif (control.model.search_result_count > 1):                   #multiple search results, get choice from user
        if ((0 < search_option) and (search_option <= control.model.search_result_count)):
            request_type = 'parse'
            control.model.entity_name = control.model.search_results[search_option - 1]
            control.set_parameters(request_type)
            control.send_request()
            control.set_wikicode()
            control.set_wiki_templates()
            control.set_wiki_headers()
            control.set_wiki_text()
            control.set_single_page_output()
            control.set_formatted_single_page_output()
        else:
            control.set_search_output()
            control.set_formatted_search_output()
    else:                                                           #zero or negative result count, return no results
        control.set_no_results_output()

    print(control.model.wiki_templates)

    return control.view.output

#model: holds info on search query
class model:
    def __init__(self):
        self.entity_name = None
        self.base_url = None
        self.custom_agent = None
        #self.request_type = None
        self.parameters = None
        self.api_response = None
        self.wikicode = None
        self.wiki_templates = None
        self.wiki_headers = None
        self.wiki_text = None
        self.search_results = None
        self.search_result_count = None

    def construct_parameters(self, request_type: str):
        if (request_type == 'search'):
            return { 'action': 'opensearch', 'search': self.entity_name, 'format': 'json', 'limit': '500' }
        elif (request_type == 'parse'):
            return { 'action': 'parse', 'prop': 'wikitext', 'page': self.entity_name, 'format': 'json'}

    def parse_api_response(self):
        data = self.api_response
        wikicode = mwparserfromhell.parse(data["parse"]["wikitext"]["*"].encode("utf-8"))
        #wikicode_as_string = str(wikicode)
        return wikicode

    # def normalize_entity_name(self, entity_name: str):
    #     stripped = entity_name.strip(entity_name)
    #     normalized = stripped.replace(" ", "_")
    #     normalized = underscored.lower()
    #     return normalized



#controller: 
class controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    #Controller -> Model: piecewise methods
    def set_entity_name(self, entity_name: str):
        #normalized_name = self.model.normalize_entity_name(entity_name)
        self.model.entity_name = entity_name

    def set_base_url(self, base_url: str):
        self.model.base_url = base_url

    def set_custom_agent(self, custom_agent: dict[str, str]):
        self.model.custom_agent = custom_agent

    def set_parameters(self, request_type: str):
        self.model.parameters = self.model.construct_parameters(request_type)

    def send_request(self):
        self.model.api_response = requests.get(self.model.base_url, headers=self.model.custom_agent, params=self.model.parameters).json()

    def set_wikicode(self):
        self.model.wikicode = self.model.parse_api_response()

    def set_wiki_templates(self):
        self.model.wiki_templates = self.model.wikicode.filter_templates()

    def set_wiki_headers(self):
        self.model.wiki_headers = self.model.wikicode.filter_headings()

    def set_wiki_text(self):
        self.model.wiki_text = self.model.wikicode.strip_code()

    def set_search_results(self):
        self.model.search_results = self.model.api_response[1]

    def set_search_result_count(self):
        self.model.search_result_count = len(self.model.api_response[1]) #api_response[1] is the list of title names

    #controller -> View methods
    def set_search_output(self):
        self.view.output = self.model.search_results

    def set_single_page_output(self):
        self.view.output = self.model.wiki_text

    def set_no_results_output(self):
        self.view.output = ["No Results found for " + self.model.entity_name + " check spelling and try again."]

    def set_formatted_search_output(self):
        self.view.format_search_output()

    def set_formatted_single_page_output(self):
        self.view.format_single_page_output()



#Defines how to send/recieve input/output for user
class View:
    def __init__(self):
        self.output = None
        self.formatted_search_output = []
        self.formatted_single_page_output = []

    def format_search_output(self):

        option_index = 1
        j = 0
        self.formatted_search_output.append("Multiple search results match your input. Please rerun the command with the 'search_option' parameter.\n")
        self.formatted_search_output[j] += "-----------------------------------------------------------------------------------------------------\n"
        for i in self.output:
            self.formatted_search_output[j] += str(option_index) + ": " + i + "\n"
            if(len(self.formatted_search_output[j]) > 1000):
                j += 1
                self.formatted_search_output.append("")
            option_index += 1
        self.formatted_search_output[j] += "------------------------------------------------------------------------------------------------------\n"
        self.formatted_search_output[j] += "Multiple search results match your input. Please rerun the command with the 'search_option' parameter.\n"
        self.output = self.formatted_search_output
        

    def format_single_page_output(self):
        split_output = self.output.splitlines(True)
        self.formatted_single_page_output.append("")
        j = 0
        for i in split_output:
            if ((len(i) > 900) or (len(i) + len(self.formatted_single_page_output[j]) > 1600)):
                temp = i.split(". ")
                self.formatted_single_page_output[j] += ". "
                for k in temp:
                    if (len(k) + len(self.formatted_single_page_output[j]) < 1600):
                        self.formatted_single_page_output[j] += k
                    else:
                        j += 1
                        self.formatted_single_page_output.append("")
            else:
                self.formatted_single_page_output[j] += i
                if(len(self.formatted_single_page_output[j]) > 1000):
                    j += 1
                    self.formatted_single_page_output.append("")
        self.output = self.formatted_single_page_output


    def format_image_output(self):
        pass