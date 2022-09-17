# Simple Terminal Spell Check
Stop slowly googling words you need to spell, quickly spell check and correct words in the terminal.

- **No Internet connection needed, uses builtin linux word list.**
- **Privately log the misspellings to learn over time.**

![spell checking words in the terminal](http://i.imgur.com/ej5kDf2.png "spell CLI useage")

## Guide

1. Download the `spell.py` file place it somewhere 
2. Install the two requirements
`pip3 install python-Levenshtein~=0.12 && pip3 install numpy`
3. Add the alias to your .bashrc
`alias spell="python3 <PATH_TO_SPELL>"`
4. Star this project. Now you can spell check one or many words in the terminal

Default setting it to log any inncorect spelling, so you can go and learn what words you need to learn to spell.
The default path is `~/spelling_log.txt`


## Flags

> - Add the flag `--private` to pause logging on a specific search.
> - Add the flag `--fix` to autocorrect the top suggested result, works best when entering sentences 

![spell checking sentances in the terminal](http://i.imgur.com/ie1TLKb.png "spell CLI useage: autocorrect")

## More Examples

```python
$ spell honey
CORRECT: honey

$ spell pancreis
INCORRECT: pancreis
 - pancreas                                0.89
 - pancreatic                              0.73
 - pancreases                              0.73
 - pancreas's                              0.73
 - pantheist                               0.70
 - pantheism                               0.70
 - panderers                               0.70
 - pancake's                               0.70

$ spell test your spelling of words you mispelt
CORRECT: test
CORRECT: your
CORRECT: spelling
CORRECT: of
CORRECT: words
CORRECT: you
INCORRECT: mispelt
 - misspelt                                0.89
 - misspent                                0.78
 - misspell                                0.78
 - misdealt                                0.78
 - respelt                                 0.75
 - dispels                                 0.75
 - spelt                                   0.71
 - dispel                                  0.71


$ spell I have been raking my brain all day about learn algera
CORRECT: i
CORRECT: have
CORRECT: been
CORRECT: raking
CORRECT: my
CORRECT: brain
CORRECT: all
CORRECT: day
CORRECT: about
CORRECT: learn
INCORRECT: algera
 - algebra                                 0.88
 - algebras                                0.78
 - Algeria                                 0.75
 - augers                                  0.71
 - angora                                  0.71
 - angers                                  0.71
 - alters                                  0.71
 - alders                                  0.71


$ spell test your spelling of words you mispelt --fix
CORRECT: test
CORRECT: your
CORRECT: spelling
CORRECT: of
CORRECT: words
CORRECT: you
INCORRECT: mispelt
 - misspelt                                0.89
 - misspent                                0.78
 - misspell                                0.78
 - misdealt                                0.78
 - respelt                                 0.75
 - dispels                                 0.75
 - spelt                                   0.71
 - dispel                                  0.71
 
AUTOCORRECT: test your spelling of words you misspelt

```

## Limitations

- Some words are not in the default word list, like `autocorrect` for example. You need to add these to a custom word list
