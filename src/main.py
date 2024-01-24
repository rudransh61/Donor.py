import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import json
import requests  # You may need to install the requests library: pip install requests

class DonationManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Donation Management System")
        self.master.geometry("800x600")

        # Password Entry
        self.password_label = tk.Label(self.master, text="Enter Password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.master, show="•")
        self.password_entry.pack(pady=10)

        # API Key Entry
        self.api_key_label = tk.Label(self.master, text="Enter API Key:")
        self.api_key_label.pack(pady=10)

        self.api_key_entry = tk.Entry(self.master, show="•")
        self.api_key_entry.pack(pady=10)

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # Donation Details Frame
        self.donation_frame = tk.Frame(self.master)
        self.donation_frame.pack(pady=10)

        # Donation Text Area
        self.donation_text = tk.Text(self.master, width=80, height=10, wrap=tk.WORD, bg="black", fg="white")
        self.donation_text.pack(pady=10)

        # Insert an empty string into the text area
        self.donation_text.insert(tk.END, "")

        # Terminal Text Area
        self.terminal_text = tk.Text(self.master, width=80, height=5, wrap=tk.WORD, bg="blue", fg="white")
        self.terminal_text.pack(pady=10, fill=tk.X)

        # Update Text Button
        self.update_button = tk.Button(self.master, text="Update Text", command=self.update_terminal_text)
        self.update_button.pack(pady=5)

        # Schedule the update every 15 seconds
        self.schedule_update()

    def login(self):
        password = self.password_entry.get()
        api_key = self.api_key_entry.get()

        # Add your password and API key validation logic here
        if self.validate_credentials(password, api_key):
            self.show_donation_ui()
        else:
            messagebox.showwarning("Login Failed", "Incorrect password or API key. Please try again.")

    def validate_credentials(self, password, api_key):
        # Placeholder logic, replace with your actual authentication mechanism
        return password == "your_password" 

    def show_donation_ui(self):
        # Destroy login-related widgets
        self.password_label.destroy()
        self.password_entry.destroy()
        self.api_key_label.destroy()
        self.api_key_entry.destroy()
        self.login_button.destroy()

        # Donation UI
        self.load_donation_details()

        # Buttons for adding and deleting entries
        add_button = tk.Button(self.master, text="Add Donation", command=self.add_donation)
        add_button.pack(pady=5)

        delete_button = tk.Button(self.master, text="Delete Entry", command=self.delete_entry)
        delete_button.pack(pady=5)

        # Calculate and display total money spent
        total_label = tk.Label(self.master, text="Total Money Spent:")
        total_label.pack(side=tk.LEFT, padx=10)

        self.total_money_label = tk.Label(self.master, text="")
        self.total_money_label.pack(side=tk.LEFT)

        self.calculate_total_money()
        self.update_terminal_text()

    def load_donation_details(self):
        # Load donation details from the file
        try:
            with open("donation_details.json", "r") as file:
                donation_details = json.load(file)
        except FileNotFoundError:
            donation_details = []

        # Display donation details in the text area
        for i, donation in enumerate(donation_details, start=1):
            details_text = f"Serial Number: {i}\nDate Time: {donation['datetime']}\nAmount: ${donation['amount']}\nPlace: {donation['place']}\n\n"
            self.donation_text.insert(tk.END, details_text)

    def add_donation(self):
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
            self.donation_text.insert(tk.END, details_text)

            self.calculate_total_money()
            self.display_terminal_message("Donation added successfully.")
            self.update_terminal_text()
        else:
            self.display_terminal_message("Invalid input. Please enter valid values.")

    def delete_entry(self):
        # Check if there is any selected text
        if not self.donation_text.tag_ranges(tk.SEL):
            self.display_terminal_message("No entry selected for deletion.")
            return

        # Get the selected text and extract the serial number
        selected_text = self.donation_text.get(tk.SEL_FIRST, tk.SEL_LAST)
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
            self.display_terminal_message("Invalid selection. Please select a valid entry to delete.")
            return

        # Save the updated donation details to the file
        with open("donation_details.json", "w") as file:
            json.dump(donation_details, file, indent=2)

        # Clear the text area and display the updated donation details
        self.donation_text.delete("1.0", tk.END)
        self.load_donation_details()

        self.calculate_total_money()
        self.display_terminal_message("Entry deleted successfully.")
        self.update_terminal_text()

    def calculate_total_money(self):
        try:
            with open("donation_details.json", "r") as file:
                donation_details = json.load(file)
        except FileNotFoundError:
            donation_details = []

        total_money = sum(entry["amount"] for entry in donation_details)
        self.total_money_label.config(text=f"${total_money}")

    def display_terminal_message(self, message):
        self.terminal_text.insert(tk.END, f"{message}\n")
        self.terminal_text.see(tk.END)

    def update_terminal_text(self):
        # Read the content of the data file
        try:
            with open("donation_details.json", "r") as file:
                donation_content = file.read()
        except FileNotFoundError:
            donation_content = ""

        # Get the API key from the entry field
        api_key = self.api_key_entry.get()

        # Call the generate_text function from ai.py with both content and API key as arguments
        try:
            from ai import generate_text
            new_text = generate_text(donation_content, api_key)
            self.terminal_text.delete("1.0", tk.END)
            self.terminal_text.insert(tk.END, new_text)
        except ImportError:
            self.terminal_text.insert(tk.END, "Error: Unable to import ai.py\n")

        # Schedule the next update after 15 seconds
        self.master.after(15000, self.update_terminal_text)

    def schedule_update(self):
        # Schedule the first update after 15 seconds
        self.master.after(15000, self.update_terminal_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = DonationManagementSystem(root)
    root.mainloop()
