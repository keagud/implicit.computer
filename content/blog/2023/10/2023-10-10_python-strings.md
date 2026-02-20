+++
title =  "Implicit String Concatenation Considered Harmful"
slug =  "python-strings"
date = 2023-10-10

[taxonomies]
tags = ["python", "programming"]

+++

Python has a specific feature (?) related to string literals that, while not undocumented, isn't too well known either. If you have two string literals that are separated only by whitespace, the interpreter treats them as a single literal. For example, if, as part of normal data collection policy as spelled out in the EULA, an API requires the user send their complete genome with each request, you might have a variable like this:

```python
my_genome = "TGGGGCCAGTAGTCCTCCACGTGGGGAATCTTTCAGCGACGCTCTCAAGCTCTGAGAAGCACGATCCCAAGGTCCGTAGCAACAATCTCCTCTT"
```

But a long string literal like that breaks [PEP 8](https://pep8.org/#maximum-line-length) and compromises readability, and more importantly the warnings my linter plugin keeps shouting at me really harshes my vibe. Guido, in His Infinite Wisdom,[^1] allows us to do this:

```python
my_genome = "TGGGGCCAGTAGTCCTCCACGTGGGGAATCTTTCAGCGACGCT" 
    "CTCAAGCTCTGAGAAGCACGATCCCAAGGTCCGTAGCAACAATCTCCTCTT"
```

Much better! Of course in practice the most common source of long string literals is URLs. [Ruff](https://astral.sh/ruff) hates this:

```python
url = "https://a-really-really-long-url.co.uk/that-makes-your-linter/lose-its-freaking-mind"
```

But it chill with this:

```python
url = "https://a-really-really-long-url.co.uk/"
    "that-makes-your-linter/lose-its-freaking-mind"
```


This is a feature more Python programmers should be aware of ... so they can avoid it. Implicit string literal concatenation is, in my experience, the single most devious [footgun](https://en.wiktionary.org/wiki/footgun) in Python. If an oddly specific genie granted me one Python-related wish, I would not hesitate to send implicit concatenation to the Shadow Realm. 

First off, it's not even really necessary. Python already has the `+` operator to concatenate strings. 

```python
url = "https://a-really-really-long-url.co.uk/" + 
"that-makes-your-linter/lose-its-freaking-mind"
```

In my mind this is a lot clearer in communicating intent. It's two literals that are *added together* to create a single string. Plus (heh) you can add other non-literal stuff to your string (although you should probably just use f-strings at that point imo).

But implicit concatenation is not merely useless, it's actively harmful. When dealing with string collections, it converts what should be an obvious and catchable syntax error into potential hours of debug hell. 



```python
gauls = ["Belgae", "Aquitani", "Celtae"  "Helvetii"]

for x in gauls:
	print(x)

# Belgae
# Aquitani
# CeltaeHelvetii
```
[^2]

This is a pretty obvious syntax error --- well, obvious to a static analysis tool, anyway. In a long list of long strings (say, hardcoded urls or CSS selectors), you'd be forgiven if your eyes glance over the missing comma. But since two adjacent string literals are treated as one, the interpreter, and even a more pedantic third party tool like [pyright](https://github.com/microsoft/pyright), will consider it Heckin Validerino.  

The immediate cause for my writing this was a bug in a script that, among other things, opened a page in [selenium](https://www.selenium.dev/) to grab some data[^3] from each element that matched one of a list of predetermined selectors.  But after what I thought was a simple formatting change, it all fell apart. 'Invalid Selector', it would say, and I would assume that I had just failed at webdev and dutifully ~~get ChatGPT to~~ rewrite the selectors, to no avail. That missing comma probably cost me half an hour, but the sum of all wasted hours induced by this feature is surely greater than the total time saved from not needing to type the '+' key between string literals.  

---
[^1]:  I have no idea if Guido Van Rossum was actually the one to introduce this feature; to me he's more of a catchall patron figure akin to [Todd Howard](https://en.wikipedia.org/wiki/Todd_Howard#Opinions_and_recognition)

[^2]: [https://www.perseus.tufts.edu/hopper/text?doc=Caes.+Gal.+toc](https://www.perseus.tufts.edu/hopper/text?doc=Caes.+Gal.+toc)

[^3]:  Why did this page require a Javascript runtime to show me like 5 KB of plain text, and force me to use a full headless browser for something that should have been a simple `requests.get`? Well front-end design isn't my strong suit, but my impression is that God is dead and it is we who have killed him
