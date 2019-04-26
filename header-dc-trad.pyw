#!/usr/bin/python3
# -*-coding:utf-8 -*
# import io
import io
from PIL import Image, ImageTk  # pip install pillow
import tkinter as tk
from tkinter import font as tkfont  # python 3
import urllib.request as urllib2
import urllib.error
from bs4 import BeautifulSoup
import webbrowser

dctradpage = 'http://www.dctrad.fr/index.php'
cat_img_urls = [
    'http://www.dctrad.fr/images/icons/forum/RebirthK.png',
    'http://www.dctrad.fr//images/icons/forum/dccomicsv2.png',
    'http://www.dctrad.fr//images/icons/forum/IconindiedctK.png',
    'http://www.dctrad.fr/images/icons/forum/MarvelK.png']
refresh_logo_url = 'http://icons.iconarchive.com/icons/graphicloads/' \
                    '100-flat-2/128/arrow-refresh-4-icon.png'
# shared lists
urllist = list()
photo = list()
cat_image_list = list()


# image from url
def imagefromurl(url):
    try:
        bytes = urllib2.urlopen(url).read()
    except urllib.error.HTTPError as e:
        print("Http error in imagefromurl")
        print (e.fp.read())
        return
    try:
        stream = io.BytesIO(bytes)
    except IOError as e:
        print(e)
        return
    try:
        pil_image = Image.open(stream)
        return pil_image
    except Exception:
        print("Error Image.open in imagefromurl")


# Open url
def OpenUrl(url):
    # webbrowser.open_new(url)
    webbrowser.open(url, new=0, autoraise=False)
    return


# Get html from url
def returnHTML(url):
    hdr = {'Accept': 'text/html', 'User-Agent': "Fiddler"}
    req = urllib2.Request(url, headers=hdr)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print (e.fp.read())
    html = response.read()
    return html


# Get inner html from tag
def getTagData(html, tag, classname):
    soup = BeautifulSoup(html, 'html.parser')
    # prettysoup = soup.prettify()
    list = soup.find_all(tag, class_=classname)
    return list


# Find all 'tag' in html
def getAllTag(html, tag):
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.find_all(tag)
    return list


# Make images from covers
def getCatCovers():
    # Catégories images
    global cat_image_list
    del cat_image_list[:]
    for cat in cat_img_urls:
        cat_image_list.append(ImageTk.PhotoImage(imagefromurl(cat)))
    return cat_image_list


# Make images from images urls
def getHeaderCovers(imgurllist):
    # Catégories images
    global photo
    del photo[:]
    for url in imgurllist:
        photo.append(ImageTk.PhotoImage(imagefromurl(url)))
    return


# Get publication posts urls
def getUrls(comicslist):
    global urllist
    del urllist[:]
    for a in comicslist:
        if a.has_attr('href'):
            urllist.append(a['href'])
    return


# Refresh images and urls in the header
def refresh(comicslist):
    coverimgurllist = list()
    html = returnHTML(dctradpage)
    soup = BeautifulSoup(html, 'html.parser')
    # headerlist = soup.find_all('span', class_="btn-cover")
    comicslist = soup.select('span.btn-cover a')
    coverlist = soup.select('span.btn-cover img')
    for img in coverlist:
        coverimgurllist.append(img['src'])
    getHeaderCovers(coverimgurllist)
    getUrls(comicslist)
    return


class DCTradapp(tk.Tk):
    global cat_image_list

    def __init__(self, *args, **kwargs):
        logo = False
        html = returnHTML(dctradpage)
        soup = BeautifulSoup(html, 'html.parser')
        # headerlist = soup.find_all('span', class_="btn-cover")
        comicslist = soup.select('span.btn-cover a')
        # coverlist = soup.select('span.btn-cover img')

        tk.Tk.__init__(self, *args, **kwargs)
        self.configure(background='SteelBlue3')
        self.title("Header DC trad")
        self.title_font = tkfont.Font(
                family='Helvetica', size=18, weight="bold", slant="italic")
        cat_image_list = getCatCovers()
        # getHeaderCovers()
        refresh(comicslist)
        # sidebar
        try:
            cat_image_list.append(
                    ImageTk.PhotoImage(imagefromurl(refresh_logo_url)))
            logo = True
        except Exception:
            logo = False

        sidebar = tk.Frame(
                self, width=200, bg='SteelBlue4', height=500,
                relief='groove', borderwidth=1)
        sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        button1 = tk.Button(
                sidebar, image=cat_image_list[0], bg='SteelBlue4',
                relief='flat', command=lambda: self.show_frame("DCRebirth"))
        button2 = tk.Button(
                sidebar, image=cat_image_list[1], bg='SteelBlue4',
                relief='flat', command=lambda: self.show_frame("DCPage"))
        button3 = tk.Button(
                sidebar, image=cat_image_list[2], bg='SteelBlue4',
                relief='flat', command=lambda: self.show_frame("Indes"))
        button4 = tk.Button(
                sidebar, image=cat_image_list[3], bg='SteelBlue4',
                relief='flat', command=lambda: self.show_frame("Marvel"))
        if logo:
            button5 = tk.Button(
                    sidebar, image=cat_image_list[4], bg='SteelBlue4',
                    relief='flat', command=refresh(comicslist))
        else:
            button5 = tk.Button(sidebar, text="Rafraîchir",
                                command=refresh(comicslist))

        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack(side='bottom')

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg='SteelBlue3', width=400, height=500)
        container.pack(expand=True, fill='both', side='right', padx=20)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["DCRebirth"] = DCRebirth(parent=container, controller=self)
        self.frames["DCPage"] = DCPage(parent=container, controller=self)
        self.frames["Indes"] = Indes(parent=container, controller=self)
        self.frames["Marvel"] = Marvel(parent=container, controller=self)

        self.frames["DCRebirth"].grid(row=0, column=0, sticky="nsew")
        self.frames["DCPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["Indes"].grid(row=0, column=0, sticky="nsew")
        self.frames["Marvel"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("DCRebirth")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class DCRebirth(tk.Frame):
    def __init__(self, parent, controller):
        global photo
        tk.Frame.__init__(self, parent)
        self.controller = controller
        coverA1 = tk.Button(
                self, image=photo[0], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[0]))
        coverA1.grid(row=0, column=0)
        coverA2 = tk.Button(
                self, image=photo[1], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[1]))
        coverA2.grid(row=0, column=1)
        coverA3 = tk.Button(
                self, image=photo[2], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[2]))
        coverA3.grid(row=0, column=2)
        coverA4 = tk.Button(
                self, image=photo[3], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[3]))
        coverA4.grid(row=1, column=0)
        coverA5 = tk.Button(
                self, image=photo[4], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[4]))
        coverA5.grid(row=1, column=1)
        coverA6 = tk.Button(
                self, image=photo[5], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[5]))
        coverA6.grid(row=1, column=2)
        coverA7 = tk.Button(
                self, image=photo[6], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[6]))
        coverA7.grid(row=2, column=0)
        coverA8 = tk.Button(
                self, image=photo[7], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[7]))
        coverA8.grid(row=2, column=1)
        coverA9 = tk.Button(
                self, image=photo[8], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[8]))
        coverA9.grid(row=2, column=2)


