AI-Powered Web App

Overview
This is an AI-powered web application that provides:
- Voice Assistance: A voice assistant that can process commands for weather, news, alarms, and AI-generated images from text.
- Sentiment Analysis: Analyzes the sentiment of user-provided text.
- Weather Dashboard: Fetches real-time weather information.

Built with Flask, Speech Recognition, TextBlob, and Pyttsx3.

Features
- Voice-controlled assistant for weather, news, alarms, and AI-generated images
- Sentiment analysis for text
- Real-time weather updates

Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/deepali971/AI-Powered-Web-App.git
   cd AI-Powered-Web-App
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

Usage
Run the application:
```sh
python app.py  # Or flask run
```
Then, open `http://127.0.0.1:5000/` in your browser.

Detailed Working
1. Voice Assistant
- Listens for voice commands using `speech_recognition`.
- Recognizes commands for:
  - Weather Updates: Fetches real-time weather using OpenWeather API.
  - News Headlines: Fetches top news using NewsAPI.
  - Set Alarms: Allows users to set a time-based alarm.
  - Generate Images: Converts text to images using PIL (Pillow library).
- Uses `pyttsx3` to provide spoken responses.

2. Sentiment Analysis
- Uses TextBlob to analyze sentiment of input text.
- Classifies text as Positive, Negative, or Neutral based on polarity.
- Provides sentiment polarity and subjectivity scores.

3. Weather Dashboard
- Users enter a city name.
- Fetches live weather data from OpenWeather API.
- Displays temperature, humidity, and weather conditions.

Libraries & APIs Used
Libraries
- Flask – Web framework
- SpeechRecognition – Voice recognition
- Pyttsx3 – Text-to-Speech conversion
- TextBlob – Sentiment analysis
- Requests – API requests handling
- Pandas & NumPy – Data processing
- Pillow (PIL) – Image generation

APIs
- OpenWeather API – Fetches real-time weather data
- NewsAPI – Retrieves the latest news headlines

Future Enhancements
- Integration with GPT: Enhance the voice assistant with AI-powered responses.
- Multi-language Support: Enable support for multiple languages in speech recognition and text analysis.
- User Authentication: Implement user login and authentication for personalized experiences.
- Database Storage: Store user interactions, sentiment analysis history, and past weather searches.
- Mobile App Integration: Extend the functionality to a mobile application.
- Improved UI/UX: Design a more interactive and user-friendly interface.
