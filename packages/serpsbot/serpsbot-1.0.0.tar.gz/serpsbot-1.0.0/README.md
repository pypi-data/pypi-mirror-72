# SerpsBot Python API Wrapper
Get Google SERPs results using SerpsBot API. This is the Python wrapper to consume data from [SerpsBot API](https://serpsbot.com).

## Installation

From PyPi:

```bash
pip install serpsbot
```

Or clone this repo and install locally:

```bash
git clone https://github.com/serpsbotapi/serpsbot-python
cd serpsbot-python
python setup.py install
```

## Consume API Data
First of all, create an account at [https://serpsbot.com/](https://serpsbot.com/) and get your API key.

```python
from serpsbot.client import SerpsBot

s = SerpsBot('your-api-key')
results = s.getresults(q='your query', pages=2, hl='en-US', gl='us', duration='', autocorrect=1)
```

If you need any help, contact us at [https://serpsbot.com/contact-us/](https://serpsbot.com/contact-us/)