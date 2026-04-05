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

def random_emp_id(length=7):
    return 'EMP' + ''.join(random.choices(string.digits, k=length - 3))

def valid_phone(phn):
    return bool(re.match(r"[789]\d{9}$", phn))

def valid_aadhar(aad):
    return aad.isdigit() and len(aad) == 12
# ============================================

root = Tk()
root.geometry("1366x768")
root.title("Retail Manager(ADMIN)")
user = StringVar()
passwd = StringVar()

# ============= Login Page ===================
class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Retail Manager(ADMIN)")
        self.img = make_bg(root, "./images/admin_login.png")
        self.entry1 = make_entry(root, 0.373, 0.273, 374, 24, font_size=10, textvariable=user)
        self.entry2 = make_entry(root, 0.373, 0.384, 374, 24, font_size=10, show="*", textvariable=passwd)
        make_button(root, 0.366, 0.685, 356, 43, "LOGIN", self.login, bg="#D2463E", font_size=20)

    def login(self, Event=None):
        username = user.get()
        password = passwd.get()
        try:
            results = db_query(
                "SELECT * FROM employee WHERE emp_id = %s AND password = %s",
                [username, password], fetch_all=True
            )
            if results:
                if results[0][6] == "Admin":
                    messagebox.showinfo("Login Page", "The login is successful.")
                    self.entry1.delete(0, END)
                    self.entry2.delete(0, END)
                    root.withdraw()
                    global adm, page2
                    adm = Toplevel()
                    page2 = Admin_Page(adm)
                    adm.protocol("WM_DELETE_WINDOW", exitt)
                    adm.mainloop()
                else:
                    messagebox.showerror("Oops!!", "You are not an admin.")
            else:
                messagebox.showerror("Error", "Incorrect username or password.")
                self.entry2.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

def exitt():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=root)
    if sure:
        adm.destroy()
        root.destroy()

# ============= Navigation ==================
def inventory():
    adm.withdraw()
    global inv, page3
    inv = Toplevel()
    page3 = Inventory(inv)
    tick(page3.clock)
    inv.protocol("WM_DELETE_WINDOW", exitt)
    inv.mainloop()

def employee():
    adm.withdraw()
    global emp, page5
    emp = Toplevel()
    page5 = Employee(emp)
    tick(page5.clock)
    emp.protocol("WM_DELETE_WINDOW", exitt)
    emp.mainloop()

def invoices():
    adm.withdraw()
    global invoice
    invoice = Toplevel()
    page7 = Invoice(invoice)
    tick(page7.clock)
    invoice.protocol("WM_DELETE_WINDOW", exitt)
    invoice.mainloop()

# ============= Admin Page ===================
class Admin_Page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("ADMIN Mode")
        self.img = make_bg(adm, "./images/admin.png")
        Label(adm, text="ADMIN", font="-family {Poppins} -size 12", fg="#ffffff",
              bg="#FE6B61", anchor="w").place(relx=0.046, rely=0.056, width=62, height=30)
        make_button(adm, 0.035, 0.106, 76, 23, "Logout", self.Logout)
        make_button(adm, 0.14, 0.508, 146, 63, "Inventory", inventory, bg="#ffffff", fg="#333333")
        make_button(adm, 0.338, 0.508, 146, 63, "Employees", employee, bg="#ffffff", fg="#333333")
        make_button(adm, 0.536, 0.508, 146, 63, "Invoices", invoices, bg="#ffffff", fg="#333333")
        make_button(adm, 0.732, 0.508, 146, 63, "About Us", lambda: None, bg="#ffffff", fg="#333333")

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=adm)
        if sure:
            adm.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

