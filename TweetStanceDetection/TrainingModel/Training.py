import joblib
import pandas as pd
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords


# import nltk #da usare solo prima volta
# nltk.download('stopwords') #da usare solo prima volta

"""
Module for training the classifier 
The classifier is stored in Backend/classifier.pkl """


def train():
    training_set = pd.read_csv("TrainingModel/training_set.csv", sep=',', names=['tweet', 'label'])
    data = pd.read_csv("TrainingModel/training_set_febbraio.csv", sep=',', usecols=['timestamp', 'username', 'tweet', 'label'])
    data = data.dropna()
    data = data.iloc[1:, :]
    training_set = training_set.iloc[1:, :]

    new_training_set = pd.concat([training_set, data])

    print(f"Number of tweets: {len(new_training_set)}")

    # Define the classifier
    clf = Pipeline([
        ('vect', StemmedCountVectorizer(min_df=3, analyzer="word", stop_words=set(stopwords.words('italian')), ngram_range=(1, 1))),
        ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
        ('clf', BernoulliNB()),
    ])

    clf.fit(new_training_set.tweet, new_training_set.label.astype(int))
    joblib.dump(clf, 'Backend/classifier.pkl')
    print("Classifier trained")


class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        italian_stemmer = SnowballStemmer('italian')
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([italian_stemmer.stem(w) for w in analyzer(doc)])


def main():
    train()


if __name__ == "__main__":
    main()
