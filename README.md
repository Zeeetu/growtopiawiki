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
from growtopiawiki import build_items
build_items()
```

on default it will look for items.dat from AppData/Local folder, but you can pass items.dat (or items.json, which will be overwritten) path to the function if you want to specify a location

```python
build_items(items_dat = "path_to_items.dat")
```

```python
build_items(items_json = "path_to_items.json")
```

## 📐 data structure

the project strives for a smaller output file size, hence why the usage of item id's instead of names.

### splicing example

recipe of door (dirt + cave background):

```json
"recipe": {
      "splice": [
        2,
        14
      ]
    }
```

where 2 is the itemid of dirt and 14 is the itemid of cave background

### combining example

recipe of slime (15x chem green + 2x chem pink + 4x chem blue), yields 4

```json
"recipe": {
      "combine": {
        "recipe": [
          914,
          15,
          918,
          2,
          920,
          4
        ],
        "yields": 4
      }
    }
```

where 914 is the itemid of green chemical (first ingredient), and 15 is amount of green chemicals required (first ingredient), etc..
if the recipe requires a certain combiner, the dictionary has the "combiner" key, which is the itemid of the required combiner.

## 🔎 how it works

first it uses [growtopia.py](https://github.com/kaJob-dev/growtopia.py) to parse items.dat to a python dictionary, after that it will extract pages from [growtopia wiki](https://growtopia.fandom.com/wiki/Growtopia_Wiki)

the extracting method takes a list of pages as input and returns all requested pages in xml format

the build_items() function takes split count as a keyword argument, which will specify how many post requests to split the items into. default is 5, and generally anywhere between 5-20 should be good, not splitting may be pretty slow.

after that xml is parsed using [mwparserfromhell](https://github.com/earwig/mwparserfromhell), which is specifically used for parsing MediaWiki content, and output is saved into items.json file

## 🏅 contributing

contributions are very welcome.
