import os
import datetime
from xmlrpc import client
from openai import OpenAI
import argparse
from google import genai
from google.genai import types
import anthropic
import wave

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"

def initialize_client(model_name):
    if model_name.startswith("gemini"):
        print("Using Gemini model, initializing client with Gemini API key.")
        client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    elif model_name.startswith("deepseek"):
        print("Using DeepSeek model, initializing client with DeepSeek API key.")
        client = OpenAI(
            api_key=os.environ.get('DEEPSEEK_API_KEY'), 
            base_url="https://api.deepseek.com"
        )
    elif model_name.startswith("claude"):
        print("Using Claude model, initializing client with Claude API key.")
        client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    else:
        print("Using OpenAI model, initializing client with OpenAI API key.")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=OPENAI_API_KEY)

    return client

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

def tts(target_language, prompt, client, model, output_file):
    print(f"Prompting for {target_language}: {prompt}")
    if model.startswith("claude"):
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            system=f"You are a knowledgable assistant that can respond in {target_language}.",
            messages=[
                {
                    "role": "user",
                    "content": f"'{prompt}'",
                }
            ],
        )
        return response.content[0].text.strip()
    elif model.startswith("gemini"):
        response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            # speech_config=types.SpeechConfig(
            #     voice_config=types.VoiceConfig(
            #         prebuilt_voice_config=types.PrebuiltVoiceConfig(
            #         voice_name='Kore',
            #         )
            #     )
            # ),
        )
        )
        print(response)
        data =response.candidates[0].content.parts[0].inline_data.data
        wave_file(output_file, data)
    else:
        with client.audio.speech.with_streaming_response.create(
            model=model,
            input=prompt,
            voice="coral",
            instructions=f"Speak in the language {target_language}.",
        ) as response:
            response.stream_to_file(output_file)

def asr(target_language, prompt, client, model) -> str:
    print(f"Prompting for {target_language}: {prompt}")
    if model.startswith("claude"):
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            system=f"You are a knowledgable assistant that can respond in {target_language}.",
            messages=[
                {
                    "role": "user",
                    "content": f"'{prompt}'",
                }
            ],
        )
        return response.content[0].text.strip()
    elif model.startswith("gemini"):
        myfile = client.files.upload(file=prompt)
        response = client.models.generate_content(
            model=model, contents=["Transcribe this audio clip in " + target_language, myfile]
        )
        return response.text
    else:
        audio_file= open(prompt, "rb")
        response = client.audio.transcriptions.create(
            model=model, 
            prompt="Transcribe this audio clip in " + target_language + " using the correct orthography and diacritics.",
            file=audio_file
        )
        return response.text
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vocabulary Quiz")
    parser.add_argument("prompt", type=str, help="The prompt")
    parser.add_argument("task", type=str, help="The task to perform (asr or tts)")
    parser.add_argument("--lang", type=str, default="Muscogee", help="Target language")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model name to use")
    args = parser.parse_args()
    model_name = args.model

    # check task
    if args.task not in ["asr", "tts"]:
        raise ValueError("Invalid task. Must be 'asr' or 'tts'.")

    # init
    client = initialize_client(model_name)

    current_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # get response
    if args.task == "tts":
        output_file = f"out_{args.lang}_{model_name}_{current_date}.wav"
        response = tts(args.lang, args.prompt, client, model_name, output_file)
    else:
        # check file exists
        filename = args.prompt
        if not os.path.isfile(filename):
            raise ValueError(f"File {filename} does not exist.")
        output_file = f"out_{args.lang}_{model_name}_{current_date}.txt"
        response = asr(args.lang, args.prompt, client, model_name)
        with open(output_file, "w") as f:
            f.write(response)