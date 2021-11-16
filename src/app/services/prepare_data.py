import json
import nltk
import numpy as np
import pandas as pd
import pymorphy2
import requests as req
import string
from collections import Counter as c
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation


class PrepareData:
    def __init__(self, good_revs, bad_revs):
        nltk.download('stopwords')

        self.good_rev = pd.read_csv(good_revs)
        self.bad_rev = pd.read_csv(bad_revs)

    def __call__(self, *args, **kwargs):
        data = self.prepare_data()

        params = self.load_params(data)

        api_result = self.call_api(params, data)

        return self.prepare_dataframe(api_result, data)

    def prepare_data(self):
        data = pd.concat([self.bad_rev, self.good_rev])

        try:
            data.drop(['Unnamed: 0'], axis='columns', inplace=True)
        except KeyError:
            pass

        data.set_axis(['review', 'rate'], axis='columns', inplace=True)
        data['review'] = self.data['review'].apply(lambda x: None if 'здравствуйте' in x.lower() else x)
        data.dropna(inplace=True)

        return data

    def load_params(self, data):
        return {
            'from_bot': '',
            'data': json.dumps(list(data['review'].values)),
            'lang': 'ru',
        }

    def call_api(self, params, data):
        res = req.post('http://canb2b.ru/clf', data=params)
        res = res.json()

        return res['good_cls']

    def prepare_dataframe(self, good_reviews, data):
        rates = []

        for review in good_reviews:
            try:
                rates.append(data[data['review'] == review]['rate'].values[0])
            except KeyError:
                rates.append(None)

        good_cls = pd.DataFrame({
            'review': good_reviews,
            'rate': rates,
        })

        good_cls.dropna(inplace=True)
        good_cls.reset_index(inplace=True, drop=True)
        good_cls = good_cls[['review', 'rate']]

        pos = '/'.join(list(good_cls[good_cls['rate'] > 3]['review'].values)).translate(str.maketrans(dict.fromkeys(string.punctuation)))
        neg = '/'.join(list(good_cls[good_cls['rate'] <= 3]['review'].values)).translate(str.maketrans(dict.fromkeys(string.punctuation)))

        pos = PrepareData.preprocess_text(pos)
        neg = PrepareData.preprocess_text(neg)

        pos_c, neg_c = dict(c(pos)), dict(c(neg))

        pos_adj, neg_adj = PrepareData.get_adj(pos_c), PrepareData.get_adj(neg_c)

        max_v_neg = sorted(neg_adj.values(), reverse=True)[1:4:2]
        max_v_pos = sorted(pos_adj.values(), reverse=True)[1:4:2]

        keywords_neg = list(filter(lambda x: neg_adj[x] in max_v_neg, neg_adj.keys()))[:4]
        keywords_pos = list(filter(lambda x: pos_adj[x] in max_v_pos, pos_adj.keys()))[:4]

        bad_report = PrepareData.output('neg', keywords_neg, good_cls)
        good_report = PrepareData.output('pos', keywords_pos, good_cls)

        return good_report, bad_report

    @staticmethod
    def output(output_type, keywords, good_cls):
        end_data = {}

        for keyword in keywords:
            rate = []
            examples = []

            for row in good_cls.values:
                if len(rate) >= 3:
                    break

                if output_type == 'neg':
                    if keyword in row[0] and row[1] <= 3:
                        rate.append(row[1])
                        examples.append(row[0])
                else:
                    if keyword in row[0] and row[1] >= 4:
                        rate.append(row[1])
                        examples.append(row[0])

            end_data[keyword] = {
                'examples': examples,
                'rates': rate,
                'mean_rate': np.array(rate).mean(),
            }

        return end_data

    @staticmethod
    def preprocess_text(text):
        mystem = Mystem()
        russian_stopwords = stopwords.words('russian')

        tokens = mystem.lemmatize(text.lower())

        return [token for token in tokens if token not in russian_stopwords and token != ' ' and token.strip() not in punctuation]

    @staticmethod
    def get_adj(position):
        morph = pymorphy2.MorphAnalyzer()
        adj = {}

        for name in position.keys():
            tag = str(morph.parse(name)[0].tag)[:4]

            if tag == 'ADJF':
                adj[name] = position[name]

        return adj
