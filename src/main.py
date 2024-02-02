import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import json
import ai
import os
from dotenv import load_dotenv

def login():
    password = password_entry.get()

    # Add your password and API key validation logic here
    if password == "pass":  # Placeholder for password validation
        show_donation_ui()
    else:
        messagebox.showwarning("Login Failed", "Incorrect password. Please try again.")

def show_donation_ui():
    # Destroy login-related widgets
    password_label.destroy()
    password_entry.destroy()
    login_button.destroy()

    # Donation UI
    load_donation_details()

    # Buttons for adding and deleting entries
    add_button = tk.Button(root, text="Add Donation", command=add_donation)
    add_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Entry", command=delete_entry)
    delete_button.pack(pady=5)

    # Calculate and display total money spent
    total_label = tk.Label(root, text="Total Money Spent:")
    total_label.pack(side=tk.LEFT, padx=10)

    global total_money_label  # Make total_money_label global
    total_money_label = tk.Label(root, text="")
    total_money_label.pack(side=tk.LEFT)

    calculate_total_money()

def load_donation_details():
    # Load donation details from the file
    try:
        with open("donation_details.json", "r") as file:
            donation_details = json.load(file)
    except FileNotFoundError:
        donation_details = []

    # Display donation details in the text area
    for i, donation in enumerate(donation_details, start=1):
        details_text = f"Serial Number: {i}\nDate Time: {donation['datetime']}\nAmount: ${donation['amount']}\nPlace: {donation['place']}\n\n"
        donation_text.insert(tk.END, details_text)

def add_donation():
    amount = simpledialog.askfloat("Amount", "Enter donation amount:")
    place = simpledialog.askstring("Place", "Enter donation place:")

    # Validate input
    if amount is not None and place is not None:
        # Create a new donation entry
        new_donation = {
            "datetime": str(datetime.now()),
            "amount": amount,
            "place": place
        }

        # Save the donation details to the file
        try:
            with open("donation_details.json", "r") as file:
                donation_details = json.load(file)
        except FileNotFoundError:
            donation_details = []

        donation_details.append(new_donation)

        with open("donation_details.json", "w") as file:
            json.dump(donation_details, file, indent=2)

        # Display the new donation in the text area
        details_text = f"Serial Number: {len(donation_details)}\nDate Time: {new_donation['datetime']}\nAmount: ${new_donation['amount']}\nPlace: {new_donation['place']}\n\n"
        donation_text.insert(tk.END, details_text)

        calculate_total_money()

    else:
        pass

def delete_entry():
    # Check if there is any selected text
    if not donation_text.tag_ranges(tk.SEL):
        return

    # Get the selected text and extract the serial number
    selected_text = donation_text.get(tk.SEL_FIRST, tk.SEL_LAST)
    serial_number = selected_text.split('\n')[0].split(': ')[-1]

    # Load donation details from the file
    try:
        with open("donation_details.json", "r") as file:
            donation_details = json.load(file)
    except FileNotFoundError:
        donation_details = []

    # Remove the selected entry
    try:
        donation_details.pop(int(serial_number) - 1)
    except (ValueError, IndexError):
        display_terminal_message("Invalid selection. Please select a valid entry to delete.")
        return

    # Save the updated donation details to the file
    with open("donation_details.json", "w") as file:
        json.dump(donation_details, file, indent=2)

    # Clear the text area and display the updated donation details
    donation_text.delete("1.0", tk.END)
    load_donation_details()

    calculate_total_money()
    

def calculate_total_money():
    try:
        with open("donation_details.json", "r") as file:
            donation_details = json.load(file)
    except FileNotFoundError:
        donation_details = []

    total_money = sum(entry["amount"] for entry in donation_details)
    total_money_label.config(text=f"${total_money}")

def display_terminal_message(message):
    terminal_text.insert(tk.END, f"{message}\n")
    terminal_text.see(tk.END)

def update_terminal_text():
    # Get the API key from the .env file
    load_dotenv() # load .env file
    api_key = os.getenv("API_KEY")

    # Call the generate_text function from ai.py with both content and API key as arguments
    try:
        with open("donation_details.json", "r") as file:
            donation_content = json.load(file)
            new_text = ai.generate_text(donation_content, api_key)
            terminal_text.delete("1.0", tk.END)
            terminal_text.insert(tk.END, new_text)
    except Exception as e:
        terminal_text.insert(tk.END, f"Error: {e}\n")

   

# Main Tkinter window
root = tk.Tk()
root.title("Donation Management System")
root.geometry("800x600")

# Password Entry
password_label = tk.Label(root, text="Enter Password:")
password_label.pack(pady=10)

password_entry = tk.Entry(root, show="•")
password_entry.pack(pady=10)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

# Donation Text Area
donation_text = tk.Text(root, width=80, height=10, wrap=tk.WORD, bg="black", fg="white")
donation_text.pack(pady=10)

# Insert an empty string into the text area
donation_text.insert(tk.END, "")

# Terminal Text Area
terminal_text = tk.Text(root, width=80, height=10, wrap=tk.WORD, bg="blue", fg="white")
terminal_text.pack(pady=10, fill=tk.X)

# Update Text Button
update_button = tk.Button(root, text="Get AI help", command=update_terminal_text)
update_button.pack(pady=5)


root.mainloop()
