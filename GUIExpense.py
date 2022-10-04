from tkinter import *
from tkinter import ttk, messagebox
# ttk is theme of Tk
import csv
from datetime import datetime

############## DATABAST ##############
import sqlite3

# สร้าง database
conn = sqlite3.connect('expense.sqlite3')
# สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้ได้เลย)
c = conn.cursor()

# สร้าง table ด้สยภาษา SQL
'''
'รหัสรายการ (transactionid) ' TEXT,
'วัน-เวลา (datetime) ' TEXT,
'รายการ (title)' TEXT,
'ค่าใช้จ่าย (expense)' REAL (float),
'จำนวน (quatity)' INTEGER,
'รวม (total) REAL'

'''
c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT,
                datetime TEXT,
                title TEXT,
                expense REAL,
                quantity INTEGER,
                total REAL
            )""")

def insert_expense(transaction_id,datetime,title,expense,quantity,total):
    ID = None
    with conn:
        c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
            (ID,transaction_id,datetime,title,expense,quantity,total))
        conn.commit() # การบันทึกข้อมูลลงในฐานข้อมูล ถ้าไม่รันตัวนี้จะไม่บันทึก
        print('Insert Success')

def show_expense():
    with conn:
        c.execute("SELECT * FROM expenselist")
        expense = c.fetchall() # คำสั่งให้ดึงข้อมูลเข้ามา
        #print(expense)

    return expense

def update_expense(transaction_id,title,expense,quantity,total):
    with conn:
        c.execute("""UPDATE expenselist SET title=?, expense=?, quantity=?, total=? WHERE transaction_id=?""",
            ([title,expense,quantity,total,transaction_id]))
    conn.commit()
    #print('Data Updated')

def delete_expense(transaction_id):
    with conn:
        c.execute("DELETE FROM expenselist WHERE transaction_id=?",([transaction_id,]))
    conn.commit()
    #print('Data Delete')

#############################

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย v.1.0')
#GUI.geometry('720x700+500+40')

w = 720
h = 700

ws = GUI.winfo_screenwidth() #screen wigth
hs = GUI.winfo_screenheight() #screen height

x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 20

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI


#-------------------- MENU --------------------#
menubar = Menu(GUI)
GUI.config(menu=menubar)

# file menu
filemenu = Menu(menubar,tearoff=0) # object
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')

# Help
def About():
    messagebox.showinfo('About','โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคให้เราไหม?\nBTC Address : abcde')

helpmenu = Menu(menubar,tearoff=0)  # object
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

# Donate
donatemenu = Menu(menubar,tearoff=0) # object
menubar.add_cascade(label='Donate',menu=donatemenu)
#----------------------------------------------#

Tab = ttk.Notebook(GUI) # ใส่ notebook ใน GUI

T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1) # expand ใช้คู่กับ fill 

expense_icon = PhotoImage(file='t1_expense.png')
#expense_icon = PhotoImage(file='t1_expense.png').subsample(2) #.subsample() = ย่อรูป
list_icon = PhotoImage(file='t2_list.png')

Tab.add(T1, text=f'{"รายการ": ^{50}}', image=expense_icon,compound='top')
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด": ^{50}}', image=list_icon,compound='top')


F1 = Frame(T1)
F1.pack()
#F1.place(x=145, y=50)


days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}


def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    number = v_number.get()

    if expense == '':
        print('No data')
        messagebox.showinfo('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return # ไม่ต้องรันข้างล่าง นอก if
    elif price == '':
        print('No data')
        messagebox.showinfo('Error','กรุณากรอกราคาสินค้า')
        return
    elif number == '':
        print('No data')
        messagebox.showinfo('Error','กรุณากรอกจำนวนสินค้า')
        return
        #number = 1


    total = float(price) * float(number)

    try:
        total = float(price) * float(number)
        # .get() ดึงค่ามาจาก v_expense = StrintingVer()
        print('รายการ : {} ราคา : {} บาท'.format(expense, price))
        print('จำนวน : {} รวมทั้งหมด : {} บาท'.format(number, total))
        print()
        text = 'รายการ : {} ราคา : {} บาท \n'.format(expense, float(price))
        text = text + 'จำนวน : {} รวมทั้งหมด : {} บาท'.format(number, total)
        v_result.set(text)
        # clear ข้อมูล
        v_expense.set('')
        v_price.set('')
        v_number.set('')

        today = datetime.now().strftime('%a') # days['Mon'] => 'จันทร์'
        print(today)
        stamp = datetime.now()
        dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
        transaction_id = stamp.strftime('%Y%m%d%H%M%f')
        dt = days[today] + '-' + dt

        #print(type(transaction_id))
        #print(tpye(price))
        insert_expense(transaction_id,dt,expense,float(price),int(number),total)

        # บันทึกข้อมูลลง csv อย่าลืม import csv
        with open('savedata.csv','a',encoding='utf-8',newline='') as f:
            # with คือ สั่งเปิดแล้วปิดไฟล์อัตโนมัติ
            # 'a' การบันทึกไปเรื่อยๆ เพิ่มข้อมูลต่อจากอันเก่า
            # newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) #สร้างฟังก์ชันสำหรับเขียนข้อมูล
            data = [transaction_id,dt, expense, float(price), number, total]
            fw.writerow(data)

        # ทำให้เคอเชอร์กลับไปตำแหน่งช่อง E1
        E1.focus()
        update_table()

    except Exception as e:
        print('ERROR',e)
        #messagebox.showerning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        #messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')

        messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        v_expense.set('')
        v_price.set('')
        v_number.set('')
        E1.focus()
    
# ทำให้กด Enter
GUI.bind('<Return>', Save) # ต้องเพิ่มใน def Save(event=None)

FONT1 = (None,20) # None เปลี่ยนเป็นชื่อ Font


# --- Image --- 
centerimg = PhotoImage(file='wallet.png')
logo = ttk.Label(F1, image=centerimg)
logo.pack()


# --- text1 ---
L = ttk.Label(F1, text='รายการค่าใช้จ่าย', font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือ ตัวแปรสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1, textvariable=v_expense, font=FONT1) # Entry ช่องรับ input
E1.pack()
# -------------------------


# --- text2 ---
L = ttk.Label(F1, text='ราคา (บาท)', font=FONT1).pack()
v_price = StringVar()
# StringVar() คือ ตัวแปรสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1, textvariable=v_price, font=FONT1)
E2.pack()
# -------------------------


# --- text3 ---
L = ttk.Label(F1, text='จำนวน (ชิ้น)', font=FONT1).pack()
v_number = StringVar()
# StringVar() คือ ตัวแปรสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1, textvariable=v_number, font=FONT1)
E3.pack()
# -------------------------

save_icon = PhotoImage(file='b_save.png')

B2 = ttk.Button(F1,text=f'{"Save": >{10}}',image=save_icon,compound='left',command=Save) #เอา B1 ใส่ใน F1
B2.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('-------- ผลลัพธิ์ --------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green') # foreground => สีข้อความ
# result = Label(F1, textvariable=v_result,font=FONT1,fg='green')
result.pack(pady=20)

########## TAB2 ##########

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr) 
    return data
        #for a,b,c,d,e in data:
        #    print(b)


    #f = open('savedata.csv',newline='',encoding='utf-8')
    #fr = csv.reader(f)
    #f.close() # .close() => ปิดไฟล์

#--- table ---#
L = ttk.Label(T2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

#for i in range(len(header)):
#    resulttable.heading(header[i],text=header[i])

#resulttable.heading(header[0],text=header[0])

for h in header:
    resulttable.heading(h,text=h)

header_width = [120,150,170,80,80,80]
for h,w in zip(header,header_width):
    resulttable.column(h,width=w)

# 'end' => ตำแหน่งสุดท้าย, 0 => ตำแหน่งบน
#resulttable.insert('','end',value=['จันทร์','ชา',30,5,150])
#resulttable.insert('','0',value=['อังคาร','ชา',30,5,150])  

alltransaction = {}

def UpdateCSV():
    with open('savedata.csv','w',newline='',encoding='utf-8') as f:
        # 'w' => การเขียนทับ
        fw = csv.writer(f)
        # เตรียมข้อมูลจาก alltransaction ให้กลายเป็น list
        data = list(alltransaction.values())
        fw.writerows(data) # multiple line from nested list [[],[],[]]
        print('Table was updated')


def UpdateSQL():
    data = list(alltransaction.values())
    #print('UPDATE SQL:',data[0])
    for d in data:
        # transaction_id,title,expense,quantity,total
        # d[0] => '2021156454545', d[1] => 'วันเสาร์ 2020-06-19', d[2] => 'Apple', d[3] => 45, d[4] => 2, d[5] => 90
        update_expense(d[0],d[2],d[3],d[4],d[5])

        

def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm','คุณต้องการลบข้อมูลใช่หรือไหม?')
    print('YES/No :',check)

    if check == True:
        print('delete')
        select = resulttable.selection()
        #print(select)
        data = resulttable.item(select)
        data = data['values']
        transaction_id = data[0]
        #print(transaction_id)
        del alltransaction[str(transaction_id)] # delete data in dict
        #print(alltransaction)
        #print(data)
        #UpdateCSV()
        delete_expense(str(transaction_id)) # delete in DB
        update_table()
    else:
        print('cancel')


BDelete = ttk.Button(T2,text='Delete',command=DeleteRecord)
BDelete.place(x=50,y=550)

resulttable.bind('<Delete>',DeleteRecord)

def update_table():
    resulttable.delete(*resulttable.get_children())

    #for c in resulttable.get_children():
    #resulttable.delete(c)
    try:
        data = show_expense() #read_csv()
        print('DATA:',data)
        for d in data:
            # creat transaction data
            alltransaction[d[1]] = d[1:] # d[1] => trancaction_id
            resulttable.insert('',0,value=d[1:])
        print('TS:',alltransaction)
    except Exception as e:
        print('No File')
        print('ERROR',e)


###### Right click menu ######
def EdidRecord():
    POPUP = Toplevel() # คล้ายๆกับ Tk()
    POPUP.title('Edit Record')
    # POPUP.geometry('500x400')
    w = 500
    h = 400

    ws = POPUP.winfo_screenwidth() #screen wigth
    hs = POPUP.winfo_screenheight() #screen height

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) - 20

    POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

    # --- text1 ---
    L = ttk.Label(POPUP, text='รายการค่าใช้จ่าย', font=FONT1).pack()
    v_expense = StringVar()
    # StringVar() คือ ตัวแปรสำหรับเก็บข้อมูลใน GUI
    E1 = ttk.Entry(POPUP, textvariable=v_expense, font=FONT1) # Entry ช่องรับ input
    E1.pack()
    # -------------------------


    # --- text2 ---
    L = ttk.Label(POPUP, text='ราคา (บาท)', font=FONT1).pack()
    v_price = StringVar()
    # StringVar() คือ ตัวแปรสำหรับเก็บข้อมูลใน GUI
    E2 = ttk.Entry(POPUP, textvariable=v_price, font=FONT1)
    E2.pack()
    # -------------------------


    # --- text3 ---
    L = ttk.Label(POPUP, text='จำนวน (ชิ้น)', font=FONT1).pack()
    v_number = StringVar()
    # StringVar() คือ ตัวแปรสำหรับเก็บข้อมูลใน GUI
    E3 = ttk.Entry(POPUP, textvariable=v_number, font=FONT1)
    E3.pack()
    # -------------------------

    def Edit():
        # print(transaction_id)
        # print(alltransaction)
        olddata = alltransaction[str(transaction_id)]
        print('OLD', olddata)
        v1 = v_expense.get()
        v2 = float(v_price.get())
        v3 = float(v_number.get())
        total = v2 * v3
        newdata = [olddata[0], olddata[1], v1 ,v2, v3, total]
        alltransaction[str(transaction_id)] = newdata
        #UpdateCSV()
        # upddate_expense(olddata[0], olddata[1], v1 ,v2, v3, total) => sing record update
        print('\n-------------')
        print(newdata)

        UpdateSQL()
        update_table()
        POPUP.destroy() # สั่งปิด popup

    save_icon = PhotoImage(file='b_save.png')

    B2 = ttk.Button(POPUP,text=f'{"Save": >{10}}',image=save_icon,compound='left',command=Edit)
    B2.pack(ipadx=50,ipady=20,pady=20)

    ###--- get data in record ---###
    select = resulttable.selection()
    #print(select)
    data = resulttable.item(select)
    data = data['values']
    print(data)
    transaction_id = data[0]

    # สั่งเซ็ตค่าเก่าไว้ตรงช่องกรอก
    v_expense.set(data[2])
    v_price.set(data[3])
    v_number.set(data[4])

    POPUP.mainloop()



rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit', command=EdidRecord)
rightclick.add_command(label='Delete', command=DeleteRecord)

def menupopup(event):
    # print(event.x_root, event.y_root) # position
    rightclick.post(event.x_root, event.y_root)


resulttable.bind('<Button-3>',menupopup)


update_table()

#print('GET CHILD',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus()) # เลื่อนเคอเซอร์ โดยปุ่ม Tab
GUI.mainloop()
