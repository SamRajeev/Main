import webbrowser
from PyDictionary import PyDictionary
import wikipedia
from urllib.request import urlopen as ureq
import re
import pyttsx3
import speech_recognition as sr
from flask import Flask
from flask_restful import Api, Resource, reqparse

try:
    from googlesearch import search
except ImportError:
    print('No google')

PythonApp = Flask(__name__)
api = Api(PythonApp)

reqobj = reqparse.RequestParser()
reqobj.add_argument("command", type=str, help="Command is required")

dictionary = PyDictionary()
result = "Sorry No results"
webbrowser.register('chrome', None,
                    webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))


def audio_data():
    r = sr.Recognizer()
    with sr.Microphone(0) as source:
        print('loop')
        audio = r.listen(source, phrase_time_limit=8)
        print('loop over')
        said = ''

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception", str(e))

    return said.lower()


# print('Listening...')
# query = audio_data()
# print(query)


def speak(text):
    engine = pyttsx3.init()
    vid = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    engine.setProperty('voice', vid)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 100)
    engine.say(text)
    engine.runAndWait()


def query_splitter(query):
    try:
        query2 = query.split(" ")
        final_query = query2.index("of") + 1
        return final_query,query2
    except:
        pass


def find_synonym(query):
    try:
        final_query,query2 = query_splitter(query)
        synonyms = dictionary.synonym(query2[final_query])
        result = ("Synonym of" + " " + query2[final_query] + " " + "is" + " " + synonyms[0] + "," + synonyms[1] + "," +
                  synonyms[2])
        speak(result)
        return result

    except:
        result = "Sorry No results"
        speak(result)
        return result


def find_meaning(query):
    try:
        final_query,query2 = query_splitter(query)
        meanings = dictionary.meaning(query2[final_query])
        final_meaning = str(meanings['Adjective'][0])
        result = ("Meaning of" + " " + query2[final_query] + " " + "is" + "  " + final_meaning)
        speak(result)
        return result
    except:
        result = "Sorry No results"
        speak(result)
        return(result)


def find_antonym(query):
    try:
        final_query,query2 = query_splitter(query)
        antonyms = dictionary.antonym(query2[final_query])
        result = ("Antonym of" +" "+ query2[final_query] + " " + "is" + " " + antonyms[0] + "," + antonyms[1] + "," +
                  antonyms[2])
        speak(result)
        return result
    except:
        result = "Sorry No results"
        speak(result)
        return result


def wikipedia_fuction(query):
    try:
        query_final = query.replace('wikipedia search ', '')
        result = wikipedia.summary(query_final, sentences=1)
        speak(result)
        return result

    except:
        result = "Sorry No results"
        speak(result)
        return result


def music(query):
    query3 = query.replace("play ", '')
    query4 = query3.replace(' ', '+')
    url = "https://www.youtube.com/results?search_query=" + query4

    uClient = ureq(url)
    page_data = uClient.read().decode()
    uClient.close()

    video_ids = re.findall(r"watch\?v=(\S{11})", page_data)
    final_url = "https://www.youtube.com/watch?v=" + video_ids[0]
    speak("Playing" + " " + query3 + " " + "from youtube")
    print("Playing" + " " + query3 + " " + "from youtube")
    webbrowser.get('chrome').open(final_url)
    return ("Playing" + " " + query3 + " " + "from youtube" + " " + final_url)


def open_site(query):
    query2 = query.replace('open ', '')
    for result in search(query2, tld='com', lang='en', num=1, stop=1, pause=2.0):
        final_result = "Opening" +" "+ query2
        speak(final_result)
        webbrowser.get('chrome').open(result)
        return final_result


def google_search(query):
    try:
        for link in search(query, tld='in', lang='en', num=1, stop=1, pause=2.0):
            if link is None:
                result_final = "Sorry No results"
            else:
                result_final = "Opening site..."
                print(result_final)
                webbrowser.get('chrome').open(link)

            return (result_final)

    except:
        result_final = "Sorry No results"
        return (result_final)


class Functions(Resource):
    def put(self):
        args = reqobj.parse_args()
        query_final = args['command']
        print(query_final)

        if "synonym" in query_final:
            final_message = find_synonym(query_final)
            return final_message

        elif "meaning" in query_final:
            final_message = find_meaning(query_final)
            return final_message

        elif "antonym" in query_final:
            final_message = find_antonym(query_final)
            return final_message

        elif "wikipedia search" in query_final:
            final_message = wikipedia_fuction(query_final)
            return final_message

        elif "play" in query_final:
            final_message = music(query_final)
            return final_message

        elif "open" in query_final:
            final_message = open_site(query_final)
            return final_message


        else:
            final_message = google_search(query_final)
            return final_message


api.add_resource(Functions, "/Functions")

if __name__ == "__main__":
    PythonApp.run(port=12345)