# ============= Inventory ====================
class Inventory:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Inventory")
        self.sel = []
        self.img = make_bg(inv, "./images/inventory.png")
        Label(inv, text="ADMIN", font="-family {Poppins} -size 10", fg="#000000",
              bg="#ffffff", anchor="w").place(relx=0.046, rely=0.055, width=136, height=30)
        self.clock = make_clock(inv)
        self.entry1 = make_entry(inv, 0.040, 0.286, 240, 28)
        make_button(inv, 0.229, 0.289, 76, 23, "Search", self.search_product, font_size=10)
        make_button(inv, 0.035, 0.106, 76, 23, "Logout", self.Logout)
        make_button(inv, 0.052, 0.432, 306, 28, "ADD PRODUCT", self.add_product)
        make_button(inv, 0.052, 0.5, 306, 28, "UPDATE PRODUCT", self.update_product)
        make_button(inv, 0.052, 0.57, 306, 28, "DELETE PRODUCT", self.delete_product)
        make_button(inv, 0.135, 0.885, 76, 23, "EXIT", self.Exit)

        self.scrollbarx = Scrollbar(inv, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(inv, orient=VERTICAL)
        self.tree = ttk.Treeview(inv, yscrollcommand=self.scrollbary.set,
                                 xscrollcommand=self.scrollbarx.set, selectmode="extended")
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)
        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        cols = ("Product ID", "Name", "Category", "Sub-Category", "In Stock", "MRP", "Cost Price", "Vendor No.")
        self.tree.configure(columns=cols)
        widths = [80, 260, 100, 120, 80, 80, 80, 100]
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col, anchor=W)
            self.tree.column(f"#{i+1}", stretch=NO, minwidth=0, width=widths[i])
        self.DisplayData()

    def DisplayData(self):
        rows = db_query("SELECT * FROM raw_inventory", fetch_all=True)
        self.tree.delete(*self.tree.get_children())
        for data in rows:
            self.tree.insert("", "end", values=data)

    def search_product(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)
        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Product Id.", parent=inv)
            return
        for search in val:
            if search == to_search:
                self.tree.selection_set(val[val.index(search) - 1])
                self.tree.focus(val[val.index(search) - 1])
                messagebox.showinfo("Success!!", f"Product ID: {self.entry1.get()} found.", parent=inv)
                break
        else:
            messagebox.showerror("Oops!!", f"Product ID: {self.entry1.get()} not found.", parent=inv)

    def on_tree_select(self, Event):
        self.sel = list(self.tree.selection())

    def delete_product(self):
        if not self.sel:
            messagebox.showerror("Error!!", "Please select a product.", parent=inv)
            return
        sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected products?", parent=inv)
        if sure:
            for item_id in self.sel:
                pid = self.tree.item(item_id)["values"][0]
                db_query("DELETE FROM raw_inventory WHERE product_id = %s", [pid], commit=True)
            messagebox.showinfo("Success!!", "Products deleted from database.", parent=inv)
            self.sel.clear()
            self.DisplayData()

    def update_product(self):
        if len(self.sel) == 1:
            global p_update, valll
            p_update = Toplevel()
            page9 = Update_Product(p_update)
            tick(page9.clock)
            p_update.protocol("WM_DELETE_WINDOW", self.ex2)
            valll = list(self.tree.item(self.sel[0])["values"])
            page9.entry1.insert(0, valll[1])
            page9.entry2.insert(0, valll[2])
            page9.entry3.insert(0, valll[4])
            page9.entry4.insert(0, valll[5])
            page9.entry6.insert(0, valll[3])
            page9.entry7.insert(0, valll[6])
            page9.entry8.insert(0, valll[7])
            p_update.mainloop()
        elif len(self.sel) == 0:
            messagebox.showerror("Error", "Please choose a product to update.", parent=inv)
        else:
            messagebox.showerror("Error", "Can only update one product at a time.", parent=inv)

    def add_product(self):
        global p_add, page4
        p_add = Toplevel()
        page4 = add_product(p_add)
        tick(page4.clock)
        p_add.mainloop()

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=inv)
        if sure:
            inv.destroy()
            adm.deiconify()

    def ex2(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=p_update)
        if sure:
            p_update.destroy()
            inv.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=inv)
        if sure:
            inv.destroy()
            adm.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

