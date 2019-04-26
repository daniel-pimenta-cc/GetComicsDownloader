#!/usr/bin/python3
# -*-coding:utf-8 -*-

import unittest
from utils.zpshare import getFileUrl, removetag
from utils import htmlsoup


class TestFonctionGet(unittest.TestCase):

    # Chaque méthode dont le nom commence par 'test_'
    # est un test.
    def test_getFileUrl(self):

        url = "https://www4.zippyshare.com/v/tbiaf4on/file.html"

        soup = htmlsoup.url2soup(url)
        # downButton = soup.select('script[type="text/javascript"]')
        downButton = soup.find('a', id="dlbutton").find_next_sibling().text

        name, out_url = getFileUrl(url, downButton)
        print("--------------------------------------")
        print(name)
        print(out_url)

        # Le test le plus simple est un test d'égalité. On se
        # sert de la méthode assertEqual pour dire que l'on
        # s'attend à ce que les deux éléments soient égaux. Sinon
        # le test échoue.
        # self.assertEqual(myurl, result)

    def test_removetag_1(self):
        print("Test removetag")
        old_name = "Doomsday Clock 09 (of 12) (2019) (Webrip) " \
                   "(The Last Kryptonian-DCP).cbr"

        valid_name = "Doomsday Clock 09 (of 12) (2019).cbr"

        new_name = removetag(old_name)

        self.assertEqual(valid_name, new_name)


# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()
