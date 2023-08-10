import os
import mysql.connector as my
con=my.connect(host="localhost",user="root",passwd="root")
cur=con.cursor()
cur.execute("show databases")
a=cur.fetchall()
c=[]
for i in a:
    c.append(i[0])
b='game' in c
if b==False:
    cur.execute("create database game")
cur.execute("use game")
cur.execute("show tables")
a=cur.fetchall()
c=[]
for i in a:
    c.append(i[0])
b='gdetail' in c
c='transactions' in c
if b==False:
    cur.execute("create table gdetail(ic varchar(10) primary key, itn varchar(20), mrp int(10))")
if c==False:
    cur.execute("create table transactions(tn int(10), ic varchar(10), itn varchar(20), mrp int(10), sp int(10), s int(10))")

def OPT():
    ch=int(input("Choose from the following:\n 1.Add Item \n 2.Bill \n 3.Delete Item \n 4.Modify Item \n 5.Print Previous Bill \n 6.Exit\n:: "))
    if ch==1:
        add()
    elif ch==2:
        bill()
    elif ch==3:
        delete()
    elif ch==4:
        modify()
    elif ch==5:
        previous()
    elif ch==6:
        while True:
            break
    else:
        print("*****Wrong Input, Please try again*****")
        OPT()

def add():
    while True:
        ic=input("Enter Item Code: ")
        itn=input("Enter Item Name: ")
        mrp=int(input("Enter Mrp: "))
        cur.execute("insert into gdetail values('{}','{}',{})".format(ic,itn,mrp))
        con.commit()
        a=input("Add One More?: ")
        if a.lower()!='y':
            break
    OPT()
    
def delete():
    sn=input("Enter Item Code: ")
    cur.execute("select * from gdetail")
    a=cur.fetchall()
    for i in a:
        if i[0]==sn:
            cur.execute("delete from gdetail where ic='{}'".format(sn))
            con.commit()
            print("Item ",sn," deleted successfully...")
            break
    else:
        print("Item ",sn," doesn't exists...")
    OPT()
    
def modify():
    si=input("Enter Item Code: ")
    cur.execute("select * from gdetail")
    a=cur.fetchall()
    for i in a:
        if i[0]==si:
            sa=int(input("ENTER Updated Price: "))
            cur.execute("update gdetail set mrp='{}' where ic='{}'".format(sa,si))
            con.commit()
            print("Item ",si," scessfully updated...")
            break
    else:
        print("Item ",si," doesn't exists...")
    OPT()
    
def previous():
    it=int(input("Enter Transaction Number: "))
    cur.execute("select * from transactions")
    data=cur.fetchall()
    f=open(r"/home/macaw/program/billing_sys/bill.txt",'w')
    f.write("               ---Welcome to vanigames---               \n")
    f.write("                 ---Today's Purchases---                  \n")
    f.write("                                Transaction Number"+str(it)+" \n")
    f.write("%10s"%"ITEM CODE"+"%15s"%"ITEM NAME"+"%10s"%"MRP"+"%10s"%"SALE PRICE"+"%10s"%"SAVING\n")
    f.write('-'*55)
    f.write('\n')
    for i in data:
        if i[0]==it:
            f.write("%10s"%i[1]+"%15s"%i[2]+"%10s"%i[3]+"%10s"%i[4]+"%10s"%i[5]+'\n')
    f.write('-'*55)
    f.write('\n')
    cur.execute("select * from transactions")
    pp=cur.fetchall()
    mm1=mm2=mm3=0
    for q in pp:
        if q[0]==it:
            mm1=mm1+q[3]
            mm2=mm2+q[4]
            mm3=mm3+q[5]
    f.write("%25s"%"Total Amount:"+"%10s"%mm1+"%10s"%mm2+"%10s"%mm3+'\n')
    f.write("TODAY'S SAVINGS: "+str(mm3)+'\n')
    f.write("             ******THANK YOU VISIT AGAIN******             \n")
    os.startfile(r"/home/macaw/program/billing_sys/bill.txt","print")
    f.close()
    OPT()

def bill():
    z=1
    cur.execute("select * from transactions")
    tt=cur.fetchall()
    for j in tt:
        if j[0]>=1:
            z=j[0]+1
    while True:
        try:
            it=input("Enter item code: ")
            cur.execute("select * from gdetail")
            data=cur.fetchall()
            for i in data:
                if it==i[0]:
                    x=i[2]-(i[2]//8)
                    y=i[2]//8
                    cur.execute("insert into transactions values({},'{}','{}',{},{},{})".format(z,i[0],i[1],i[2],x,y))
                    con.commit()
        except KeyboardInterrupt:
            f=open(r"/home/macaw/program/billing_sys/bill.txt",'w')
            f.write("               ---Welcome to vanigames---               \n")
            f.write("                 ---Today's Purchases---                  \n")
            f.write("                                Transaction Number"+str(z)+" \n")
            f.write("%10s"%"ITEM CODE"+"%15s"%"ITEM NAME"+"%10s"%"MRP"+"%10s"%"SALE PRICE"+"%10s"%"SAVING\n")
            f.write('-'*55)
            f.write('\n')
            cur.execute("select * from transactions")
            data=cur.fetchall()
            for i in data:
                if z==i[0]:
                    f.write("%10s"%i[1]+"%15s"%i[2]+"%10s"%i[3]+"%10s"%i[4]+"%10s"%i[5]+'\n')
            break
    f.write('-'*55)
    f.write('\n')
    cur.execute("select * from transactions")
    pp=cur.fetchall()
    mm1=mm2=mm3=0
    for q in pp:
        if q[0]==z:
            mm1=mm1+q[3]
            mm2=mm2+q[4]
            mm3=mm3+q[5]
    f.write("%25s"%"Total Amount:"+"%10s"%mm1+"%10s"%mm2+"%10s"%mm3+'\n')
    f.write("TODAY'S SAVINGS: "+str(mm3)+'\n')
    f.write("             ******THANK YOU VISIT AGAIN******             \n")
    os.startfile(r"/home/macaw/program/billing_sys/bill.txt","print")
    f.close()
    OPT()
    
OPT()
con.close()
