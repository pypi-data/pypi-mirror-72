# Play Store Scrapper
Using this package you can easily scrap data from Google Play Store.

## Installation
```
pip install play-store-scrapper
```
### Environment Variables
Set the following Environment variables before running.

`GECKO_DRIVER_PATH` Path to Gecko Web Driver  (You also need Firefox to run this. For now no other browser option is added)

## Usage
```python
from play_store_scapper import PlayStore
store = PlayStore()
store.get_app_detail("com.cstayyab.beemy")
```

