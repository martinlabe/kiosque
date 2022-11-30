# Kioque

 A program scrapping YggTorrent to download the newspapers every day.
 
## Environment

To run the project please install the python requirements:

```python
pip install -r requirements.txt
```

The dependencies are:
- [Requests](https://github.com/psf/requests)~=2.28.1
- [pycountry](https://github.com/flyingcircusio/pycountry)~=22.3.5
- [YggTorrentCcraper](https://github.com/Harkame/YggTorrentScraper)~=1.2.12
- [python-qBittorrent](https://github.com/v1k45/python-qBittorrent)
- [dateparser](https://github.com/scrapinghub/dateparser)==1.1.4


Also, you need to have [qBittorrent](https://www.qbittorrent.org/) installed on your computer.


## Usage

```python
python main.py [--test]
```

## Description

The program is made from three classes:
- __ConnectionChecker__: Check if the connection located in the desired country. Abort otherwise.
- __Utils__: Provide some useful functions to hide our bot behaviour.
- __YggNewsPapersInterface__: Create an object allowing the user to download the newspapers available on YggTorrent.

Supported newspaper are:
- __The Economist__
- __Le Monde__
- __Le Monde Diplomatique__
- __Le Canard Enchaîné__

## Contribution

To add your favorite newspapers to the program you'll have to modify:
- main.py:medias[]
- YggNewsPapersInterface:get_request_for()
- YggNewsPapersInterface:parse()
- YggNewsPapersInterface:match()

The documentation is available in the code.

## Troubleshooting

This project uses the great [YggTorrentScraper](https://github.com/Harkame/YggTorrentScraper) library.
You might have to modify the variable _YGGTORRENT_TLD_ in _YggTorrentScraper/yggtorrentscraper/yggtorrentscraper.py_ 
file to put the right Top Level Domain used by YggTorrent platform at the moment you are using it.


## About

Author: Martin Labé

Date: 11/22
