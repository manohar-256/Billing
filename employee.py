# ==================imports===================
import re
import random
import string
from tkinter import *
from tkinter import messagebox, ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
import db_config
# ============================================

# =============== Helpers ====================
def make_button(parent, relx, rely, w, h, text, command, bg="#CF1E14", fg="#ffffff", font_size=12):
    btn = Button(parent, text=text, command=command, relief="flat", overrelief="flat",
                 activebackground=bg, cursor="hand2", fg=fg, bg=bg,
                 font=f"-family {{Poppins SemiBold}} -size {font_size}", bd=0)
    btn.place(relx=relx, rely=rely, width=w, height=h)
    return btn

def make_entry(parent, relx, rely, w, h, font_size=12, show=None, textvariable=None, vcmd=None):
    entry = Entry(parent, font=f"-family {{Poppins}} -size {font_size}", relief="flat")
    if show: entry.configure(show=show)
    if textvariable: entry.configure(textvariable=textvariable)
    if vcmd: entry.configure(validate="key", validatecommand=vcmd)
    entry.place(relx=relx, rely=rely, width=w, height=h)
    return entry

def make_bg(parent, image_path, w=1366, h=768):
    lbl = Label(parent)
    lbl.place(relx=0, rely=0, width=w, height=h)
    img = PhotoImage(file=image_path)
    lbl.configure(image=img)
    lbl.image = img
    return img

def make_clock(parent, relx=0.9, rely=0.065):
    clock = Label(parent, font="-family {Poppins Light} -size 12", fg="#000000", bg="#ffffff")
    clock.place(relx=relx, rely=rely, width=102, height=36)
    return clock

def db_query(query, params=None, fetch_all=False, fetch_one=False, commit=False):
    conn = db_config.get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params or [])
    result = None
    if fetch_all: result = cur.fetchall()
    elif fetch_one: result = cur.fetchone()
    if commit: conn.commit()
    cur.close()
    conn.close()
    return result

def tick(clock_label):
    clock_label.config(text=strftime("%H:%M:%S %p"))
    clock_label.after(1000, tick, clock_label)

def random_bill_number(length=8):
    chars = string.ascii_letters.upper() + string.digits
    return 'BB' + ''.join(random.choices(chars, k=length - 2))

def valid_phone(phn):
    return bool(re.match(r"[789]\d{9}$", phn))
# ============================================

root = Tk()
root.geometry("1366x768")
root.title("Retail Manager")

user = StringVar()
passwd = StringVar()
cust_name = StringVar()
cust_num = StringVar()
cust_new_bill = StringVar()
cust_search_bill = StringVar()
bill_date = StringVar()

# ============= Data Classes =================
class Item:
    def __init__(self, name, price, qty):
        self.product_name = name
        self.price = price
        self.qty = qty

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()
        self.dictionary.clear()

    def total(self):
        return sum(i.price * i.qty for i in self.items)

    def isEmpty(self):
        return len(self.items) == 0

    def allCart(self):
        self.dictionary.clear()
        for i in self.items:
            if i.product_name in self.dictionary:
                self.dictionary[i.product_name] += i.qty
            else:
                self.dictionary[i.product_name] = i.qty

# ============= Login ========================
def login(Event=None):
    global username
    username = user.get()
    password = passwd.get()
    try:
        results = db_query(
            "SELECT * FROM employee WHERE emp_id = %s AND password = %s",
            [username, password], fetch_all=True
        )
        if results:
            messagebox.showinfo("Login Page", "The login is successful")
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)
            root.withdraw()
            global biller, page2
            biller = Toplevel()
            page2 = bill_window(biller)
            tick(page2.clock)
            biller.protocol("WM_DELETE_WINDOW", exitt)
            biller.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect username or password.")
            page1.entry2.delete(0, END)
    except Exception as e:
        messagebox.showerror("Error", f"Database Error: {e}")

def logout():
    sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=biller)
    if sure:
        biller.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

def exitt():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=biller)
    if sure:
        biller.destroy()
        root.destroy()

class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Retail Manager")
        self.img = make_bg(root, "./images/employee_login.png")
        self.entry1 = make_entry(root, 0.373, 0.273, 374, 24, font_size=10, textvariable=user)
        self.entry2 = make_entry(root, 0.373, 0.384, 374, 24, font_size=10, show="*", textvariable=passwd)
        make_button(root, 0.366, 0.685, 356, 43, "LOGIN", login, bg="#D2463E", font_size=20)

