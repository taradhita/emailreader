from tkinter import *
from tkinter import ttk
import email
from email import parser
import smtplib, poplib
import subprocess

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class LoginWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)  
        self.master = master
        self.login_input()
        self.login_button = Button(self, text='Login',command=self.login_click)
        self.login_button.grid(column = 1, row=2)
        self.grid()

    def login_input(self):
        self.login_label = name = Label(self, text="Username").grid(row=0,column = 0)
        self.pass_label = name = Label(self, text="Password").grid(row=1,column = 0)
        self.email_input = Entry(self)
        self.email_input.grid(row=0,column=1)
        self.pass_input = Entry(self,show="*")
        self.pass_input.grid(row=1,column=1)

    def login_click(self):
        self.userid = self.email_input.get()
        self.password = self.pass_input.get()
        self.connection = self.connect(self.userid,self.password)
        #print(self.email_input.get())
        #print(self.pass_input.get())
        messages=self.readMail(self.connection)
        #treeview
        self.tree = ttk.Treeview( self.master, columns=('From', 'Subject'))
        self.tree.heading('#0', text='No')
        self.tree.heading('#1', text='From')
        self.tree.heading('#2', text='Subject')
        self.tree.column('#1', stretch=YES)
        self.tree.column('#2', stretch=YES)
        self.tree.column('#0', stretch=YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0
        
        self.getInsideMails(messages)
        
        
    def connect(self,uid,pwd):
        print('Connect..')
        pop_conn=poplib.POP3_SSL('pop.gmail.com')
        pop_conn.user(self.userid)
        pop_conn.pass_(self.password)
        return pop_conn

    def readMail(self, pop_conn):
        print (pop_conn.getwelcome())
        print(pop_conn.stat())
        #self.msgCount, self.msgBytes = pop_conn.stat()
        #print('There are', self.msgCount, 'mail messages in', self.msgBytes, 'bytes')
        msg=[pop_conn.retr(i) for i in range(1,len(pop_conn.list()[1])+1)]
        msg=[b'\n'.join(m[1]).decode() for m in msg]
        msg=[parser.Parser().parsestr(m) for m in msg]
        pop_conn.quit()
        return msg

    def getInsideMails(self,messages):
        print ('Inbox: '+str(len(messages)))
        while self.i<len(messages):
            #print ('['+str(self.i+1)+'] ',messages[self.i]['from'], messages[self.i]['subject'])
            self.treeview.insert('', 'end', text=str(self.i+1), values=(messages[self.i]['from'], messages[self.i]['subject']))
            self.i=self.i+1
        self.tree.bind("<Double-1>", lambda event, arg=messages: self.OnDoubleClick(event, arg))

    def OnDoubleClick(self, event, arg):
        #curItem = self.tree.focus()
        #print (self.tree.item(curItem))
        item = self.tree.selection()[0]
        id_item=self.tree.item(item,"text")
        print("you clicked on", id_item)
        mail_id=int(id_item)-1
        print(arg[mail_id])
        
        

    def getBody(self, message):
        if message.is_multipart():
            for part in message.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
        else:
            body = message.get_payload(decode=True)
            
if __name__ == '__main__':
    root=Tk()
    login = LoginWindow(root)
    root.title("Email Reader")
    root.geometry("800x500")
    root.mainloop()
