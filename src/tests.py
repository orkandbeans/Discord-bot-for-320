#Aaron Laferty Unit Testing for OpenAI Class
import time
from openAI import openAI
from dotenv import load_dotenv
import os

AI = openAI()
load_dotenv()
APIkey = os.getenv('API_TOKEN')

#test time of dalle Response(White Box Test) (Covers Dalle Classes generate method)
def testTimeOfResponseDalle():
    print("Testing Time of Dalle Response")
    startTime = time.time_ns()
    url = AI.dalle.generate("A house on the beach" , APIkey, False)
    endTime = (time.time_ns()-startTime)/1000000000.0
    print(f"Time (s): {endTime}")
    if (endTime < 10.00):
        print("Test Successful")
    else:
        print("Test Failed")

#test time of response from chat (White Box Test) (Covers ChatGPT Classes generate method)
def testTimeOfResponseChat():
    print("Testing Time of ChatGPT Response")
    startTime = time.time_ns()
    chat = AI.chatGPT.generate("Write a Poem", 100 ,APIkey)
    endTime = (time.time_ns()-startTime)/1000000000.0
    print(f"Time (s): {endTime}")
    if (endTime < 10.00):
        print("Test Successful")
    else:
        print("Test Failed")

#test to see if we will reject a bad API (White Box Test) (Covers OpenAI Classes that rely on API key validity)
def testRejectionByAPI():
    print("Testing Rejection By Invalid API")
    chat = AI.chatGPT.generate("Write a Poem", 100, 123456789)
    print(chat)
    if (chat == "ERROR CODE 1"):
        print("Test Successful")
    else:
        print("Test Failed")

#test to see if we will reject a violation of OpenAI TOS (White Box Test) (Covers OpenAI Classes that rely on API key validity)
def testRejectionByTOSViolation():
    print("Testing Rejection By TOS Violation")
    violatingPhrase = os.getenv("HATE")
    url = AI.dalle.generate(str(violatingPhrase), APIkey, False)
    print(url)
    if (url == "ERROR CODE 4"):
        print("Test Successful")
    else:
        print("Test Failed")

#test to see if we will reject because of reaching a user's monthly limit (White Box Test) (Covers OpenAI Classes that rely on API key validity)
def testRejectionByLimit():
    print("Testing Rejection By Limited")
    url = AI.dalle.generate("A balloon in the sky", APIkey, False)
    if (url == "ERROR CODE 2"):
        print("Test Successful")
    else:
        print("Test Failed")

#test to see if we will reject when the site is unavailable (White Box Test) (Covers OpenAI Classes that rely on API key validity)
def testRejectionBySiteFailure():
    print("Testing Rejection By Site Failure")
    url = AI.dalle.generate("A balloon in the sky", APIkey, False)
    if (url == "ERROR CODE 3"):
        print("Test Successful")
    else:
        print("Test Failed")

#test the time of dalle when downloading the image instead. (White Box Test) (Covers Dalle classes' generate method with download image time)
def testTimeOfResponseDalleDownload():
    print("Testing Time of Dalle Download Response")
    startTime = time.time_ns()
    url = AI.dalle.generate("A house on the beach" , APIkey, True)
    endTime = (time.time_ns()-startTime)/1000000000.0
    print(f"Time (s): {endTime}")
    if (endTime < 10.00 and os.path.isfile("temp/dalle.png")):
        print("Test Successful")
    else:
        print("Test Failed")
    os.remove("temp/dalle.png")

#test to see if dalle will send a response after valid arguments (Covers Dalle Classes generate method)
def testResponseDalle():
    print("Testing Dalle Response")
    try:
        url = AI.dalle.generate("A house on the beach" , APIkey, False)
    except:
        print("Test Failed")
    print("Test successful")

#test to see if dalle will send a downloaded response after valid arguments (Covers Dalle Classes generate and download method)
def testResponseDownloadDalle():
    print("Testing Dalle Download Response")
    url = AI.dalle.generate("A house on the beach" , APIkey, True)
    if (os.path.isfile("temp/dalle.png")):
        print("Test Successful")
    else:
        print("Test Failed")
    os.remove("temp/dalle.png")

#test to see if chatgpt will send a response after valid arguments (Covers chatGPT Classes generate method)
def testResponseChat():
    print("Testing chatGPT Response")
    try:
        url = AI.chatGPT.generate("Write a poem", 100 , APIkey)
    except:
        print("Test Failed")
    print("Test successful")

#test to see if dalle will work after retrieving an API key from our database (Covers Dalle Classes generate method and fetchAPI fetchAPI method)
def testDalleAfterRetrieval():
    print("Testing Dalle with Database for key")
    fetchedAPI = AI.fetchAPI(1320440213)
    try:
        url = AI.dalle.generate("A house on the beach" , fetchedAPI, False)
    except:
        print("Test Failed")
    print("Test successful")

#test to see if chatGPT will work after retrieving an API key from our database. (Covers chatGPT Classes generate method and fetchAPI method)
def testChatGPTAfterRetrieval():
    print("Testing chatGPT with Database for key")
    fetchedAPI = AI.fetchAPI(69804325834)
    try:
        url = AI.chatGPT.generate("Write a poem", 100 , fetchedAPI)
    except:
        print("Test Failed")
    print("Test successful")


def main():
    testResponseDalle()
    print()
    testResponseChat()
    print()
    testResponseDownloadDalle()
    print()
    testDalleAfterRetrieval()
    print()
    testChatGPTAfterRetrieval()
    print()
    testTimeOfResponseDalle()
    print()
    testTimeOfResponseChat()
    print()
    testTimeOfResponseDalleDownload()
    print()
    testRejectionByAPI()
    print()
    testRejectionByLimit()
    print()
    testRejectionBySiteFailure()
    print()
    testRejectionByTOSViolation()

if __name__ == "__main__":
    main()
