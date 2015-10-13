import re, collections
import itertools
from nltk.corpus import wordnet

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
  model = collections.defaultdict(lambda: 1)
  for f in features:
    model[f] += 1
  return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
  splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
  deletes    = [a + b[1:] for a, b in splits if b]
  transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
  replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
  inserts    = [a + c + b     for a, b in splits for c in alphabet]
  return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
  return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
  candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
  return max(candidates, key=NWORDS.get)

LWORDS = set()
with open("list1.txt") as f:
  for line in f.readlines():
    LWORDS.add(line.strip())

def check_dictionary_list(w):
  for word in LWORDS:
    if len(word) != len(w): continue
    found = True
    for c in w:
      found &= c in word
    if found:
      print word

def chunks(lst, n):
  """ Yield successive n-sized chunks from l.
  """
  # words = lst.split(' ')
  begin = 0
  while begin < len(lst):
    end = begin + n
    while end < len(lst) and lst[end] != ' ':
      end += 1 
    yield lst[begin:end]
    begin = end + 1

def wordnet_test(w):
  synsets = wordnet.synsets(w)
  if len(synsets) > 0: 
    # print synsets
    print w
    for synset in synsets:
      indent = " " * 2
      print indent, "-" * 10
      print indent, "Name:", synset.name
      # print "Lexical Type:", synset.lexname
      # print "Lemmas:", synset.lemma_names
      definition = synset.definition
      max_length = 55
      if len(definition) > max_length:
        definition = ('\n' + (indent * 3)).join( list(chunks(definition, max_length)) )
      print indent, "Definition:", definition
      # for example in synset.examples:
      #   print indent, "Example:", example
    return True
  return False

def check(st, length):
  for x in itertools.combinations(st, length):
    for i in itertools.permutations(x, length):
      t = ''.join(i)
      # word = correct(t)
      # # print t, word
      # if word == t:
      #   print word
      wordnet_test(t)

def check2(st, length):
  for x in itertools.combinations(st, length):
    check_dictionary_list(x)

check('nzlelmhage', 7)