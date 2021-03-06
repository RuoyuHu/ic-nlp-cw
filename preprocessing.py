import os
import pandas as pd
import string
from collections import defaultdict
from sklearn.preprocessing import MultiLabelBinarizer
# Importing Libraries 
import nltk
import re
from unidecode import unidecode

nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


class Preprocessor:
	"""
	An object that handles preprocessing of text data
	Adapted from
	https://github.com/meyrow/pcl-detection-task4-semeval2022/blob/main/preprocessing/DPM_preprocessing_over_sampling.py
	"""

	def __init__(self,
				 do_remove_newlines_and_tabs: bool = True,
				 do_strip_html_tags: bool = True,
				 do_remove_links: bool = True,
				 do_remove_extra_whitespace: bool = True,
				 do_remove_accented_characters: bool = True,
				 do_remove_incorrect_repetition: bool = True,
				 do_expand_contractions: bool = True,
				 do_remove_special_characters: bool = True):

		self.do_remove_newlines_and_tabs = do_remove_newlines_and_tabs
		self.do_strip_html_tags = do_strip_html_tags
		self.do_remove_links = do_remove_links
		self.do_remove_extra_whitespace = do_remove_extra_whitespace
		self.do_remove_accented_characters = do_remove_accented_characters
		self.do_remove_incorrect_repetition = do_remove_incorrect_repetition
		self.do_expand_contractions = do_expand_contractions
		self.do_remove_special_characters = do_remove_special_characters

		self.CONTRACTION_MAP = {
			"ain't": "is not",
			"aren't": "are not",
			"can't": "cannot",
			"can't've": "cannot have",
			"'cause": "because",
			"could've": "could have",
			"couldn't": "could not",
			"couldn't've": "could not have",
			"didn't": "did not",
			"doesn't": "does not",
			"don't": "do not",
			"hadn't": "had not",
			"hadn't've": "had not have",
			"hasn't": "has not",
			"haven't": "have not",
			"he'd": "he would",
			"he'd've": "he would have",
			"he'll": "he will",
			"he'll've": "he he will have",
			"he's": "he is",
			"how'd": "how did",
			"how'd'y": "how do you",
			"how'll": "how will",
			"how's": "how is",
			"i'd": "i would",
			"i'd've": "i would have",
			"i'll": "i will",
			"i'll've": "i will have",
			"i'm": "i am",
			"i've": "i have",
			"isn't": "is not",
			"it'd": "it would",
			"it'd've": "it would have",
			"it'll": "it will",
			"it'll've": "it will have",
			"it's": "it is",
			"let's": "let us",
			"ma'am": "madam",
			"mayn't": "may not",
			"might've": "might have",
			"mightn't": "might not",
			"mightn't've": "might not have",
			"must've": "must have",
			"mustn't": "must not",
			"mustn't've": "must not have",
			"needn't": "need not",
			"needn't've": "need not have",
			"o'clock": "of the clock",
			"oughtn't": "ought not",
			"oughtn't've": "ought not have",
			"shan't": "shall not",
			"sha'n't": "shall not",
			"shan't've": "shall not have",
			"she'd": "she would",
			"she'd've": "she would have",
			"she'll": "she will",
			"she'll've": "she will have",
			"she's": "she is",
			"should've": "should have",
			"shouldn't": "should not",
			"shouldn't've": "should not have",
			"so've": "so have",
			"so's": "so as",
			"that'd": "that would",
			"that'd've": "that would have",
			"that's": "that is",
			"there'd": "there would",
			"there'd've": "there would have",
			"there's": "there is",
			"they'd": "they would",
			"they'd've": "they would have",
			"they'll": "they will",
			"they'll've": "they will have",
			"they're": "they are",
			"they've": "they have",
			"to've": "to have",
			"wasn't": "was not",
			"we'd": "we would",
			"we'd've": "we would have",
			"we'll": "we will",
			"we'll've": "we will have",
			"we're": "we are",
			"we've": "we have",
			"weren't": "were not",
			"what'll": "what will",
			"what'll've": "what will have",
			"what're": "what are",
			"what's": "what is",
			"what've": "what have",
			"when's": "when is",
			"when've": "when have",
			"where'd": "where did",
			"where's": "where is",
			"where've": "where have",
			"who'll": "who will",
			"who'll've": "who will have",
			"who's": "who is",
			"who've": "who have",
			"why's": "why is",
			"why've": "why have",
			"will've": "will have",
			"won't": "will not",
			"won't've": "will not have",
			"would've": "would have",
			"wouldn't": "would not",
			"wouldn't've": "would not have",
			"y'all": "you all",
			"y'all'd": "you all would",
			"y'all'd've": "you all would have",
			"y'all're": "you all are",
			"y'all've": "you all have",
			"you'd": "you would",
			"you'd've": "you would have",
			"you'll": "you will",
			"you'll've": "you will have",
			"you're": "you are",
			"you've": "you have",
		}

	def remove_newlines_and_tabs(self, text):
		"""
		This function will remove all the occurrences of newlines, tabs, and combinations like: \\n, \\.
		
		arguments:
			input_text: "text" of type "String". 
						
		return:
			value: "text" after removal of newlines, tabs, \\n, \\ characters.
			
		Example:
		Input : This is her \\ first day at this place.\n Please,\t Be nice to her.\\n
		Output : This is her first day at this place. Please, Be nice to her. 
		
		"""

		# Replacing all the occurrences of \n,\\n,\t,\\ with a space.
		formatted_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t', ' ').replace('\\', ' ').replace(
			'. com', '.com')
		return formatted_text

	def strip_html_tags(self, text):
		""" 
		This function will remove all the occurrences of html tags from the text.
		
		arguments:
			input_text: "text" of type "String". 
						
		return:
			value: "text" after removal of html tags.
			
		Example:
		Input : This is a nice place to live. <IMG>
		Output : This is a nice place to live.  
		"""
		# Initiating BeautifulSoup object soup.
		soup = BeautifulSoup(text, "html.parser")
		# Get all the text other than html tags.
		stripped_text = soup.get_text(separator=" ")
		return stripped_text

	def remove_links(self, text):
		"""
		This function will remove all the occurrences of links.
		
		arguments:
			input_text: "text" of type "String". 
						
		return:
			value: "text" after removal of all types of links.
			
		Example:
		Input : To know more about this website: kajalyadav.com  visit: https://kajalyadav.com//Blogs
		Output : To know more about this website: visit:     
		
		"""

		# Removing all the occurrences of links that starts with https
		remove_https = re.sub(r'http\S+', '', text)
		# Remove all the occurrences of text that ends with .com
		remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
		return remove_com

	def remove_extra_whitespace(self, text):
		"""
		This function will remove extra whitespaces from the text
		arguments:
			input_text: "text" of type "String". 
						
		return:
			value: "text" after extra whitespaces removed .
			
		Example:
		Input : How   are   you   doing   ?
		Output : How are you doing ?
		"""
		pattern = re.compile(r'\s+')
		without_whitespace = re.sub(pattern, ' ', text)
		# There are some instances where there is no space after '?' & ')', 
		# So I am replacing these with one space so that It will not consider two words as one token.
		text = without_whitespace.replace('?', ' ? ').replace(')', ') ')
		return text

	# Code for accented characters removal
	def remove_accented_characters(self, text):
		# this is a docstring
		"""
		The function will remove accented characters from the 
		text contained within the Dataset.

		arguments:
			input_text: "text" of type "String". 
						
		return:
			value: "text" with removed accented characters.
			
		Example:
		Input : M??laga, ????????hello
		Output : Malaga, aeeohello    
			
		"""
		# Remove accented characters from text using unidecode.
		# Unidecode() - It takes unicode data & tries to represent it to ASCII characters. 
		text = unidecode(text)
		return text

	# Code for removing repeated characters and punctuations

	def remove_incorrect_repetition(self, text):
		"""
		This Function will reduce repetition to two characters
		for alphabets and to one character for punctuations.
		
		arguments:
		input_text: "text" of type "String".
		return:
		value: Finally formatted text with alphabets repeating to
		two characters & punctuations limited to one repetition
			
		Example:
		Input : Realllllllllyyyyy,        Greeeeaaaatttt   !!!!?....;;;;:)
		Output : Reallyy, Greeaatt !?.;:)
		
		"""
		# Pattern matching for all case alphabets
		pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)

		# Limiting all the  repetition to two characters.
		formatted_text = pattern_alpha.sub(r"\1\1", text)

		# Pattern matching for all the punctuations that can occur
		pattern_punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')

		# Limiting punctuations in previously formatted string to only one.
		combined_formatted = pattern_punct.sub(r'\1', formatted_text)

		# The below statement is replacing repetition of spaces that occur more than two times with that of one occurrence.
		final_formatted = re.sub(' {2,}', ' ', combined_formatted)
		return final_formatted

	# The code for expanding contraction words
	def expand_contractions(self, text):
		"""
		expand shortened words to the actual form.
		e.g. don't to do not

		arguments:
			input_text: "text" of type "String".

		return:
			value: Text with expanded form of shortened words.

		Example:
			Input : ain't, aren't, can't, cause, can't've
			Output :  is not, are not, cannot, because, cannot have
		"""
		# Tokenizing text into tokens.
		list_of_tokens = text.split(' ')

		# Checks whether the given token matches with the key & replacing word with key's value.

		# Check whether wrd is in list_of_tokens or not.
		for word in list_of_tokens:
			# Check whether found word is in dictionary "Contraction Map" or not as a key. 
			if word in self.CONTRACTION_MAP:
				# If Word is present in both dictionary & list_of_tokens, replace that word with the key value.
				list_of_tokens = [item.replace(word, self.CONTRACTION_MAP[word]) for item in list_of_tokens]

		# Converting list of tokens to String.
		string_of_tokens = ' '.join(str(e) for e in list_of_tokens)
		return string_of_tokens

	# The code for removing special characters
	def remove_special_characters(self, text):
		"""
		Removing all the special characters except the one that is passed within
		the regex to match, as they have imp meaning in the text provided.
		
		arguments:
		input_text: "text" of type "String".

		return:
			value: Text with removed special characters that don't require.
			
		Example: 
		Input : Hello, K-a-j-a-l. Thi*s is $100.05 : the payment that you will receive! (Is this okay?)
		Output :  Hello, Kajal. This is $100.05 : the payment that you will receive! Is this okay?
		"""

		# The formatted text after removing not necessary punctuations.
		formatted_text = re.sub(r"[^a-zA-Z0-9:;$-,%.?!]+", ' ', text)
		# In the above regex expression,I am providing necessary set of punctuations that are frequent in
		# this particular dataset.
		return formatted_text

	def preprocess(self, df: pd.DataFrame):
		"""
		Applies the chosen preprocessing functions to the text data in the given dataframe
		"""

		def perform_preprocess(text: str):
			if self.do_expand_contractions:
				text = self.expand_contractions(text)

			if self.do_remove_newlines_and_tabs:
				text = self.remove_newlines_and_tabs(text)

			if self.do_strip_html_tags:
				text = self.strip_html_tags(text)

			if self.do_remove_links:
				text = self.remove_links(text)

			if self.do_remove_extra_whitespace:
				text = self.remove_extra_whitespace(text)

			if self.do_remove_accented_characters:
				text = self.remove_accented_characters(text)

			if self.do_remove_incorrect_repetition:
				text = self.remove_incorrect_repetition(text)

		df["text"].apply(lambda x: perform_preprocess(x))