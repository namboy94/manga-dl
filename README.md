# Manga Downloader
![Logo](manga_dl/resources/images/logo-readme.png "Logo")

This is a Manga Downloader that can download managa series from various sources.

Currently supported are:

 * [Mangafox](http://mangafox.me)

## Usage

### Installation

**Via pip**

    $ pip install manga_dl --user

**From source**

    $ python setup.py install --user

**Binary Files**

If you would like to not install the program and instead use a single binary
file, you can download them from our [Github releases page](https://github.com/namboy94/manga-downloader/releases).

### CLI

The program offers a simple wget-like CLI. To download a series, simply enter:
    
    $ manga-dl <URL>
    
This will create a new directory with the series name in the current working
directory and subsequently download all currently available pages of the series

The CLI does offer some configuration:

* ```--destination```, ```-d``` (type: string)
  - Specifies the directory in which the series will be stored
  - Defaults to the current working directory + the series name
* ```--threads```, ```-t``` (type: integer)
  - Specifies how many threads the program may use. Using more threads may speed up the parsing
  - Defaults to the amount of logical processors the system has
* ```--verbose```, ```-v```
  - If set, the program will print it's progress to the console
* ```--update```
  - If set, the program will only check for content that have not been downloaded yet
* ```--repair```
  - If set, the program will check each previously downloaded file for errors
  - If errors are found, the file in question is re-downloaded
* ```--zip-volumes```
  - Zips the series by volume after the download is completed
* ```--zip-chapters```
  - Zips the series by chapter after the download is completed

## Further Information

* [Changelog](https://gitlab.namibsun.net/namboy94/manga-downloader/raw/master/CHANGELOG)
* [Gitlab](https://gitlab.namibsun.net/namboy94/manga-downloader)
* [Github](https://github.com/namboy94/manga-downloader)
* [Python Package Index Site](https://pypi.python.org/pypi/manga_dl)
* [Documentation(HTML)](https://docs.namibsun.net/html_docs/manga-downloader/index.html)
* [Documentation(PDF)](https://docs.namibsun.net/pdf_docs/manga-downloader.pdf)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/manga-downloader/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/manga-downloader/index.html)
* [Test Coverage](https://coverage.namibsun.net/manga-downloader/index.html)
