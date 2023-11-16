# 📜 growtopiawiki

parse growtopia wiki and output to json

## ⚙️ installation

clone package

```bash
  git clone https://github.com/Zeeetu/growtopiawiki
```

enter directory

```bash
  cd growtopiawiki
```

install with pip

```bash
  pip install -U .
```

## 📙 usage

use it in a python script

```python
from growtopiawiki import WikiParser
parser = WikiParser()
parser.wikiToJson()
```

on default it will look for items.dat from AppData/Local folder, but you can pass items.dat (or items.json, which will be overwritten) path to WikiParser if you want to specify a location

```python
WikiParser(items_dat = "path_to_items.dat")
```

```python
WikiParser(items_json = "path_to_items.json")
```

## 🔎 how it works

first it uses [growtopia.py](https://github.com/kaJob-dev/growtopia.py) to parse items.dat to a readable .json file, after that it will extract pages from [growtopia wiki](https://growtopia.fandom.com/wiki/Growtopia_Wiki)

the extracting method takes a list of pages as input and returns all requested pages in xml format

the wikiToJson() function takes split count as an argument, which will specify how many post requests to split the items into. default is 5, and generally anywhere between 5-20 should be good, not splitting may be pretty slow.

after that xml is parsed using [mwparserfromhell](https://github.com/earwig/mwparserfromhell), which is specifically used for parsing MediaWiki content, and output is saved into items.json file

## 🏅 contributing

contributions are very welcome.

**warning, pretty messy code**