# ============= Bill Window ==================
class bill_window:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Billing System")

        self.cart = Cart()
        self.state = 1

        self.img = make_bg(biller, "./images/bill_window.png")
        Label(biller, text=username, font="-family {Poppins} -size 10", fg="#000000",
              bg="#ffffff", anchor="w").place(relx=0.038, rely=0.055, width=136, height=30)
        self.clock = make_clock(biller)

        self.entry1 = make_entry(biller, 0.509, 0.23, 240, 24, textvariable=cust_name)
        self.entry2 = make_entry(biller, 0.791, 0.23, 240, 24, textvariable=cust_num)
        self.entry3 = make_entry(biller, 0.102, 0.23, 240, 24, textvariable=cust_search_bill)

        make_button(biller, 0.031, 0.104, 76, 23, "Logout", logout)
        make_button(biller, 0.315, 0.234, 76, 23, "Search", self.search_bill)
        make_button(biller, 0.048, 0.885, 86, 25, "Total", self.total_bill, font_size=10)
        make_button(biller, 0.141, 0.885, 84, 25, "Generate", self.gen_bill, font_size=10)
        make_button(biller, 0.230, 0.885, 86, 25, "Clear", self.clear_bill, font_size=10)
        make_button(biller, 0.322, 0.885, 86, 25, "Exit", exitt, font_size=10)
        make_button(biller, 0.098, 0.734, 86, 26, "Add To Cart", self.add_to_cart, font_size=10)
        make_button(biller, 0.194, 0.734, 68, 26, "Remove", self.remove_product, font_size=10)
        make_button(biller, 0.274, 0.734, 84, 26, "Clear", self.clear_selection, font_size=10)

        # Comboboxes for product selection
        text_font = ("Poppins", "8")
        self.combo1 = ttk.Combobox(biller, font="-family {Poppins} -size 8", state="readonly")
        self.combo1.place(relx=0.035, rely=0.408, width=477, height=26)
        self.combo1.option_add("*TCombobox*Listbox.font", text_font)
        self.combo1.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")

        # Load categories
        result1 = db_query("SELECT DISTINCT product_cat FROM raw_inventory", fetch_all=True)
        self.combo1.configure(values=[r[0] for r in result1])

        self.combo2 = ttk.Combobox(biller, font="-family {Poppins} -size 8", state="disabled")
        self.combo2.place(relx=0.035, rely=0.479, width=477, height=26)
        self.combo2.option_add("*TCombobox*Listbox.font", text_font)

        self.combo3 = ttk.Combobox(biller, font="-family {Poppins} -size 8", state="disabled")
        self.combo3.place(relx=0.035, rely=0.551, width=477, height=26)
        self.combo3.option_add("*TCombobox*Listbox.font", text_font)

        self.entry4 = ttk.Entry(biller, font="-family {Poppins} -size 8", foreground="#000000", state="disabled")
        self.entry4.place(relx=0.035, rely=0.629, width=477, height=26)

        self.Scrolledtext1 = tkst.ScrolledText(top, bd=0, font="-family {Podkova} -size 8", state="disabled")
        self.Scrolledtext1.place(relx=0.439, rely=0.586, width=695, height=275)

        # Bill header widgets (created once, reused)
        self.name_message = Text(biller, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.name_message.place(relx=0.514, rely=0.452, width=176, height=30)
        self.name_message.configure(state="disabled")
        self.num_message = Text(biller, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.num_message.place(relx=0.894, rely=0.452, width=90, height=30)
        self.num_message.configure(state="disabled")
        self.bill_message = Text(biller, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.bill_message.place(relx=0.499, rely=0.477, width=176, height=26)
        self.bill_message.configure(state="disabled")
        self.bill_date_message = Text(biller, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.bill_date_message.place(relx=0.852, rely=0.477, width=90, height=26)
        self.bill_date_message.configure(state="disabled")

        self.combo1.bind("<<ComboboxSelected>>", self.get_category)

    def get_category(self, Event):
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        result2 = db_query("SELECT DISTINCT product_subcat FROM raw_inventory WHERE product_cat = %s",
                           [self.combo1.get()], fetch_all=True)
        self.combo2.configure(values=[r[0] for r in result2])
        self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
        self.combo3.configure(state="disabled")

    def get_subcat(self, Event):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        result3 = db_query("SELECT product_name FROM raw_inventory WHERE product_cat = %s AND product_subcat = %s",
                           [self.combo1.get(), self.combo2.get()], fetch_all=True)
        self.combo3.configure(values=[r[0] for r in result3])
        self.combo3.bind("<<ComboboxSelected>>", self.show_qty)
        self.entry4.configure(state="disabled")

    def show_qty(self, Event):
        self.entry4.configure(state="normal")
        if not hasattr(self, 'qty_label'):
            self.qty_label = Label(biller, font="-family {Poppins} -size 8", anchor="w",
                                   bg="#ffffff", fg="#333333")
            self.qty_label.place(relx=0.033, rely=0.664, width=82, height=26)
        results = db_query("SELECT stock FROM raw_inventory WHERE product_name = %s",
                           [self.combo3.get()], fetch_one=True)
        self.qty_label.configure(text=f"In Stock: {results[0]}", fg="#333333")

    def add_to_cart(self):
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)

        # If Total exists, strip it first
        if strr.find('Total') != -1:
            self.Scrolledtext1.delete('1.0', END)
            lines = [l for l in strr.split("\n") if l.strip() and l.find('Total') == -1 and l.find('─') == -1]
            for line in lines:
                self.Scrolledtext1.insert('insert', line + '\n')

        product_name = self.combo3.get()
        if not product_name:
            self.Scrolledtext1.configure(state="disabled")
            return messagebox.showerror("Oops!", "Choose a product.", parent=biller)

        product_qty = self.entry4.get()
        results = db_query("SELECT mrp, stock FROM raw_inventory WHERE product_name = %s",
                           [product_name], fetch_all=True)
        stock, mrp = results[0][1], results[0][0]

        if not product_qty.isdigit():
            self.Scrolledtext1.configure(state="disabled")
            return messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
        if stock - int(product_qty) < 0:
            self.Scrolledtext1.configure(state="disabled")
            return messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)

        sp = mrp * int(product_qty)
        self.cart.add_item(Item(product_name, mrp, int(product_qty)))
        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
        self.Scrolledtext1.insert('insert', bill_text)
        self.Scrolledtext1.configure(state="disabled")

    def remove_product(self):
        if self.cart.isEmpty():
            return messagebox.showerror("Oops!", "Add a product.", parent=biller)

        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)

        # Strip Total lines if present
        lines = [l for l in strr.split("\n") if l.strip() and l.find('Total') == -1 and l.find('─') == -1]

        try:
            self.cart.remove_item()
        except IndexError:
            messagebox.showerror("Oops!", "Cart is empty", parent=biller)
            self.Scrolledtext1.configure(state="disabled")
            return

        lines.pop()  # Remove last product line
        self.Scrolledtext1.delete('1.0', END)
        for line in lines:
            self.Scrolledtext1.insert('insert', line + '\n')
        self.Scrolledtext1.configure(state="disabled")

    def total_bill(self):
        if self.cart.isEmpty():
            return messagebox.showerror("Oops!", "Add a product.", parent=biller)

        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total') == -1:
            divider = "\n\n\n" + ("─" * 61)
            self.Scrolledtext1.insert('insert', divider)
            total = "\nTotal\t\t\t\t\t\t\t\t\t\t\tRs. {}".format(self.cart.total())
            self.Scrolledtext1.insert('insert', total)
            divider2 = "\n" + ("─" * 61)
            self.Scrolledtext1.insert('insert', divider2)
        self.Scrolledtext1.configure(state="disabled")

    def gen_bill(self):
        if self.state != 1:
            return
        if not cust_name.get():
            return messagebox.showerror("Oops!", "Please enter a name.", parent=biller)
        if not cust_num.get():
            return messagebox.showerror("Oops!", "Please enter a number.", parent=biller)
        if not valid_phone(cust_num.get()):
            return messagebox.showerror("Oops!", "Please enter a valid number.", parent=biller)
        if self.cart.isEmpty():
            return messagebox.showerror("Oops!", "Cart is empty.", parent=biller)

        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total') == -1:
            self.total_bill()

        # Fill bill header
        self._set_text(self.name_message, cust_name.get())
        self._set_text(self.num_message, cust_num.get())
        cust_new_bill.set(random_bill_number())
        self._set_text(self.bill_message, cust_new_bill.get())
        bill_date.set(str(date.today()))
        self._set_text(self.bill_date_message, bill_date.get())

        try:
            conn = db_config.get_db_connection()
            curr = conn.cursor()
            curr.execute(
                "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details) VALUES(%s,%s,%s,%s,%s)",
                [cust_new_bill.get(), bill_date.get(), cust_name.get(), cust_num.get(),
                 self.Scrolledtext1.get('1.0', END)]
            )
            conn.commit()

            self.cart.allCart()
            for name, qty in self.cart.dictionary.items():
                curr.execute("UPDATE raw_inventory SET stock = stock - %s WHERE product_name = %s", [qty, name])
                conn.commit()

            curr.close()
            conn.close()
            messagebox.showinfo("Success!!", "Bill Generated", parent=biller)
            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.state = 0
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=biller)

    def _set_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete(1.0, END)
        widget.insert(END, text)
        widget.configure(state="disabled")

    def clear_bill(self):
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        for w in [self.name_message, self.num_message, self.bill_message, self.bill_date_message]:
            w.configure(state="normal")
            w.delete(1.0, END)
            w.configure(state="disabled")
        self.Scrolledtext1.configure(state="normal")
        self.Scrolledtext1.delete(1.0, END)
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1

    def clear_selection(self):
        self.entry4.delete(0, END)
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        if hasattr(self, 'qty_label'):
            self.qty_label.configure(fg="#ffffff")

    def search_bill(self):
        results = db_query("SELECT * FROM bill WHERE bill_no = %s",
                           [cust_search_bill.get().rstrip()], fetch_all=True)
        if results:
            self.clear_bill()
            self._set_text(self.name_message, results[0][2])
            self._set_text(self.num_message, results[0][3])
            self._set_text(self.bill_message, results[0][0])
            self._set_text(self.bill_date_message, results[0][1])
            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")
            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.state = 0
        else:
            messagebox.showerror("Error!!", "Bill not found.", parent=biller)
            self.entry3.delete(0, END)

# ============================================
page1 = login_page(root)
root.bind("<Return>", login)
root.mainloop()