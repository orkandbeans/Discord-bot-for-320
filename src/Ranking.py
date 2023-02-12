from db import db as database



class BRIAN():

    def __init__(self):
        self.scoreCalculator = ScoreCalculator()
        self.memberController = MemberController()  

        #when a BRIAN is created, make sure there is a database to access. 
        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT UNIQUE, ranking_score INTEGER, happy INTEGER, angry INTEGER, funny INTEGER)"
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
        

    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore)
        pass

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
        
    def addRole(self,name,role):
        #add a specific role to the member. return 0 on success and 1 on failure
        return 0

    def removeRole(self,name,role):
        #remove a specific role from the member. return 0 on success and 1 on failure
        return 0
        

class RoleModule():
    
    def adjustSpecificRole(self,name,role,addRole):
        #if addRole is true, add a specific node to a member, else, remove a specific role from a member. 
        return 0

    def getRoles(self,name):
        #get all roles that member "name" has. return list of roles
        return []


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

    def safeCommit(self):
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
    mm = MemberModule()
    mm.removeMember('Logansclone#1316')

    pass
   
if __name__ == "__main__":
    main()
