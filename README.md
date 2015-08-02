# Yota Client

Script to change yota tariff or show one (It shows tariff price not speed)

## How does it work?

Get your current tariff:

```
> ./yota.py -t
Your tariff is 500
```

Сhange current triff to 300:

```
> ./yota.py -s 300
```

Help output:

```
> ./yota.py -h
usage: yota.py [-h] [-s {300,350,400,450,500,550,600,650,700,750,800,850,900}]
               [-t]
 
Script to change yota tariff or show one (It shows tariff price not speed)
 
optional arguments:
  -h, --help            show this help message and exit
  -s {300,350,400,450,500,550,600,650,700,750,800,850,900}, --speed {300,350,400,450,500,550,600,650,700,750,800,850,900}
                        Speed to set for yota in rubles
  -t, --tariff          Show the current tariff in rubles
```
