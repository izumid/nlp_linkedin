from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
from nltk.tokenize import ToktokTokenizer
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("rslp")
from deep_translator import GoogleTranslator
from langdetect import detect
import json
import spacy

def bigram_test():
	from nltk.collocations import BigramCollocationFinder
	from nltk.metrics import BigramAssocMeasures
	from nltk.tokenize import word_tokenize

	text = "New York is a big city and New York has tall buildings"
	tokens = word_tokenize(text)

	finder = BigramCollocationFinder.from_words(tokens)
	bigrams = finder.nbest(BigramAssocMeasures.likelihood_ratio, 10)

	print(bigrams)  # [('New', 'York'), ('York', 'has'), ...]

def debug_code(debug,message,var=None):
	if debug: 
		if var is None: print(f"{message};\r\n")
		else: print(f"{message}: \r\n{var};\r\n")


def tokenization(text,language,top_word,add_stop_word):
	tokens = ToktokTokenizer().tokenize(text)

	custom_stopwords = set(stopwords.words(language))
	custom_stopwords.update(add_stop_word)

	clean_num_diacritic = [t.lower() for t in tokens if t.isalpha()]
	cleaned_stopwords = [t for t in clean_num_diacritic if t not in custom_stopwords]
	words_frequency = Counter(cleaned_stopwords)

	return(words_frequency.most_common(top_word))


def trash_content(soup):
	for tag in soup.find_all('header'):
		tag.decompose()

	for tag in soup.find_all('aside', class_='scaffold-layout__aside'):
		tag.decompose()

	for tag in soup.find_all('section', class_='artdeco-card pv-profile-card break-words'):
		tag.decompose()

	for tag in soup.find_all('footer'):
		tag.decompose()


def get_word(path_root,position,language,top_word,add_stop_word):
	translator = GoogleTranslator(source="en", target="pt")

	frequency = []
	for file in sorted(os.listdir(path_root)):
		abs_path = os.path.join(path_root,file)
		if os.path.isfile(abs_path):
			with open(abs_path, 'r', encoding='utf-8') as f: conteudo = f.read()
			soup = BeautifulSoup(conteudo, 'html.parser')
			
			if position: element = soup.find("article", class_="jobs-description__container")
			else: trash_content(soup=soup)
			
			if not element is None:
				if position: text = ' '.join(tag.get_text(separator=' ', strip=True) for tag in element.find_all(["span","p"]))
				else: text = ' '.join(tag.get_text(separator=' ', strip=True) for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'span', 'li', 'section', 'div']))
				
				if detect(text)== "en":
					sentence = nltk.tokenize.sent_tokenize(text)
					translated_text = ""
					for s in sentence:
						translated_text.join(translator.translate(s))

					frequency.extend(tokenization(text=translated_text,language=language,top_word=top_word,add_stop_word=add_stop_word))
				else:
					frequency.extend(tokenization(text=text,language=language,top_word=top_word,add_stop_word=add_stop_word))

	return(dict(frequency))


def word_cloud(final_text):
	path_destination = os.path.join(os.getcwd(), "img")
	if not os.path.exists(path_destination): os.makedirs(path_destination)

	wordcloud = WordCloud(
		width=1920,
		height=1080,
		background_color='black',
		#collocations=True,
		colormap="BuGn"
	).generate_from_frequencies(final_text)

	plt.figure(figsize=(12, 6))
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis('off')
	plt.title('Word Cloud')
	plt.savefig(os.path.join(path_destination,"word_cloud.svg"), format='svg')
	plt.close()

def stemmatization(word_frequency,debug=False):
	stemmer = RSLPStemmer()
	stemmed = {}
	for word, freq in word_frequency.items():
		stem = stemmer.stem(word)
		stemmed[stem] = stemmed.get(stem,0) + freq

	
	debug_code(debug,"stemmed",var=stemmed)
	return stemmed


def lemmatization(word_frequency,debug=False):
	spy = spacy.load("pt_core_news_sm")
	lemmatized = {}
	for word, freq in word_frequency.items():
		doc = spy(word)
		lemma = doc[0].lemma_
		lemmatized[lemma] = lemmatized.get(lemma,0) + freq
	
	debug_code(debug,"lemmatized",var=lemmatized)
	return lemmatized

def main(position=True):
	with open("config/config.json") as jsf: config_json = json.load(jsf)
	add_stop_word = config_json["stop_word"]
	debug = config_json["debug"]

	if position: path_root =  os.path.join(os.getcwd(),"__position")
	else: path_root =  os.path.join(os.getcwd(),"__profile")

	webpage_word = get_word(path_root=path_root,position=True,language="portuguese",top_word=20,add_stop_word=add_stop_word)
	debug_code(debug,"webpage_word",var=webpage_word)
	word_frequency=lemmatization(word_frequency=webpage_word,debug=debug_code)
	word_cloud(word_frequency)
	
if __name__ == '__main__': main()
