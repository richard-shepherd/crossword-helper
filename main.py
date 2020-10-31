import itertools
from crossword_libs import AnagramHelper
from crossword_libs import DefinitionHelper
from crossword_libs import Utils
from crossword_libs import WordManager
from crossword_libs import Words



Utils.log_to_stdout()

# for word in Words().match(".str.n.m.."):
#     print(word)

# for word in Words().match("b..tle"):
#     print(word)

# for word in Words().anagrams("rats").match("t..."):
#     print(word)

# for word in Words().length(20):
#     print(word)

Words().definition("rodents").length(5).print()

#Words().definition("rodent").length(5).print()


    


# for word in DefinitionHelper.words_for_definition("stargazer"):
#     print(word)

# for word in AnagramHelper().anagrams("rats"):
#     print(word)

# print(WordManager().lemma_infos["fast"].word_forms)
# print(WordManager().lemma_infos["table"].word_forms)
# print(WordManager().lemma_infos["astronomer"].word_forms)

#words = WordManager().get_words()
#for word in itertools.islice(words, 0, 10):
#    print(word)



