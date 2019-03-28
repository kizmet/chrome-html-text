import requests
import re
import nltk
from nltk.text import Text
from nltk.corpus import stopwords
from collections import Counter
from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class Scraper():
  def __init__(self, url):
    self.url = url
    opts = Options()
    opts.set_headless()
    self.driver = Chrome(options=opts)
    self.driver.get(url)
    self.r = self.driver.page_source
    self.driver.close()
    self.get_soup()
### ---------------------------------------------------- ####

  def get_soup(self):  
      self.soup = BeautifulSoup(self.r, 'html5lib')
      blacklist = ['meta', 'base', 'link', 'noscript', 'button', 'svg',
                   'sw-breadcrumb', 'img', 'sw-icon', 'g', 'circle', 'iframe', 'script', 'a', 'style']
      for tag in self.soup.find_all():
          if tag.name.lower() in blacklist:
              tag.extract()
      comments = self.soup.findAll(text=lambda text:isinstance(text, Comment))
      for comment in comments:
          comment.extract()
      self.raw = self.soup.get_text()
      self.raw = self.raw.lower()
      self.get_words()

  def get_words(self):
      #nltk.data.path.append('./nltk_data/')  # set the path
      nltk.data.path.append('/Users/bryant/Code/flask-by-example/nltk_data/')
      self.tokens = nltk.word_tokenize(self.raw)
      self.text = nltk.Text(self.tokens)
      nonPunct = re.compile('.*[A-Za-z].*')
      self.raw_words = [w for w in self.text if nonPunct.match(w)]
      self.raw_word_count = Counter(self.raw_words)
      ignored_words = stopwords.words('english')
      self.no_ignored_words = [w for w in self.raw_words if w.lower()  not in ignored_words]
      self.no_ignored_words_count = Counter(self.no_ignored_words)
      self.items = self.no_ignored_words_count.items()

  def print_tags(self):
      for tag in self.soup.find_all():
        print(tag.name, '|', str(len(str(tag))), ' | ', tag.attrs)
      

# url = 'https://www.juniper.net/us/en/dm/mc-ready-campus/?pageVersion=campus1_Definition'
# mydata = Scraper(url)
#mydata.get_soup()
#mydata.get_words()
#mydata.print_tags()
### ---------------------------------------------------- ####



