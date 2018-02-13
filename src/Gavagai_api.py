import requests
import pprint
import json


class GavagaiAPI:

    def __init__(self, headers, descriptions):

        self.headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "85830f60-3a2e-2885-4135-691cd8047662"
        }

        self.payload = self.build_payload(headers, descriptions)

    def base_url(self, functionality):
        return "https://api.gavagai.se/v3/"+functionality+"?apiKey=a0ab105640abd18d6c682bcac7233a78&language=EN"


    def get_topics(self):
        response = requests.post(self.base_url("topics"), data=json.dumps(self.payload), headers=self.headers)
        print(response.status_code, response.reason)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json.loads(response.text))
        return json.loads(response.text)

    def get_keywords(self):
        response = requests.post(self.base_url("keywords"), data=json.dumps(self.payload), headers=self.headers)
        #print(response.status_code, response.reason)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json.loads(response.text))

        return json.loads(response.text)

    def get_tonality(self):
        response = requests.post(self.base_url("tonality"), data=json.dumps(self.payload), headers=self.headers)
        # print(response.status_code, response.reason)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json.loads(response.text))

        return json.loads(response.text)

    def build_payload(self, head, desc):
        topics_dict = {}
        topics_dict['language'] = 'en'
        topics_dict['texts'] = []

        for idx, text in enumerate(desc):
            topics_dict_sample = {}
            topics_dict_sample['body'] = desc[idx]
            topics_dict_sample['title'] = head[idx]
            topics_dict_sample['id'] = str(idx)

            topics_dict['texts'].append(topics_dict_sample)

        return topics_dict