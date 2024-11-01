from textblob import TextBlob

# Analyze a sentence for polarity and subjectivity
def analyze_sentence(sentence):
    blob = TextBlob(sentence)  # Create TextBlob object for analysis
    sentiment = blob.sentiment  # Get sentiment properties from TextBlob
    return sentiment.polarity, sentiment.subjectivity  # Return polarity and subjectivity scores

