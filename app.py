from flask import Flask, render_template, request, jsonify, redirect, url_for
from textblob import TextBlob
import requests
import speech_recognition as sr
import pyttsx3
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import datetime
import threading

app = Flask(__name__)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# API Keys (Replace with valid keys)
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

# Voice Assistant Functions
def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return "Sorry, I did not understand that."

# Sentiment Analysis Function
def analyze_sentiment(text):
    """Analyze sentiment of a given text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity, 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral'

# Weather Function
def get_weather(city):
    """Fetch real-time weather for a given city."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        weather_info = f"The temperature in {city} is {data['main']['temp']}°C with {data['weather'][0]['description']}."
        speak(weather_info)
        return {'temperature': data['main']['temp'], 'humidity': data['main']['humidity'], 'weather': data['weather'][0]['description']}
    else:
        error_msg = "Sorry, I couldn't fetch the weather data."
        speak(error_msg)
        return {'error': error_msg}

# News Function
def get_news():
    """Fetch top 5 news headlines with summaries."""
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "articles" in data:
        top_articles = data["articles"][:5]
        news_list = [
            f"{i+1}. {article['title']} - {article['description'][:100]}..." 
            for i, article in enumerate(top_articles)
        ]
        news_response = "Here are the top 5 news headlines: " + " ".join(news_list)
        speak(news_response)
        return news_response
    else:
        error_msg = "Sorry, I couldn't fetch the news."
        speak(error_msg)
        return error_msg

# Image Generation Function
def generate_image_from_text(text):
    """Generate an image from the given text."""
    img = Image.new('RGB', (400, 200), color='white')
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 10), text, fill=(0, 0, 0), font=font)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return img_base64

# Alarm Function
def set_alarm(alarm_time):
    """Set an alarm at the given time."""
    now = datetime.datetime.now()
    alarm_datetime = datetime.datetime.strptime(alarm_time, "%H:%M")
    alarm_datetime = alarm_datetime.replace(year=now.year, month=now.month, day=now.day)

    time_to_wait = (alarm_datetime - now).total_seconds()
    if time_to_wait < 0:
        error_msg = "You cannot set an alarm for the past. Please provide a future time."
        speak(error_msg)
        return error_msg

    def alarm_thread():
        """Trigger the alarm."""
        time.sleep(time_to_wait)
        speak("Time to wake up! Your alarm is ringing.")

    threading.Thread(target=alarm_thread, daemon=True).start()
    confirmation = f"Alarm set for {alarm_time}."
    speak(confirmation)
    return confirmation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice')
def voice():
    return render_template('voice.html')

@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

@app.route('/weather_dashboard')
def weather_dashboard():
    return render_template('weather.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze sentiment from user input."""
    text = request.json.get('text', '')
    polarity, subjectivity, classification = analyze_sentiment(text)
    return jsonify({'polarity': polarity, 'subjectivity': subjectivity, 'classification': classification})

@app.route('/weather_data', methods=['GET'])
def weather_data():
    """Fetch weather data based on city."""
    city = request.args.get('city')
    weather_data = get_weather(city)
    return jsonify(weather_data)

@app.route('/generate_image', methods=['POST'])
def generate_image():
    """Generate an image from text input."""
    text = request.json.get('text', '')
    img_base64 = generate_image_from_text(text)
    return jsonify({'image': img_base64})

@app.route('/listen', methods=['GET'])
def listen_voice():
    """Process voice commands for weather, news, alarms, and image generation."""
    command = listen()
    
    if "weather in" in command:
        city = command.split("weather in")[-1].strip()
        response = get_weather(city) if city else "Please specify a city for the weather."
    elif "news" in command:
        response = get_news()
    elif "generate image of" in command:
        description = command.split("generate image of")[-1].strip()
        response = generate_image_from_text(description) if description else "Please specify an image description."
    elif "set alarm for" in command:
        alarm_time = command.split("set alarm for")[-1].strip()
        response = set_alarm(alarm_time) if alarm_time else "Please specify a time for the alarm."
    else:
        response = f"You said: {command}"
        speak(response)

    return jsonify({'text': command, 'response': response})

if __name__ == '__main__':
    app.run(debug=True)
