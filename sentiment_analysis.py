from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import os


class SentimentAnalyzer:

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def generate_sentiment_analysis(self, file_path, chunk_size):
        sentiment_scores = {
            "pos": 0,
            "neg": 0,
            "neu": 0,
            "compound": 0,
            "confidence": 0,
        }

        # Read the input text file
        with open(file_path, "r", encoding="utf-8") as file:

            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                sentiment = self.sia.polarity_scores(chunk)
                for key in sentiment_scores:
                    if key != "confidence":
                        sentiment_scores[key] += sentiment[key]
                    else:
                        sentiment_scores[key] += abs(sentiment["compound"])

        file_size = os.path.getsize(file_path)

        total_chunks = file_size // chunk_size
        if file_size % chunk_size != 0:
            total_chunks += 1
        for key in sentiment_scores:
            sentiment_scores[key] /= total_chunks
        return sentiment_scores

    def analyze_sentiment(self, file_path, chunk_size=1000):
        sentiment_scores = self.generate_sentiment_analysis(file_path, chunk_size)
        output = {}
        if sentiment_scores["compound"] > 0.05:
            output["sentiment"] = "positive"
        elif sentiment_scores["compound"] < -0.05:
            output["sentiment"] = "negative"
        else:
            output["sentiment"] = "neutral"
            sentiment_scores['confidence'] = 1.0

        output["confidence"] = sentiment_scores["confidence"]

        return output

if __name__ == '__main__':
    # Print the sentiment scores
    print("Sentiment Analysis Results:")
    file_path = "test.txt"
    analyzer_obj = SentimentAnalyzer()
    sentiment_scores = analyzer_obj.analyze_sentiment(file_path, 1000)
    print(sentiment_scores)

