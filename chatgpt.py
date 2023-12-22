from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep 
import pyttsx3
import speech_recognition as sr
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# this import is for path liberary so that data has to be stored in chromedata
import pathlib
from Clap import MainClapExe
MainClapExe()

def speak(text):
    engine = pyttsx3.init() 
    Id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    engine.setProperty('voice', Id)
    engine.say(text=text)
    engine.runAndWait()

def speechrecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source,0,8)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language="en")
        return query.lower()
    
    except: 
        return ""


ScriptDir = pathlib.Path().absolute()
 
ChatNumber = 3
url = "https://flowgpt.com/chat"
chrome_option = Options()
user_agent ="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"
chrome_option.add_argument(f"user-agent={user_agent}")
# 2 lines are for chromedata
chrome_option.add_argument('--profile-directory=Default')
chrome_option.add_argument("--headless=new")
chrome_option.add_argument(f'user-data-dir={ScriptDir}\\chromedata')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_option)
driver.maximize_window()
driver.get(url=url)
# sleep(500)

def Checker():
    global ChatNumber
    
    for i in range(1,1000):
        if i%2 != 0:
            try:
                ChatNumber = str(i)
                Xpath = f"/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div[{ChatNumber}]/div/div/div/div[1]"
                driver.find_element(by=By.XPATH,value=Xpath)
            except:
                print(f"The next ChatNumber is : {i}")
                ChatNumber = str(i)
                break


def Websiteopener():
    while True:
        try:
            xPATH = '/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div[3]/textarea'
            driver.find_element(by=By.XPATH,value=xPATH)
            break
        except:
            pass

def SendMessage(Query):
    xPATH = '/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div[3]/textarea'
    driver.find_element(by=By.XPATH,value=xPATH).send_keys(Query)
    sleep(0.5)
    Xpath2 = '/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div[3]/button'
    driver.find_element(by=By.XPATH,value=Xpath2).click()
# /html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div[9]/div/div/div/div[1]
# /html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div[7]/div/div/div/div[1]
def Resultscrapper():
    global ChatNumber
    ChatNumber = str(ChatNumber)
    Xpath = f"/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div[{ChatNumber}]/div/div/div/div[1]"
    Text = driver.find_element(by=By.XPATH,value=Xpath).text
    ChatNumberNew = int(ChatNumber) + 2
    ChatNumber = ChatNumberNew
    return Text

# def Popupremover():
#     Xpath = '/html/body/div[3]/div[3]/div/section/div/div[3]/button[2]'
#     driver.find_element(by=By.XPATH,value=Xpath).click()

# Popupremover()
# sleep(5000)
def waitfortheanswer():
    #  this is the xpath of stop generating button in chatgpt
    sleep(2)
    Xpath ="/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div/button"
    while True:
       try:
           driver.find_element(by=By.XPATH,value=Xpath)
       except:
           break



Websiteopener() 
Checker()
while True:
    Query = speechrecognition()
    if len(str(Query))<3:
        pass
    elif Query == None:
        pass
    else:
        SendMessage(Query=Query)
        waitfortheanswer()
        Text = Resultscrapper()
        speak(Text)
