import unittest
import time
from osrsinfo import *

class TestOutput(unittest.TestCase):
    #TEST 1: Integration test: model view and controller classes all work to produce
    #the final output. [Big-bang] since the modules where written prior to the assignment.
    def test_no_results_output(self):

        output = osrsinfo("sdadfalks", 0)
        
        self.assertEqual(output, ['No Results found for sdadfalks check spelling and try again.'])

    #Test 2: Integration test: model view and controller classes all work to produce
    #the final output. [Big-bang] since the modules where written prior to the assignment.
    def test_output_longer_than_single_message(self):
        output = osrsinfo("Barbarian", 0) #contains 2 messages worth of output
        self.assertTrue(len(output) > 1)

    #Test 3: Integration test: model view and controller classes all work to produce
    #the final output. [Big-bang] since the modules where written prior to the assignment.
    def test_output_single_message(self):
        output = osrsinfo("Abyssal Whip", 0) #contains 1 messages worth of output
        self.assertTrue(len(output) == 1)

class TestModel(unittest.TestCase):
    entity_name = "Barbarian"

    #TEST 4: acceptance test
    def test_construct_parameters_search(self):

        result_search = model.construct_parameters(self, "search")
        self.assertEqual(result_search, { 'action': 'opensearch', 'search': self.entity_name, 'format': 'json', 'limit': '500' })

    #TEST 5: acceptance test
    def test_construct_parameters_parse(self):
        result_parse = model.construct_parameters(self, "parse")
        self.assertEqual(result_parse, { 'action': 'parse', 'prop': 'wikitext', 'page': self.entity_name, 'format': 'json'})
        
    #TEST 6: acceptance test
    def test_construct_parameters_unsupported(self):
        result_other = model.construct_parameters(self, "hello")

        self.assertIsNone(result_other)

    #TEST 7: acceptance test
    def test_contruct_parameters_none(self):
        result_not_set = model.construct_parameters(self, None)

        self.assertIsNone(result_not_set)

class TestController(unittest.TestCase):
    #set base parameters
    BASE_URL = 'https://oldschool.runescape.wiki/api.php?'
    CUSTOM_AGENT = { 'User-Agent': 'Arnoldbot_OSRS_lookup', 'From': 'john0893@gmail.com' }
    control = controller(model(), view())
    control.set_base_url(BASE_URL)
    control.set_custom_agent(CUSTOM_AGENT)

    #TEST 8: acceptance test
    def test_result_count_good_search(self):
        #setup request
        request_type = "search"
        entity_name = "Barbarian" #known to have 37 results
        self.control.set_entity_name(entity_name)
        self.control.set_parameters(request_type)
        self.control.send_request()

        #method to be tested
        self.control.set_search_results()
        self.control.set_search_result_count()
        
        self.assertEqual(self.control.model.search_result_count, 37)

    #TEST 9: acceptance test
    def test_result_count_bad_search(self):
        #setup request
        request_type = "search"
        entity_name = "asdfja;lsdjfl"
        self.control.set_entity_name(entity_name)
        self.control.set_parameters(request_type)
        self.control.send_request()

        #method to be tested
        self.control.set_search_results()
        self.control.set_search_result_count()
            
        self.assertEqual(self.control.model.search_result_count, 0)



class TestView(unittest.TestCase):
    #setup request
    BASE_URL = 'https://oldschool.runescape.wiki/api.php?'
    CUSTOM_AGENT = { 'User-Agent': 'Arnoldbot_OSRS_lookup', 'From': 'john0893@gmail.com' }
    control = controller(model(), view())
    control.set_base_url(BASE_URL)
    control.set_custom_agent(CUSTOM_AGENT)

    #TEST 10:  White box test: codition coverage %100, branch coverage %100
    # Discord messages have a maximum length of 2000 characters.
    # This method takes text input and creates a list of strings of less than 2000 characters
    # The request above sets the single_page_output to data containing single splits that
    # have greater than 900 characters, splits containing greater than 1600 characters when
    # combined with the previous split, and splits less than 900 characters.
    # the inner for loop combines tokens of these splits until they reach a length of 1600 characters
    # which is covered because the splits longer than 1600 characters contain tokens of less than 1600 characters
    
    # code being tested:
    # def format_single_page_output(self):
    #     split_output = self.output.splitlines(True)
    #     self.formatted_single_page_output.append("")
    #     j = 0
    #     for i in split_output:
    #         if ((len(i) > 900) or (len(i) + len(self.formatted_single_page_output[j]) > 1600)):
    #             temp = i.split(". ")
    #             self.formatted_single_page_output[j] += ". "
    #             for k in temp:
    #                 if (len(k) + len(self.formatted_single_page_output[j]) < 1600):
    #                     self.formatted_single_page_output[j] += k
    #                 else:
    #                     j += 1
    #                     self.formatted_single_page_output.append("")
    #         else:
    #             self.formatted_single_page_output[j] += i
    #             if(len(self.formatted_single_page_output[j]) > 1000):
    #                 j += 1
    #                 self.formatted_single_page_output.append("")
    #     self.output = self.formatted_single_page_output

    def test_format_single_page_output_character_split_length(self):
        #setup request
        request_type = 'parse'
        self.control.model.entity_name = "Abyssal whip"
        self.control.set_parameters(request_type)
        self.control.send_request()
        self.control.set_wikicode()
        self.control.set_wiki_templates()
        self.control.set_wiki_headers()
        self.control.set_wiki_text()
        self.control.set_single_page_output()
        self.control.set_formatted_single_page_output()

        #method to be tested
        for i in self.control.view.formatted_single_page_output:
            self.assertTrue(len(i) < 2000)

    #TEST 11: 
    def test_format_search_output_result_count(self):
        #setup request
        request_type = 'search'
        self.control.model.entity_name = "Abyssal whip"
        self.control.set_parameters(request_type)
        self.control.send_request()
        self.control.set_search_results()
        self.control.set_search_result_count()
        self.control.set_search_output()
        before_formatting = self.control.view.output
        self.control.set_formatted_search_output()

        split_output = self.control.view.formatted_search_output[0].splitlines(True)

        self.assertEqual(len(split_output), (len(before_formatting)+4))

    #TEST 12: acceptance test
    def test_acceptable_command_execution_time(self):
        startTime = time.time()
        output = osrsinfo("sdadfalks", 0)
        endTime = time.time()
        self.assertTrue((endTime - startTime) < 1)

if __name__ == '__main__':
    unittest.main()

