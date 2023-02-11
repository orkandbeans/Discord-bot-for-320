from db import db as database



class BRIAN():

    def __init__(self):
        self.scoreCalculator = ScoreCalculator()
        self.memberController = MemberController()  

        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT UNIQUE, ranking_score INTEGER, happy INTEGER, angry INTEGER, funny INTEGER)"
        database.execute(createCommand)
        database.commit()


    def botCommand(self,comType,name,message):
        #take a bot command and determine what needs to be changed. comType will tell the method what to do.
        
        if comType == "updateMembers":
            for member in name:
                self.memberController.addMember(member)
        
        if comType == "updateScore":
            self.scoreCalculator.changeScore(name,self.scoreCalculator.calculateStr(message))

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
        command = "INSERT OR IGNORE INTO members VALUES ((SELECT max(member_id) FROM members)+1,?,0,0,0,0)"
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
        self.wordDict = {"please":(0,5),"hate":(1,5),"LOL":(2,5)}
    
    def changeScore(self,name,attributeList):
        #increment the member's score by the chat increment amount plus "extra"

        self.scoreModule.adjustScore(name,attributeList)

        return(0)

    def calculateStr(self,message):
        #calculate the score of a specific string that a member sent
        attributeList = [0,0,0] #this is a list that tracks how nice, mean, and funny someone is. [nice, mean, funny] 

        for word in message.split():
            if word in self.wordDict:
                attributeList[self.wordDict[word][0]] += self.wordDict[word][1]

        return(attributeList)


class ScoreModule():
    
    def adjustScore(self,name,aL):
        #adjust the score of "name" by "amount" in the database
        command = "UPDATE members SET ranking_score=ranking_score + 1, happy=happy + ?2, angry=angry + ?3, funny=funny + ?4 WHERE member_name=?1"
        database.execute(str(command),str(name),aL[0],aL[1],aL[2])
        database.commit()
        



def main():
    pass
   
if __name__ == "__main__":
    main()
