import random
import json
import sys
import nltk
import re

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from googletrans import Translator
from nltk.stem import WordNetLemmatizer 

nltk.download('popular')

class ProxyLoader():

    def __init__(self):
        print("[ProxyLoader] Setup ProxyLoader")
        self.proxies = []
        self.proxy_index = -1

        user_agent = UserAgent()
        # Retrieve latest proxies
        proxies_req = Request('https://www.sslproxies.org/')
        proxies_req.add_header('User-Agent', user_agent.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')
        # Save proxies in the array
        for row in proxies_table.tbody.find_all('tr'):
            self.proxies.append({
              'ip':   row.find_all('td')[0].string,
              'port': row.find_all('td')[1].string
            })

    def _get_random_index(self):
        return random.randint(0, len(self.proxies) - 1)

    def refresh_proxy(self):
        if self.proxy_index != -1:
            del self.proxies[self.proxy_index]
        self.proxy_index = self._get_random_index()
        print("[ProxyLoader] Using Proxy {ip}:{port}"
              .format(ip=self.proxies[self.proxy_index]['ip'], port=self.proxies[self.proxy_index]['port']))
        return self.proxies[self.proxy_index]
"""
This preprocessor can only use json data like following example:
{<test_index>:{<field_1>:<value_1>, ...}}
"""

class JsonPreprocessor():

    def __init__(self):
        pass

    def preprocessing(self, json_data):
        processing_counter = 0
        total_test_case = len(json_data.items())
        for test_index, attributes in json_data.items():
            processing_counter += 1
            sys.stdout.write("\r[{}] {}/{}".format(self.__class__.__name__, processing_counter, total_test_case))
            sys.stdout.flush()
            for field, filed_value in attributes.items():
                json_data[test_index][field] = self._transform_function(filed_value)
            sys.stdout.write('\n')

    def _transform_function(self, data_value):
        """
        TO DO:
            what transform you want to do for every field_value and replace the original data
        """
        pass


class JsonPreprocessorLanguageTranslator(JsonPreprocessor):

    def __init__(self, src_language='zh-CN', dest_language='en'):
        super(JsonPreprocessorLanguageTranslator, self).__init__()
        self.src_language = src_language
        self.dest_language = dest_language
        self.proxy_loader = ProxyLoader()
        proxy = self.proxy_loader.refresh_proxy()
        self.translator = Translator(proxies={'https':'{ip}:{port}'
                                              .format(ip=proxy['ip'], port=proxy['port'])}, timeout=None)

    def _transform_function(self, data_value):
        try:
            transformed_data = self.translator.translate(data_value, src=self.src_language, dest=self.dest_language).text
        except TypeError:
            transformed_data = ''
        except json.decoder.JSONDecodeError:
            proxy = self.proxy_loader.refresh_proxy()
            self.translator=Translator(proxies={'https':'{ip}:{port}'
                                              .format(ip=proxy['ip'], port=proxy['port'])}, timeout=None)
            transformed_data = self.translator.translate(data_value, src=self.src_language, dest=self.dest_language).text
        return transformed_data

class JsonPreprocessorLemmatizer(JsonPreprocessor):

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer() 

    def _transform_function(self, data_value):
        lemmatized_words = []
        for words in data_value.split(' '):
            lemmatized_words.append(self.lemmatizer.lemmatize(words))
        return ' '.join(lemmatized_words)

class JsonPreprocessorRawTextParser(JsonPreprocessor):

    def __init__(self):
        pass

    def _transform_function(self, data_value):
        # Split line and remove the step number if exist
        data_value_list = data_value.split('\n')
        for j, line in enumerate(data_value_list):
            line = line.lower()
            unwant_list = re.findall(r'[[\w\d]+\-]*[\w\d]*', line)
            for word in unwant_list:
                line = line.replace(word, '')
            parse_result = ' '.join(re.findall(r"[a-z ]*",line))
            while '  ' in parse_result:
                parse_result = parse_result.replace('  ',' ')
            for i, word in enumerate(parse_result):
                if word != ' ':
                    parse_result = parse_result[i:]
                    break
            data_value_list[j] = parse_result
        return ' '.join(data_value_list)
"""
To Do :
    disambiguation_dict preprocessor
"""

