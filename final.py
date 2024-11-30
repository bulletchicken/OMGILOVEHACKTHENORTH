# ---------------------------------------------------------------------------- #
#                                   CV                                         #
# ---------------------------------------------------------------------------- #

import cv2
from ultralytics import YOLO
from serial import Serial
import os
import math
import time


# ---------------------------------------------------------------------------- #
#                                    Arduino                                   #
# ---------------------------------------------------------------------------- #

from serial import Serial
import os
ser = Serial('/dev/cu.usbserial-11340', 9600)
from pygame import mixer
import pygame
mixer.init()


# ---------------------------------------------------------------------------- #
#                                play and claude                               #
# ---------------------------------------------------------------------------- #

import os
import subprocess
from pyht import Client, TTSOptions, Format
import anthropic
import base64
import httpx

# ---------------------------------------------------------------------------- #
#                                   Selenium                                   #
# ---------------------------------------------------------------------------- #

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# ---------------------------------------------------------------------------- #
#                                 assembly tts                                 #
# ---------------------------------------------------------------------------- #

import assemblyai as aai
import os; import appscript; import time
import pyautogui
aai.settings.api_key = "0b4ddfbf65af49a885ff85ea61576f52"


# ---------------------------------------------------------------------------- #
#                          the start up                                        #
# ---------------------------------------------------------------------------- #
cam = cv2.VideoCapture(0)
# ---------------------------------------------------------------------------- #
#                                    playAI                                    #
# ---------------------------------------------------------------------------- #

def turnOnPlay():
    clickable = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button, a, [role='button']"))
    )
    clickable.click()
    print("Clicked on a clickable element within the iframe")

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()

#keeps the tab open
chrome_options.add_experimental_option("detach", True)

# chrome_options.add_argument("--headless")  # Uncomment this if you want to run headless

# Setup the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Get the absolute path to your HTML file
html_path = os.path.abspath("test.html")

# Navigate to the page using the file:// protocol
driver.get(f"file://{html_path}")


iframe = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "play-ai-embed"))
)

print(f"Iframe found: ID = {iframe.get_attribute('id')}, Src = {iframe.get_attribute('src')}")

# Switch to the iframe
driver.switch_to.frame(iframe)

# Wait for the iframe content to load (adjust timeout as needed)
time.sleep(3)
    
try:
    #startup
    # Try to find a clickable element within the iframe
    turnOnPlay()

except Exception as e:
    print(f"An error occurred: {e}")
    # Take a screenshot for debugging
    driver.save_screenshot("error_screenshot.png")
    print("Screenshot saved as error_screenshot.png")



# ---------------------------------------------------------------------------- #
#                                      stt                                     #
# ---------------------------------------------------------------------------- #

def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
    #starup

    # ---------------------------------------------------------------------------- #
    #                                      stt                                     #
    # ---------------------------------------------------------------------------- #
        
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(transcript.text, end="\r\n")
        print(transcript.text)

        if(transcript.text.lower().find("hi")!=-1):
            ser.write("wave".encode())
        elif(transcript.text.lower().find("check out")!=-1):
            #send to manual claude and disable play.ai
            driver.refresh()
            claude(transcript.text)

        elif(transcript.text.lower().find("help me")!=-1):
            driver.refresh()
            process = subprocess.Popen(['python3', 'emergency.py'])


        elif(transcript.text.lower().find("feel too")!=-1):
            driver.refresh()
            ser.write("readPulse".encode())
            mixer.music.load('public_audio/handhold.mp3')
            mixer.music.play()

            pygame.time.delay(7000)
            print("past")
            playAudio()



        elif(transcript.text.lower().find("ted")!=-1):
            print(ser.readline())
            ser.write("leftRight".encode())

        elif(transcript.text.lower().find("michael jackson")!=-1):

            mixer.music.load('public_audio/billie.mp3')
            mixer.music.play()
            ser.write("dance".encode())
        
        elif(transcript.text.lower().find("your move")!=-1):

            mixer.music.load('public_audio/billie.mp3')
            mixer.music.play()
            ser.write("dance".encode())

        elif(transcript.text.lower().find("call up")!=-1):
            os.popen('open facetime://' + "6729993167")
            appscript.app('FaceTime').activate() 
            time.sleep(1)
            pyautogui.click(90,750)
        elif(transcript.text.lower().find("end the call")!=-1):
            pyautogui.click(90,750)


    else:
        print(transcript.text, end="\r")

        


def playAudio():
    mixer.music.load('public_audio/bpmtest.mp3')
    mixer.music.play()








def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def claude(message):
    global ret, img
    ret, img = cam.read()

    os.remove("picture.png") #reset
    img_name = "picture.png".format(0)

    cv2.imwrite(img_name, img)
    image_name = "picture.png"
    
    base64_image = encode_image(image_name)

    client = anthropic.Anthropic(api_key="")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=50,
        temperature=0.8,
        system="You are an assistive healthcare and funny and chatty teddy bear.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_image
                        }
                    },
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        ]
    )
    
    return response.content[0].text

# Initialize PlayHT API with your credentials
playht_client = Client('Y7YFtCv3NPZXQptFTNcQQSLYIBF3', "8e09ec1f89d9441b8cc84e9a99a73ae0")

def TTS(response):
    # Configure your stream
    options = TTSOptions(
        voice="s3://voice-cloning-zero-shot/ac9e2984-c7bb-44c8-8b6b-5c10728ad5cf/original/manifest.json",
        sample_rate=44_100,
        format=Format.FORMAT_MP3,
        speed=1,
    )
    
    # Text to be converted to speech
    text = response
    
    # Output file name
    output_file = "public_audio/output.mp3"
    
    # Generate and save the audio
    with open(output_file, "wb") as f:
        for chunk in playht_client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
            f.write(chunk)
    
    print(f"Audio saved to {output_file}")
    
    # Play the audio using afplay
    subprocess.run(["afplay", output_file])

#sdfsdf

# ---------------------------------------------------------------------------- #
#                                   assembly                                   #
# ---------------------------------------------------------------------------- #


def on_error(error: aai.RealtimeError):
    print("An error occured:", error)


def on_close():
    print("Closing Session")


transcriber = aai.RealtimeTranscriber(
    sample_rate=8_000,
    on_data=on_data,
    on_error=on_error,
    on_open=on_open,
    on_close=on_close,
    end_utterance_silence_threshold=0
    #to change the threshhold midway (maybe after the keyword is said? jk that would be no improvement) -> transcriber.configure_end_utterance_silence_threshold(300)
)

transcriber.connect()


microphone_stream = aai.extras.MicrophoneStream(sample_rate=8_000)
transcriber.stream(microphone_stream)

