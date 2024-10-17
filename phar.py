import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pymysql


class pharmacy():
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Pharmacy Management System", bd=4, relief="groove", font=("Arial",50,"bold"), bg=self.clr(240,150,200))
        title.pack(side="top", fill="x")

        # global variable
        self.bill = 0

        # add Frame
        
        addFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(200,240,150))
        addFrame.place(width=self.width/3, height=self.height-180, x=20, y=100)

        nameLbl = tk.Label(addFrame, text="Medicine:", bg=self.clr(200,240,150),font=("Arial",15,"bold"))
        nameLbl.grid(row=0, column=0, padx=20, pady=30)
        self.nameIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial",15))
        self.nameIn.grid(row=0, column=1, padx=10, pady=30)

        priceLbl = tk.Label(addFrame, text="Price:", bg=self.clr(200,240,150),font=("Arial",15,"bold"))
        priceLbl.grid(row=1, column=0, padx=20, pady=30)
        self.priceIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial",15))
        self.priceIn.grid(row=1, column=1, padx=10, pady=30)

        quantLbl = tk.Label(addFrame, text="Quantity:", bg=self.clr(200,240,150),font=("Arial",15,"bold"))
        quantLbl.grid(row=2, column=0, padx=20, pady=30)
        self.quantIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial",15))
        self.quantIn.grid(row=2, column=1, padx=10, pady=30)

        expLbl = tk.Label(addFrame, text="Expiry:", bg=self.clr(200,240,150),font=("Arial",15,"bold"))
        expLbl.grid(row=3, column=0, padx=20, pady=30)
        self.expIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial",15))
        self.expIn.grid(row=3, column=1, padx=10, pady=30)

        addBtn = tk.Button(addFrame,command=self.insertFun, text="Add Medicine", bd=2, relief="raised",font=("Arial",20,"bold"), width=20)
        addBtn.grid(row=4,column=0, padx=30, pady=40, columnspan=2)

        # detail Frame
        self.detFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(220,200,240))
        self.detFrame.place(width=self.width/2-100, height=self.height-180, x=self.width/3+40,y=100)

        lbl = tk.Label(self.detFrame, text="Details", bg="gray", bd=3, relief="groove", font=("Arial",30,"bold"))
        lbl.pack(side="top", fill="x")
        self.tabFun()

        # options Frame
        optFrame = tk.Frame(self.root,bd=4, relief="ridge", bg=self.clr(200,240,150))
        optFrame.place(width=self.width/3-200, height=self.height-180, x=self.width/3+self.width/2-40,y=100)

        srchBtn = tk.Button(optFrame,command=self.searchFun, text="Search", width=10, font=("Arial",20,"bold"),bg="gray")
        srchBtn.grid(row=0, column=0, padx=20, pady=25)

        allBtn = tk.Button(optFrame,command=self.showAll, text="Show All", width=10, font=("Arial",20,"bold"),bg="gray")
        allBtn.grid(row=1, column=0, padx=20, pady=25)

        quantBtn = tk.Button(optFrame,command=self.addQuant, text="Add Quantity", width=10, font=("Arial",20,"bold"),bg="gray")
        quantBtn.grid(row=2, column=0, padx=20, pady=25)

        purBtn = tk.Button(optFrame,command=self.billFun, text="Purchase", width=10, font=("Arial",20,"bold"),bg="gray")
        purBtn.grid(row=3, column=0, padx=20, pady=25)

        closeBtn = tk.Button(optFrame, text="Exit", width=10, font=("Arial",20,"bold"),bg="gray")
        closeBtn.grid(row=5, column=0, padx=20, pady=25)

        self.warnFun()


    def clr(self,r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame,bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2-140, height=self.height-270,x=20, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, columns=("name","price","quant", "exp"), xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set)


        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("name", text="Medicine")
        self.table.heading("price", text="Price")
        self.table.heading("quant", text="Quantity")
        self.table.heading("exp", text="Expiry")
        self.table["show"]= "headings"

        self.table.column("name", width=150)
        self.table.column("price", width=120)
        self.table.column("quant", width=100)
        self.table.column("exp", width=150)

        self.table.pack(fill="both", expand=1)

    def insertFun(self):
        name = self.nameIn.get() 
        p = self.priceIn.get()  
        q = self.quantIn.get()
        exp = self.expIn.get()
        expDate = datetime.strptime(exp, "%Y-%m-%d")

        if name and p and q and exp:
            price = int(p)
            quant = int(q)
            try:
                self.dbFun()
                query = f"insert into pharmacy(name,price,quant,exp) values(%s,%s,%s,%s)"
                self.cur.execute(query,(name,price,quant,expDate))
                self.con.commit()
                tk.messagebox.showinfo("Success",f"{name} medicine is added successfuly!")
                self.tabFun()
                self.table.delete(*self.table.get_children())
                query2= f"select * from pharmacy where name=%s"
                self.cur.execute(query2,name)
                row = self.cur.fetchone()
                self.table.insert('',tk.END,values=row)
                self.con.close()
                self.clearFun()

            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

        else:
            tk.messagebox.showerror("Error","Fill All Input Fields")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def clearFun(self):
        self.nameIn.delete(0,tk.END)
        self.priceIn.delete(0,tk.END)
        self.quantIn.delete(0,tk.END)
        self.expIn.delete(0,tk.END)
    
    def searchFun(self):
        self.srchFrame = tk.Frame(self.root, bg=self.clr(140,100,200), bd=4, relief="ridge")
        self.srchFrame.place(width=self.width/3, height=300, x=self.width/2-50, y=110)

        lbl = tk.Label(self.srchFrame, text="Medicine: ", bg=self.clr(140,100,200), fg="light green", font=("Arial",15,"bold"))
        lbl.grid(row=0, column=0, padx=20, pady=30)
        self.medIn = tk.Entry(self.srchFrame, width=20, font=("Arial",15),bd=2)
        self.medIn.grid(row=0, column=1, padx=10, pady=30)

        okBtn = tk.Button(self.srchFrame,command=self.searchMed, text="OK", bg="cyan", font=("Arial",20,"bold"),width=20)
        okBtn.grid(row=1,column=0, padx=30, pady=50, columnspan=2)

    def searchMed(self):
        medicine = self.medIn.get()

        if medicine:
            try:
                self.dbFun()
                query =f"select * from pharmacy where name=%s"
                self.cur.execute(query,medicine)
                row = self.cur.fetchone()
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END,values=row)
                self.con.close()
                self.srchFrame.destroy()

            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}") 

        else:
            tk.messagebox.showerror("Error","Insert Medicine Name!") 

    def showAll(self):
        try:
            self.dbFun()
            self.cur.execute("select * from pharmacy")
            data = self.cur.fetchall()
            self.tabFun()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END,values=i)
            self.con.close()

        except Exception as e:
            tk.messagebox.showerror("Error",f"Error: {e}") 

    def addQuant(self):
        self.addQauntFrame = tk.Frame(self.root, bg=self.clr(140,100,200), bd=4, relief="ridge")
        self.addQauntFrame.place(width=self.width/3, height=300, x=self.width/2-50, y=110)

        lbl = tk.Label(self.addQauntFrame, text="Medicine: ", bg=self.clr(140,100,200), fg="light green", font=("Arial",15,"bold"))
        lbl.grid(row=0, column=0, padx=20, pady=20)
        self.medicsIn = tk.Entry(self.addQauntFrame, width=20, font=("Arial",15),bd=2)
        self.medicsIn.grid(row=0, column=1, padx=10, pady=20)

        lbl2 = tk.Label(self.addQauntFrame, text="Quantity: ", bg=self.clr(140,100,200), fg="light green", font=("Arial",15,"bold"))
        lbl2.grid(row=1, column=0, padx=20, pady=20)
        self.qtIn = tk.Entry(self.addQauntFrame, width=20, font=("Arial",15),bd=2)
        self.qtIn.grid(row=1, column=1, padx=10, pady=20)

        okBtn = tk.Button(self.addQauntFrame,command=self.insertQuant, text="OK", bg="cyan", font=("Arial",20,"bold"),width=20)
        okBtn.grid(row=2,column=0, padx=30, pady=40, columnspan=2)   

    def insertQuant(self):
        name = self.medicsIn.get()
        q = self.qtIn.get()

        if name and q:
            quant = int(q)
            try:
                self.dbFun()
                query = f"select quant from pharmacy where name=%s"
                self.cur.execute(query,name)
                row = self.cur.fetchone()
                perQuant = row[0]
                newVal = perQuant + quant
                query2 = f"update pharmacy set quant=%s where name=%s"
                self.cur.execute(query2,(newVal,name))
                self.con.commit()
                
                self.tabFun()
                self.table.delete(*self.table.get_children())

                self.cur.execute("select * from pharmacy where name =%s",name)
                val = self.cur.fetchone()
                self.table.insert('',tk.END, values=val)
                tk.messagebox.showinfo("Success",f"Quantity is added for {name}")
                self.con.close()
                self.addQauntFrame.destroy()

                

            except Exception as e:
                  tk.messagebox.showerror("Error",f"Error: {e}")   

        else:
            tk.messagebox.showerror("Error","Enter Values in Both Input Fields!")
    
    def purchaseFun(self):
        self.purFrame = tk.Frame(self.root, bg=self.clr(140,100,200), bd=4, relief="ridge")
        self.purFrame.place(width=self.width/3, height=300, x=self.width/2-50, y=110)

        lbl = tk.Label(self.purFrame, text="Medicine: ", bg=self.clr(140,100,200), fg="light green", font=("Arial",15,"bold"))
        lbl.grid(row=0, column=0, padx=20, pady=20)
        self.medicineIn = tk.Entry(self.purFrame, width=20, font=("Arial",15),bd=2)
        self.medicineIn.grid(row=0, column=1, padx=10, pady=20)

        lbl2 = tk.Label(self.purFrame, text="Quantity: ", bg=self.clr(140,100,200), fg="light green", font=("Arial",15,"bold"))
        lbl2.grid(row=1, column=0, padx=20, pady=20)
        self.quantityIn = tk.Entry(self.purFrame, width=20, font=("Arial",15),bd=2)
        self.quantityIn.grid(row=1, column=1, padx=10, pady=20)

        okBtn = tk.Button(self.purFrame,command=self.innerPur, text="OK", bg="cyan", font=("Arial",20,"bold"),width=20)
        okBtn.grid(row=2,column=0, padx=30, pady=40, columnspan=2) 
        

    def billFun(self):
        self.billFrame = tk.Frame(self.root, bg=self.clr(140,100,200), bd=4, relief="ridge")
        self.billFrame.place(width=self.width/3+200, height=500, x=self.width/2-250, y=110)

        lbl = tk.Label(self.billFrame, bd=3, relief="groove", bg="cyan",font=("Arial",30,"bold"),text="Bill Frame")
        lbl.place(width=self.width/3+195,height=80, x=0, y=0)

        self.list = tk.Listbox(self.billFrame, width=53,height=11, bg="gray", fg="white",font=("Arial",15,"bold"))
        self.list.grid(row=2, column=0, padx=20, pady=90)

        pButton = tk.Button(self.billFrame,command=self.purchaseFun, text="Purchase", bd=2, relief="raised",width=8,font=("Arial",20,"bold"),bg="cyan")
        pButton.place(x=30, y=400)

        billButton = tk.Button(self.billFrame,command=self.totalBill, text="Print Bill", bd=2, relief="raised",width=8,font=("Arial",20,"bold"),bg="cyan")
        billButton.place(x=230, y=400)

        exitButton = tk.Button(self.billFrame,command=self.exitFun, text="Exit", bd=2, relief="raised",width=8,font=("Arial",20,"bold"),bg="cyan")
        exitButton.place(x=430, y=400)



    def innerPur(self):
        
        name = self.medicineIn.get()
        q = self.quantityIn.get()

        if name and q:
            quant = int(q)
            try:
                self.dbFun()
                query = f"select price, quant from pharmacy where name =%s"
                self.cur.execute(query,name)
                data = self.cur.fetchone()
                prc = data[0]
                qnt=data[1]
                if qnt >=quant:
                    amount = prc * quant
                    self.bill = self.bill + amount
                    newQuant = qnt-quant
                    
                    #self.list.delete(0,tk.END)
                    line = f"Amount of {name} is:{amount}."
                    self.list.insert(tk.END,line)

                    query2= f"update pharmacy set quant=%s where name=%s "
                    self.cur.execute(query2,(newQuant,name))
                    self.con.commit()
                    self.con.close()
                    self.destroyFun()
                else:
                    tk.messagebox.showerror("Error","Out of Stock")
                    self.destroyFun()

            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")
                self.destroyFun()

        else:
            tk.messagebox.showerror("Error","Enter Values in Both Input Fields")

    def destroyFun(self):
        self.purFrame.destroy()

    def totalBill(self):
        line = f"----------------------------"
        self.list.insert(tk.END,line)
        line2 = f"Total Bill is:----{self.bill}"
        self.list.insert(tk.END,line2)

    def exitFun(self):
        self.billFrame.destroy()

    def warnFun(self):
        try:
            self.dbFun()
            query = f"select name,exp from pharmacy"
            self.cur.execute(query)
            data = self.cur.fetchall()

            today = datetime.now().date()
            for name,exp in data:
                warDays = (exp - today).days

            if warDays <=60:
                tk.messagebox.showwarning("Warning",f"Medicine {name} will expire within {warDays} days")
            elif warDays <=0:
                tk.messagebox.showerror("Error",f"Medicine {name} is Expired!")
                

        except Exception as e:
            tk.messagebox.showerror("Error",f"Error: {e}")

root = tk.Tk()
obj = pharmacy(root)
root.mainloop()