from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import re

# ---------------- CONFIG ----------------
API_KEY = "YOUR_API_KEY_HERE"
VIDEO_ID = "VIDEO_ID_HERE"
MAX_COMMENTS = 200
# ----------------------------------------

youtube = build("youtube", "v3", developerKey=API_KEY)

def fetch_comments(video_id, max_comments):
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request and len(comments) < max_comments:
        response = request.execute()

        for item in response["items"]:
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

        request = youtube.commentThreads().list_next(request, response)

    return comments


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text


def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"


def main():
    comments = fetch_comments(VIDEO_ID, MAX_COMMENTS)

    df = pd.DataFrame(comments, columns=["comment"])
    df["clean_comment"] = df["comment"].apply(clean_text)
    df["sentiment"] = df["clean_comment"].apply(get_sentiment)

    print("\nSentiment Percentage:")
    print(df["sentiment"].value_counts(normalize=True) * 100)

    # Visualization
    plt.figure(figsize=(6,4))
    sns.countplot(x="sentiment", data=df)
    plt.title("YouTube Comment Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Comments")
    plt.tight_layout()
    plt.savefig("output/sentiment_distribution.png")
    plt.show()

    # Negative insights
    print("\nTop Negative Keywords:")
    negative_words = (
        df[df["sentiment"] == "Negative"]["clean_comment"]
        .str.split(expand=True)
        .stack()
        .value_counts()
        .head(10)
    )
    print(negative_words)


if __name__ == "__main__":
    main()
