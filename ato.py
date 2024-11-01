import speech_recognition as sr
import tts  # Import the text-to-speech module
import lp   # Import the language processing module for sentiment analysis
import tkinter as tk
from tkinter import scrolledtext
import threading

# Initialize recognizer and a flag to track if recording is active
recognizer = sr.Recognizer()
is_recording = False
transcribed_text = ""  # Store the last transcription to replay with TTS

# Function to interpret polarity and subjectivity into descriptive sentiment labels
def interpret_sentiment(polarity, subjectivity):
    # Classify polarity into sentiment categories
    if polarity > 0.5:
        sentiment = "Very Positive"
    elif polarity > 0:
        sentiment = "Positive"
    elif polarity == 0:
        sentiment = "Neutral"
    elif polarity < -0.5:
        sentiment = "Very Negative"
    else:
        sentiment = "Negative"

    # Classify subjectivity level
    if subjectivity > 0.7:
        subjectivity_description = "Highly Subjective"
    elif subjectivity > 0.3:
        subjectivity_description = "Somewhat Subjective"
    else:
        subjectivity_description = "Fairly Objective"

    return sentiment, subjectivity_description

# Fucntion to initialize GUI elements and define button functionality
def init_gui(root):
    global transcript_label, transcript_box, start_button, stop_button, exit_button, transcribed_text

    # Function to start recording audio and display recording status
    def start_recording():
        global is_recording
        is_recording = True  # Activate recording state
        transcript_label.config(text="Recording...")  # Update status label
        stop_button['state'] = 'normal'  # Enable stop button
        start_button['state'] = 'disabled'  # Disable start button during recording
        threading.Thread(target=record_audio).start()  # Start recording in a separate thread

    # Function to stop recording when button is pressed
    def stop_recording():
        global is_recording
        is_recording = False  # Deactivate recording state
        stop_button['state'] = 'disabled'  # Disable stop button

    # Functiuon to capture audio in a loop until stopped by the user
    def record_audio():
        global is_recording
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            while is_recording:  # Continue capturing audio until stopped
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Record audio
                    process_audio(audio)  # Process the recorded audio
                except sr.WaitTimeoutError:
                    continue  # Restart recording if timeout occurs

    # Function to convert audio to text, analyze sentiment, and store for TTS replay
    def process_audio(audio):
        global transcribed_text
        try:
            transcribed_text = recognizer.recognize_google(audio)  # Convert audio to text
            transcript_box.config(state='normal')
            transcript_box.delete(1.0, tk.END)  # Clear previous transcript
            transcript_box.insert(tk.END, transcribed_text)  # Display new transcript
            transcript_box.config(state='disabled')
            
            # Perform sentiment analysis
            polarity, subjectivity = lp.analyze_sentence(transcribed_text)
            sentiment, subjectivity_description = interpret_sentiment(polarity, subjectivity)
            
            # Use TTS to announce sentiment analysis results
            tts.speak(f"This is considered {sentiment} and {subjectivity_description}")
            
            # Display sentiment analysis results in the GUI label
            transcript_label.config(text=f"Sentiment: {sentiment} | Subjectivity: {subjectivity_description}")
        except sr.RequestError:
            transcript_label.config(text="API unavailable, please try again")  # Error handling for API issues
        except sr.UnknownValueError:
            transcript_label.config(text="Unable to recognize speech, please try again")  # Error for unrecognized speech
        finally:
            start_button['state'] = 'normal'  # Re-enable start button for new recordings

    # Label to show instructions or feedback on sentiment analysis
    transcript_label = tk.Label(root, text="Press 'Start Recording' to begin")
    transcript_label.pack()

    # Scrollable text box to display the transcribed text
    transcript_box = scrolledtext.ScrolledText(root, state='disabled', height=10)
    transcript_box.pack()

    # Button to start recording and sentiment analysis
    start_button = tk.Button(root, text="Perform Sentiment Analysis", command=start_recording)
    start_button.pack()

    # Button to stop recording
    stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state='disabled')
    stop_button.pack()

    # Button to repeat the last transcription using TTS
    tts_button = tk.Button(root, text="Repeat Transcription", command=lambda: tts.speak(transcribed_text))
    tts_button.pack()

    # Button to exit the application
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack()
