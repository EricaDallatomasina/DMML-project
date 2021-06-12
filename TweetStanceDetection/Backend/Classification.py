from datetime import datetime
import joblib as joblib
import pandas as pd
import matplotlib.pyplot as plt
from TrainingModel.Training import StemmedCountVectorizer
from nltk.corpus import stopwords


def classify(start_date, end_date, vaccine):
    # imposto valori di default se i parametri passati sono nulli
    if not start_date:
        start_date = "2021-03-01"

    if not end_date:
        now = datetime.now()
        end_date = now.strftime("%Y-%m-%d")

    if not vaccine:
        vaccine = "tutti"

    clf = joblib.load('Backend/classifier.pkl')
    dataset = __OpenDataset("Backend/FullDataset.csv")
    __doClassification(dataset, clf, vaccine, start_date, end_date)


def __OpenDataset(filename):
    test_set = pd.read_csv(filename, sep=',', usecols=['timestamp', 'username', 'tweet'])
    test_set.drop_duplicates(subset=['tweet'])
    test_set = test_set.dropna()

    news = []
    with open('Backend/AccountToDelete.txt') as f:
        for line in f:
            news.append(line.strip())

    index_names = test_set[test_set['username'].isin(news)].index
    test_set.drop(index_names, inplace=True)

    return test_set


def __doClassification(test_set: pd.DataFrame, clf, vaccine, start_date, end_date):
    data = __search_Vaccine_Period(test_set, vaccine, start_date, end_date).copy()

    # Adopting the text classifier on a limited set of data
    data["label"] = clf.predict(data.tweet)
    data = data.sort_values(by=['label'], ascending=False)
    data.to_csv("tweetFiltered_labeled.csv")
    print("File tweetFiltered_labeled (that contains the predicted class for each label) has been created \n")

    # Count label
    label = [0, 0, 0]
    indexNames = data[data['label'] == "label"].index
    data.drop(indexNames, inplace=True)
    data.label = data.label.astype(int)

    for w in data.label:
        if w == 0:
            label[0] = label[0] + 1
        if w == 1:
            label[1] = label[1] + 1
        if w == 2:
            label[2] = label[2] + 1

    print("Risultati della classicazione:")
    print("dataset len: " + str(len(data)))
    print("classe negativo len: " + str(label[0]))
    print("classe positivo: " + str(label[1]))
    print("classe neutro: " + str(label[2]))

    # Pie-chart
    classes = ["Negativo", "Positivo", "Neutro"]
    plt.figure(figsize=(7, 7))
    plt.title(f"Classificazione tweet dal {start_date} al {end_date}")
    plt.pie(label, labels=classes, radius=0.8, labeldistance=1.4, autopct=lambda p: '{:.1f}%'.format(p, (p / 100)))
    plt.show()


def __search_Vaccine_Period(df: pd.DataFrame, vaccine, start_date, end_date):
    __validate(start_date)
    __validate(end_date)

    if start_date < "2021-03-01":
        raise ValueError("Incorrect data from, should be > 2021-03-01")

    if vaccine == "tutti":
        return df[(df['timestamp'] > start_date) & (df['timestamp'] < end_date)]
    else:
        vaccine = vaccine.lower()
        return df[(df['timestamp'] > start_date) & (df['timestamp'] < end_date) & (df["tweet"].str.match(vaccine))]


def __validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
