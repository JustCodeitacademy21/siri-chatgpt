import speech_recognition as sr
import pyttsx3
import time
import openai

openai.api_key='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'
messages=[
    {"role":"system",
     "content":"You are a intelligent assistant."
     }
]

engine = pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)


def callback(recognizer,audio):
    try:
        voice=recognizer.recognize_google(audio,language="ru-RU").lower()
        print("Распознано: "+voice)
        messages.append(
            {"role":"user","content":voice},
        )
        chat=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",messages=messages
        )
        reply=chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        engine.say(reply)
        engine.runAndWait()
    except sr.UnknownValueError:
        print('Голос не распознан')
    except sr.RequestError:
        print('Неизвестная ошибка!')

def record_sound():

    r=sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)
        callback(r,audio)

engine.say("Привет! Я новая сири-GPT! Слушаю вас, чем могу вам помочь?")
engine.runAndWait()


while True:
    record_sound()