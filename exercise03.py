import nltk
import matplotlib.pyplot as plt
from nltk.corpus import gutenberg, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# Download necessary resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Read Moby Dick from Gutenberg dataset
moby_dick = gutenberg.raw('melville-moby_dick.txt')

# Tokenization
tokens = word_tokenize(moby_dick)

# Stopwords filtering
stop_words = set(stopwords.words('english'))
filtered_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

# Parts-of-Speech (POS) tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# POS frequency
pos_counts = FreqDist(tag for word, tag in pos_tags)
top_pos = pos_counts.most_common(5)

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word, pos=pos) for word, pos in pos_tags][:20]

# Plotting frequency distribution
plt.figure(figsize=(10, 6))
pos_counts.plot(30, title='POS Frequency Distribution')
plt.show()

# Sentiment Analysis
sentences = sent_tokenize(moby_dick)
sentiment_scores = [TextBlob(sentence).sentiment.polarity for sentence in sentences]
average_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)

# Determine overall text sentiment
if average_sentiment_score > 0.05:
    overall_sentiment = "positive"
else:
    overall_sentiment = "negative"

# Print the results
print("Top 5 most common parts of speech and their frequencies:")
for pos, count in top_pos:
    print(f"{pos}: {count}")

print("\nTop 20 lemmatized tokens:")
print(lemmatized_tokens)

print("\nAverage Sentiment Score:", average_sentiment_score)
print("Overall Text Sentiment:", overall_sentiment)