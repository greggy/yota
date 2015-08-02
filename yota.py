#!/usr/bin/env python

import requests
import ConfigParser
import argparse


TARIFF_CODES = {'300':'POS-MA13-0002', '350':'POS-MA13-0003', '400':'POS-MA13-0004', '450':'POS-MA13-0005', '500':'POS-MA13-0006', '550':'POS-MA13-0007', '600':'POS-MA13-0008', '650':'POS-MA13-0009', '700':'POS-MA13-0010', '750':'POS-MA13-0011', '800':'POS-MA13-0012', '850':'POS-MA13-0013', '900':'POS-MA13-0014'}
AVAILABLE_SPEED = TARIFF_CODES.keys()
AVAILABLE_SPEED.sort()

def get_settings():
    "Get login/password from config"
    cnf = ConfigParser.ConfigParser()
    cnf.readfp(open('.yota.cnf'))
    login = cnf.get('general', 'login')
    password = cnf.get('general', 'password')

    return login, password

def get_args():
    arg_parse = argparse.ArgumentParser(description='Script to change yota tariff or show one (It shows tariff price not speed)')
    arg_parse.add_argument('-s', '--speed', dest='speed', choices=AVAILABLE_SPEED, type=str, help='Speed to set for yota in rubles')
    arg_parse.add_argument('-t', '--tariff', dest='tariff', action="store_true", help='Show the current tariff in rubles')
    args = arg_parse.parse_args()
    return args

def auth_yota(sess):
    auth_url = 'https://login.yota.ru/UI/Login'
    login, password = get_settings()

    payload = {'IDToken1' : login, 'IDToken2' : password, 
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
    for key, value in TARIFF_CODES.iteritems():
        if value == offerCode:
            print 'Your tariff is %s' % key
            break
    else:
        print 'Error. Yota nas not such tariff'
    return


def main():
    args = get_args()

    sess = requests.Session()
    r = auth_yota(sess)
    output = r.text.split('\n')
    product = ''
    offerCode = ''
    for line in output:
        if 'name="product"' in line:
            product = line.split()[3].split('=')[1]
            product = int(product.replace('"', ''))
        if 'name="offerCode"' in line:
            offerCode = line.split()[3].split('=')[1]
            offerCode = offerCode.replace('"', '')

    if args.tariff:
        if offerCode == '':
            print 'Error. Offer code value is empty'

        show_offer(offerCode)
    else:
        if product == '':
            print 'Error. Product value is empty'

        change_offer(sess, product, args.speed)



if __name__ == '__main__':
    main()