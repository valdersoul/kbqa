from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

import csv

def read_wq_entitylinking(wq_tsvfile):
    """
    read the WebQuesiton entitylinking top 10 result tsv file and
    :param wq_tsvfile:
    :return:
    """
    with open(wq_tsvfile) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        q_id, entity_mention, e_id, e_name, score1 = [], [], [], [], []

        for line in tsvreader:
            q_id.append(line[0])  #question id
            entity_mention.append(line[1])
            e_id.append(line[4])
            score1.append(line[6])
            # reomve _ in the e_name(entity name)

            e_name.append(line[5].replace("_", " "))  # e_name is not as same as entity_mention

        return q_id, entity_mention, e_id, e_name,score1



def parse_noun(raw_question):
    """
    tag all the words in the raw text question and return all the noun word
    :param raw_question: raw taxt question
    :return: all noun words
    """
    taged_words = pos_tag(word_tokenize(raw_question), tagset='universal')  # tokenize and add tag
    print taged_words
    noun_entity = []
    for word, tag in taged_words:
        if tag == u'NOUN':
            noun_entity.append(word)

    print noun_entity
    return noun_entity




"""for test"""
tsvfile = "webquestions.examples.train.e2e.top10.filter.tsv"
q_id, entity_mention, e_id, e_name,score1 = read_wq_entitylinking(tsvfile)
print e_name
# # raw_question = "Which character did Emma Watson perform in 2015? "
# raw_question = "Who did Obama play with?"
# parse_noun(raw_question)
