from tkinter import *
from dbhelper import DBHelper
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter import filedialog
import shutil, os


class Tinder:

    def __init__(self):

        self.db=DBHelper()
        self.constructGUI()


    def constructGUI(self):
        self.root = Tk()

        self.root.title("Tinder")

        self.root.minsize(425, 500)
        self.root.maxsize(425, 550)

        self.root.configure(background="#E7497C")

        self.loadloginGUI()

        self.root.mainloop()



    def loadloginGUI(self):
        self.clear()
        self.title=Label(self.root, text="TINDER",bg="#E7497C", fg="#fff")
        self.title.configure(font=("Sans serif",30,"bold"))
        self.title.pack(pady=(30,30))

        self.title2 = Label(self.root, text="Kindly login to proceed", bg="#E7497C", fg="#fff")
        self.title2.configure(font=("Sans serif", 14, "bold"))
        self.title2.pack(pady=(5, 20))

        self.frame1=Frame(self.root)
        self.frame1.pack(pady=(5,15))

        self.emailLabel=Label(self.frame1,text="Email",bg="#E7497C", fg="#fff")
        self.emailLabel.configure(font=("Times",12))
        self.emailLabel.pack(side=LEFT)

        self.emailInput=Entry(self.frame1)
        self.emailInput.pack(side=RIGHT,ipady=5,ipadx=20)

        self.frame2 = Frame(self.root)
        self.frame2.pack(pady=(5, 15))

        self.passwordLabel = Label(self.frame2, text="Password", bg="#E7497C", fg="#fff")
        self.passwordLabel.configure(font=("Times", 12))
        self.passwordLabel.pack(side=LEFT)

        self.passwordInput = Entry(self.frame2)
        self.passwordInput.pack(side=RIGHT, ipady=5, ipadx=20)

        self.login=Button(self.root,text="Login",bg="#fff",fg="#000",width=20,height=2, command=lambda: self.dologin())
        self.login.pack(pady=(10,15))

        self.title3=Label(self.root,text="Not a member yet? Sign up now", bg="#E7497C", fg="#fff")
        self.title3.pack(pady=(5,10))

        self.register=Button(self.root,text="Sign up", bg="#fff", fg="#000", command=lambda: self.loadRegisterGUI())
        self.register.pack()


    def loadRegisterGUI(self):
        self.clear()

        self.title = Label(self.root, text="TINDER", bg="#E7497C", fg="#fff")
        self.title.configure(font=("Sans serif", 30, "bold"))
        self.title.pack(pady=(30, 30))

        self.nameLabel = Label(self.root, text="NAME:", bg="#E7497C", fg="#fff")
        self.nameLabel.pack()

        self.nameInput = Entry(self.root)
        self.nameInput.pack()

        self.emailLabel = Label(self.root, text="EMAIL:", bg="#E7497C", fg="#fff")
        self.emailLabel.pack()

        self.emailInput = Entry(self.root)
        self.emailInput.pack()

        self.passwordLabel = Label(self.root, text="PASSWORD:", bg="#E7497C", fg="#fff")
        self.passwordLabel.pack()

        self.passwordInput = Entry(self.root)
        self.passwordInput.pack()

        self.ageLabel = Label(self.root, text="AGE:", bg="#E7497C", fg="#fff")
        self.ageLabel.pack()

        self.ageInput = Entry(self.root)
        self.ageInput.pack()

        self.genderLabel = Label(self.root, text="GENDER:", bg="#E7497C", fg="#fff")
        self.genderLabel.pack()

        self.genderInput = Entry(self.root)
        self.genderInput.pack()

        self.locationLabel = Label(self.root, text="LOCATION:", bg="#E7497C", fg="#fff")
        self.locationLabel.pack()

        self.locationInput = Entry(self.root)
        self.locationInput.pack()

        self.bioLabel = Label(self.root, text="BIO:", bg="#E7497C", fg="#fff")
        self.bioLabel.pack()

        self.bioInput = Entry(self.root)
        self.bioInput.pack()

        self.dpLabel = Label(self.root, text="UPLOAD DP:", bg="#E7497C", fg="#fff")
        self.dpLabel.pack()

        self.register = Button(self.root, text="Register", bg="#fff", fg="#000", command=lambda: self.doRegister())
        self.register.pack()

        self.frame = Frame(self.root)
        self.frame.pack(pady=(10))

        self.message = Label(self.frame, text="Go back to Login", bg="#E7497C", fg="#fff")
        self.message.pack(side=LEFT)

        self.loginBtn = Button(self.frame, text="Login", command=lambda: self.loadloginGUI())
        self.loginBtn.pack(side=RIGHT)


    def doRegister(self):

        name = self.nameInput.get()
        email = self.emailInput.get()
        password = self.passwordInput.get()
        age = self.ageInput.get()
        gender = self.genderInput.get()
        location = self.locationInput.get()
        bio = self.bioInput.get()

        # call dbhelper
        response = self.db.performRegistration(name, email, password, age, gender, location, bio,"avatar.png")

        if (response == 1):
            messagebox.showinfo("Registration Successful", "Successfully Registered")
        else:
            messagebox.showerror("Error", "User already exists")


    def dologin(self):
        email=self.emailInput.get()
        password=self.passwordInput.get()
        #send this data to database lland check if user exists or not
        self.data=self.db.checklogin(email,password)
        if len(self.data)>0:
            #print the GUI
            self.user_id=self.data[0][0]
            self.loadUserProfile(self.data)
        else:
            messagebox.showerror("Error","Incorrect credentials")


    def loadUserProfile(self,data):
        self.userProfileGUI(data)


    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()


    def headerMenu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="Home", menu=filemenu)
        filemenu.add_command(label="My Profile", command=lambda: self.loadOwnProfile())
        filemenu.add_command(label="Edit Profile",command=lambda: self.loadEditProfileGUI())
        filemenu.add_command(label="View Other Profiles",command=lambda: self.fetchOtherUsersData())
        filemenu.add_command(label="Logout", command=lambda: self.logout())

        helpmenu = Menu(menu)
        menu.add_cascade(label="Proposals", menu=helpmenu)
        helpmenu.add_command(label="My Proposals",command=lambda: self.showProposals())
        helpmenu.add_command(label="My Requests",command=lambda: self.showRequests())
        helpmenu.add_command(label="My Matches",command=lambda: self.showMatches())

    def loadOwnProfile(self):

        data = self.db.loadOwnData(self.user_id)
        self.loadUserProfile(data)


    def showMatches(self):
        data = self.db.fetchMatches(self.user_id)
        new_data = []
        for i in data:
            i = i[3:]
            new_data.append(i)
        self.userProfileGUI(new_data, mode=3)



    def loadEditProfileGUI(self):
        self.clear()
        self.title = Label(self.root, text="TINDER", bg="#E7497C", fg="#fff")
        self.title.configure(font=("Sans serif", 30, "bold"))
        self.title.pack(pady=(30, 30))

        self.ageLabel = Label(self.root, text="Edit Age:", bg="#E7497C", fg="#fff")
        self.ageLabel.pack()

        self.ageInput = Entry(self.root)
        self.ageInput.pack()

        self.locationLabel = Label(self.root, text="Edit Location:", bg="#E7497C", fg="#fff")
        self.locationLabel.pack()

        self.locationInput = Entry(self.root)
        self.locationInput.pack()

        self.bioLabel = Label(self.root, text="Edit Bio:", bg="#E7497C", fg="#fff")
        self.bioLabel.pack()

        self.bioInput = Entry(self.root)
        self.bioInput.pack()

        self.fileInput=Button(self.root,text="Change Profile Picture", command=lambda: self.uploadFile())
        self.fileInput.pack(pady=(5,5))

        self.filename=Label(self.root)
        self.filename.pack(pady=(5,5))

        self.editBtn = Button(self.root, text="Edit profile", command=lambda: self.editProfile())
        self.editBtn.pack()


    def uploadFile(self):

        self.pathname = filedialog.askopenfilename(initialdir="/images", title="Somehting")
        self.filename['text']=self.pathname



    def editProfile(self):
        age=self.ageInput.get()
        location=self.locationInput.get()
        bio=self.bioInput.get()
        actualfilename=self.pathname.split("/")[-1]
        response=self.db.editProfile(age,location,bio,actualfilename,self.user_id,)
        if response==1:
            destination="C:\\Codes\\Python Codes\\Pycharm\\tinder\\images\\"+self.pathname.split("/")[-1]
            shutil.copyfile(self.pathname, destination)
            messagebox.showinfo("Success","Profile updated successfully")
        else:
            messagebox.showerror("Error","Some error occure d")



    def showRequests(self):
        data = self.db.fetchRequests(self.user_id)
        new_data = []
        for i in data:
            i = i[3:]
            new_data.append(i)
        self.userProfileGUI(new_data, mode=3)


    def showProposals(self):
        data=self.db.fetchProposals(self.user_id)
        new_data=[]
        for i in data:
            i=i[3:]
            new_data.append(i)
        self.userProfileGUI(new_data,mode=3)


    def userProfileGUI(self,data,mode=1,index=0):

        self.clear()
        self.headerMenu()
        #Image (For Later)
        imageUrl = "images/{}".format(data[index][-1])

        load = Image.open(imageUrl)
        load = load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(image=render)
        img.image = render
        img.pack()
        #1.Name
        self.nameLabel=Label(self.root,text=data[index][1],bg="#E7497C",fg="#fff")
        self.nameLabel.config(font=("Times,20"))
        self.nameLabel.pack(pady=(30,15))
        self.frame=Frame(self.root)
        self.frame.pack(pady=(2,20))

        #2.Age
        self.ageLabel=Label(self.frame,text=str(data[index][4])+" "+"years old",bg="#E7497C",fg="#fff")
        self.ageLabel.config(font=("Times,20"))
        self.ageLabel.pack(side=LEFT)

        # 3.Gender
        self.genderLabel = Label(self.frame, text=data[index][5], bg="#E7497C", fg="#fff")
        self.genderLabel.config(font=("Times,20"))
        self.genderLabel.pack(side=LEFT)

        #4.City
        self.locationLabel = Label(self.frame, text="From"+" "+data[index][6], bg="#E7497C", fg="#fff")
        self.locationLabel.config(font=("Times,20"))
        self.locationLabel.pack(side=LEFT)

        # 5.BIO
        self.bioLabel = Label(self.frame, text=","+" "+data[index][7], bg="#E7497C", fg="#fff")
        self.bioLabel.config(font=("Times,20"))
        self.bioLabel.pack(side=LEFT)

        if mode==2:

            self.frame2=Frame(self.root)
            self.frame2.pack(pady=(20,20))

            self.previous=Button(self.frame2, text="PREVIOUS",command=lambda: self.viewOtherUsers(data,index,invoker=2,mode=2))
            self.previous.pack(side=LEFT)

            self.propose = Button(self.frame2, text="PROPOSE",command=lambda: self.proposeUser(data[index][0]))
            self.propose.pack(side=LEFT)

            self.next = Button(self.frame2, text="NEXT",command=lambda: self.viewOtherUsers(data,index,invoker=1,mode=2))
            self.next.pack(side=LEFT)

        if mode==3:
            self.frame2 = Frame(self.root)
            self.frame2.pack(pady=(20, 20))

            self.previous = Button(self.frame2, text="PREVIOUS",
                                   command=lambda: self.viewOtherUsers(data, index, invoker=2,mode=3))
            self.previous.pack(side=LEFT)

            self.next = Button(self.frame2, text="NEXT", command=lambda: self.viewOtherUsers(data, index, invoker=1,mode=3))
            self.next.pack(side=LEFT)

        #Edit Proile


    def proposeUser(self,receiver_id):
        sender_id=self.user_id
        receiver_id=receiver_id
        response=self.db.propose(sender_id,receiver_id)
        if response==1:
            messagebox.showinfo("Proposal Sent","Fingers crossed")
        elif response==-1:
            messagebox.showerror("Error cc ", "Already Proposed")
        else:
            messagebox.showerror("Error","Some error occured")


    def logout(self):

        self.root.destroy()
        self.constructGUI()


    def fetchOtherUsersData(self):
        # fetch data of all other users except login user
        data=self.db.fetchOtherUsersData(self.user_id)
        self.viewOtherUsers(data,index=-1,mode=2)


    def viewOtherUsers(self,data,index=0,invoker=0,mode=0):
        if invoker==1:
            if(index==len(data)-1):
                self.userProfileGUI(data, mode=mode, index=0)
            else:
                self.userProfileGUI(data, mode=mode,index=index+1)
        elif invoker==2:
            if (index == 0):
                self.userProfileGUI(data, mode=mode, index=len(data)-1)
            else:
                self.userProfileGUI(data, mode=mode, index=index - 1)
        else:
            self.userProfileGUI(data, mode=mode, index=0)







obj=Tinder()

