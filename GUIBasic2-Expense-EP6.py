from tkinter import *
from tkinter import ttk, messagebox
# ttk is theme of Tk
import csv
from datetime import datetime


GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย')
GUI.geometry('600x700+500+50')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI

#-------------------- MENU --------------------#
menubar = Menu(GUI)
GUI.config(menu=menubar)

# file menu
filemenu = Menu(menubar)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')

# Help

helpmenu = Menu(menubar)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About')

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
# F1.pack()
F1.place(x=145, y=50)


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
        text = 'รายการ : {} ราคา : {} บาท \n'.format(expense, price)
        text = text + 'จำนวน : {} รวมทั้งหมด : {} บาท'.format(number, total)
        v_result.set(text)
        # clear ข้อมูล
        v_expense.set('')
        v_price.set('')
        v_number.set('')

        today = datetime.now().strftime('%a') # days['Mon'] => 'จันทร์'
        dt = datetime.now().strftime('%d-%m-%y %H:%M:%S')
        dt = days[today] + '-' + dt
        # บันทึกข้อมูลลง csv อย่าลืม import csv
        with open('savedata.csv','a',encoding='utf-8',newline='') as f:
            # with คือ สั่งเปิดแล้วปิดไฟล์อัตโนมัติ
            # 'a' การบันทึกไปเรื่อยๆ เพิ่มข้อมูลต่อจากอันเก่า
            # newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) #สร้างฟังก์ชันสำหรับเขียนข้อมูล
            data = [dt, expense, price, number, total]
            fw.writerow(data)

        # ทำให้เคอเชอร์กลับไปตำแหน่งช่อง E1
        E1.focus()
        update_table()

    except:
        print('ERROR')
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

header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10)
resulttable.pack()

#for i in range(len(header)):
#    resulttable.heading(header[i],text=header[i])

#resulttable.heading(header[0],text=header[0])

for h in header:
    resulttable.heading(h,text=h)

header_width = [150,170,80,80,80]
for h,w in zip(header,header_width):
    resulttable.column(h,width=w)

# 'end' => ตำแหน่งสุดท้าย, 0 => ตำแหน่งบน
#resulttable.insert('','end',value=['จันทร์','ชา',30,5,150])
#resulttable.insert('','0',value=['อังคาร','ชา',30,5,150])  


def update_table():
    resulttable.delete(*resulttable.get_children())

    #for c in resulttable.get_children():
    #    resulttable.delete(c)

    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()
#print('GET CHILD',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus()) # เลื่อนเคอเซอร์ โดยปุ่ม Tab
GUI.mainloop()
