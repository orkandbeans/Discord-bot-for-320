from db import db as database
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer



class BRIAN():

    def __init__(self):
        self.scoreCalculator = ScoreCalculator()
        self.memberController = MemberController()

        #when a BRIAN is created, make sure there is a database to access. 
        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT UNIQUE, ranking_score INTEGER, sentiment REAL, sentiment_divisor INTEGER)"
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
        

    def updateMembers(self,memberList):
        #add each member of the discord to the database and update their roles.
        for member in memberList:
            self.memberController.addMember(member)
                
    def updateScore(self,name,message):
        #change the member "name"'s score based on what they said in their message
        if self.scoreCalculator.changeScore(name,self.scoreCalculator.calculateStr(message)) != 0:
            print("ERROR: Failed to change %s's score.",name)

    def getMRoles(self,name):
        #get all roles that a member has and return a list of role names.
        return self.memberController.roleFind(name)

    def addRemoveMember(self,name,addMember):
        #remove or add a member from the database based on the variable, "addMember"

        if addMember:
            if self.memberController.addMember(name) != 0:
                print("ERROR: Failed to add %s to the database.",name)
            return

        if self.memberController.removeMember(name) != 0:
            print("ERROR: Failed to remove %s from the database.",name)
        return
    
    def addRemoveRole(self,role,score=0,addRole=True):
        #add or remove a role from the database based on the variable, "addRole"
        
        if addRole:

            if self.memberController.newRole(role,score) != 0:
                print("ERROR: Failed to add %s role to the database.",role)
                return 1
            return 0
        
        if self.memberController.deleteRole(role) != 0:
            print("ERROR: Failed to remove %s role from the database.",role)
            return 1
        return 0


class MemberController():
    def __init__(self):
        self.roleModule = RoleModule()
        self.memberModule = MemberModule()

    def roleFind(self,name):
        #check a member's roles from the db and return a list of roles that the member has
        result = self.roleModule.getRoles(name,True)
        roleList = []
        for role in result:
            roleList.append(role[1])

        return roleList

    def removeMember(self,name):
        #remove a member from the db based on their name. return 0 on success and 1 on failure
        return self.memberModule.removeMember(name)
    
    def addMember(self,name):
        #add a member to the db with member_name = "name".
        result = self.memberModule.addMember(name)
        if result == 0:
            print("Added " + str(name) + " to the database.")

        result = self.roleModule.resetRoles(name)
        if result == 0:
            print("Added " + str(name) + "'s roles to the database.")
        #reset the member's roles to init them in the role system
        self.roleModule.resetRoles(name)
        
        
    def newRole(self,role,scoreToGet):
        #adds a new role to the database as well as the score needed to get the role.
        if scoreToGet == -1:
            scoreToGet = self.roleModule.getNewRoleScore()
            if scoreToGet == -1:
                return 1

        return self.roleModule.newRole(role,scoreToGet)
        
    
    def deleteRole(self,role):
        #calls the rolemodule to delete a role from the database.
        return self.roleModule.deleteRole(role)

    def addMemberRole(self,name,role):
        #add a specific role to the member. return 0 on success and 1 on failure
        return 0

    def removeMemberRole(self,name,role):
        #remove a specific role from the member. return 0 on success and 1 on failure
        return 0

    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore)
        self.roleModule.resetRoles(name)
        

class RoleModule():
    
    def __init__(self):
        self.roles = {""}

    def getNewRoleScore(self):
        command = "SELECT max(roleCost) FROM roles"
        result = database.record(command)

        if result:
            return result + 20
        return 0

    def newRole(self,role,scoreToGet):
        #add a new role into the database.
        command = "INSERT OR IGNORE INTO roles VALUES((SELECT max(role_id) FROM roles)+1,?1,?2)"
        database.execute(str(command),str(role),scoreToGet)
        return self.safeCommit()
            
    def deleteRole(self,role):
        #delete a role from the database
        command = "DELETE FROM roles WHERE role_name = ?"
        database.execute(str(command),str(role))
        return self.safeCommit()

    def adjustSpecificRole(self,name,role,addRole):
        #if addRole is true, add a specific role to a member, else, remove a specific role from a member. 
        return 0

    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore) ((((do not remove member added roles))))
        shouldHave = self.getRoles(name)

        command = "SELECT member_id FROM members WHERE member_name=?"
        id = database.record(str(command),str(name))
        
        assert id is not None

        for role in shouldHave:#for each role that the member should have, try to insert that role into the database
            command = "INSERT OR IGNORE INTO rolloc VALUES (?,?)"
            database.execute(str(command),int(id[0]),int(role))
        return self.safeCommit()

    def getRoles(self,name,allStats=False):
        #get all roles that member "name" is authorized to have. return list of roles as tuples
        roleList = []
        memberScore = database.record('SELECT ranking_score FROM members WHERE member_name=?',str(name))
        result = database.records('SELECT role_id, role_name, role_cost FROM roles')

        if result is None or memberScore is None:
            return []

        for cell in result:#for each role that a member should have, append it to the list
            if memberScore[0] >= cell[2]:
                roleList.append(cell) if allStats else roleList.append(cell[0])

        return roleList
    
    def safeCommit(self):#runs the commit command while checking if the table was altered at all. return 0 if database was saved, 1 if not
        if database.rowCount() == 1:
            database.commit()
            return 0
        return 1


class MemberModule():

    def addMember(self, name):#insert a member into the members table with member_name = "name", if exists ignore this command
        command = "INSERT OR IGNORE INTO members VALUES ((SELECT max(member_id) FROM members)+1,?,0,0,0)"
        database.execute(str(command),str(name))
        return self.safeCommit()

    def removeMember(self,name):#remove a member from the members table with member_name = "name"
        command = "SELECT member_id FROM members WHERE member_name = ?"
        id = database.record(str(command),str(name))
        
        assert id is not None
        
        command = "DELETE FROM members WHERE member_name = ?"
        database.execute(str(command),str(name))

        command = "DELETE FROM rolloc WHERE Rmember_id = ?"
        database.execute(str(command),int(id))

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


    ##############################################################change this for sentiment ###############################################
        for word in message.split():#for each word in the members chat message, check if it matches a key in the wordDict and adjust score accordingly
            if word in self.wordDict:
                attributeList[self.wordDict[word][0]] += self.wordDict[word][1]

        return attributeList


class ScoreModule():
    ##############################################################change this for sentiment##################################################
    def adjustScore(self,name,aL):#adjust the ranking score of "name" by 1 and each attribute by the amount described by the list "aL"
        command = "UPDATE members SET ranking_score=ranking_score + 1, happy=happy + ?2, angry=angry + ?3, funny=funny + ?4 WHERE member_name=?1"
        database.execute(str(command),str(name),aL[0],aL[1],aL[2])
        database.commit()
        

def main():
  
    #database.execute("DROP TABLE roles")

    #b = BRIAN()

    #print(b.getMRoles('orkandbeans#3110'))

    """
    command = "INSERT OR IGNORE INTO roles VALUES (1,'pleb',0)"
    database.execute(str(command))
    database.commit()
    command = "INSERT OR IGNORE INTO roles VALUES (2,'teamMember',30)"
    database.execute(str(command))
    database.commit()
    command = "INSERT OR IGNORE INTO roles VALUES (3,'admin',50)"
    database.execute(str(command))
    database.commit()"""

    pass
   
if __name__ == "__main__":
    main()
