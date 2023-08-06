# EvolutionGaming BundleShare Downloader

![EvolutionGaming](https://i.ibb.co/Hh5Xw2n/logo.png")

A command line utility tool for downloading bundle files from [EvolutionGaming Bundle Repository](https://bundle-repo.evo-games.com/).

## Installation
You can either download the package from [pip](https://pip.pypa.io/en/stable/installing/) *(assuming you have already pip installed in your system)*:

```
sudo pip install evolutiongaming-bundle-downloader
```

or you can run the following command to manually install the package:

```
sudo python setup.py install evolutiongaming
```

## Usage
This package can both be used with python shell or as a command line script:

```
>>> from evolutiongaming import downloader
>>>
>>> client = downloader.Downloader(username="<your email address>", password="<your password>", client_id="<your client id>")
>>> token = client.authentication_token()
>>> secret = client.authorization_token(token)
>>> 
>>> client.download_files(secret)
[(u'bundle-6.20200528.55355.39-52d3154ff9-native.zip',
  u'https://bundle-repo.evo-games.com/api/download/bundle-6.20200528.55355.39-52d3154ff9-native.zip'),
 (u'bundle-6.20200228.164151-4b4d16b9.zip',
  u'https://bundle-repo.evo-games.com/api/download/bundle-6.20200228.164151-4b4d16b9.zip'),
 (u'bundle-6.20200326.100947-707f2c25.zip',
  u'https://bundle-repo.evo-games.com/api/download/bundle-6.20200326.100947-707f2c25.zip'),
 (u'bundle-6.20191126.154224-50b1457e.zip',
  u'https://bundle-repo.evo-games.com/api/download/bundle-6.20191126.154224-50b1457e.zip'),
 (u'bundle-6.20191121.111140-2c066ecb.zip',
  u'https://bundle-repo.evo-games.com/api/download/bundle-6.20191121.111140-2c066ecb.zip')]
>>>
>>> client.download_file("medusa_scratch.zip", "https://bundle-repo.evo-games.com/api/download/bundle-6.20200528.55355.39-52d3154ff9-native.zip", secret, directory="/tmp", timeout=10)
>>> # Downloads to game to path: /tmp/medusa_scratch.zip
```

You can also download all games at once from the command line as follows:

```
$ python downloader.py --help
usage: downloader.py [-h] [-i CLIENT_ID] [-o OUTPUT_DIRECTORY] [-p PASSWORD]
                     [-t TIMEOUT] [-u USERNAME] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i CLIENT_ID, --client-id CLIENT_ID
  -l, --latest          retrieve only the latest games
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
  -p PASSWORD, --password PASSWORD
  -t TIMEOUT, --timeout TIMEOUT
                        timeout when downloading games
  -u USERNAME, --username USERNAME
  -v, --verbose         increase output verbosity
```
```
$ python downloader.py --username=<username> --password=<password> --client-id=<client_id> --verbose

INFO:root:Retrieving authentication token: johndoe@evogaming.com/c******************u
INFO:root:Retrieved authentication token: 20111Axht7AH61RWKHtsDg0K3aR7uBFPwOmHrY4OICK85tYXlCmRU8T
INFO:root:Retrieving authorization token: 20111Axht7AH61RWKHtsDg0K3aR7uBFPwOmHrY4OICK85tYXlCmRU8T
INFO:root:Retrieved authorization token: eyJraWQiOiJ4eGZ2VXdfc0h5MlJScDNTZDh1OU9NMGtBS3ZoUmdXb1RESE1VbWtlQzZRIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwMHUzeWMybDgzNWJ3b2szWTBpNyIsIm5hbWUiOiJSdWZhdCBNaXJ6YSIsImxvY2FsZSI6ImVuLVVTIiwiZW1haWwiOiJydWZhdC5taXJ6YUBiZXRidWxsLmNvbSIsInZlciI6MSwiaXNzIjoiaHR0cHM6Ly9ldm9sdXRpb25nYW1pbmcub2t0YS1lbWVhLmNvbSIsImF1ZCI6IjBvYTMybnFiMGtQbXNraFVNMGk3IiwiaWF0IjoxNTkzMTA3ODE2LCJleHAiOjE1OTMxMTE0MTYsImp0aSI6IklELmNGOGZ0MDlJSDJfS05UUUpWajZDZ0J6SHJPTmFTR0pLaDNVU1hhMVlfZ0EiLCJhbXIiOlsicHdkIl0sImlkcCI6IjAwbzFoYnBja2FnSFZDM0lMMGk3Iiwibm9uY2UiOiJzdGF0aWNOb25jZSIsInByZWZlcnJlZF91c2VybmFtZSI6InJ1ZmF0Lm1pcnphQGJldGJ1bGwuY29tIiwiZ2l2ZW5fbmFtZSI6IlJ1ZmF0IiwiZmFtaWx5X25hbWUiOiJNaXJ6YSIsInpvbmVpbmZvIjoiQW1lcmljYS9Mb3NfQW5nZWxlcyIsInVwZGF0ZWRfYXQiOjE1OTAwNDkzNzAsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdXRoX3RpbWUiOjE1OTMxMDc4MTZ9.VKNe_xl-HDifIVc12uWnTi85xY-X2qYK3jrdoFE6xo4X9qAcT3caEWQcBF35-VU3GNZ7I4UwmAspJLpvab_7mydAf0s1hJ2HZv2zimaWFouiAFBA17C2QC3f0P34OACNhTqSz3DVdEtukZNVLL7KsXvBQFL6oPOTJhFmHhqtZfG1O_khX4g6xY5oDvDYgv4F9XG5r54ixwniGTh8t60EVCsYHQ4CErhcPrxaaLm6EXWLEqHm1N6sZwxqeLE0Qi9Qtgg1Sq0bQn_pKOv6NAP9ljI-uzsI1OPfz2ea6KhwTIpRH5vuFBscvBSzsr_cwIRkqhPKIYtUJyf4DyGK1fF5Zg
INFO:root:Retrieving list of available games: https://bundle-repo.evo-games.com/api/list_files
INFO:root:Retrieved:
 * bundle-6.20200528.55355.39-52d3154ff9-native.zip
 * bundle-6.20200228.164151-4b4d16b9.zip
 * bundle-6.20200326.100947-707f2c25.zip
 * bundle-6.20191126.154224-50b1457e.zip
 * bundle-6.20191121.111140-2c066ecb.zip
INFO:root:Downloading https://bundle-repo.evo-games.com/api/download/bundle-6.20200528.55355.39-52d3154ff9-native.zip into /tmp/bundle-6.20200528.55355.39-52d3154ff9-native.zip
INFO:root:Download finished: /tmp/bundle-6.20200528.55355.39-52d3154ff9-native.zip
INFO:root:Downloading https://bundle-repo.evo-games.com/api/download/bundle-6.20200228.164151-4b4d16b9.zip into /tmp/bundle-6.20200228.164151-4b4d16b9.zip
INFO:root:Download finished: /tmp/bundle-6.20200228.164151-4b4d16b9.zip
INFO:root:Downloading https://bundle-repo.evo-games.com/api/download/bundle-6.20200326.100947-707f2c25.zip into /tmp/bundle-6.20200326.100947-707f2c25.zip
INFO:root:Download finished: /tmp/bundle-6.20200326.100947-707f2c25.zip
INFO:root:Downloading https://bundle-repo.evo-games.com/api/download/bundle-6.20191126.154224-50b1457e.zip into /tmp/bundle-6.20191126.154224-50b1457e.zip
INFO:root:Download finished: /tmp/bundle-6.20191126.154224-50b1457e.zip
INFO:root:Downloading https://bundle-repo.evo-games.com/api/download/bundle-6.20191121.111140-2c066ecb.zip into /tmp/bundle-6.20191121.111140-2c066ecb.zip
INFO:root:Download finished: /tmp/bundle-6.20191121.111140-2c066ecb.zip
```

## LICENSE
Copyright 2020 © Ozgur Vatansever

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
