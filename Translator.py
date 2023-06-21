import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS
import pyttsx3


r = sr.Recognizer()
translator = google_translator()
tts = pyttsx3.init()
#language = 'en';
language = input("Enter language to translate to, en for English and es for Spanish    ")
while True:
    #aquire text from audio
    with sr.Microphone() as source:
       
        print("Speak/Play Audio Now!")
        r.adjust_for_ambient_noise(source,duration = 1)
        #audio = r.listen(source,timeout=7)
        audio = r.listen(source)
        try:
            speech_text = r.recognize_google(audio)
            print(speech_text)        
        
            #translate text aquired    

            translated_text = translator.translate(speech_text,lang_tgt=f'{language}')
            print(translated_text)
            tts.say(translated_text)
            tts.runAndWait()
            #generate file with text translation and generate audio mp3 file
            #voice = gTTS(translated_text,lang='en')
            #voice.save("translatedAudio.mp3")
        except sr.UnknownValueError:
            print("Could not process/understand audio")
        except sr.RequestError:
            print("Could not request result from Google")
        except sr.WaitTimeoutError:
            print("No audio detected for the time limit")



