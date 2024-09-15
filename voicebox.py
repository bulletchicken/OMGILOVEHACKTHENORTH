import os
import subprocess
from pyht import Client, TTSOptions, Format
import anthropic
playht_client = Client("Y7YFtCv3NPZXQptFTNcQQSLYIBF3", "8e09ec1f89d9441b8cc84e9a99a73ae0")

def TTS():
    # Configure your stream
    options = TTSOptions(
        voice="s3://voice-cloning-zero-shot/ac9e2984-c7bb-44c8-8b6b-5c10728ad5cf/original/manifest.json",
        sample_rate=44_100,
        format=Format.FORMAT_MP3,
        speed=1,
    )
    
    # Text to be converted to speech
    text = ""

    
    
    # Output file name
    output_file = "bpmtest.mp3"
    
    # Generate and save the audio
    with open(output_file, "wb") as f:
        for chunk in playht_client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
            f.write(chunk)
    
    print(f"Audio saved to {output_file}")
    
    # Play the audio using afplay
    subprocess.run(["afplay", output_file])

TTS()