# ============ Add Product ===================
class add_product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Product")
        self.img = make_bg(p_add, "./images/add_product.png")
        self.clock = make_clock(p_add, relx=0.84)
        r2 = p_add.register(lambda val: val.isdigit() or val == "")
        self.entry1 = make_entry(p_add, 0.132, 0.296, 996, 30)
        self.entry2 = make_entry(p_add, 0.132, 0.413, 374, 30)
        self.entry3 = make_entry(p_add, 0.132, 0.529, 374, 30, vcmd=(r2, "%P"))
        self.entry4 = make_entry(p_add, 0.132, 0.646, 374, 30)
        self.entry6 = make_entry(p_add, 0.527, 0.413, 374, 30)
        self.entry7 = make_entry(p_add, 0.527, 0.529, 374, 30)
        self.entry8 = make_entry(p_add, 0.527, 0.646, 374, 30, vcmd=(r2, "%P"))
        make_button(p_add, 0.408, 0.836, 96, 34, "ADD", self.add, font_size=14)
        make_button(p_add, 0.526, 0.836, 86, 34, "CLEAR", self.clearr, font_size=14)

    def add(self):
        pname, pcat, pqty = self.entry1.get(), self.entry2.get(), self.entry3.get()
        pmrp, psubcat, pcp, pvendor = self.entry4.get(), self.entry6.get(), self.entry7.get(), self.entry8.get()

        if not pname.strip(): return messagebox.showerror("Oops!", "Please enter product name", parent=p_add)
        if not pcat.strip(): return messagebox.showerror("Oops!", "Please enter product category.", parent=p_add)
        if not psubcat.strip(): return messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_add)
        if not pqty: return messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_add)
        if not pcp: return messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_add)
        try: float(pcp)
        except ValueError: return messagebox.showerror("Oops!", "Invalid cost price.", parent=p_add)
        if not pmrp: return messagebox.showerror("Oops!", "Please enter MRP.", parent=p_add)
        try: float(pmrp)
        except ValueError: return messagebox.showerror("Oops!", "Invalid MRP.", parent=p_add)
        if not valid_phone(pvendor): return messagebox.showerror("Oops!", "Invalid phone number.", parent=p_add)

        try:
            db_query("INSERT INTO raw_inventory(product_name, product_cat, product_subcat, stock, mrp, cost_price, vendor_phn) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                     [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp), pvendor], commit=True)
            messagebox.showinfo("Success!!", "Product successfully added in inventory.", parent=p_add)
            p_add.destroy()
            page3.DisplayData()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=p_add)

    def clearr(self):
        for e in [self.entry1, self.entry2, self.entry3, self.entry4, self.entry6, self.entry7, self.entry8]:
            e.delete(0, END)

