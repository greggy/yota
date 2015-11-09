# Yota Client

Script to change yota tariff or show one (It shows tariff price not speed)

## Configure
Write your credintials in yota.py file:
```
LOGIN = 'Your email'
PASSWORD = 'Your password'
```

## Dependencies
 * python-requests
 * python-argparse
 * python-lxml

## How does it work?
Get your current tariff:

```
> ./yota.py -s
Your tariff is 500
```

Сhange current tariff to 300:

```
> ./yota.py -t 300
```

```
bin/yota.py -l
Your tariff will be available 18 дней осталось
```

Help output:

```
> ./yota.py -h
usage: yota.py [-h] [-t {300,350,400,450,500,550,600,650,700,750,800,850,900}]
               [-s]

Script to change yota tariff or show one (It shows tariff price not speed)

optional arguments:
  -h, --help            show this help message and exit
  -t {300,350,400,450,500,550,600,650,700,750,800,850,900}, --tariff {300,350,400,450,500,550,600,650,700,750,800,850,900}
                        Tariff to set for yota in rubles
  -s, --show            Show the current tariff in rubles
  -l, --long            Show how long your paid tariff will be available

```
