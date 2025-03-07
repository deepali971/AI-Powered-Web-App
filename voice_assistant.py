import speech_recognition as sr
import logging
import pyttsx3
import requests
import datetime
import time
import threading
from flask import Flask, jsonify

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Replace with your actual API keys
NEWS_API_KEY = "Y3d2051db41124ee38f9423003ab599c0"
WEATHER_API_KEY = "ca143c002e5243d728b17b496a8e734e"

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    """Fetch real-time weather for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        weather_response = f"The current temperature in {city} is {temp}°C with {description}."
        speak(weather_response)  # Speak the weather
        return weather_response
    else:
        error_message = f"Sorry, I couldn't find weather details for {city}."
        speak(error_message)
        return error_message

def get_news():
    """Fetch latest news headlines."""
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "articles" in data:
        top_articles = data["articles"][:5]  # Get top 5 headlines
        news_list = [f"{i+1}️⃣ {article['title']} – {article['description']}" for i, article in enumerate(top_articles)]
        news_response = "Here are the latest news headlines: " + " ".join(news_list)
        speak(news_response)  # Speak the news
        return news_response
    else:
        error_message = "Sorry, I couldn't fetch the news."
        speak(error_message)
        return error_message

def set_alarm(alarm_time):
    """Set an alarm at the given time."""
    now = datetime.datetime.now()
    alarm_datetime = datetime.datetime.strptime(alarm_time, "%H:%M")
    alarm_datetime = alarm_datetime.replace(year=now.year, month=now.month, day=now.day)

    time_to_wait = (alarm_datetime - now).total_seconds()
    if time_to_wait < 0:
        error_message = "You cannot set an alarm for the past. Please provide a future time."
        speak(error_message)
        return error_message

    def alarm_thread():
        time.sleep(time_to_wait)
        speak("Time to wake up! Your alarm is ringing.")

    threading.Thread(target=alarm_thread, daemon=True).start()
    confirmation = f"Alarm set for {alarm_time}."
    speak(confirmation)
    return confirmation

app = Flask(__name__)

@app.route('/listen', methods=['GET'])
def listen_route():
    """Listens to the user's voice and converts it to text, then processes the command."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio).lower()  # Speech-to-text
            print(f"Recognized: {text}")

            response = "I did not understand that."
            
            if "weather in" in text:
                city = text.split("weather in")[-1].strip()
                response = get_weather(city) if city else "Please specify a city for the weather."
            elif "news" in text:
                response = get_news()
            elif "set alarm for" in text:
                alarm_time = text.split("set alarm for")[-1].strip()
                response = set_alarm(alarm_time) if alarm_time else "Please specify a time for the alarm."
            else:
                response = f"You said: {text}"
                speak(response)  # Speak the response

            return jsonify({'text': text, 'response': response})

        except sr.UnknownValueError:
            logging.error("Speech recognition could not understand audio.")
            return jsonify({'text': "Sorry, I did not understand.", 'response': "Sorry, I did not understand."})
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            return jsonify({'text': "Speech recognition service is unavailable.", 'response': "Speech recognition service is unavailable."})

@app.route('/')
def index():
    return open("voice.html").read()

# Example usage
if __name__ == "__main__":
    app.run(debug=True)
