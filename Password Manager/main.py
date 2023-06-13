from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# --------------------------PASSWORD GENERATOR-------------------- #


def generate_password():
    """Generating Random Password"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q',
               'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letter + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------SAVE PASSWORD------------------------ #


def save():
    """Saving the form details in json file after validating and confirming the info"""
    ans = ''
    website = website_entry.get().strip().title()
    email = email_entry.get()
    password = password_entry.get()
    new_entry = {
        website: {"email": email,
                  "password": password
                  }
    }

    if len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Opps!!", message="You can't leave any field empty")
    else:
        ans = messagebox.askyesnocancel(title="Confirm Entry", message=f"These are details entered:\n\n"
                                                                       f"Website: {website}\nEmail: {email}\nPassword: "
                                                                       f"{password}\n\nProceed?")
    if ans:
        # Writing the info and clearing the form
        try:
            with open("data.json", "r") as f:
                # reading json data
                data = json.load(f)
                # updating json data
                data.update(new_entry)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                # Writing json data
                json.dump(new_entry, f, indent=4)
        else:
            with open("data.json", "w") as f:
                # Writing json data
                json.dump(data, f, indent=4)
        finally:
            # Clearing the form
            website_entry.delete(0, END)
            password_entry.delete(0, END)

    elif ans is None:
        # Clearing Form if user select cancel
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# -------------------------- SEARCH ----------------------------- #
def search():
    website = website_entry.get().strip().title()
    # Validating website entry
    if (website is not None) and (website != ''):
        # Checking if data file exist
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Not Found", message=f"{website} info doesn't exist")
        else:
            if website in data:
                messagebox.showinfo(title=f"Your {website.title()} Info",
                                    message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}")
                pyperclip.copy(data[website]["password"])

            else:
                messagebox.showinfo(title="Not Found", message=f"{website} info doesn't exist")
        finally:
            website_entry.delete(0, END)
    else:
        messagebox.showinfo(title="Opps!", message="Please entry a name in website box")


# --------------------------UI SETUP----------------------------- #


window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=1)

# Labels

add_label = Label()
add_label.grid(row=0, column=1)

website_label = Label(text="Website :", justify="right")
website_label.grid(column=0, row=2, sticky="e")

email_label = Label(text="Email/username :")
email_label.grid(column=0, row=3)

password_label = Label(text="Password :")
password_label.grid(column=0, row=4, sticky="e")

# Buttons

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=4)

add_button = Button(text="Add", width=42, command=save)
add_button.grid(column=1, row=5, columnspan=2)

search_button = Button(text="Search", width=14, command=search)
search_button.grid(row=2, column=2)

# Entries

website_entry = Entry(width=32)
website_entry.focus()
website_entry.grid(column=1, row=2, )

email_entry = Entry(width=50)
email_entry.insert(0, "ikram87388@gmail.com")
email_entry.grid(column=1, row=3, columnspan=2)

password_entry = Entry(width=31)
password_entry.grid(column=1, row=4)

window.mainloop()
