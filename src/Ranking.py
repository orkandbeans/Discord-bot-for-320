from db import db as database



class BRIAN():

    def __init__(self):
        self.scoreCalculator = ScoreCalculator()
        self.memberController = MemberController()  

        #when a BRIAN is created, make sure there is a database to access. 
        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT UNIQUE, ranking_score INTEGER, happy INTEGER, angry INTEGER, funny INTEGER)"
        database.execute(createCommand)
        database.commit()

        createCommand = "CREATE TABLE IF NOT EXISTS roles(role_id INTEGER PRIMARY KEY, role_name TEXT UNIQUE, role_cost INTEGER)"
        database.execute(createCommand)
        database.commit()

        createCommand = '''CREATE TABLE IF NOT EXISTS rolloc(
                            Rmember_id INTEGER,
                            Rrole_id INTEGER,
                            FOREIGN KEY(Rmember_id) REFERENCES members(member_id),
                            FOREIGN KEY(Rrole_id) REFERENCES roles(role_id),
                            UNIQUE(Rmember_id,Rrole_id))'''
        database.execute(createCommand)
        database.commit()
        


    def botCommand(self,comType,name,message):
        #take a bot command and determine what needs to be changed. comType will tell the method what to do.
        
        if comType == "updateMembers":#This will update the database with each member in the discord guild, adding them if they don't exist ignoring if they do
            for member in name:
                if self.memberController.addMember(member) != 0:
                    print("ERROR: Failed to add %s to the database.",member)

        return

    def updateScore(self,name,message):
        #change the member "name"'s score based on what they said in their message
        if self.scoreCalculator.changeScore(name,self.scoreCalculator.calculateStr(message)) != 0:
            print("ERROR: Failed to change %s's score.",name)
        


    def adjustRole(self,name,addRole,role):
        #change the member "name" to either add or delete "role" based on addRole
        pass

    def addRemoveMember(self,name,addMember):
        #remove or add a member from the database based on the variable, "addMember"

        if addMember:
            if self.memberController.addMember(name) != 0:
                print("ERROR: Failed to add %s to the database.",name)
            return

        if self.memberController.removeMember(name) != 0:
            print("ERROR: Failed to remove %s to the database.",name)
        return


class MemberController():
    def __init__(self):
        self.roleModule = RoleModule()
        self.memberModule = MemberModule()

    def roleCheck(self,name):
        #check a member's roles from the db and return a list of roles that the member has
        return []

    def removeMember(self,name):
        #remove a member from the db based on their name. return 0 on success and 1 on failure
        return self.memberModule.removeMember(name)
    
    def addMember(self,name):
        #add a member to the db with member_name = "name". return 0 on success and 1 on failure
        return self.memberModule.addMember(name)
        
    def newRole(self,role,scoreToGet):
        #adds a new role to the database as well as the score needed to get the role.
        if not scoreToGet:
            scoreToGet = self.roleModule.getNewRoleScore()
            if scoreToGet == -1:
                return 1

        self.roleModule.newRole(role,scoreToGet)
        return 0

    def addRole(self,name,role):
        #add a specific role to the member. return 0 on success and 1 on failure
        return 0

    def removeRole(self,name,role):
        #remove a specific role from the member. return 0 on success and 1 on failure
        return 0

    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore)
        self.roleModule.resetRoles(name)
        

