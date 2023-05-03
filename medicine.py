from tkinter import * # standard library 
from tkinter import ttk #ttk , extention module of tkinter 
from tkinter import messagebox
from mysql_configa_medocare import dbConfig_Medocare
import _mysql_connector as mycon 

sql_cnt = mycon.connect(**dbConfig_Medocare)
#the connect , function basically is used to create connection to the server and python 
#the double asterisks basically means its going to unpack the content of that dictonary key to the function 
cursor_cnt =sql_cnt.cursor()
# A cursor is an object which helps to execute the query and fetch the records from the database


class MedoCareDB:
    def __init__(self):
        sql_cnt = mycon.connect (**dbConfig_Medocare)
        cursor_cnt =sql_cnt.cursor()
        print("You have connected to the database")
        print(sql_cnt)
    
    def __del__(self):
        self.sql_cnt.close() #used to close the connection 

    def display(self):
        self.cursor.execute("select * from medicine") # you pass in the SQL command or query as a string argument. The method then sends that SQL command or query to the database and executes it.
        rows = self.cursor.fetchall()
        # the fetchall () method will fetch all the rows of the query method in line 23 and returns a tuple . 
        return rows 

    def insert_list (self,medi_name ,pharma_name ,n_of_sa):
        inset_list=(" INSERT INTO medicine(medi_name ,pharma_name,n_of_sa)Values (%s,%s,%s) ") #%s , placeholder 
        values =[medi_name,pharma_name,n_of_sa]
        self.cursor.execute(inset_list,values)
        self.sql_cnt.commit ()
        #This method sends a COMMIT statement to the MySQL server, committing the current transaction.Since by default Connector/Python does not autocommit, it is important to call this method after every transaction that modifies data for tables that use transactional storage engines
        messagebox.showinfo(title="Medicine_List Databse", message= "New medicine is added to the database")
    
    def update_list (self,id,medi_name ,pharma_name ,n_of_sa):
        update_list=(" update medicine medi_name= %s,pharma_name = %s,n_of_sa=%s where id=%s ") #%s , placeholder 
        values =[medi_name,pharma_name,n_of_sa,id]
        self.cursor.execute(update_list,values)
        self.sql_cnt.commit ()
        messagebox.showinfo(title="Medicine_List Databse", message= "Updated")

    def delete_list (self,id):
        delete_list=(" delete medicine where id=%s ") #%s , placeholder 
        
        self.cursor.execute(delete_list,[id])
        self.sql_cnt.commit ()
        messagebox.showinfo(title="Medicine_List Databse", message= "Updated")


# end of the class MedoCareDB 


db = MedoCareDB ()


#standalone functions 

def get_selected_row (event):#event : The event parameter is likely an object that contains information about the event that triggered the function, such as the widget that was interacted with or the specific row or item that was selected.
    global select_row
    index = list_bx.curselection() #curselection() is method in some GUI like tkinter , The curselection() method returns a tuple of integers that represent the index positions of the currently selected items. 
    select_row = list_bx.get(index)#The get() method in Tkinter takes one index as its argument and returns the text of the item at that index.
    mediName_entry.delete(0,'end') # tkinter built-in method :0 -> starting index , end -> ending index , delete(0,'end') means removes all the items in the Listbox widget.
    mediName_entry.insert('end',select_row[1]) # tkinter built-in method :insert('end', item) adds the value of the item variable to the end of the Listbox.
    pharName_entry.delete(0,'end') 
    pharName_entry.insert('end',select_row[2])
    recId__entry.delete(0,'end')
    recId__entry.insert('end',select_row[3])
#through this event if you select any row in the list box , following items will appear in their respective entry boxes .

#event for the view btn 
def view_list():
    list_bx.delete(0 ,'end')
    for list in db.display():
        list_bx.insert('end',list)

#event for addmedicine btn
def add_medicine():
    db.insert_list(mediName_text.get(),pharName_text.get(),recId_text.get())
    list_bx.delete(0,'end')
    list_bx.insert('end',(mediName_text.get(),pharName_text.get(),recId_text.get()))
    mediName_entry.delete(0,'end')
    pharName_entry.delete(0,'end')
    recId__entry.delete(0,'end')
    sql_cnt.commit()

