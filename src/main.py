import tkinter as tk
from tkinter import messagebox
import json
import random

class DonationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Donation Management System")

        # Initialize data structures
        self.donors = self.load_data("donors.json")
        self.campaigns = self.load_data("campaigns.json")

        # Create widgets
        self.label = tk.Label(master, text="Welcome to the Donation App")
        self.label.pack(pady=10)

        self.donor_button = tk.Button(master, text="Donor", command=self.donor_page)
        self.donor_button.pack(pady=5)

        self.campaign_button = tk.Button(master, text="Campaign", command=self.campaign_page)
        self.campaign_button.pack(pady=5)

        # Bind the closing event to save data
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_data(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)

    def donor_page(self):
        donor_window = tk.Toplevel(self.master)
        donor_window.title("Donor Page")

        # Sample donor data
        donor_name = f"Donor{len(self.donors) + 1}"
        self.donors.append({"name": donor_name, "donations": []})

        label = tk.Label(donor_window, text=f"Welcome, {donor_name}")
        label.pack(pady=10)

        donate_button = tk.Button(donor_window, text="Donate", command=lambda: self.make_donation(donor_name))
        donate_button.pack(pady=5)

    def campaign_page(self):
        campaign_window = tk.Toplevel(self.master)
        campaign_window.title("Campaign Page")

        # Sample campaign data
        campaign_name = f"Campaign{len(self.campaigns) + 1}"
        self.campaigns.append({"name": campaign_name, "donations": []})

        label = tk.Label(campaign_window, text=f"Welcome to {campaign_name}")
        label.pack(pady=10)

        view_donations_button = tk.Button(campaign_window, text="View Donations", command=lambda: self.view_donations(campaign_name))
        view_donations_button.pack(pady=5)

    def make_donation(self, donor_name):
        amount = random.randint(1, 100)
        campaign = random.choice(self.campaigns)

        # Update data structures
        donor = next((d for d in self.donors if d["name"] == donor_name), None)
        donor["donations"].append({"amount": amount, "campaign": campaign["name"]})

        campaign["donations"].append({"donor": donor_name, "amount": amount})

        messagebox.showinfo("Donation", f"Thank you, {donor_name}, for donating ${amount} to {campaign['name']}.")

    def view_donations(self, campaign_name):
        campaign = next((c for c in self.campaigns if c["name"] == campaign_name), None)

        if campaign:
            donations_text = "\n".join([f"{donation['donor']}: ${donation['amount']}" for donation in campaign["donations"]])
            messagebox.showinfo("Donations", f"Donations for {campaign_name}:\n{donations_text}")
        else:
            messagebox.showwarning("Campaign Not Found", f"{campaign_name} not found.")

    def on_closing(self):
        # Save data before closing the application
        self.save_data(self.donors, "donors.json")
        self.save_data(self.campaigns, "campaigns.json")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DonationApp(root)
    root.mainloop()