# =========== Update Product =================
class Update_Product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Update Product")
        self.img = make_bg(p_update, "./images/update_product.png")
        self.clock = make_clock(p_update, relx=0.84)
        r2 = p_update.register(lambda val: val.isdigit() or val == "")
        self.entry1 = make_entry(p_update, 0.132, 0.296, 996, 30)
        self.entry2 = make_entry(p_update, 0.132, 0.413, 374, 30)
        self.entry3 = make_entry(p_update, 0.132, 0.529, 374, 30, vcmd=(r2, "%P"))
        self.entry4 = make_entry(p_update, 0.132, 0.646, 374, 30)
        self.entry6 = make_entry(p_update, 0.527, 0.413, 374, 30)
        self.entry7 = make_entry(p_update, 0.527, 0.529, 374, 30)
        self.entry8 = make_entry(p_update, 0.527, 0.646, 374, 30)
        make_button(p_update, 0.408, 0.836, 96, 34, "UPDATE", self.update, font_size=14)
        make_button(p_update, 0.526, 0.836, 86, 34, "CLEAR", self.clearr, font_size=14)

    def update(self):
        pname, pcat, pqty = self.entry1.get(), self.entry2.get(), self.entry3.get()
        pmrp, psubcat, pcp, pvendor = self.entry4.get(), self.entry6.get(), self.entry7.get(), self.entry8.get()

        if not pname.strip(): return messagebox.showerror("Oops!", "Please enter product name", parent=p_update)
        if not pcat.strip(): return messagebox.showerror("Oops!", "Please enter product category.", parent=p_update)
        if not psubcat.strip(): return messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_update)
        if not pqty: return messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_update)
        if not pcp: return messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_update)
        try: float(pcp)
        except ValueError: return messagebox.showerror("Oops!", "Invalid cost price.", parent=p_update)
        if not pmrp: return messagebox.showerror("Oops!", "Please enter MRP.", parent=p_update)
        try: float(pmrp)
        except ValueError: return messagebox.showerror("Oops!", "Invalid MRP.", parent=p_update)
        if not valid_phone(pvendor): return messagebox.showerror("Oops!", "Invalid phone number.", parent=p_update)

        try:
            db_query("UPDATE raw_inventory SET product_name=%s, product_cat=%s, product_subcat=%s, stock=%s, mrp=%s, cost_price=%s, vendor_phn=%s WHERE product_id=%s",
                     [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp), pvendor, valll[0]], commit=True)
            messagebox.showinfo("Success!!", "Product successfully updated.", parent=p_update)
            valll.clear()
            page3.sel.clear()
            page3.DisplayData()
            p_update.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=p_update)

    def clearr(self):
        for e in [self.entry1, self.entry2, self.entry3, self.entry4, self.entry6, self.entry7, self.entry8]:
            e.delete(0, END)

# =========== Employee Management ============
class Employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Employee Management")
        self.sel = []
        self.img = make_bg(emp, "./images/employee.png")
        Label(emp, text="ADMIN", font="-family {Poppins} -size 10", fg="#000000",
              bg="#ffffff", anchor="w").place(relx=0.046, rely=0.055, width=136, height=30)
        self.clock = make_clock(emp)
        self.entry1 = make_entry(emp, 0.040, 0.286, 240, 28)
        make_button(emp, 0.229, 0.289, 76, 23, "Search", self.search_emp, font_size=10)
        make_button(emp, 0.035, 0.106, 76, 23, "Logout", self.Logout)
        make_button(emp, 0.052, 0.432, 306, 28, "ADD EMPLOYEE", self.add_emp)
        make_button(emp, 0.052, 0.5, 306, 28, "UPDATE EMPLOYEE", self.update_emp)
        make_button(emp, 0.052, 0.57, 306, 28, "DELETE EMPLOYEE", self.delete_emp)
        make_button(emp, 0.135, 0.885, 76, 23, "EXIT", self.Exit)

        self.scrollbarx = Scrollbar(emp, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(emp, orient=VERTICAL)
        self.tree = ttk.Treeview(emp, yscrollcommand=self.scrollbary.set,
                                 xscrollcommand=self.scrollbarx.set, selectmode="extended")
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)
        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        cols = ("Employee ID", "Employee Name", "Contact No.", "Address", "Aadhar No.", "Password", "Designation")
        self.tree.configure(columns=cols)
        widths = [80, 260, 100, 198, 80, 80, 80]
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col, anchor=W)
            self.tree.column(f"#{i+1}", stretch=NO, minwidth=0, width=widths[i])
        self.DisplayData()

    def DisplayData(self):
        rows = db_query("SELECT * FROM employee", fetch_all=True)
        self.tree.delete(*self.tree.get_children())
        for data in rows:
            self.tree.insert("", "end", values=data)

    def search_emp(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)
        to_search = self.entry1.get()
        for search in val:
            if search == to_search:
                self.tree.selection_set(val[val.index(search) - 1])
                self.tree.focus(val[val.index(search) - 1])
                messagebox.showinfo("Success!!", f"Employee ID: {self.entry1.get()} found.", parent=emp)
                break
        else:
            messagebox.showerror("Oops!!", f"Employee ID: {self.entry1.get()} not found.", parent=emp)

    def on_tree_select(self, Event):
        self.sel = list(self.tree.selection())

    def delete_emp(self):
        if not self.sel:
            messagebox.showerror("Error!!", "Please select an employee.", parent=emp)
            return
        sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected employee(s)?", parent=emp)
        if sure:
            for item_id in self.sel:
                eid = self.tree.item(item_id)["values"][0]
                if str(eid) == "EMPAdmin":
                    messagebox.showerror("Error!!", "Cannot delete master admin.", parent=emp)
                    return
                db_query("DELETE FROM employee WHERE emp_id = %s", [eid], commit=True)
            messagebox.showinfo("Success!!", "Employee(s) deleted from database.", parent=emp)
            self.sel.clear()
            self.DisplayData()

    def update_emp(self):
        if len(self.sel) == 1:
            global e_update, vall
            e_update = Toplevel()
            page8 = Update_Employee(e_update)
            tick(page8.clock)
            e_update.protocol("WM_DELETE_WINDOW", self.ex2)
            vall = list(self.tree.item(self.sel[0])["values"])
            page8.entry1.insert(0, vall[1])
            page8.entry2.insert(0, vall[2])
            page8.entry3.insert(0, vall[4])
            page8.entry4.insert(0, vall[6])
            page8.entry5.insert(0, vall[3])
            page8.entry6.insert(0, vall[5])
            e_update.mainloop()
        elif len(self.sel) == 0:
            messagebox.showerror("Error", "Please select an employee to update.", parent=emp)
        else:
            messagebox.showerror("Error", "Can only update one employee at a time.", parent=emp)

    def add_emp(self):
        global e_add
        e_add = Toplevel()
        page6 = add_employee(e_add)
        tick(page6.clock)
        e_add.protocol("WM_DELETE_WINDOW", self.ex)
        e_add.mainloop()

    def ex(self):
        e_add.destroy()
        self.DisplayData()

    def ex2(self):
        e_update.destroy()
        self.DisplayData()

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=emp)
        if sure:
            emp.destroy()
            adm.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=emp)
        if sure:
            emp.destroy()
            adm.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

