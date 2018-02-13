import pprint

class Article:

    def __init__(self, desc = "", spaCy="", header = "", id = 1):
        self.header = header
        self.text = desc
        self.spaCy = spaCy
        self.entities = {}
        self.topics = []
        self.keywords = []
        self.id = id
        self.node_name = self.create_node_name() #header.lower().replace(" ", "").replace("-","").replace(",", "").replace(".","")
        self.similar_articles = []

    def look_for_entities(self):
        self.entities = self.spaCy.entity_dic(self.text, self.id)
        #pprint.pprint(self.entities)


    # the entry dictionary is the one obtained from gavagai api
    def set_topics(self, topic_array):
        self.topics = topic_array
        print(topic_array)

    def create_node_name(self):
        validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRST"
        newString = ""
        for char in self.header:
            if char in validLetters:
                newString += char
        return newString

    def setSpaCy(self, spaCy_instance):
        self.spaCy = spaCy_instance

    def set_entities(self, entity):
        self.entities = entity

    def set_similar_articles(self, candidates):
        self.similar_articles = candidates



