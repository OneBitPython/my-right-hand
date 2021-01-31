from tkinter import *
import tkinter.scrolledtext as st
import wikipedia
from Get_image import find_image, download
from PIL import ImageTk, Image


def Console(text):
    print("Please wait as I open a window for you.")
    result = wikipedia.summary(text, sentences=10, auto_suggest=False)
    link = wikipedia.page(text, auto_suggest=False)
    urls = link.url
    search = wikipedia.search(text)
    print(link)
    print(urls)
    print(search)

    img = find_image(text)
    if img == '':
        root = Tk()
        root.title("Info Console")
        root.geometry('400x950')
        root.configure(bg='RoyalBlue3')


        head = Label(root, text="Info Console", foreground='white', background='RoyalBlue3', font=("Arial", 38))
        head.place(x=10, y=0)

        square1 = Canvas(root, width=350, height=300, bg='white')
        square1.place(x=25, y=100)

        topic = Label(root, text=text, foreground='white', background='RoyalBlue3', font=("Arial", 15))
        topic.place(x=20, y=420)

        square2 = Canvas(root, width=350, height=450, bg='white')
        square2.place(x=25, y=450)

        # Creating scrolled text area
        # widget with Read only by
        # disabling the state
        text_area = st.ScrolledText(root,
                                    width=33,
                                    height=20,
                                    font=("Times New Roman",
                                          15))

        text_area.grid(column=0, pady=450, padx=25)

        # Inserting Text which is read only
        text_area.insert(INSERT, result)

        # Making the text read only
        text_area.configure(state='disabled')

        root.mainloop()



    else:
        download(img)

        root = Tk()
        root.title("Info Console")
        root.geometry('400x950')
        root.configure(bg='RoyalBlue3')

        head = Label(root, text="Info Console", foreground='white', background='RoyalBlue3', font=("Arial", 38))
        head.place(x=10, y=0)

        square1 = Canvas(root, width=350, height=300, bg='white')
        square1.place(x=25, y=100)

        img = Image.open('img.jpg')
        image = img.resize((350, 300), Image.ANTIALIAS)
        my_img = ImageTk.PhotoImage(image)

        topic = Label(root, text=text, foreground='white', background='RoyalBlue3', font=("Arial", 15))
        topic.place(x=20, y=420)

        square1.create_image(0, 0, anchor=NW, image=my_img)

        square2 = Canvas(root, width=350, height=450, bg='white')
        square2.place(x=25, y=450)

        # Creating scrolled text area
        # widget with Read only by
        # disabling the state
        text_area = st.ScrolledText(root,
                                    width=33,
                                    height=20,
                                    font=("Times New Roman",
                                          15))

        text_area.grid(column=0, pady=450, padx=25)

        # Inserting Text which is read only
        text_area.insert(INSERT, result)

        # Making the text read only
        text_area.configure(state='disabled')

        root.after(30000, lambda: root.destroy())

        root.mainloop()