class RoleModule():
    
    def __init__(self):
        self.roles = {""}

    def getNewRoleScore(self):
        command = "SELECT max(roleCost) from roles"

    def newRole(self,role,scoreToGet):
        pass

    def adjustSpecificRole(self,name,role,addRole):
        #if addRole is true, add a specific node to a member, else, remove a specific role from a member. 
        return 0

    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore)
        shouldHave = self.getRoles(name)
        command = "SELECT Rrole_id FROM rolloc where Rmember_id=(SELECT member_id FROM members WHERE member_name=?)"
        doesHave = database.records(command,name)
        SHRoleIds = [item[0] for item in shouldHave]
        doesHave = [item[0] for item in doesHave]


        for role in doesHave:
            if role not in SHRoleIds:
                command = "DELETE FROM rolloc WHERE Rmember_id = (SELECT member_id FROM members WHERE member_name=?1) AND Rrole_id = ?2"
                database.execute(str(command),str(name),role)
                if self.safeCommit():
                    print("didn't remove this role %d",role)

        for role in shouldHave:#for each role that the member should have, try to insert that role into the database
            command = "INSERT OR IGNORE INTO rolloc VALUES ((SELECT member_id FROM members WHERE member_name=?),?)"
            database.execute(str(command),str(name),role[0])
            if self.safeCommit():
                print("didn't add this role %d",role[0])


    def getRoles(self,name):
        #get all roles that member "name" is authorized to have. return list of roles as tuples
        roleList = []
        memberScore = database.record('SELECT ranking_score FROM members WHERE member_name=?',str(name))
        result = database.records('SELECT role_id, role_cost FROM roles')

        for cell in result:#for each role that a member should have, append it to the list
            if memberScore[0] > cell[1]:
                roleList.append(cell)
        return roleList
    
    def safeCommit(self):#runs the commit command while checking if the table was altered at all. return 0 if database was saved, 1 if not
        if database.rowCount() == 1:
            database.commit()
            return 0
        return 1


class MemberModule():

    def addMember(self, name):#insert a member into the members table with member_name = "name", if exists ignore this command
        command = "INSERT OR IGNORE INTO members VALUES ((SELECT max(member_id) FROM members)+1,?,0,0,0,0)"
        database.execute(str(command),str(name))
        return self.safeCommit()

    def removeMember(self,name):#remove a member from the members table with member_name = "name"
        command = "DELETE FROM members WHERE member_name = ?"
        database.execute(str(command),str(name))
        return self.safeCommit()

    def dropDb(self):#drop the members table from the database
        dropCommand = "DROP TABLE members"
        database.execute(dropCommand)
        return self.safeCommit()

    def getMember(self,name):#get the member with member_name = "name"
        command = "SELECT * FROM members WHERE member_name = ?"
        database.execute(str(command),str(name))
        return self.safeCommit()

    def safeCommit(self):#runs the commit command while checking if the table was altered at all. return 0 if database was saved, 1 if not
        if database.rowCount() == 1:
            database.commit()
            return 0
        return 1
        
    

class ScoreCalculator():

    def __init__(self):#store the word dictionary in self.wordDict in order to rank the attribute scores of each member's messages
        self.scoreModule = ScoreModule()
        self.wordDict = {"please":(0,5),"hate":(1,5),"LOL":(2,5)}#the format is "word of interest":(attributeID,attributeIncrement)
    
    def changeScore(self,name,attributeList):#increment the member's score by the chat increment amount and increment each attribute score by the values in "attributeList"
        self.scoreModule.adjustScore(name,attributeList)
        return 0

    def calculateStr(self,message):#calculate the score of a specific string that a member sent
        attributeList = [0,0,0] #this is a list that tracks how nice, mean, and funny someone is. [nice, mean, funny] 

        for word in message.split():#for each word in the members chat message, check if it matches a key in the wordDict and adjust score accordingly
            if word in self.wordDict:
                attributeList[self.wordDict[word][0]] += self.wordDict[word][1]

        return attributeList


class ScoreModule():
    
    def adjustScore(self,name,aL):#adjust the ranking score of "name" by 1 and each attribute by the amount described by the list "aL"
        command = "UPDATE members SET ranking_score=ranking_score + 1, happy=happy + ?2, angry=angry + ?3, funny=funny + ?4 WHERE member_name=?1"
        database.execute(str(command),str(name),aL[0],aL[1],aL[2])
        database.commit()
        



def main():
  
    """command = "INSERT OR IGNORE INTO roles VALUES (1,'pleb',20)"
    database.execute(str(command))
    database.commit()
    command = "INSERT OR IGNORE INTO roles VALUES (2,'teamMember',30)"
    database.execute(str(command))
    database.commit()
    command = "INSERT OR IGNORE INTO roles VALUES (3,'admin',50)"
    database.execute(str(command))
    database.commit()"""

    #database.execute("DROP TABLE rolloc")
    #brian = BRIAN()

    #database.execute("INSERT INTO rolloc VALUES(5,3)")
    #database.commit()

    rm = RoleModule()
    rm.resetRoles('orkandbeans#3110')



    pass
   
if __name__ == "__main__":
    main()