#event for delete_medicine btn
def delete_row():
    db.delete_list(select_row[0]) #the 0 number index of select_row carries the id , which is the primary key for the table 
    sql_cnt.commit()

#event for the clear_screen btn 
def clear_screen():
    list_bx.delete(0,'end')
    mediName_entry.delete(0,'end')
    pharName_entry.delete(0,'end')
    recId__entry.delete(0,'end')

#event for the update_screen btn 
def update_record():
    db.update_list(select_row[0],mediName_text.get(),pharName_text.get(),recId_text.get())
    mediName_entry.delete(0,'end')
    pharName_entry.delete(0,'end')
    recId__entry.delete(0,'end')
    sql_cnt.commit()

def on_closing():
    delc= db 
    if messagebox.askokcancel('quit','Do you want to quit?'):
        window.destroy()
        del delc
    


# GUI of the program : 

window = Tk() # toolkit , tk gui toolkit , Tkinter is build upon 

window.title("MedoCare") # creating the window 
window.configure(background="light yellow") #color of the window
window.geometry("700x600") 
window.resizable(width=False,height=False) # with this you can not resize the window 

#listing the widgets and entry box 
mediName_label = ttk.Label(window,text="Name of the Medicine:" , background="black", font=("TkDefaultFont", 12))
mediName_label.grid(row=0,column=1,padx=2) #works as a table 
mediName_text = StringVar()
mediName_entry = ttk.Entry(window,width=20, textvariable=mediName_text)
mediName_entry.grid(row=0,column=2, pady=2)


pharName_label = ttk.Label(window,text="Name of the Pharma:" , background="red", font=("TkDefaultFont", 12))
pharName_label.grid(row=1,column=1,padx=2) #works as a table 
pharName_text = StringVar()
pharName_entry = ttk.Entry(window,width=20, textvariable=pharName_text)
pharName_entry.grid(row=1,column=2, pady=2)


recId_label = ttk.Label(window,text="Record Id:" , background="black", font=("TkDefaultFont", 12))
recId_label.grid(row=2,column=1,padx=2) #works as a table 
recId_text= StringVar()
recId__entry = ttk.Entry(window,width=20, textvariable=recId_text)
recId__entry.grid(row=2,column=2, pady=2)


add_btn = Button(window , text="Add Medicine" , bg="light blue",fg="black",font="helvetica 10 bold",command=add_medicine ) #command is what responds to the action or the event of the button when the button is clicked.
add_btn.grid(row=4, column=1 ,padx=2 , pady=2)

#list box and scroll bar 
list_bx = Listbox(window,height=20,width=60, font="helvetica 10 bold",bg="light blue")
list_bx.grid(row=6,column=1,columnspan=14, sticky=W + E ,padx=10 ,pady=40)
list_bx.bind('<<ListboxSelect>>',get_selected_row) #bind() is a method in the Tkinter module of Python that is used to associate a function with a particular event that occurs on a widget.

scroll_bar =Scrollbar (window)
scroll_bar.grid(row=4,column=14,rowspan=14,sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set) #setting the scrollbar with the list box 
scroll_bar.configure(command=list_bx.yview)

#buttons below the list box
view_btn = Button(window , text="View Medicine List" , bg="light blue",fg="black",font="helvetica 10 bold",command=view_list)
view_btn.grid(row=14, column=1)

modify_btn = Button(window , text="Modify Medicine List" , bg="light blue",fg="black",font="helvetica 10 bold",command=update_record)
modify_btn.grid(row=14, column=2 )

delete_btn = Button(window , text="Delete any medicine" , bg="light blue",fg="black",font="helvetica 10 bold",command=delete_row )
delete_btn.grid(row=14, column=3)

clear_btn = Button(window , text="Clean Screen" , bg="light blue",fg="black",font="helvetica 10 bold",command=clear_screen )
clear_btn.grid(row=14, column=4  )

exit_btn = Button(window , text="Exit Application" , bg="light blue",fg="black",font="helvetica 10 bold",command=window.destroy)
exit_btn.grid(row=14, column=5 )




window.mainloop()

