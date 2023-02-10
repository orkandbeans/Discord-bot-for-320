from db import db as database



class BRIAN():

    def __init__(self):
        self.scoreCalculator = ScoreCalculator()
        self.memberController = MemberController()  

        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT UNIQUE, ranking_score INTEGER)"
        database.execute(createCommand)
        database.commit()


    def botCommand(self,comType,name,message):
        #take a bot command and determine what needs to be changed. comType will tell the method what to do.
        
        if comType == "updateMembers":
            for member in name:
                self.memberController.addMember(member)

        return
    
    def updateScore(self,name,message):
        #change the member "name"'s score based on what they said in their message
        pass

    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore)
        pass

    def adjustRole(self,name,addRole,role):
        #change the member "name" to either add or delete "role" based on addRole
        pass

    def addRemoveMember(self,name,addMember):
        #remove or add a member from the database based on the variable, "addMember"
        pass

    


class MemberController():
    def __init__(self):
        self.roleModule = RoleModule()
        self.memberModule = MemberModule()

    def roleCheck(self,name):
        #check a member's roles from the db and return a list of roles that the member has
        return(0)

    def removeMember(self,name):
        #remove a member from the db based on their name. return 0 on success and 1 on failure
        return(0)
    
    def addMember(self,name):
        #add a member to the db with member_name = "name". return 0 on success and 1 on failure
        self.memberModule.addMember(name)
        return(0)
        
    def addRole(self,name,role):
        #add a specific role to the member. return 0 on success and 1 on failure
        return(0)

    def removeRole(self,name,role):
        #remove a specific role from the member. return 0 on success and 1 on failure
        return(0)
        

class RoleModule():
    
    def adjustSpecificRole(self,name,role,addRole):
        #if addRole is true, add a specific node to a member, else, remove a specific role from a member. 
        pass

    def getRoles(self,name):
        #get all roles that member "name" has. return list of roles
        pass


class MemberModule():

    def addMember(self, name):
        command = "INSERT OR IGNORE INTO members VALUES ((SELECT max(member_id) FROM members)+1,?,0)"
        database.execute(str(command),str(name))
        database.commit()

    def removeMember(self,name):

        command = "DELETE FROM members WHERE member_name = ?"
        database.execute(command,name)
        database.commit()

    def dropDb(self):

        dropCommand = "DROP TABLE members"
        database.execute(dropCommand)
        database.commit()

    def getMember(self,name):

        command = "SELECT * FROM members WHERE member_name = ?"
        database.execute(command,name)




class ScoreCalculator():

    def __init__(self):
        self.scoreModule = ScoreModule()
        self.wordDict = {}
    
    def calculateStr(self,message):
        #calculate the score of a specific string that a member sent
        return(0)

    def changeScore(self,name,extra):
        #increment the member's score by the chat increment amount plus "extra"
        return(0)


class ScoreModule():
    
    def adjustScore(self,name,amount):
        #adjust the score of "name" by "amount" in the database
        command = "UPDATE members SET ranking_score=?2 WHERE member_name=?1"
        database.execute(str(command),name,amount)
        database.commit()
        



def main():
    sc = ScoreModule()
    sc.adjustScore('orkandbeans#3110',0)
    #brian = BRIAN()
    #MemberModule().dropDb()
    #brian.createDb()
    #brian.removeMember("jimmy")
    #brian.addMember("jimmy")
    #brian.addMember("jaden")
   
   
if __name__ == "__main__":
    main()
