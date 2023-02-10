#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 1: osrs_info --- Date: 02/05/2023

#DESCRIPTION:

import requests #for API calls in osrsinfo

#create a View to take initial input and serve final output for the user
class CommandView:

    def __init__(self):
        __user_args: str
        __response_builder_template: dict[str, list[str]]
        text_output: str
        image_output: Buffered_Image
        pass

    def __send_to_bot(self, Buffered_Image):
        pass

    def __send_to_bot_text(self, str):
        pass

    def build_response(self):
        pass

    def cleanup(self):
        pass


#controller for program flow
class Controller:
    def __init__(self):
        initial_args: str
        current_args: str
        parsed_args: list[str]
        __process_stage: StrEnum
        __arg_parser: ArgParser
        __request_handler: RequestHandler
        __user_relay: UserRelay
        pass
    
    def change_stage(self):
        pass

    def control_loop(self, str):
        pass

    def on_error(self):
        pass


#make a parser/formatter to format text for database
class RequestHandler:
    def __init__(self):
        __api_base_url: str
        __request_url:str
        __custom_agent: dict[str, str]
        __wiki_response: str
        __request_params_template: list[str]
        __request_params: dict[str, str]
    pass

    def __change_stage():
        pass

    def __control_loop(str):
        pass

    def __on_error():
        pass


#create a way to query/receive information from the api/database
class ArgParser:
    def __init__(self):
        to_parse: str
        pass

    def is_valid(a:str, b:str):
        pass

    def __parse_user_args(str) -> list[str]:
        pass

    def __parse_from_search_query_response(str) -> list[str]:
        pass

    def __parse_from_page_query_response(str) -> list[str]:
        pass

    def __parse_from_user_selection(str) -> list[Str]:
        pass

    def __parse_error_response(str) -> list[str]:
        pass

    def __format_user_args(str) -> str:
        pass

    def __format_to_user_selections(current_args:list[str]) -> str:
        pass

    def __format_to_text_output(str) -> str:
        pass

    def __format_error_return(current_args:list[str]) -> str:
        pass


#make a parser/formatter for the returned text
class UserRelay:
    def __init__(self):
        __user_selection: int
        pass

    def __get_user_selection(str) -> int:
        pass


    # result = "Searching for " + info_type + "s " + "of " + entity_type + ": " + name
    # return result
    # output = requests.get("https://secure.runescape.com/m=itemdb_oldschool/api/info.json")
    # output = requests.get("https://api.osrsbox.com")
    # return(output.json())