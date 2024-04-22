import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from googletrans import Translator
from tkinter import messagebox
from gtts import gTTS
import os
import speech_recognition as spr
import pandas as pd
from tkinter import filedialog
import subprocess

# Function to handle file upload and conversion
def convert_excel_to_csv():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xls *.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            csv_file_path = file_path.replace('.xls', '.csv')
            csv_file_path = csv_file_path.replace('.xlsx', '.csv')
            df.to_csv(csv_file_path, index=False, encoding='utf-8')  # Specify encoding
            messagebox.showinfo('File Conversion', f'File converted to CSV: {csv_file_path}')
        except Exception as e:
            messagebox.showerror('File Conversion Error', f'Error converting the file: {str(e)}')

# Function to translate text
def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang).text
    return translation

# Function to run another Python program
def run_another_program():
    program_path = r'C:\\Users\\Nithint\\Desktop\\TRANSLATOR\\fileTrans.py'
    subprocess.Popen(['python', program_path], shell=True)

# Declare a variable to store the last selected path
last_save_path = ""

# ---------------------------------------------------Language Translator--------------------------------------------------------------
# UI is developed using Tkinter library
root = tk.Tk()
root.title('Language Translator')
root.geometry('1060x660')
root.maxsize(1060, 660)
root.minsize(1060, 660)
# Background color
root.configure(bg='#dadada')

# Tittle bar icon image used in Tkinter GUI
title_bar_icon = PhotoImage(file="resources/icons/translation.png")
root.iconphoto(False, title_bar_icon)
cl = ''
output = ''

# Heading
heading_label = Label(root, text="Deduce Language Translator", font=('Corbel', 30, 'bold'), bg='#dadada')
heading_label.place(x=283, y=30)

# For Performing Main Translation Function
def translate():
    language_1 = t1.get("1.0", "end-1c")
    global cl
    cl = choose_langauge.get()

    if language_1 == '':
        messagebox.showerror('Language Translator', 'Please fill the Text Box for Translation')
    else:
        t2.delete(1.0, 'end')
        translator = Translator()
        global output
        output = translator.translate(language_1, dest=cl)
        output = output.text
        t2.insert('end', output)

# combobox for from-language selection
a = tk.StringVar()
auto_detect = ttk.Combobox(root, width=20, textvariable=a, state='readonly', font=('Corbel', 20, 'bold'))
auto_detect['values'] = (
    'Choose Language',
    'Bengali',
    'English',
    'Gujarati',
    'Hindi',
    'Kannada',
    'Malayalam',
    'Marathi',
    'Odia',
    'Punjabi',
    'Tamil',
    'Telugu',
    'Urdu',
)

auto_detect.place(x=50, y=140)
auto_detect.current(0)
l = tk.StringVar()

# combobox for to-language selection
choose_langauge = ttk.Combobox(root, width=20, textvariable=l, state='readonly', font=('Corbel', 20, 'bold'))
choose_langauge['values'] = (
    'Choose Language',
    'Bengali',
    'English',
    'Gujarati',
    'Hindi',
    'Kannada',
    'Malayalam',
    'Marathi',
    'Odia',
    'Punjabi',
    'Tamil',
    'Telugu',
    'Urdu',
)

choose_langauge.place(x=600, y=140)
choose_langauge.current(0)

# Load and resize the icon images for buttons
translate_text_icon_img = Image.open("resources/icons/documents.png")
resized_translate_text_icon = translate_text_icon_img.resize((32, 32), Image.Resampling.LANCZOS)
translate_text_icon = ImageTk.PhotoImage(resized_translate_text_icon)

# Load and resize the icon images for buttons
translate_text_icon_img1 = Image.open("resources/icons/icons8.png")
resized_translate_text_icon1 = translate_text_icon_img1.resize((32, 32), Image.Resampling.LANCZOS)
translate_text_icon1 = ImageTk.PhotoImage(resized_translate_text_icon1)

# Load and resize the icon images for buttons
translate_text_icon_img2 = Image.open("resources/icons/xltocsv.png")
resized_translate_text_icon2 = translate_text_icon_img2.resize((32, 32), Image.Resampling.LANCZOS)
translate_text_icon2 = ImageTk.PhotoImage(resized_translate_text_icon2)

# Load and resize the icon image
translate_text_icon_img3 = Image.open("resources/icons/Deduce.png")
resized_translate_text_icon3 = translate_text_icon_img3.resize((200, 45), Image.LANCZOS)
translate_text_icon3 = ImageTk.PhotoImage(resized_translate_text_icon3)

# Create a Label widget to display the image
image_label = tk.Label(root, image=translate_text_icon3, bg='#ffffff')
image_label.place(x=50, y=30)  # Adjust the x and y coordinates to move the image

# Load and resize the icon image
translate_text_icon_img4 = Image.open("resources/icons/translate.png")
resized_translate_text_icon4 = translate_text_icon_img4.resize((140, 80), Image.LANCZOS)
translate_text_icon4 = ImageTk.PhotoImage(resized_translate_text_icon4)

# Create a Label widget to display the image
image_label = tk.Label(root, image=translate_text_icon4, bg='#dadada')
image_label.place(x=850, y=20)  # Adjust the x and y coordinates to move the image

# Text Widget settings used in Tkinter GUI
t1 = Text(root, width=45, height=13, borderwidth=0, relief=RIDGE, font=('Calibri', 16))
t1.place(x=20, y=200)
t2 = Text(root, width=45, height=13, borderwidth=0, relief=RIDGE, font=('Calibri', 16))
t2.place(x=550, y=200)

# Button settings used in Tkinter GUI
translate_button = Button(root, text="Translate Text", image=translate_text_icon, compound="right", relief=RIDGE,
                          borderwidth=0, font=('Corbel', 15, 'bold'), cursor="hand2",
                          command=translate, bg="#ffffff")
translate_button.place(x=20, y=565)

# Create a button for downloading the translated data
download_button = tk.Button(root, text='Run File', image=translate_text_icon1, compound="right", relief=RIDGE,
                            borderwidth=0,
                            font=('Corbel', 15, 'bold'), cursor='hand2', command=run_another_program, bg='#ffffff')
download_button.place(x=200, y=565)

# # Create a button for Excel to CSV conversion
# convert_button = Button(root, text="xls to csv", image=translate_text_icon2, compound="right", relief=RIDGE,
#                         borderwidth=0, font=('Corbel', 15, 'bold'),
#                         cursor="hand2", command=convert_excel_to_csv, bg="#ffffff")
# convert_button.place(x=550, y=565)

root.mainloop()