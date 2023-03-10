from kivy.app import App
from googletrans import Translator
import speech_recognition as sr
import os
from gtts import gTTS
from playsound import playsound
import arabic_reshaper
from bidi.algorithm import get_display

r = sr.Recognizer()
mic = sr.Microphone()
tr = Translator()

class SpeechCarrierApp(App):
    pass

    def convert_text_to_code(self, lang):

        global code_language_for_googletrans

        if (lang == "English"):
            code_language_for_googletrans = 'en'

        if (lang == "Arabic"):
            code_language_for_googletrans = 'ar'



    def voice_language(self, lang_voice):

        global code_language_for_speech_recognition

        if (lang_voice == "English"):
            code_language_for_speech_recognition = 'en'

        if (lang_voice == "Arabic"):
            code_language_for_speech_recognition = 'ar'



    def record(self):

        global content
        global texttt
        try:
            with mic as source:
                audio = r.listen(source)
                content = r.recognize_google(audio, language=code_language_for_speech_recognition)
                print("Did you say ", content)

                reshaped_text_field1 = arabic_reshaper.reshape(content)
                bidi_text_field1 = get_display(reshaped_text_field1)
                field = self.root.ids['field1']
                field.text = bidi_text_field1

                translated = tr.translate(content, code_language_for_googletrans)
                texttt = translated.text

                reshaped_text = arabic_reshaper.reshape(texttt)
                bidi_text = get_display(reshaped_text)

                field = self.root.ids['field2']
                field.text = bidi_text

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

    def playysound(self):

        tts = gTTS(text=texttt, lang=code_language_for_googletrans)
        filename = "w.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)

if __name__ == '__main__':
    SpeechCarrierApp().run()