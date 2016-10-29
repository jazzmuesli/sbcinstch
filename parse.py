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

import fsunits
class HeightQuestion(Question):
  def __init(self):
    self.id = 'height'

  def nouns(self):
    return ['ft','feet','cm','in','inches','foot','feet']

  def parse(self, answer):
    for unit in self.nouns():
      answer = re.sub(r"([0-9.]+)" + unit, "\\1 " + unit, answer)
      print("answer:" + answer)
    ur = Question.parse(self,answer)
    if ur:
      qty = fsunits.convert_distance(float(ur.qty), to_unit='cm', from_unit=ur.unit)
      return UserResponse(ur.question, ur.answer, qty, 'cm')
    return ur

import unittest

qs = [CoffeeQuestion(), GenderQuestion(), BirthYearQuestion(), AgeQuestion(), HeightQuestion()]
def parse_user_response(sentence):
  for q in qs:
    ret = q.parse(unicode(sentence,encoding="utf-8"))
    if ret:
      print(ret)
      return ret
  print "ERROR: ", sentence, " cannot be parsed"
  return None

class QuestionTest(unittest.TestCase):
  def test_age(self):
    ur = parse_user_response('I am 25 years old')
    self.assertFalse(ur == None)
    self.assertEquals(int(ur.qty), 25)

  def test_born(self):
    ur = parse_user_response('I was born 1985')
    self.assertFalse(ur == None)
    self.assertEquals(int(ur.qty), 1985)

  def test_coffee(self):
    ur = parse_user_response('I drink 5 cups per day')
    self.assertFalse(ur == None)
    self.assertEquals(int(ur.qty), 5)

  def test_gender(self):
    ur = parse_user_response('I am male')
    self.assertFalse(ur == None)
    self.assertEquals(ur.qty, 'male')
    for snt in ['Actually I am a male', 'No, I am a male']:
      self.assertEquals(parse_user_response(snt).qty, 'male')


  def test_height(self):
   for snt in ["I'm 6ft tall", "I'm 182cm tall"]:
     ur = parse_user_response(snt)
     self.assertFalse(ur == None)
     self.assertEquals(int(ur.qty), 182)

unittest.main()

