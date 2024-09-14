import os
import subprocess
from pyht import Client, TTSOptions, Format
import anthropic

def run():
    client = anthropic.Anthropic(api_key="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")
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=50,
        temperature=0.8,
        system="You are a world-class poet. Respond only with short poems.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Why is the ocean salty?"
                    }
                ]
            }
        ]
    )
    response = message.content[0].text  # Extract the text from the response
    TTS(response)

# Initialize PlayHT API with your credentials
playht_client = Client("Y7YFtCv3NPZXQptFTNcQQSLYIBF3", "8e09ec1f89d9441b8cc84e9a99a73ae0")

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
    output_file = "output.mp3"
    
    # Generate and save the audio
    with open(output_file, "wb") as f:
        for chunk in playht_client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
            f.write(chunk)
    
    print(f"Audio saved to {output_file}")
    
    # Play the audio using afplay
    subprocess.run(["afplay", output_file])

run()