# =========== Add Employee ===================
class add_employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Employee")
        self.img = make_bg(e_add, "./images/add_employee.png")
        self.clock = make_clock(e_add, relx=0.84)
        r1 = e_add.register(lambda val: val.isdigit() or val == "")
        r2 = e_add.register(lambda val: val.isalpha() or val == "")
        self.entry1 = make_entry(e_add, 0.132, 0.296, 374, 30)
        self.entry2 = make_entry(e_add, 0.132, 0.413, 374, 30, vcmd=(r1, "%P"))
        self.entry3 = make_entry(e_add, 0.132, 0.529, 374, 30, vcmd=(r1, "%P"))
        self.entry4 = make_entry(e_add, 0.527, 0.296, 374, 30, vcmd=(r2, "%P"))
        self.entry5 = make_entry(e_add, 0.527, 0.413, 374, 30)
        self.entry6 = make_entry(e_add, 0.527, 0.529, 374, 30, show="*")
        make_button(e_add, 0.408, 0.836, 96, 34, "ADD", self.add, font_size=14)
        make_button(e_add, 0.526, 0.836, 86, 34, "CLEAR", self.clearr, font_size=14)

    def add(self):
        ename, econtact, eaadhar = self.entry1.get(), self.entry2.get(), self.entry3.get()
        edes, eadd, epass = self.entry4.get(), self.entry5.get(), self.entry6.get()

        if not ename.strip(): return messagebox.showerror("Oops!", "Please enter employee name.", parent=e_add)
        if not valid_phone(econtact): return messagebox.showerror("Oops!", "Invalid phone number.", parent=e_add)
        if not valid_aadhar(eaadhar): return messagebox.showerror("Oops!", "Invalid Aadhar number.", parent=e_add)
        if not edes: return messagebox.showerror("Oops!", "Please enter designation.", parent=e_add)
        if not eadd: return messagebox.showerror("Oops!", "Please enter address.", parent=e_add)
        if not epass: return messagebox.showerror("Oops!", "Please enter a password.", parent=e_add)

        try:
            emp_id = random_emp_id()
            db_query("INSERT INTO employee(emp_id, name, contact_num, address, aadhar_num, password, designation) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                     [emp_id, ename, econtact, eadd, eaadhar, epass, edes], commit=True)
            messagebox.showinfo("Success!!", f"Employee ID: {emp_id} successfully added.", parent=e_add)
            self.clearr()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=e_add)

    def clearr(self):
        for e in [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6]:
            e.delete(0, END)