class DCPage(tk.Frame):
    def __init__(self, parent, controller):
        global photo
        tk.Frame.__init__(self, parent)
        self.controller = controller
        coverA1 = tk.Button(
                self, image=photo[10], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[10]))
        coverA1.grid(row=0, column=0)
        coverA2 = tk.Button(
                self, image=photo[11], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[11]))
        coverA2.grid(row=0, column=1)
        coverA3 = tk.Button(
                self, image=photo[12], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[12]))
        coverA3.grid(row=0, column=2)
        coverA4 = tk.Button(
                self, image=photo[13], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[13]))
        coverA4.grid(row=1, column=0)
        coverA5 = tk.Button(
                self, image=photo[14], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[14]))
        coverA5.grid(row=1, column=1)
        coverA6 = tk.Button(
                self, image=photo[15], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[15]))
        coverA6.grid(row=1, column=2)
        coverA7 = tk.Button(
                self, image=photo[16], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[16]))
        coverA7.grid(row=2, column=0)
        coverA8 = tk.Button(
                self, image=photo[17], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[17]))
        coverA8.grid(row=2, column=1)
        coverA9 = tk.Button(
                self, image=photo[18], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[18]))
        coverA9.grid(row=2, column=2)


class Indes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        coverA1 = tk.Button(
                self, image=photo[20], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[20]))
        coverA1.grid(row=0, column=0)
        coverA2 = tk.Button(
                self, image=photo[21], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[21]))
        coverA2.grid(row=0, column=1)
        coverA3 = tk.Button(
                self, image=photo[22], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[22]))
        coverA3.grid(row=0, column=2)
        coverA4 = tk.Button(
                self, image=photo[23], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[23]))
        coverA4.grid(row=1, column=0)
        coverA5 = tk.Button(
                self, image=photo[24], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[24]))
        coverA5.grid(row=1, column=1)
        coverA6 = tk.Button(
                self, image=photo[25], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[25]))
        coverA6.grid(row=1, column=2)
        coverA7 = tk.Button(
                self, image=photo[26], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[26]))
        coverA7.grid(row=2, column=0)
        coverA8 = tk.Button(
                self, image=photo[27], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[27]))
        coverA8.grid(row=2, column=1)
        coverA9 = tk.Button(
                self, image=photo[28], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[28]))
        coverA9.grid(row=2, column=2)


class Marvel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        coverA1 = tk.Button(
                self, image=photo[30], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[30]))
        coverA1.grid(row=0, column=0)
        coverA2 = tk.Button(
                self, image=photo[31], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[31]))
        coverA2.grid(row=0, column=1)
        coverA3 = tk.Button(
                self, image=photo[32], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[32]))
        coverA3.grid(row=0, column=2)
        coverA4 = tk.Button(
                self, image=photo[33], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[33]))
        coverA4.grid(row=1, column=0)
        coverA5 = tk.Button(
                self, image=photo[34], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[34]))
        coverA5.grid(row=1, column=1)
        coverA6 = tk.Button(
                self, image=photo[35], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[35]))
        coverA6.grid(row=1, column=2)
        coverA7 = tk.Button(
                self, image=photo[36], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[36]))
        coverA7.grid(row=2, column=0)
        coverA8 = tk.Button(
                self, image=photo[37], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[37]))
        coverA8.grid(row=2, column=1)
        coverA9 = tk.Button(
                self, image=photo[38], bg='SteelBlue3', relief='flat',
                command=lambda: OpenUrl(urllist[38]))
        coverA9.grid(row=2, column=2)


if __name__ == "__main__":
    app = DCTradapp()
    app.mainloop()
