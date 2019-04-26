#!/usr/bin/python3
# -*-coding:utf-8 -*-
import sys
import os
from utils import getcomics
import tkinter as tk
import tkinter.messagebox as msg
import sqlite3
import threading

exit_thread = False
exit_success = False


class Std_redirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        if not exit_thread:
            self.widget.insert(tk.END, string)
            self.widget.see(tk.END)

    def flush(self):
        pass


# Our comicsList
class MyComicsList(tk.Tk):
    def __init__(self, comic=None):
        super().__init__()

        # List MyComicsList[] initialisation
        if not comic:
            self.comic = []
        else:
            self.comic = comic

        w = 300  # width for the Tk
        h = 600  # height for the Tk
        # Get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # Calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        longtext = "Ajoutez ou supprimez les séries à chercher dans " \
            "les derniers posts \n\"Weekly\" de Getcomics.info"
        # ascii_dctrad = """
# ██████╗  ██████╗    ████████╗██████╗  █████╗ ██████╗
# ██╔══██╗██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗
# ██║  ██║██║            ██║   ██████╔╝███████║██║  ██║
# ██║  ██║██║            ██║   ██╔══██╗██╔══██║██║  ██║
# ██████╔╝╚██████╗       ██║   ██║  ██║██║  ██║██████╔╝
# ╚═════╝  ╚═════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ """
        ascii_title = """
██████╗ ███████╗████████╗ ██████╗ ██████╗ ███╗   ███╗██╗ ██████╗███████╗
██╔════╝ ██╔════╝╚══██╔══╝██╔════╝██╔═══██╗████╗ ████║██║██╔════╝██╔════╝
██║  ███╗█████╗     ██║   ██║     ██║   ██║██╔████╔██║██║██║     ███████╗
██║   ██║██╔══╝     ██║   ██║     ██║   ██║██║╚██╔╝██║██║██║     ╚════██║
╚██████╔╝███████╗   ██║   ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║╚██████╗███████║
 ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚═════╝╚══════╝"""

        self.comic_canvas = tk.Canvas(self)
        self.message = tk.Label(
                self, text=longtext, anchor=tk.W, justify=tk.CENTER,
                wraplength=250, font=("Helvetica", 12))
        self.asciititle = tk.Label(
                self, text=ascii_title, anchor=tk.W, justify=tk.LEFT,
                font=("Courier", 4))
        self.comic_frame = tk.Frame(self.comic_canvas)
        self.text_frame = tk.Frame(self)
        self.output_text = tk.Text(self, bg="black", fg="white")
        self.button = tk.Button(
                self, text="Télécharger les comics", command=self.run)
        self.scrollbar = tk.Scrollbar(
                self.comic_canvas, orient="vertical",
                command=self.comic_canvas.yview)
        self.comic_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.title("Télécharger All V2")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.comic_create = tk.Text(
                self.text_frame, height=3, bg="white", fg="black")

        self.asciititle.pack()
        self.message.pack()
        self.comic_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_frame = self.comic_canvas.create_window(
                (0, 0), window=self.comic_frame, anchor="n")

        # self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack()
        self.button.pack()
        self.comic_create.pack()
        self.output_text.pack(side=tk.BOTTOM, fill=tk.X)
        # self.button.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_idletasks()

        # self.comic_create.pack(side=tk.BOTTOM, fill=tk.X)

        self.comic_create.focus_set()

        self.colour_schemes = [
            {"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

        current_comic = self.load_comic()
        for comic in current_comic:
            comic_text = comic[0]
            self.add_comic(None, comic_text, True)

        self.bind("<Return>", self.add_comic)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.comic_canvas.bind("<Configure>", self.comic_width)

    def run(self):
        sys.stdout = Std_redirector(self.output_text)
        current_comic = self.load_comic()
        comicslist = list()
        for row in current_comic:
            comicslist.append(row[0].lower().replace(' ', '-'))
        thread1 = threading.Thread(
                target=getcomics.getWeeklyComics, args=[comicslist])
        thread1.start()

    # add comic - create new button and add comic in the database
    def add_comic(self, event=None, comic_text=None, from_db=False):
        if not comic_text:
            comic_text = self.comic_create.get(1.0, tk.END).strip()

        if len(comic_text) > 0:
            new_comic = tk.Label(self.comic_frame, text=comic_text, pady=10)

            self.set_comic_colour(len(self.comic), new_comic)

            new_comic.bind("<Button-1>", self.remove_comic)
            new_comic.pack(side=tk.TOP, fill=tk.X)

            self.comic.append(new_comic)

            if not from_db:
                self.save_comic(comic_text)

        self.comic_create.delete(1.0, tk.END)

    # remove comic - delete button and remove from database
    def remove_comic(self, event):
        comic = event.widget
        if msg.askyesno(
                "Confirmation de suppressions",
                "Supprimer " + comic.cget("text") + "de la liste ?"):
            self.comic.remove(event.widget)

            delete_comic_query = "DELETE FROM comics_dc WHERE comic=?"
            delete_comic_data = (comic.cget("text"),)
            self.runQuery(delete_comic_query, delete_comic_data)

            event.widget.destroy()

            self.recolour_comic()

    # recursive recolour comics
    def recolour_comic(self):
        for index, comic in enumerate(self.comic):
            self.set_comic_colour(index, comic)

    # recolour comics (odd or even in the list)
    def set_comic_colour(self, position, comic):
        _, comic_style_choice = divmod(position, 2)

        my_scheme_choice = self.colour_schemes[comic_style_choice]

        comic.configure(bg=my_scheme_choice["bg"])
        comic.configure(fg=my_scheme_choice["fg"])

    def on_frame_configure(self, event=None):
        self.comic_canvas.configure(scrollregion=self.comic_canvas.bbox("all"))

    def comic_width(self, event):
        canvas_width = event.width
        self.comic_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def mouse_scroll(self, event):
        if event.delta:
            self.comic_canvas.yview_scroll(-1*(event.delta/120), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.comic_canvas.yview_scroll(move, "units")

    # add new comic in database
    def save_comic(self, comic):
        insert_comic_query = "INSERT INTO comics_dc VALUES (?)"
        insert_comic_data = (comic,)
        self.runQuery(insert_comic_query, insert_comic_data)

    # read database
    def load_comic(self):
        load_comic_query = "SELECT comic FROM comics_dc"
        my_comic = self.runQuery(load_comic_query, receive=True)
        return my_comic

    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect(".comics.db")
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()

    @staticmethod
    def firstTimeDB():
        # Create_tables = "CREATE TABLE comics_dc (comic TEXT)"
        create_table1 = "CREATE TABLE IF NOT EXISTS comics_dc (comic TEXT)"
        MyComicsList.runQuery(create_table1)
        create_table2 = "CREATE TABLE IF NOT EXISTS comics_marvel (comic TEXT)"
        MyComicsList.runQuery(create_table2)
        create_table3 = "CREATE TABLE IF NOT EXISTS comics_indies (comic TEXT)"
        MyComicsList.runQuery(create_table3)
        create_table4 = "CREATE TABLE IF NOT EXISTS comics_image (comic TEXT)"
        MyComicsList.runQuery(create_table4)

        default_comic_data = ("--- Ajoutez vos séries de comics ---",)
        default_dc_query = "INSERT INTO comics_dc VALUES (?)"
        MyComicsList.runQuery(default_dc_query, default_comic_data)
        default_marvel_query = "INSERT INTO comics_marvel VALUES (?)"
        MyComicsList.runQuery(default_marvel_query, default_comic_data)
        default_indie_query = "INSERT INTO comics_indies VALUES (?)"
        MyComicsList.runQuery(default_indie_query, default_comic_data)
        default_image_query = "INSERT INTO comics_image VALUES (?)"
        MyComicsList.runQuery(default_image_query, default_comic_data)

# thread1 = threading.Thread(target=call_gen)


if __name__ == "__main__":
    if not os.path.isfile(".comics.db"):
        MyComicsList.firstTimeDB()
    comicsList = MyComicsList()
    comicsList.mainloop()