# =========== Update Employee ================
class Update_Employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Update Employee")
        self.img = make_bg(e_update, "./images/update_employee.png")
        self.clock = make_clock(e_update, relx=0.84)
        r1 = e_update.register(lambda val: val.isdigit() or val == "")
        r2 = e_update.register(lambda val: val.isalpha() or val == "")
        self.entry1 = make_entry(e_update, 0.132, 0.296, 374, 30)
        self.entry2 = make_entry(e_update, 0.132, 0.413, 374, 30, vcmd=(r1, "%P"))
        self.entry3 = make_entry(e_update, 0.132, 0.529, 374, 30, vcmd=(r1, "%P"))
        self.entry4 = make_entry(e_update, 0.527, 0.296, 374, 30, vcmd=(r2, "%P"))
        self.entry5 = make_entry(e_update, 0.527, 0.413, 374, 30)
        self.entry6 = make_entry(e_update, 0.527, 0.529, 374, 30, show="*")
        make_button(e_update, 0.408, 0.836, 96, 34, "UPDATE", self.update, font_size=14)
        make_button(e_update, 0.526, 0.836, 86, 34, "CLEAR", self.clearr, font_size=14)

    def update(self):
        ename, econtact, eaadhar = self.entry1.get(), self.entry2.get(), self.entry3.get()
        edes, eadd, epass = self.entry4.get(), self.entry5.get(), self.entry6.get()

        if not ename.strip(): return messagebox.showerror("Oops!", "Please enter employee name.", parent=e_update)
        if not valid_phone(econtact): return messagebox.showerror("Oops!", "Invalid phone number.", parent=e_update)
        if not valid_aadhar(eaadhar): return messagebox.showerror("Oops!", "Invalid Aadhar number.", parent=e_update)
        if not edes: return messagebox.showerror("Oops!", "Please enter designation.", parent=e_update)
        if not eadd: return messagebox.showerror("Oops!", "Please enter address.", parent=e_update)
        if not epass: return messagebox.showerror("Oops!", "Please enter a password.", parent=e_update)

        try:
            db_query("UPDATE employee SET name=%s, contact_num=%s, address=%s, aadhar_num=%s, password=%s, designation=%s WHERE emp_id=%s",
                     [ename, econtact, eadd, eaadhar, epass, edes, vall[0]], commit=True)
            messagebox.showinfo("Success!!", f"Employee ID: {vall[0]} successfully updated.", parent=e_update)
            vall.clear()
            page5.sel.clear()
            page5.DisplayData()
            e_update.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=e_update)

    def clearr(self):
        for e in [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6]:
            e.delete(0, END)

