from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re
import os
from nltk.tokenize import ToktokTokenizer
from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


def text_cleaning(text):
	text = re.sub(r'<[^>]+>', '', text)
	text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', text) 
	text = text.lower()

	return(text)

def tokenization(text, top):
	tokens = ToktokTokenizer().tokenize(text)

	custom_stopwords = set(stopwords.words("portuguese"))
	cleaned_stopwords = [t for t in tokens if t.lower() not in custom_stopwords]
	words_frequency = Counter(cleaned_stopwords)

	return(words_frequency.most_common(top))


def trash_content(soup):
	for tag in soup.find_all('header'):
		tag.decompose()

	for tag in soup.find_all('aside', class_='scaffold-layout__aside'):
		tag.decompose()

	for tag in soup.find_all('section', class_='artdeco-card pv-profile-card break-words'):
		tag.decompose()

	for tag in soup.find_all('footer'):
		tag.decompose()


def get_word(path_root,position):

	text_final = []
	for file in sorted(os.listdir(path_root)):
		abs_path = os.path.join(path_root,file)
		if os.path.isfile(abs_path):
			with open(abs_path, 'r', encoding='utf-8') as f: conteudo = f.read()
			soup = BeautifulSoup(conteudo, 'html.parser')
			
			if position: element = soup.find("article", class_="jobs-description__container")
			else: trash_content(soup=soup)
			
			#//article[contains(@class, 'jobs-description__container')]

			if not element is None:
				if position: text_complete = ' '.join(tag.get_text(separator=' ', strip=True) for tag in element.find_all(["span","p"]))
				else: text_complete = ' '.join(tag.get_text(separator=' ', strip=True) for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'span', 'li', 'section', 'div']))
				
				#txt_cleaning = text_cleaning(text_complete)
				txt_cleaning = tokenization(text_complete, 5)
				text_final.append(txt_cleaning)

		result_string = ", ".join(text_final)
	return(result_string)


def word_cloud(stop_word, final_text):
	wordcloud = WordCloud(
		width=1000,
		height=600,
		background_color='white',
		stopwords=stop_word,
		collocations=True
	).generate(final_text)

	plt.figure(figsize=(12, 6))
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis('off')
	plt.title('Word Cloud - LinkedIn')
	plt.savefig("plot.svg")
	plt.close()


def main(position=True):
	if position: path_root =  os.path.join(os.getcwd(),"_position")
	else: path_root =  os.path.join(os.getcwd(),"_profile")

	final_text = get_word(path_root=path_root,position=True)

	stop_word = set(STOPWORDS)

	stop_word.update([
        'linkedin', 'profile', 'experience', 'company', 'present', 'month', 'year',
        'gabriela', 'ferraz'
    ])

	if 1 == 0:
		stop_word = set([
			'de', 'da', 'do', 'em', 'para', 'com', 'o', 'a', 'e', 'é', 'na', 'no', 'os', 'as',
			'por', 'uma', 'um', 'ao', 'como', 'que', 'se', 'não', 'mais', 'também', 'entre',
			'sobre', 'minha', 'meu', 'sou', 'tenho', 'anos', 'linkedin', 'perfil'
		])

	word_cloud(stop_word, final_text)

if __name__ == '__main__': main()
