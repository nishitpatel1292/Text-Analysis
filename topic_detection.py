import gensim
from gensim.utils import simple_preprocess
from gensim.models import LdaModel
from nltk.corpus import stopwords

class TopicDetection:

    def preprocess(self, text):
        stop_words = set(stopwords.words('english'))
        return [word for word in simple_preprocess(text, deacc=True) if word not in stop_words]
    
    def preprocess_file(self, file_path, chunk_size = 10000):
        preprocessed_text = []
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break 
                preprocessed_chunk = self.preprocess(chunk)
                preprocessed_text.append(preprocessed_chunk)
        return preprocessed_text
    
    def train_lda_model (self, corpus, dictionary):
        return LdaModel(corpus, num_topics=4, id2word=dictionary)
    
    def extract_topics(self, lda_model):
        topics=[]

        for topic in lda_model.print_topics():
            topics.append(topic[1])
        return topics
        
    
    # Topic detection function
    def detect_topics(self, file_path, chunk_size=10000):
        preprocessed_text = self.preprocess_file(file_path, chunk_size)

        # Create dictionary and corpus
        dictionary = gensim.corpora.Dictionary(preprocessed_text)
        corpus = [dictionary.doc2bow(text) for text in preprocessed_text]

        lda_model = self.train_lda_model(corpus, dictionary)

        topics = self.extract_topics(lda_model)        
        top_keywords_per_topic=[]
        for topic in topics:
            keywords = [word.split('"')[1] for word in topic.split(' + ')]
            top_keywords_per_topic.append(keywords)

        output = {}
        for idx, keywords in enumerate(top_keywords_per_topic):
            output.update({f'Topic {idx}': keywords})
        

        return output

if __name__ == '__main__':
    obj = TopicDetection()
    output =  obj.detect_topics('test.txt')
    print(output)
    
