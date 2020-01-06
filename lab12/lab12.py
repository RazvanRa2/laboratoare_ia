#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import log
import re
from random import shuffle
import zipfile

zipFile = zipfile.ZipFile("review_polarity.zip")
pos_files = [f for f in zipFile.namelist() if 'pos/cv' in f]
neg_files = [f for f in zipFile.namelist() if 'neg/cv' in f]

pos_files.sort()
neg_files.sort()

print("Recenzii pozitive: " + str(len(pos_files)) +
      "; Recenzii negative: " + str(len(neg_files)))

# Raspunsul asteptat: "Recenzii pozitive: 1000; Recenzii negative: 1000"
assert(len(pos_files) == 1000 and len(neg_files) == 1000)

tr_pos_no = int(.8 * len(pos_files))
tr_neg_no = int(.8 * len(neg_files))

# shuffle(pos_files)
# shuffle(neg_files)

pos_train = pos_files[:tr_pos_no]  # Recenzii pozitive pentru antrenare
pos_test = pos_files[tr_pos_no:]  # Recenzii pozitive pentru testare
neg_train = neg_files[:tr_neg_no]  # Recenzii negative pentru antrenare
neg_test = neg_files[tr_neg_no:] # Recenzii negative pentru testare

STOP_WORDS = []
STOP_WORDS = [line.strip() for line in open("Lab12-stop_words")]


def parse_document(path):
    for word in re.findall(r"[-\w']+", zipFile.read(path).decode("utf-8")):
        if len(word) > 1 and word not in STOP_WORDS:
            yield word


def count_words():
    vocabulary = {}
    pos_words_no = 0
    neg_words_no = 0

    # ------------------------------------------------------
    # <TODO 1> numrati aparitiile in documente pozitive si
    # in documente negative ale fiecarui cuvant, precum si numarul total
    # de cuvinte din fiecare tip de recenzie
    for f in pos_train:
        words = parse_document(f)
        for word in words:
            if word in vocabulary:
                (pos, neg) = vocabulary[word]
                vocabulary[word] = (pos + 1, neg)
            else:
                vocabulary[word] = (1, 0)
            pos_words_no += 1
    
    for f in neg_train:
        words = parse_document(f)
        for word in words:
            if word in vocabulary:
                (pos, neg) = vocabulary[word]
                vocabulary[word] = (pos, neg + 1)
            else:
                vocabulary[word] = (0, 1)
            neg_words_no += 1

    # ------------------------------------------------------

    return (vocabulary, pos_words_no, neg_words_no)


# -- VERIFICARE --
training_result_words = count_words()

(voc, p_no, n_no) = training_result_words
print("Vocabularul are ", len(voc), " cuvinte.")
print(p_no, " cuvinte in recenziile pozitive si ",
      n_no, " cuvinte in recenziile negative")
print("Cuvantul 'beautiful' are ", voc.get("beautiful", (0, 0)), " aparitii.")
print("Cuvantul 'awful' are ", voc.get("awful", (0, 0)), " aparitii.")

# Daca se comentează liniile care reordonează aleator listele cu exemplele pozitive și negative,
# rezultatul așteptat este:
#
# Vocabularul are  44895  cuvinte.
# 526267  cuvinte in recenziile pozitive si  469812  cuvinte in recenziile negative
# Cuvantul 'beautiful' are  (165, 75)  aparitii.
# Cuvantul 'awful' are  (16, 89)  aparitii.


def predict(params, path, alpha=1):
    (vocabulary, pos_words_no, neg_words_no) = params
    log_pos = log(0.5)
    log_neg = log(0.5)

    # ----------------------------------------------------------------------
    # <TODO 2> Calculul logaritmilor probabilităților
    words = parse_document(path)

    for word in words:
        pos_val = vocabulary[word][0] if word in vocabulary else 0.0
        neg_val = vocabulary[word][1] if word in vocabulary else 0.0

        pos_probab = (float)((pos_val + alpha)) / (pos_words_no + len(vocabulary.keys()) * alpha)
        neg_probab = (float)((neg_val + alpha)) / (neg_words_no + len(vocabulary.keys()) * alpha)

        log_pos += log(pos_probab)
        log_neg += log(neg_probab)
    # ----------------------------------------------------------------------

    if log_pos > log_neg:
        return "pos", log_pos
    else:
        return "neg", log_neg


