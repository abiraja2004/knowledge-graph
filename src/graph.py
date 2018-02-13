import pandas as pd
import numpy as np

from py2neo import authenticate, Graph, Node, Relationship, NodeSelector

import subprocess
import webbrowser
import sys
import itertools


class GraphObject:

    def __init__(self):

        self.nodes = []
        self.user = 'neo4j'
        self.password = "f1234567"
        # pass es f*
        #self.user = 'admin2'
        #self.password = '123456'

        self.idx_to_node = pd.Series()
        self.name_to_idx = {}
        self.launchneo4j(popup=False)
        self.graph.delete_all()

    # Create or return existing :)
    # properties should be a json dictionary
    # name a string
    #potser cal canviar a string el json
    def match_relationship(self, n1, n2, relationship):

        query ='''
           MERGE ('''+n1['node_name']+''':'''+n1['type']+''' {name: "'''+n1['properties']['name']+''','''+n1['properties']['title']+'''"})
           MERGE ('''+n2['node_name']+''':'''+n2['type']+''' {name: "'''+n2['properties']['name']+'''"})
           CREATE UNIQUE ('''+n1['node_name']+''')-[:'''+relationship+''']->('''+n2['node_name']+''')
        '''

        my_node = self.graph.evaluate(query)

        """
        my_node = self.graph.evaluate('''
           MERGE (tom:Person {name: "Tom"})
           MERGE (jerry:Person {name: "Jerry"})
           CREATE UNIQUE (tom)-[:KNOWS]->(jerry)
        ''')
        """

    def match_document_relationship(self, n1, n2, relationship):
        query ='''
           MATCH ('''+n1['node_name']+''':'''+n1['type']+''' {name: "'''+n1['properties']['name']+''','''+n1['properties']['title']+'''"})
           MATCH ('''+n2['node_name']+''':'''+n2['type']+''' {name: "'''+n2['properties']['name']+''','''+n2['properties']['title']+'''"})
           CREATE UNIQUE ('''+n1['node_name']+''')-[:'''+relationship+''']->('''+n2['node_name']+''')
        '''

        my_node = self.graph.evaluate(query)

    def add_topics_to_articles(self, articles):
        for article in articles:
            #print(article.node_name, "\n")
            n1 = {'properties': {"name": "DOCUMENT "+str(article.id), "title":self.clean_name(article.header)}, 'type': 'DOCUMENT', 'node_name': article.node_name}
            for topic in article.topics:
                topic_clean_name = self.clean_name(topic)
                n2 = {'properties': {"name": topic}, 'type': 'TOPIC', 'node_name': topic_clean_name}
                self.match_relationship(n1, n2, "CONTAINS_TOPIC")

    def add_entities_to_articles(self, articles):
        print("Adding entities to articles...")

        for idx, article in enumerate(articles):
            print(idx,"/",len(articles))

            #selectedones = [50, 130, 153, 190, 43, 89, 91, 70, 77, 38, 40, 50, 14]
            #if idx in selectedones:

            # print(article.node_name, "\n")
            n1 = {'properties': {"name": "DOCUMENT " + str(article.id), "title":self.clean_name(article.header)}, 'type': 'DOCUMENT',
                  'node_name': article.node_name}
            for entity in article.entities:
                entity_clean_name = self.clean_name(entity)

                for type in article.entities[entity]:
                    #print("type",type)
                    #print("name",entity_clean_name)
                    n2 = {'properties': {"name": str(entity)}, 'type': type, 'node_name': entity_clean_name}
                    self.match_relationship(n1, n2, "CONTAINS_ENTITY")

    def add_similarities_to_articles(self, articles):
        print("Adding similarities to articles...")

        for idx, article in enumerate(articles):
            print(idx,"/",len(articles))

            #selectedones = [50, 130, 153, 190, 43, 89, 91, 70, 77, 38, 40, 50, 14]
            #if idx in selectedones:

            # print(article.node_name, "\n")
            n1 = {'properties': {"name": "DOCUMENT " + str(article.id), "title":self.clean_name(article.header)}, 'type': 'DOCUMENT',
                  'node_name': article.node_name}
            for similar_article in article.similar_articles:
                n2 = {'properties': {"name": "DOCUMENT " + str(articles[similar_article].id), "title": self.clean_name(articles[similar_article].header)},
                      'type': 'DOCUMENT',
                      'node_name': articles[similar_article].node_name}

                self.match_document_relationship(n1, n2, "SIMILAR_TO")



    def add_entities_to_articles_safecopy(self, articles):
        for idx, article in enumerate(articles):

            selectedones = [50, 130, 153, 190, 43, 89, 91, 70, 77, 38, 40, 50, 14]
            if idx in selectedones:

                # print(article.node_name, "\n")
                n1 = {'properties': {"name": "DOCUMENT " + str(article.id)}, 'type': 'DOCUMENT',
                      'node_name': article.node_name}
                for entity in article.entities:
                    entity_clean_name = self.clean_name(entity)
                    n2 = {'properties': {"name": entity}, 'type': 'ENTITY', 'node_name': entity_clean_name}
                    self.match_relationship(n1, n2, "CONTAINS_ENTITY")

    # Adds the node specified in the input dictionary, can be more than one.
    def add_node(self, dict_nodes):
        # key = type, value = name
        nodes_to_append = []
        nodes_num = 0
        for key, value in dict_nodes.items():
            for index in range(0,len(value)):
                node_name = dict_nodes[key][index]
                n = Node(key, name=node_name)
                self.graph.create(n)
                #if n not in nodes_to_append:
                self.name_to_idx[node_name] = index
                nodes_to_append.append(n)

        series_to_append = pd.Series(nodes_to_append,
                              index=np.arange(len(nodes_to_append)))

        self.idx_to_node = pd.concat([self.idx_to_node, series_to_append], axis= 0)

    # Adds the node specified in the input dictionary, can be more than one.
    def add_node(self, dict_nodes, article_num):
        # key = type, value = name
        nodes_to_append = []
        nodes_num = 0
        for key, value in dict_nodes.items():
            for index in range(0,len(value)):
                node_name = dict_nodes[key][index]
                n = Node(key, name=node_name, article=article_num)
                self.graph.create(n)
                #if n not in nodes_to_append:
                self.name_to_idx[node_name] = index
                nodes_to_append.append(n)

        series_to_append = pd.Series(nodes_to_append,
                              index=np.arange(len(nodes_to_append)))

        self.idx_to_node = pd.concat([self.idx_to_node, series_to_append], axis= 0)

    def merge_duplicates(self):
        cypher = self.graph.cypher



    # Adds the relationship specified in the input dictionary, can be more than one.
    #TODO I need to initialize an id for each node so that i can refer to it when creating the relationship
    #TODO HALF DONE, just refer to the index
    def add_relationship(self, dict_relationships):
        # key = type, "src" = initial , "dst" = destination
        #for key, value in dict_relationships.items():
        #self.graph.create(Relationship(,"KNOWS", ))
        return "a"

    def add_constant_relationship_test2(self, dict_entities, article_num):
        # key = type, "src" = initial , "dst" = destination
        selector = NodeSelector(self.graph)
        selected = selector.select(article=article_num)

        for i, n1 in enumerate(list(selected)):
            print("Building links... node ", i,"/",len(list(selected)))
            for n2 in list(selected):
                if n1 != n2:
                    self.graph.create(Relationship(n1, "SEMANTIC",n2))

    def add_constant_relationship(self, dict_entities, article_num):
        # key = type, "src" = initial , "dst" = destination
        selector = NodeSelector(self.graph)
        selected = selector.select(article=article_num)

        document = Node("DOCUMENT", name=str(article_num), article=article_num)
        self.graph.create(document)

        for i, n1 in enumerate(list(selected)):
            print("Building links... node ", i,"/",len(list(selected)))
            self.graph.create(Relationship(n1, "MENTIONED IN",document))



    def add_constant_relationship_test1(self, dict_entities):
        # key = type, "src" = initial , "dst" = destination
        entities = []
        for key, value in dict_entities.items():
            #print(key, value)
            entities = entities + dict_entities[key]
        relationships = itertools.combinations(entities, 2)
        for link in relationships:
            #self.print_full_series(self.idx_to_node)
            a = self.name_to_idx[link[0]]
            self.graph.create(Relationship(self.idx_to_node[self.name_to_idx[link[0]]], "SEMANTIC",self.idx_to_node[self.name_to_idx[link[1]]]))

            #print("idx to node",self.idx_to_node)
            #print("a")

    def launchneo4j(self, popup = True):
        # connect to authenticated graph database
        authenticate("localhost:7474", self.user, self.password)
        self.graph = Graph("http://localhost:7474/db/data/")
        if popup:
            url = "http://localhost:7474/browser/"
            if sys.platform == 'darwin':  # in case of OS X
                subprocess.Popen(['open', url])
            else:
                webbrowser.open_new_tab(url)

    def print_full_series(self, x):
        pd.set_option('display.max_rows', len(x))
        print("\n\n",x)
        pd.reset_option('display.max_rows')



    def clean_name(self, name):
        validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRST"
        newString = ""
        for char in name:
            if char in validLetters:
                newString += char
        if newString == "":
            newString = "Enigma"
        return newString


"""
graph = GraphObject()
dict_nodes = {"Person": {"name":"Nicole"}}
graph.add_Node(dict_nodes)
"""
"""
nicole = Node("Person", name="Nicole")
# self.nicole = print(nicole.__uuid__)
self.graph.create(nicole)
adam = Node("Person", name="Adam")
self.graph.create(adam)
self.graph.create(Relationship(nicole, "KNOWS", adam))
self.graph.create(Relationship(adam, "LOVES", nicole))

"""

