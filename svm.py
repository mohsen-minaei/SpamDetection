import glob
from sklearn import svm
import time
from nltk.corpus import stopwords
import operator

labels_file = "../CSDMC2010_SPAM/SPAM.label"
labels = {}

train_path = "../CSDMC2010_SPAM/TRAINING_PREPROCESSING/"
test_path = "../CSDMC2010_SPAM/TESTING_PREPROCESSING/"

all_words_list = []
num_features = 300


# This function retrieves the labels from the file
def get_labels():
    for l in open(labels_file):
        st = l.strip().split(" ")
        labels[st[1]] = int(st[0])

# This function goes through all the keywords in the training files and creates a dictionary.
# Among all the extracted keywords we select the top most used
def create_dict_words():
    words_dict =  {}
    stop_words = set(stopwords.words('english'))
    for f in glob.glob(train_path + "*"):
        for l in open(f):
            for w in l.split():
                if w in stop_words:
                    continue
                if w in words_dict:  # count the freq of words in the dictionary
                    words_dict[w] += 1
                else:
                    words_dict[w] = 1
    # below takes the top most used keywords as the dictionary vector.
    for w, v in sorted(words_dict.items(), key=operator.itemgetter(1), reverse=True):
        all_words_list.append(w)
        if len(all_words_list) > num_features:
            return


# Given a filename this function extracts the features and returns the feature vector of the file.
def get_word_vector(fname):

    file_word_dict = {}
    for l in open(fname):
        for w in l.split():
            try:
                file_word_dict[w] += 1
            except:
                file_word_dict[w] = 1
    x = []
    for w in all_words_list:
        if w in file_word_dict:
            #x.append(file_word_dict[w])  # if the freq is important use this rather than the boolean vector
            x.append(1)
        else:
            x.append(0)
    return x


def train():
    X = []
    Y = []
    for f in glob.glob(train_path + "*"):
        fname = f.split("/")[-1]
        if fname not in labels:
            continue

        x = get_word_vector(f)
        X.append(x)
        Y.append(labels[fname])

    clf = svm.SVC()
    clf.fit(X, Y)

    return clf


def test(clf):
    predictions = {}
    X = []
    Y = []
    for f in glob.glob(test_path + "*"):
        fname = f.split("/")[-1]
        if fname not in labels:
            continue

        x = get_word_vector(f)
        X.append(x)
        y = clf.predict([x])
        predictions[fname] = y[0]
    return predictions


def evaluate(test_perdictions):
    eval = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for fname, prediction in test_perdictions.items():
        if prediction == 1 and labels[fname] == prediction:
            eval['TP'] += 1
        elif prediction == 1 and labels[fname] != prediction:
            eval['FP'] += 1
        elif prediction == 0 and labels[fname] == prediction:
            eval['TN'] += 1
        else:
            eval['FN'] += 1

    precision = float(eval['TP'])/(eval['TP'] + eval['FP'])
    recall = float(eval['TP'])/(eval['TP'] + eval['FN'])
    f1 = (2 * recall * precision)/(recall + precision)

    print eval
    print "precision: ", precision
    print "recall: ", recall
    print "F-score: ", f1


if __name__ == "__main__":
    get_labels()
    create_dict_words()
    clf = train()
    predictions = test(clf)
    evaluate(predictions)