# -- VERIFICARE --
print(zipFile.read(pos_test[14]).decode("utf-8"))
print(predict(training_result_words, pos_test[14]))

# Daca se comentează liniile care reordonează aleator listele cu exemplele pozitive și negative,
# rezultatul așteptat este:
#
# ('pos', -1790.27088356391) pentru un film cu Hugh Grant și Julia Roberts (o mizerie siropoasă)
#
# Recenzia este clasificată corect ca fiind pozitivă.


def evaluate(params, prediction_func):
    conf_matrix = {}
    conf_matrix["pos"] = {"pos": 0, "neg": 0}
    conf_matrix["neg"] = {"pos": 0, "neg": 0}
    accuracy = 0

    # ----------------------------------------------------------------------
    # <TODO 3> : Calcularea acurateței și a matricei de confuzie
    for f in pos_test:
        predict_type, _ = prediction_func(params, f)
        if predict_type == "pos":
            conf_matrix["pos"]["pos"] += 1
        else:
            conf_matrix["pos"]["neg"] += 1

    for f in neg_test:
        predict_type, _ = prediction_func(params, f)
        if predict_type == "neg":
            conf_matrix["neg"]["neg"] += 1
        else:
            conf_matrix["neg"]["pos"] += 1

    accuracy = (conf_matrix["pos"]["pos"] + conf_matrix["neg"]["neg"]) / \
        (conf_matrix["pos"]["pos"] + conf_matrix["neg"]
         ["neg"] + conf_matrix["pos"]["neg"] + conf_matrix["neg"]["pos"])
    #------------------------------------------------------------

    return accuracy, conf_matrix
# -----------------------------------------------------------


def print_confusion_matrix(cm):
    print("    | ", "{0:^10}".format("pos"), " | ", "{0:^10}".format("neg"))
    print("{0:-^3}".format(""), "+", "{0:-^12}".format(""),
          "+", "{0:-^12}".format("-", fill="-"))
    print("pos | ", "{0:^10}".format(
        cm["pos"]["pos"]), " | ", "{0:^10}".format(cm["pos"]["neg"]))
    print("neg | ", "{0:^10}".format(
        cm["neg"]["pos"]), " | ", "{0:^10}".format(cm["neg"]["neg"]))


# -- VERIFICARE --
(acc_words, cm_words) = evaluate(training_result_words, predict)
print("Acuratetea pe setul de date de test: ",
      acc_words * 100, "%. Matricea de confuzie:")
print_confusion_matrix(cm_words)

# Daca se comentează liniile care reordonează aleator listele cu exemplele pozitive și negative,
# rezultatul așteptat este:
#
# Acuratetea pe setul de date de test:  80.5 %. Matricea de confuzie:
#     |     pos      |     neg
# --- + ------------ + ------------
# pos |     155      |      45
# neg |      33      |     167


def count_bigrams():
    bigrams = {}
    pos_bigrams_no = 0
    neg_bigrams_no = 0

    # ----------------------------------------------------------------------
    # <TODO 4>: Numarati bigramele
    for f in pos_train:
        words = parse_document(f)
        for i in range(len(words) - 1):
            bigram = words[i] + ":" + words[i + 1]
            if bigram in bigrams:
                (pos, neg) = bigrams[bigram]
                bigrams[bigram] = (pos + 1, neg)
            else:
                bigrams[bigram] = (1, 0)
            pos_bigrams_no += 1

    for f in neg_train:
        words = parse_document(f)
        for i in range(len(words) - 1):
            bigram = words[i] + ":" + words[i + 1]
            if bigram in bigrams:
                (pos, neg) = bigrams[bigram]
                bigrams[bigram] = (pos, neg + 1)
            else:
                bigrams[bigram] = (0, 1)
            neg_bigrams_no += 1
    #-----------------------------------------------

    return bigrams, pos_bigrams_no, neg_bigrams_no


