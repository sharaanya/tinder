import mysql.connector

class DBHelper:
    def __init__(self):

        #connect to the database
        try:
            self.conn=mysql.connector.connect(host="localhost",user="root",password="",database="tinder")
            self.mycursor=self.conn.cursor()
            print("Database connection succesfull")
        except:
            print("Not connected")

    def checklogin(self,email,password):
        query ="SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'".format(email,password)
        self.mycursor.execute(query)
        data=self.mycursor.fetchall()

        return data

    def loadOwnData(self, user_id):

        query = "SELECT * FROM users WHERE user_id={}".format(user_id)
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()

        return data


    def performRegistration(self, name, email, password, age, gender, location, bio, dp):

        query = "INSERT INTO users (user_id,name,email,password,age,gender,location,bio,dp) VALUES (NULL,'{}','{}','{}',{},'{}','{}','{}','{}')".format(
            name, email, password, age, gender, location, bio, dp)

        try:
            self.mycursor.execute(query)
            self.conn.commit()
            return 1
        except:
            return 0

    def fetchOtherUsersData(self,user_id):
        query ="SELECT * FROM `users` WHERE user_id NOT LIKE {}".format(user_id)
        self.mycursor.execute(query)
        data=self.mycursor.fetchall()
        return data

    def propose(self,sender_id,receiver_id):
        query= "INSERT INTO proposals (proposal_id,sender_id,receiver_id) VALUES (NULL,{},{})".format(sender_id,receiver_id)
        try:
            response = self.relationshipExists(sender_id,receiver_id)
            if response==1:
                self.mycursor.execute(query)
                self.conn.commit()
                return 1
            else:
                return -1
        except:
            return 0

    def relationshipExists(self,sender_id,receiver_id):
        query = "SELECT * FROM proposals WHERE sender_id={} AND receiver_id={}".format(sender_id,receiver_id)
        self.mycursor.execute(query)
        data=self.mycursor.fetchall()
        if len(data)>0:
            return 0
        else:
            return 1

    def fetchProposals(self,sender_id):
        query= "SELECT * FROM proposals p JOIN users u ON u.user_id=p.receiver_id WHERE p.sender_id={}".format(sender_id)
        self.mycursor.execute(query)
        data=self.mycursor.fetchall()
        return data

    def fetchRequests(self,receiver_id):
        query= "SELECT * FROM proposals p JOIN users u ON u.user_id=p.sender_id WHERE p.receiver_id={}".format(receiver_id)
        self.mycursor.execute(query)
        data=self.mycursor.fetchall()
        return data

    def fetchMatches(self,user_id):
        query= "SELECT * FROM proposals p JOIN users u ON u.user_id=p.sender_id WHERE p.sender_id IN (SELECT p.receiver_id FROM proposals p WHERE p.sender_id={}) AND p.receiver_id={}".format(user_id,user_id)
        self.mycursor.execute(query)
        data=self.mycursor.fetchall()
        return data

    def editProfile(self, age, location, bio, dp, user_id):

        query = "UPDATE users SET age={},location='{}',bio='{}',dp='{}' WHERE user_id={}".format(age, location, bio, dp,
                                                                                                 user_id)
        try:
            self.mycursor.execute(query)
            self.conn.commit()
            return 1
        except:
            return 0




