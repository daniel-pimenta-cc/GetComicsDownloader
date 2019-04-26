#!/usr/bin/python3
# -*-coding:utf-8 -*-

from bs4 import BeautifulSoup  # html parser
import requests
import urllib.request
import urllib.error


# Def url 2 soup
def url2soup(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        res.close()
        return soup
    except ValueError as e:
        print("url2soup error")
        print(e)
        raise
    except urllib.error.HTTPError as e:
        print("url2soup error")
        print(e)
        raise
    except Exception as e:
        print(e)
        print("Error in URL -> soup")
        raise


# Get beautiful soup
def html2soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


# Get a lit of all links in input html
def getaALLhref(html, tag):
    urllist = list()
    soup = html2soup(html)
    for link in soup.find_all(tag):
        if link.has_attr('href'):
            urllist.append(link['href'])
    return urllist


# Get href urls based text
def getHrefwithName(liste_a, name):
    urllist = list()
    for a in liste_a:
        if a.has_attr('href') and a.text == name:
            urllist.append(a['href'])
    return urllist
