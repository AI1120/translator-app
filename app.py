import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play

st.title("Arabic to English Voice Translator")

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    with microphone as source:
        st.info("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        st.info("Listening...")
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language="ar-SA")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def translate_text(text, src='ar', dest='en'):
    """Translate text from source language to destination language."""
    translator = Translator()
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text

def text_to_speech(text, lang='en'):
    """Convert text to speech."""
    tts = gTTS(text=text, lang=lang)
    tts.save("translated_audio.mp3")
    return "translated_audio.mp3"

recognizer = sr.Recognizer()
microphone = sr.Microphone()

if st.button("Translate"):
    st.info("Speak now...")

    speech = recognize_speech_from_mic(recognizer, microphone)

    if speech["transcription"]:
        st.success("Transcription: " + speech["transcription"])
        translation = translate_text(speech["transcription"])
        st.success("Translation: " + translation)

        audio_file = text_to_speech(translation)

        audio = AudioSegment.from_mp3(audio_file)
        st.audio(audio_file, format="audio/mp3")

        play(audio)
        os.remove(audio_file)
    else:
        st.error(speech["error"])
