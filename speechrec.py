import streamlit as st
import time
import speech_recognition as sr

# create a list of available APIs
API_OPTIONS = ['Google', 'Microsoft', 'Amazon Transcribe']

# add a dropdown menu to select the API
selected_api = st.selectbox('Select the speech recognition API:', API_OPTIONS)

# create a list of available languages
LANGUAGES = ['English', 'Spanish', 'French', 'German']

# add a dropdown menu to select the language
selected_language = st.selectbox('Select the language:', LANGUAGES)

# modify the transcribe_speech() function to use the selected API and language
def transcribe_speech(pause=False):
    # Initialize recognizer class
    r = sr.Recognizer()

    # Reading Microphone as source
    with sr.Microphone() as source:

        # create a streamlit spinner that shows progress
        with st.spinner(text='Silence please, Calibrating background noise.....'):
            time.sleep(3)

        r.adjust_for_ambient_noise(source, duration=1)  # ..... Adjust the surround noise
        st.info("Speak now...")

        audio_text = None
        language_code = 'en-US'  # default language code

        if selected_language == 'Spanish':
            language_code = 'es-ES'
        elif selected_language == 'French':
            language_code = 'fr-FR'
        elif selected_language == 'German':
            language_code = 'de-DE'

        while True:
            if pause:
                r.wait_for_resume()
            else:
                audio_text = r.listen(source)  # listen for speech and store in audio_text variable

            with st.spinner(text='Transcribing your voice to text'):
                time.sleep(2)

            try:
                if selected_api == 'Google':
                    # using Google speech recognition to recognize the audio
                    text = r.recognize_google(audio_text, language=language_code)
                elif selected_api == 'Amazon Transcribe':
                    # using Amazon Transcribe API to recognize the audio
                    text = r.recognize_aws(audio_text, language_code)
                elif selected_api == 'Microsoft':
                    # using Microsoft Azure API to recognize the audio
                    text = r.recognize_azure(audio_text, language=language_code)
                else:
                    # invalid API selected
                    return "Invalid API selected."

                return text

            except sr.WaitTimeoutError:
                pass
            except sr.RequestError:
                return "Sorry, something went wrong with the speech recognition service."
            except sr.UnknownValueError:
                return "Sorry, I did not understand what you said."


if st.button("Save Transcript"):
    # show a file save dialog and get the filename and location
    filename = st.text_input("Enter the filename:")
    location = st.text_input("Enter the location (optional):")
    file_path = location + '/' + filename if location else filename

    # get the transcribed text
    transcribed_text = transcribe_speech()

    # write the transcribed text to the file
    with open(file_path, 'w') as f:
        f.write(transcribed_text)

    st.write("Transcript saved to:", file_path)
