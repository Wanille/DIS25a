import nltk
from bs4 import BeautifulSoup
import re
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

tokenizer=ToktokTokenizer()


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

def remove_special_characters(text, remove_digits=True):
    pattern=r'[^a-zA-z0-9\s]'
    text=re.sub(pattern,'',text)
    return text

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = remove_special_characters(text, remove_digits=True)
    return text

def simple_stemmer(text):
    ps=nltk.porter.PorterStemmer()
    text= ' '.join([ps.stem(word) for word in text.split()])
    return text


tokenizer=ToktokTokenizer()
stopword_list=nltk.corpus.stopwords.words('english')

def remove_stopwords(text, is_lower_case=False):
    stop=set(stopwords.words('english'))
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text



def clean_text(text):
    text = denoise_text(text)
    text = remove_stopwords(text)
    text = simple_stemmer(text)
    return text