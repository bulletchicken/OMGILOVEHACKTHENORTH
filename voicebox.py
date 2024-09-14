import time
import anthropic

# Timing the API request
start_time = time.time()

api_key = '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'
client = anthropic.Anthropic(api_key=api_key)

with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "good morning!"}],
    model="claude-3-5-sonnet-20240620",
) as stream:
  for text in stream.text_stream:
      print(text, end="", flush=True)


# ---------------------------------------------------------------------------- #
#                                Text to Speech                                #
# ---------------------------------------------------------------------------- #


from pyht import Client, TTSOptions, Format

client = Client("Y7YFtCv3NPZXQptFTNcQQSLYIBF3", "8e09ec1f89d9441b8cc84e9a99a73ae0")


options = TTSOptions(
  
    voice="s3://voice-cloning-zero-shot/ac9e2984-c7bb-44c8-8b6b-5c10728ad5cf/original/manifest.json",


    sample_rate=44_100,
  

    format=Format.FORMAT_MP3,

    speed=1,
)

text = "hello! my name is ted"


for chunk in client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
    # Do whatever you want with the stream, you could save it to a file, stream it in realtime to the browser or app, or to a telephony system
    pass




print("API request took", time.time() - start_time, "seconds.")
