from tkinter import Button, PhotoImage, Label, Tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt


YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
BUTTON_FONT = (FONT_NAME, 12, 'normal')


def upload_file():
    f_types = [("JPG", "*.jpg"), ("PNG", "*.png")]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)
    img2 = Image.open(filename)
    draw = ImageDraw.Draw(img2)
    #
    # # add watermark
    draw.text((50, 50), "puppy", fill=(0, 0, 0), anchor='ms')
    img = PhotoImage(draw)

    e1 = Label()
    e1.grid(row=3, column=1)
    e1.image = img
    e1["image"] = img



window = Tk()
window.config(padx=50, pady=50, bg=YELLOW)
window.minsize(500, 300)
window.maxsize(800, 600)
window.title("Image Watermarking")


# Labels
label_1 = Label(text="Upload Image", width=50, font=BUTTON_FONT, bg=YELLOW)
label_1.grid(row=1, column=2, columnspan=4)


# Button
upload_button = Button(text="Upload Image", width=40, command=lambda: upload_file())
upload_button.grid(row=2, column=2, columnspan=4)




window.mainloop()
