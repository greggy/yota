#!/usr/bin/env python

import requests
import argparse
from lxml import etree


LOGIN = ''
PASSWORD = ''

TARIFF_CODES = {'300':'POS-MA13-0002', '350':'POS-MA13-0003', '400':'POS-MA13-0004', '450':'POS-MA13-0005', '500':'POS-MA13-0006', '550':'POS-MA13-0007', '600':'POS-MA13-0008', '650':'POS-MA13-0009', '700':'POS-MA13-0010', '750':'POS-MA13-0011', '800':'POS-MA13-0012', '850':'POS-MA13-0013', '900':'POS-MA13-0014'}
AVAILABLE_SPEED = TARIFF_CODES.keys()
AVAILABLE_SPEED.sort()


def get_args():
    arg_parse = argparse.ArgumentParser(description='Script to change yota tariff or show one (It shows tariff price not speed)')
    arg_parse.add_argument('-t', '--tariff', dest='tariff', choices=AVAILABLE_SPEED, type=str, help='Tariff to set for yota in rubles')
    arg_parse.add_argument('-s', '--show', dest='show', action="store_true", help='Show the current tariff in rubles')
    arg_parse.add_argument('-l', '--long', dest='long', action="store_true", help='Show how long your paid tariff will be available')
    args = arg_parse.parse_args()
    return args

def auth_yota(sess):
    auth_url = 'https://login.yota.ru/UI/Login'

    payload = {'IDToken1' : LOGIN, 'IDToken2' : PASSWORD, 
                'goto' : 'https://my.yota.ru/selfcare/loginSuccess', 
                'gotoOnFail' : 'https://my.yota.ru/selfcare/loginError',
                'old-token' : '',
                'org' : 'customer' }
    result = sess.post(auth_url, payload)
    return result

def change_offer(sess, product, speed):
    tariff_url = 'https://my.yota.ru/selfcare/devices/changeOffer'
    tariff_payload = {'product' : product, 'offerCode' : TARIFF_CODES[speed],
                      'homeOfferCode' : '', 'areOffersAvailable' : 'false',
                      'period' : '', 'status' : 'custom',
                      'autoprolong': 0, 'isSlot' : 'false', 'resourceId' : '',
                      'Device' : 1, 'username' : '', 'isDisablingAutoprolong' : 'false'}

    result = sess.post(tariff_url, tariff_payload)
    return result

def show_offer(offerCode):
    if LOGIN == '' or PASSWORD == '':
        return 'Add your credintials in file yota.py'

    ans = None
    for key, value in TARIFF_CODES.iteritems():
        if value == offerCode:
            return 'Your tariff is {0}'.format(key)
    else:
        return 'Error. Yota nas not such tariff'

def get_result(sess, args):
    r = auth_yota(sess)
    ans = None

    try:
        tree = etree.HTML(r.text)
        product = tree.xpath('//div[contains(@id, "product_")]/form/input[1]')[0].get('value')
        offerCode = tree.xpath('//div[contains(@id, "product_")]/form/input[2]')[0].get('value')
        longCode = tree.xpath('//div[contains(@class, "time")]/strong')[0].text
    except IndexError as err:
        print(err)
        ans = 'Error. Your tariff page was broken or changed'
    except Exception as err:
        print(err)
        ans = 'Error. Something goes wrong'
    else:
        if args.show:
            if offerCode == '':
                ans = 'Error. Offer code value is empty'

            ans = show_offer(offerCode)
        elif args.long:
            if longCode == '':
                ans = 'Error. How long your tariff will be on code value is empty'

            add = tree.xpath('//div[contains(@class, "time")]/span')[0].text
            ans = u'Your tariff will be available {0} {1}'.format(longCode, add)
        else:
            if product == '':
                ans = 'Error. Product value is empty'

            rc = change_offer(sess, product, args.tariff)
            ans = 'Error. Your tariff wasn\'t changed'
            if rc.status_code == 200:
                ans = 'Now your tariff is {0}'.format(args.tariff)
    return ans


def main():
    args = get_args()
    sess = requests.Session()
    print(get_result(sess, args))


if __name__ == '__main__':
    main()
