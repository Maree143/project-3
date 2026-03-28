import tkinter as tk
from tkinter import messagebox
import os
import datetime

# Create Bills folder if not exist
if not os.path.exists('Bills'):
    os.mkdir('Bills')

bill_counter_file = "Bills/bill_count.txt"
if not os.path.exists(bill_counter_file):
    with open(bill_counter_file, "w") as f:
        f.write("1000")

def get_next_bill_number():
    with open(bill_counter_file, "r") as f:
        num = int(f.read())
    with open(bill_counter_file, "w") as f:
        f.write(str(num + 1))
    return num

class GroceryBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Billing System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")

        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.discount_percent = tk.DoubleVar()
        self.cart = []
        self.bill_window = None

        self.categories = {
            "Grocery": {
                "Rice": 50, "Sugar": 40, "Salt": 20, "Oil": 150, 
                "Wheat": 45, "Dhal": 70, "Chilli Powder": 80, "Turmeric": 60
            },
            "Snacks": {
                "Chips": 20, "Biscuits": 25, "Chocolate": 10, "Noodles": 35,
                "Popcorn": 30, "Cookies": 40, "Namkeen": 45, "Cake": 50
            },
            "Milk Products": {
                "Milk": 25, "Curd": 30, "Cheese": 80, "Paneer": 90,
                "Butter": 85, "Ghee": 120, "Lassi": 20, "Flavored Milk": 35
            },
            "Drinks": {
                "Water Bottle": 20, "Soda": 25, "Juice": 30, "Soft Drink": 35,
                "Energy Drink": 50, "Lemonade": 25, "Cold Coffee": 40, "Milkshake": 45
            },
            "Vegetables": {
                "Potato": 20, "Tomato": 25, "Onion": 30, "Carrot": 40,
                "Beans": 35, "Cabbage": 30, "Spinach": 20, "Brinjal": 25
            },
            "Fruits": {
                "Apple": 50, "Banana": 10, "Orange": 40, "Mango": 60,
                "Grapes": 45, "Pineapple": 70, "Papaya": 30, "Watermelon": 50
            }
        }
        self.qty_vars = {}

        self.show_login()

    def show_login(self):
        self.clear_window()
        login_frame = tk.Frame(self.root, bg="#dbeafe", bd=2, relief=tk.RIDGE)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_frame, text="Customer Details", font=("Arial Bold", 18), bg="#dbeafe", fg="#1e3a8a").grid(row=0, columnspan=2, pady=20)
        tk.Label(login_frame, text="Name:", font=("Arial", 14), bg="#dbeafe").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(login_frame, textvariable=self.customer_name, font=("Arial", 12)).grid(row=1, column=1, padx=10)

        tk.Label(login_frame, text="Phone:", font=("Arial", 14), bg="#dbeafe").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(login_frame, textvariable=self.customer_phone, font=("Arial", 12)).grid(row=2, column=1, padx=10)

        tk.Button(login_frame, text="Continue", font=("Arial", 12, "bold"), bg="#3b82f6", fg="white", command=self.show_main_app).grid(row=3, columnspan=2, pady=20)

    def show_main_app(self):
        if not self.customer_name.get() or not self.customer_phone.get():
            messagebox.showwarning("Missing Info", "Please enter customer name and phone.")
            return
        self.clear_window()

        bill_frame = tk.Frame(self.root, bg="#93c5fd", pady=10)
        bill_frame.pack(fill="x")
        tk.Label(bill_frame, text=f"Welcome {self.customer_name.get()} | Phone: {self.customer_phone.get()}", font=("Arial", 16, "bold"), bg="#93c5fd", fg="#1e40af").pack()

        discount_frame = tk.Frame(self.root, bg="#f0f2f5")
        discount_frame.pack(pady=10)
        tk.Label(discount_frame, text="Discount (%):", font=("Arial", 12, "bold"), bg="#f0f2f5").pack(side=tk.LEFT)
        tk.Entry(discount_frame, textvariable=self.discount_percent, width=5, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

        self.canvas_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#f0f2f5")
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f2f5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        for category, items in self.categories.items():
            cat_frame = tk.LabelFrame(self.scrollable_frame, text=category, font=("Arial", 14, "bold"), bg="#dbeafe", padx=10, pady=5, labelanchor="n")
            cat_frame.pack(fill="x", pady=5, padx=10)

            for idx, (item, price) in enumerate(items.items()):
                if item not in self.qty_vars:
                    self.qty_vars[item] = tk.IntVar()

                item_frame = tk.Frame(cat_frame, bg="#dbeafe")
                item_frame.grid(row=idx//4, column=idx%4, padx=5, pady=5, sticky="w")

                tk.Label(item_frame, text=f"{item}\n(₹{price})", bg="#dbeafe", font=("Arial", 9), width=15, anchor="w").pack()
                tk.Entry(item_frame, textvariable=self.qty_vars[item], width=5, font=("Arial", 10)).pack()

        button_frame = tk.Frame(self.root, pady=10, bg="#f0f2f5")
        button_frame.pack()
        tk.Button(button_frame, text="Generate Bill", command=self.open_bill_page, bg="#16a34a", fg="white", font=("Arial", 12, "bold"), width=15).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Clear", command=self.clear_all, bg="#ef4444", fg="white", font=("Arial", 12, "bold"), width=15).grid(row=0, column=1, padx=10)

    def open_bill_page(self):
        self.cart.clear()
        total = 0
        for category, items in self.categories.items():
            for item, price in items.items():
                qty = self.qty_vars[item].get()
                if qty > 0:
                    line_total = qty * price
                    self.cart.append((item, qty, price, line_total))
                    total += line_total

        if not self.cart:
            messagebox.showwarning("Cart Empty", "No items selected.")
            return

        now = datetime.datetime.now()
        self.bill_num = get_next_bill_number()
        self.cust_code = f"CUST{now.strftime('%Y%m%d')}{self.bill_num}"
        self.date_str = now.strftime("%d-%m-%Y %H:%M")

        self.bill_text = f"Customer Code: {self.cust_code}\n"
        self.bill_text += f"Customer Name: {self.customer_name.get()}\n"
        self.bill_text += f"Phone: {self.customer_phone.get()}\n"
        self.bill_text += f"Date: {self.date_str}\n"
        self.bill_text += f"{'='*70}\n"
        self.bill_text += f"{'Item':<30}{'Qty':<10}{'Price':<10}{'Total'}\n"
        self.bill_text += f"{'-'*70}\n"

        for item, qty, price, line_total in self.cart:
            self.bill_text += f"{item:<30}{qty:<10}{price:<10}{line_total}\n"

        self.bill_text += f"{'-'*70}\n"
        self.bill_text += f"Subtotal: ₹{total:.2f}\n"

        discount = self.discount_percent.get()
        if discount > 0:
            discount_amt = (discount / 100) * total
            total -= discount_amt
            self.bill_text += f"Discount ({discount}%): -₹{discount_amt:.2f}\n"

        self.bill_text += f"Total: ₹{total:.2f}\n"
        self.bill_text += f"{'='*70}\n"

        self.show_bill_window()

    def show_bill_window(self):
        self.bill_window = tk.Toplevel(self.root)
        self.bill_window.title("Generated Bill")
        self.bill_window.geometry("600x600")

        bill_area = tk.Text(self.bill_window, font=("Courier New", 10))
        bill_area.pack(expand=True, fill="both")
        bill_area.insert(tk.END, self.bill_text)
        bill_area.config(state="disabled")

        button_frame = tk.Frame(self.bill_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save Bill", command=self.save_bill, bg="#16a34a", fg="white", width=15, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Back", command=self.bill_window.destroy, bg="#facc15", fg="black", width=15, font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)

    def save_bill(self):
        filename = f"Bills/{self.cust_code}.txt"
        with open(filename, "w") as f:
            f.write(self.bill_text)
        messagebox.showinfo("Bill Saved", f"Bill saved as {filename}")

    def clear_all(self):
        for var in self.qty_vars.values():
            var.set(0)
        self.discount_percent.set(0.0)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryBillingSystem(root)
    root.mainloop()