# -- VERIFICARE --
training_result_bigrams = count_bigrams()

(big, pos_b, neg_b) = training_result_bigrams
print("Tabelul are ", len(big), " bigrame.")
print(pos_b, " bigrame in recenziile pozitive si ",
      neg_b, " bigrame in recenziile negative")
print("Bigrama 'beautiful actress' are ", big.get(
    "beautiful:actress", (0, 0)), " aparitii.")
print("Bigrama 'awful movie' are ", big.get(
    "awful:movie", (0, 0)), " aparitii.")

# Daca se comentează liniile care reordonează aleator listele cu exemplele pozitive și negative,
# rezultatul așteptat este:
#
# Tabelul are  428997  bigrame.
# 525467  bigrame in recenziile pozitive si  469012  bigrame in recenziile negative
# Bigrama 'beautiful actress' are  (2, 0)  aparitii.
# Bigrama 'awful movie' are  (1, 4)  aparitii.


def predict2(params, path, alpha=1):
    (bigrams, pos_bigrams_no, neg_bigrams_no) = params
    log_pos = log(0.5)
    log_neg = log(0.5)

    # ----------------------------------------------------------------------
    # <TODO 5> Calculul logaritmilor probabilităților folosind bigramele

    words = parse_document(path)
    vocabulary = bigrams
    pos_words_no = pos_bigrams_no
    neg_words_no = neg_bigrams_no
    
    for i in range(len(words) - 1):
        bigram = words[i] + ":" + words[i + 1]
        word = bigram

        pos_val = vocabulary[word][0] if word in vocabulary else 0.0
        neg_val = vocabulary[word][1] if word in vocabulary else 0.0

        pos_probab = (float)((pos_val + alpha)) / (pos_words_no + len(vocabulary.keys()) * alpha)
        neg_probab = (float)((neg_val + alpha)) / (neg_words_no + len(vocabulary.keys()) * alpha)

        log_pos += log(pos_probab)
        log_neg += log(neg_probab)


    # ----------------------------------------------------------------------

    if log_pos > log_neg:
        return "pos", log_pos
    else:
        return "neg", log_neg


# -- VERIFICARE --
print(zipFile.read(pos_test[14]).decode("utf-8"))
predict2(training_result_bigrams, pos_test[14])

# Daca se comentează liniile care reordonează aleator listele cu exemplele pozitive și negative,
# rezultatul așteptat este:
#
# ('pos', -3034.428732037113) pentru același film cu Hugh Grant

# -- VERIFICARE --
(acc_bigrams, cm_bigrams) = evaluate(training_result_bigrams, predict2)
print("Acuratetea pe setul de date de test, cu bigrame: ",
      acc_bigrams * 100, "%. Matricea de confuzie:")
print_confusion_matrix(cm_bigrams)

# Daca se comentează liniile care reordonează aleator listele cu exemplele pozitive și negative,
# rezultatul așteptat este:
#
# Acuratetea pe setul de date de test:  84.5 %. Matricea de confuzie:
#     |     pos      |     neg
# --- + ------------ + ------------
# pos |     161      |      39
# neg |      23      |     177

print("Acuratetea pe setul de date de test, cu cuvinte simple: ",
      acc_words * 100, "%. Matricea de confuzie:")
print_confusion_matrix(cm_words)

print("\n\nAcuratetea pe setul de date de test, cu bigrame: ",
      acc_bigrams * 100, "%. Matricea de confuzie:")
print_confusion_matrix(cm_bigrams)
