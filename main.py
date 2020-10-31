import itertools
from crossword_libs import AnagramHelper
from crossword_libs import Utils
from crossword_libs import WordManager



Utils.log_to_stdout()

for word in AnagramHelper().anagrams("rats"):
    print(word)

# print(WordManager().lemma_infos["fast"].word_forms)
# print(WordManager().lemma_infos["table"].word_forms)
# print(WordManager().lemma_infos["astronomer"].word_forms)

#words = WordManager().get_words()
#for word in itertools.islice(words, 0, 10):
#    print(word)



