import json



import numpy as np
import pandas as pd

import spaCy
import Article
import FrequencySummarizer
import SimilarDocuments
import graph

class Main:

    def __init__(self):
        self.articles = []
        head, desc = self.opendataset()

        ## new
        amount = 50
        head_long = head[:amount]
        desc_long = desc[:amount]

        head = head[:amount]
        desc = desc[:amount]


        # # # Extractive Summarization
        fs = FrequencySummarizer.FrequenySummarizer()
        for i in range(0, amount):
            summary, total_sentences = fs.summarize( desc[i], 3)
            desc[i] = ' '.join(summary)
        # # #

        for index in range(0, len(desc)):
            article = Article.Article(desc=desc[index], header=head[index], id=index)
            self.articles.append(article)

        my_graph = graph.GraphObject()
        # # # # # # Layer 1
        # # # Topics
        """# Query Gavagai
        gavagai_api = Gavagai_api.GavagaiAPI(head, desc)
        response = gavagai_api.get_topics()
        self.dump_json('./data/response.json', response)
        """

        #activate to test it is GAVAGAI
        """
        response = self.load_stored_json('./data/response.json')
        self.add_topics_to_articles(response)

        my_graph.add_topics_to_articles(self.articles)

        """

        # # # Entities
        self.add_entities_to_articles(self.articles)
        my_graph.add_entities_to_articles(self.articles)


        # # # Similar Documents
        simdoc = SimilarDocuments.SimilarDocuments(desc_long, 2, 200)
        Signature_Matrix = simdoc.build_Signature_Matrix()
        S = simdoc.signature_Similarities(Signature_Matrix)
        print(S)

        for i in range(0, amount):
            pos_most_similar_article = np.argmax(S[i, :])
            # TOP 2
            top10_similar_articles = S[i, :].argsort()[-5:][::-1]

            for idx, document in enumerate(top10_similar_articles):
                if S[i, document] == 0.0:
                    np.delete(top10_similar_articles, idx)


            self.articles[i].set_similar_articles(top10_similar_articles)
        my_graph.add_similarities_to_articles(self.articles)

        """
        for idx, article in enumerate(self.articles):
            # To narrow and analyse only the ones that have topics
            selectedones = [50, 130, 153, 190, 43, 89, 91, 70, 77, 38, 40, 50, 14]
            if idx in selectedones:
                my_graph.add_node(article.entities, idx)
                my_graph.add_constant_relationship(article.entities, idx)
                print("idx:", idx, "\n",article.entities)
        """


        # # # # # #
        """ Old
        my_graph = graph.GraphObject()

        self.layer1(desc[0:3])
        for idx, article in enumerate(self.articles):
            print(desc[idx])
            my_graph.add_node(article.entities, idx)
            my_graph.add_constant_relationship(article.entities, idx)
            print("idx:", idx, "\n",article.entities)

        #self.layerTest(desc)
        """

    # This should be the layer of identifying the entities and adding them to the graph
    def layer1(self, articles):
        spacy_instance = spaCy.SpaCy()

        for index in range(0, len(articles)):
            article = Article.Article(articles[index], spacy_instance)
            article.look_for_entities()
            self.articles.append(article)


    def layerTest(self, articles):
        spacy_instance = spaCy.SpaCy()
        article = Article.Article(articles[0], spacy_instance)
        print(article.text)
        spacy_instance.part_of_speech_tagging(article.text)





    def opendataset(self):
        with open('./data/articles.csv') as myCSV:
            # idx, title, publication, author, date, year, month, url, content
            data = pd.read_csv(myCSV)

        head = data['title']
        desc = data['content']

        return head, desc

    def add_topics_to_articles(self, response_dict):
        print("articles_length", len(self.articles))
        for index, text in enumerate(response_dict['topics']):
            # delete for final version
            if index < len(self.articles):
                for doc_index in range(0,len(text['texts'])):
                    index = int(text['texts'][doc_index]['id'])
                    self.articles[index].set_topics(text['keywords'])

    def add_entities_to_articles(self, articles):
        spacy_instance = spaCy.SpaCy()

        print("Extracting Entities...\n")
        for count, article in enumerate(self.articles):
            print("Entity ", count, "of ", len(self.articles))
            article.setSpaCy(spacy_instance)
            article.look_for_entities()



    def load_stored_json(self, address):
        return json.load(open(address))


    def dump_json(self, address, data):
        with open(address, 'w') as fp:
            json.dump(data, fp)


Main()



"""
for entity in a:
    print(entity.text, entity.label_)
"""
