#!/usr/bin/env python
# coding=utf-8

import os
from random import choice

from bs4 import BeautifulSoup


def random_choice_cookie():
    cookies = parser_cookies()
    return choice(cookies)


def parser_cookies():
    """
    read cookies file
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies')
    if not os.path.isfile(file_path):
        return None

    f = open(file_path)
    cookies = {}
    for line in f.readline():
        line = line.split(':')
        for i in line:
            name, value = i.strip().split('=', 1)
            cookies[name] = value
    return cookies


def parser_product(content):
    """
    parser search idnex page
    page like: https://list.tmall.com/search_product.htm?q=%C5%AE%D7%B0&type=p&
    vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp.pc_1_searchbutton
    """
    soup = BeautifulSoup(content, 'html.parser', from_encoding='GB18030')
    product = soup.find_all('div', class_='product')

    product_list = []
    for p in product:
        if len(p['class']) != 2:
            continue
        product_info = {}
        product_info['detail'] = 'https:' + p.find('a',class_='productImg')['href']
        product_info['price'] = p.find('p', class_='productPrice').find('em')['title']
        product_info['title'] = p.find('p', class_='productTitle').find('a')['title']
        product_info['shop'] = p.find('div', class_='productShop').find('a').get_text().strip()
        try:
            productStatus = p.find('p', class_='productStatus').find_all('span')
            product_info['deal'] = productStatus[0].find('em').get_text()
            product_info['comment'] = productStatus[1].find('a').get_text()
        except AttributeError:
            product_info['deal'] = None
            product_info['comment'] = None

        img = p.find('a', class_='productImg').find('img')

        if 'data-ks-lazyload' in img.attrs:
            product_info['img'] = img['data-ks-lazyload']
        else:
            product_info['img'] = img['src']

        product_list.append(product_info)
    return product_list


def parser_detail(soup):
    """
    parser detail info from detail page
    """
    attr_info = {}
    attr_list = soup.find('ul', id="J_AttrUL").find_all('li')
    for i in attr_list:
        name, value = i.get_text().split(":")
        attr_info[name] = value
    return attr_info


def parser_info(content):
    """
    parser product detail info
    """
    soup = BeautifulSoup(content, 'html.parser')

    info = {}
    try:
        info['collect_count'] = soup.find('span', id='J_CollectCount').get_text()
    except AttributeError:
        info['collect_count'] = None
    try:
        info['comment_count'] = soup.find('span', class_='tm-count').get_text()
    except AttributeError:
        info['comment_count'] = None

    info['detail'] = parser_detail(soup)
    return info