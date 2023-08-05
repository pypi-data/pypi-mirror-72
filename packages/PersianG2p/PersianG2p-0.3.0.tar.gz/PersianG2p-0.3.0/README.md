# Simple persian (farsi) grapheme-to-phoneme converter

It uses [this neural net](https://github.com/AzamRabiee/Persian_G2P) to convertion persian texts (with arabic symbols) into phonemes text.

Features of farsi:

* arabic notation
* the characters have different forms depended on position into word
* vowels are often not written but pronounced; for example:
    * سس pronounces **sos** but written **ss**
    * من pronounces **man** but written **mn**
    * سلام pronounces **salām** but written **slām**
    * شما pronounces **šomā** but written **šmā**
    * ممنون pronounces **mamnun** but written **mmnun**
* the same symbols have different pronounces: in the word مو the symbol و pronounces **u**, but in the word میوه this symbol goes after vowel and pronounces **w**
* no overlap of vowel sounds
* verbs are at the end of sentence
* no sex
* no cases
* adjectives and definitions append to the end of nouns

## How it works

There is the dictionary with 1867 pairs like (persian word, pronouncing of one). Some of these word (in English): *water, there, feeling, use, people, throw, he, can, highway, was, hall, guarantee, production, sentence, account, god, self, they know, dollar, mind, novel, earthquake, organizing, weapons, personal, martyr, necessity, opinion, french, legal, london, deprived, people, studies, source, fruit, they take, system, the light, are, and, leg, bridge, what, done, do*.

Firstly, your text is **normalized**, after --- **tokenized**. 
1. If token is not a symbol of arabic alphabet then it does nothing. 
2. If token is the word from dictionary then it chooses the pronouncing from dictionary.
3. Otherwise the pronouncing will be predicted by neural net.

If token was a word from dictionary then it's pronouncing is the word like  t h i s  (spaces between symbols and in the end and begin of word). If the word is continues then it's the predicted word.


## Comparison with [epitran](https://github.com/dmort27/epitran)

[Code](https://github.com/PasaOpasen/PersianG2P/blob/master/PersianG2p/compares.py)

| persian word        | epitran convertion           | PersianG2p conversion  | expected  |
| -------------: |:-------------:| :-----:| :-----:|
|سلام |slɒm |salām| salām|
|ممنون |mmnvn |mamnun| mamnun|
|خب |xb |xab| xāb|
|ساحل |sɒhl |sāhel| sāhel|
|یخ |jx |yax| yax|
|لاغر |lɒɣr |lāġar| lāġar|
|پسته |پsth |peste| peste|
|مثلث |msls |mosles| mosles|
|سال ها |sɒl hɒ |sālehā| sālhā|
|لذت |lzt |lazt| lezzat|
|دژ |dʒ |dož| dež|
|برف |brf |barf| barf|
|خدا حافظ |xdɒ hɒfz | x o d ā  hāfez| xodā hāfez|
|دمپایی |dmپɒjj |dampāyi| dampāyi|
|نشستن |nʃstn |nešastan| nešastan|
|متأسفانه |mtɒʔsfɒnh |motsafe`āne| mota’assefāne|

## Installation
```
pip install PersianG2p
```

## Usage 

```python
from PersianG2p import Persian_g2p_converter

PersianG2Pconverter = Persian_g2p_converter()

PersianG2Pconverter.transliterate('ما الان درحال بازی بودیم', tidy = False)
# ' m A   a l A n  darhAl  b A z i   b u d i m '

PersianG2Pconverter.transliterate('ما الان درحال بازی بودیم')
# ' m ā   a l ā n  darhāl  b ā z i   b u d i m '

PersianG2Pconverter.transliterate('نه تنها یک کلمه')
# ' n o h   t a n h ā   y e k  kalame'
```