# ============= Invoices =====================
class Invoice:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Invoices")
        self.sel = []
        self.img = make_bg(invoice, "./images/invoices.png")
        Label(invoice, text="ADMIN", font="-family {Poppins} -size 10", fg="#000000",
              bg="#ffffff", anchor="w").place(relx=0.046, rely=0.055, width=136, height=30)
        self.clock = make_clock(invoice)
        self.entry1 = make_entry(invoice, 0.040, 0.286, 240, 28)
        make_button(invoice, 0.229, 0.289, 76, 23, "Search", self.search_inv, font_size=10)
        make_button(invoice, 0.035, 0.106, 76, 23, "Logout", self.Logout)
        make_button(invoice, 0.052, 0.432, 306, 28, "DELETE INVOICE", self.delete_invoice)
        make_button(invoice, 0.135, 0.885, 76, 23, "EXIT", self.Exit)

        self.scrollbarx = Scrollbar(invoice, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(invoice, orient=VERTICAL)
        self.tree = ttk.Treeview(invoice, yscrollcommand=self.scrollbary.set,
                                 xscrollcommand=self.scrollbarx.set, selectmode="extended")
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.double_tap)
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)
        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        cols = ("Bill Number", "Date", "Customer Name", "Customer Phone No.")
        self.tree.configure(columns=cols)
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col, anchor=W)
            self.tree.column(f"#{i+1}", stretch=NO, minwidth=0, width=219)
        self.DisplayData()

    def DisplayData(self):
        rows = db_query("SELECT bill_no, date, customer_name, customer_no FROM bill", fetch_all=True)
        self.tree.delete(*self.tree.get_children())
        for data in rows:
            self.tree.insert("", "end", values=data)

    def on_tree_select(self, Event):
        self.sel = list(self.tree.selection())

    def double_tap(self, Event):
        item = self.tree.identify('item', Event.x, Event.y)
        if not item:
            return
        global bill_num, bill
        bill_num = self.tree.item(item)['values'][0]
        bill = Toplevel()
        open_bill(bill)
        bill.mainloop()

    def delete_invoice(self):
        if not self.sel:
            messagebox.showerror("Error!!", "Please select an invoice", parent=invoice)
            return
        sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected invoice(s)?", parent=invoice)
        if sure:
            for item_id in self.sel:
                bno = self.tree.item(item_id)["values"][0]
                db_query("DELETE FROM bill WHERE bill_no = %s", [bno], commit=True)
            messagebox.showinfo("Success!!", "Invoice(s) deleted from database.", parent=invoice)
            self.sel.clear()
            self.DisplayData()

    def search_inv(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)
        to_search = self.entry1.get()
        for search in val:
            if search == to_search:
                self.tree.selection_set(val[val.index(search) - 1])
                self.tree.focus(val[val.index(search) - 1])
                messagebox.showinfo("Success!!", f"Bill Number: {self.entry1.get()} found.", parent=invoice)
                break
        else:
            messagebox.showerror("Oops!!", f"Bill Number: {self.entry1.get()} not found.", parent=invoice)

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=invoice)
        if sure:
            invoice.destroy()
            adm.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=invoice)
        if sure:
            invoice.destroy()
            adm.deiconify()

# ============= Open Bill ====================
class open_bill:
    def __init__(self, top=None):
        top.geometry("765x488")
        top.resizable(0, 0)
        top.title("Bill")
        self.img = make_bg(bill, "./images/bill.png", w=765, h=488)

        self.name_message = Text(bill, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.name_message.place(relx=0.178, rely=0.205, width=176, height=30)
        self.num_message = Text(bill, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.num_message.place(relx=0.854, rely=0.205, width=90, height=30)
        self.bill_message = Text(bill, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.bill_message.place(relx=0.150, rely=0.243, width=176, height=26)
        self.bill_date_message = Text(bill, font="-family {Podkova} -size 10", bd=0, bg="#ffffff")
        self.bill_date_message.place(relx=0.780, rely=0.243, width=90, height=26)
        self.Scrolledtext1 = tkst.ScrolledText(top, bd=0, font="-family {Podkova} -size 8", state="disabled")
        self.Scrolledtext1.place(relx=0.044, rely=0.41, width=695, height=284)

        results = db_query("SELECT * FROM bill WHERE bill_no = %s", [bill_num], fetch_all=True)
        if results:
            self.name_message.insert(END, results[0][2])
            self.name_message.configure(state="disabled")
            self.num_message.insert(END, results[0][3])
            self.num_message.configure(state="disabled")
            self.bill_message.insert(END, results[0][0])
            self.bill_message.configure(state="disabled")
            self.bill_date_message.insert(END, results[0][1])
            self.bill_date_message.configure(state="disabled")
            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")

# ============================================
page1 = login_page(root)
root.bind("<Return>", lambda e: page1.login())
root.mainloop()