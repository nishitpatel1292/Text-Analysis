from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter

class KeywordGenerator:

     def preprocess(self, text, stop_words):
          return [
          word for word in word_tokenize(text.lower()) 
          if word.isalpha() and word not in stop_words
     ]    
     
     def generate_keyword_cloud(self, file_path, max_words,chunk_size):
          all_words_freq = Counter()
          # Removing stop words
          stop_words = set(stopwords.words('english'))

          with open(file_path,'r', encoding='utf-8') as file:
               while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                         break   
                    
                    # Allowing only alpha     
                    words = self.preprocess(chunk, stop_words)

                    all_words_freq.update(words)


          top_words = all_words_freq.most_common(max_words)   
          return top_words
     
     def generate_keyword_cloud_dict(self, top_words):
          return [{"keyword": word, "count": count} for word, count in top_words]

     def generate_picture(self, words, image_path):
          
          wordcloud = WordCloud(background_color='white', 
                              colormap='copper_r', 
                              margin = 2, 
                              max_font_size = 90, 
                              prefer_horizontal=0.9).generate_from_frequencies(dict(words))

          wordcloud.to_file(image_path)


if __name__ == '__main__':
          obj = KeywordGenerator()
          final_words = obj.generate_keyword_cloud('test.txt', 40 ,10000)

          obj.generate_picture(final_words,'wordcloud_sample.png')
          cloud = obj.generate_keyword_cloud_dict(final_words)
          print(cloud)