import spacy

import snowballstemmer
import re
stemmer = snowballstemmer.stemmer('english')
nlp = spacy.load('en')

def as_number(s):
  m = re.search('([0-9.]+)', s)
  if m:
    return m.group(1)
  return None

class Question:
  def _init__(self,id,question):
    self.id=id
    self.question = question

  def range():
    pass

  def nouns(self):
    return [] 


  def parse(self, answer):
    doc = nlp(answer)
    ns = self.nouns()
    #print("ns:", ns)
    words = stemmer.stemWords([str(x) for x in doc])
    #print("ws:", words)
    return self.parse_stemmed_words(answer, words)

  def parse_stemmed_words(self, answer, words):
    ns = self.nouns()
    for i in range(len(words)):
      word = words[i]
      prev_word = as_number('' if i < 1 else words[i-1])
      next_word = as_number('' if i >= len(words)-1 else words[i+1])
 
      if word in ns:
        print('Found: ',word, prev_word, next_word)
        qty = None
        if prev_word:
          qty = prev_word
        if next_word:
          qty = next_word
        if qty:
          return UserResponse(self,answer, qty, word)
    return None
  
class GenderQuestion(Question):
  def __init__(self):
    self.id = 'coffee'

  def parse_stemmed_words(self,answer, words):
    print("words:", words)
    gender = None
    for word in words:
      if re.search('man|male|buy|guy', word):
        gender = 'male'
      if re.search('woman|female|lady|girl', word):
        gender = 'female'
    if gender:
      ur = UserResponse(self, answer, gender, 'gender')   
      return ur

  

class CoffeeQuestion(Question):
  def __init__(self):
    self.id = 'coffee'

  def range(self):
    return (0,10)

  def nouns(self):
    return ['cup']


class AgeQuestion(Question):
  def __init__(self):
    self.id = 'coffee'

  def range(self):
    (0,100)

  def nouns(self):
    return ['year']

class BirthYearQuestion(Question):
  def __init__(self):
    self.id = 'coffee'

  def range(self):
    return (1900,2016)

  def nouns(self):
    return ['born']

class UserResponse:
  def __init__(self,question,answer,qty,unit):
    self.question = question
    self.answer = answer
    self.qty = qty
    self.unit = unit

  def __str__(self):
    return 'User input "%s" is handy for question %s, it contains qty=%s in %s units' % (self.answer, self.question, self.qty, self.unit)

sentences=['I am 25 years old','I drink 5 cups per day','About 5 cups','I am male','I was born 1985']
qs = [CoffeeQuestion(), GenderQuestion(), BirthYearQuestion(), AgeQuestion()]
for sent in sentences:
  ret = None
  for q in qs:
    ret = q.parse(unicode(sent,encoding="utf-8"))
    if ret:
      print(ret)
      break

  if ret == None:
      print("Cannot parse:" + sent)
