# Manga Downloader

|master|develop|
|:---:|:---:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/manga-dl/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/manga-dl/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/manga-dl/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/manga-dl/commits/develop)|

![Logo](resources/logo/logo-readme.png "Logo")

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
file, you can download them from our [Github releases page](https://github.com/namboy94/manga-dl/releases).

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

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/manga-dl)
* [Github](https://github.com/namboy94/manga-dl)
* [Progstats](https://progstats.namibsun.net/projects/manga-dl)
* [PyPi](https://pypi.org/project/manga-dl)