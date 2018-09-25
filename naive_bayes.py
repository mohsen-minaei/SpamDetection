import glob
import math


labels_file = "../CSDMC2010_SPAM/SPAM.label"
labels = {}

train_path = "../CSDMC2010_SPAM/TRAINING_PREPROCESSING/"
test_path = "../CSDMC2010_SPAM/TESTING_PREPROCESSING/"


prior_count = {0: 0, 1: 0} # counting how many files are labeled 0 and 1, AKA the prior of the class
word_count = {0: {}, 1: {}}  # count of each word based on their labeled field
total_words = {}  # total number of words in each class
classes = {0, 1}


# This function retrieves the labels from the file
def get_labels():
    for l in open(labels_file):
        st = l.strip().split(" ")
        labels[st[1]] = int(st[0])


# This function starts counting the words within the files AKA training the model
def train():
    # go through each file and count the number of words
    for f in glob.glob(train_path + "*"):
        f_name = f.strip().split("/")[-1] # file name
        try:
            f_label = labels[f_name]  # get the label of the file
            prior_count[f_label] += 1
        except:
            continue

        for l in open(f):  # split each line of the line and getting the words out
            l = l.split()
            for w in l:
                try:
                    word_count[f_label][w] += 1
                except:
                    word_count[f_label][w] = 1

    total_words[0] = sum(word_count[0].values())
    total_words[1] = sum(word_count[1].values())


def test():
    prediction_classes = {}
    total_words_unique = len(set().union(*[word_count[0], word_count[1]]))  # total number of unique words in each class AKA dictionary size

    for f in glob.glob(test_path + "*"):
        f_name = f.strip().split("/")[-1]
        prob_class = {0: math.log(float(prior_count[0])/(prior_count[0] + prior_count[1])), 1: math.log(float(prior_count[1])/(prior_count[0] + prior_count[1]))}  # prob of each class
        for c in classes:   # we run the below code for each class
            for l in open(f):  # split each line of the file and getting the words out
                l = l.split()
                for w in l:
                    try:
                        prob_class[c] += math.log(float((word_count[c][w] + 1)) / (total_words[c] + total_words_unique))
                    except:
                        prob_class[c] += math.log(float((0 + 1)) / (total_words[c] + total_words_unique))


        if prob_class[0] > prob_class[1]:
            prediction_classes[f_name] = 0
        else:
            prediction_classes[f_name] = 1

    return prediction_classes


def evaluate(test_perdictions):
    eval = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for fname, prediction in test_perdictions.items():
        if prediction == 0 and labels[fname] == prediction:
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


if __name__ == '__main__':
    get_labels()
    train()
    perdictions = test()
    evaluate(perdictions)