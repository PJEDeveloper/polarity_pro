import pyttsx3

# Function to convert the provided text to speech
def speak(text):
    engine = pyttsx3.init()  # Initialize the TTS engine
    voices = engine.getProperty('voices')  # Retrieve available voices
    try:
        engine.setProperty('voice', voices[1].id)  # Set to female voice if available
    except IndexError:
        print("Female voice not found...using default voice...")  # Use default if female voice is unavailable
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Process the TTS and wait for completion
