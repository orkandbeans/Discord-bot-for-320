import nltk
from nltk.sentiment import SentimentIntensityAnalyzer as SIA



class BRIAN:

    def __init__(self, testMode=False):
        

        if testMode:
            from db import dbFT as database
        else:
            from db import db as database

        self.scoreCalculator = ScoreCalculator(database)
        self.memberController = MemberController(database)

        #when a BRIAN is created, make sure there is a database to access. 
        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT UNIQUE, number_messages INTEGER, ranking_score INTEGER, negative REAL, neutral REAL, Positive REAL, history INTEGER)"
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
        
    def shouldSearch(self):
        #check if the bot should search the history of the channels or not
        return self.memberController.shouldHistory()
        

    def historyCheck(self,name):
        #check if this members history has been reviewed or not
        result = self.memberController.getMemberHistory(name)
        return result

    def historyUpdate(self):
        #update this members history 
        return self.memberController.updateMemberHistory()

    def initRoles(self,roleList):
        #add each role into the database for use.
        for role in roleList:
            self.memberController.newRole(role)

    def updateMembers(self,memberList):
        #add each member of the discord to the database and update their roles.
        for member in memberList:
            self.newMember(member)
                
    def updateScore(self,name,message):
        #change the member "name"'s score based on what they said in their message
        if self.scoreCalculator.changeScore(name,message) != 0:
            print(f"ERROR: Failed to change {name}'s score.")
        self.memberController.resetRoles(name)

    def getMRoles(self,name):
        #get all roles that a member has and return a list of role names.
        return self.memberController.roleFind(name)
    
    def newMember(self,name):
        #add a member to the database
        if self.memberController.addMember(name) != 0:
            print(f"ERROR: Failed to add {name} to the database.")
            return 1
        return 0
    
    def deleteMember(self,name):
        #remove a member from the database
        if self.memberController.removeMember(name) != 0:
            print(f"ERROR: Failed to remove {name} from the database.")
            return 1
        return 0
    
    def newRole(self,role,score=0):
        #add a role to the database
        if self.memberController.newRole(role,score) != 0:
            print(f"ERROR: Failed to add {role} role to the database.")
            return 1
        return 0
    
    def deleteRole(self,role):
        #remove a role from the database
        if self.memberController.deleteRole(role) != 0:
            print(f"ERROR: Failed to remove {role} role from the database.")
            return 1
        return 0
    
    def addMemberRole(self,role,name):
        #add a role to a member in the database
        assert isinstance(role,str), 'Argument is not a string.'
        assert isinstance(name,str), 'Argument is not a string.'

        if self.memberController.isMember(name):
            if self.memberController.addMemberRole(name,role) != 0:
                print(f"ERROR: Failed to give {name} the role {role}.")
                return 1
            return 0
        
        print(f"ERROR: {name} was not found in the database.")
        return 1
    
    def removeMemberRole(self,role,name):
        #remove a role from a member in the database
        assert isinstance(role,str), 'Argument is not a string.'
        assert isinstance(name,str), 'Argument is not a string.'

        if self.memberController.isMember(name):
            if self.memberController.removeMemberRole(name,role) != 0:
                print(f"ERROR: Failed to remove the role {role} from {name}.")
                return 1
            return 0

        print(f"ERROR: {name} was not found in the database.")
        return 1
    
    def getMemberRankList(self):
        #gets the list of members that are in the database in ranking score order.
        result = self.memberController.getRanking()
        return result


class MemberController:
    def __init__(self,database):
        self.roleModule = RoleModule(database)
        self.memberModule = MemberModule(database)

    def getMemberHistory(self,name):
        #get the history value from a member in the database
        return self.memberModule.getHistory(name)

    def updateMemberHistory(self):
        #update the history value from a member in the database
        return self.memberModule.updateHistory()

    def shouldHistory(self):
        #check if the history stat is true for all members
        result = self.memberModule.getAllMembers()

        for member in result:
            if member[7] == 0:
                return True
        return False


    def roleFind(self,name):
        #check a member's roles from the db and return a list of roles that the member has
        result = self.roleModule.getRoles(name,True)
        roleList = []
        for role in result:
            roleList.append(role[1])

        return roleList

    def getRanking(self):
        #creates a ranked list for all the members in the discord
        result = self.memberModule.getAllMembers()
        rankings = []
        for member in result:
            if member[3] != 0:
                rankings.append([member[3],member[1]])
        rankings.sort(reverse=True)

        return rankings

    def removeMember(self,name):
        #remove a member from the db based on their name. return 0 on success and 1 on failure
        if self.isMember:
            return self.memberModule.removeMember(name)
        return 1     
            
    
    def addMember(self,name):
        #add a member to the db with member_name = "name".
        result = self.memberModule.addMember(name)
        if result == 0:
            print("Added " + str(name) + " to the database.")
        else:
            return 1

        #reset the member's roles to init them in the role system
        self.roleModule.resetRoles(name)
        return 0
        
    def isMember(self,name):
        #check if name is a member in the database
        result = self.memberModule.getMember(name)
        return True if result != 1 else False
    
    def isRole(self,role):
        #check if role is a role in the database
        result = self.roleModule.getRole(role)
        return True if result != 1 else False
        
    def newRole(self,role,scoreToGet=-1):
        #adds a new role to the database as well as the score needed to get the role.
        if scoreToGet == -1:
            scoreToGet = self.roleModule.getNewRoleScore()
            
        return self.roleModule.newRole(role,scoreToGet)
        
    
    def deleteRole(self,role):
        #calls the rolemodule to delete a role from the database.
        return self.roleModule.deleteRole(role)

    def addMemberRole(self,name,role):
        #add a specific role to the member. return 0 on success and 1 on failure
         
        if self.isMember(name) and self.isRole(role):
            result = self.roleModule.adjustSpecificRole(name,role,True)
            return result
        
        return 1

    def removeMemberRole(self,name,role):
        #remove a specific role from the member. return 0 on success and 1 on failure
        if self.isMember(name) and self.isRole(role):
            result = self.roleModule.adjustSpecificRole(name,role,False)
            return result

        return 1
    
    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore)
        self.roleModule.resetRoles(name)
        

class RoleModule:
    
    def __init__(self,database):
        self.database = database
        

    def getNewRoleScore(self):
        check = "SELECT role_cost FROM roles"
        result = self.database.record(check)
        if result is None:
            return 0
        
        command = "SELECT MAX(role_cost) FROM roles"
        result = self.database.record(command)
        
        return result[0] + 20

    def newRole(self,role,scoreToGet):
        #add a new role into the database.
        command = "INSERT OR IGNORE INTO roles VALUES((SELECT max(role_id) FROM roles)+1,?1,?2)"
        self.database.execute(str(command),str(role),scoreToGet)
        return self.safeCommit()
            
    def deleteRole(self,role):
        #delete a role from the database
        command = "SELECT role_id FROM roles WHERE role_name = ?"
        roleId = self.database.record(str(command), str(role))
        
        command = "DELETE FROM rolloc WHERE Rrole_id = ?"
        self.database.execute(str(command),int(roleId[0]))

        command = "DELETE FROM roles WHERE role_name = ?"
        self.database.execute(str(command),str(role))
    
        return self.safeCommit()

    def adjustSpecificRole(self,name,role,addRole):
        #if addRole is true, add a specific role to a member, else, remove a specific role from a member. 

        command = "SELECT member_id FROM members WHERE member_name=?"
        memId = self.database.record(str(command),str(name))
        command = "SELECT role_id FROM roles WHERE role_name=?"
        rolId = self.database.record(str(command),str(role))
        
        memId = memId[0]
        rolId = rolId[0]

        assert memId is not None
        assert rolId is not None
        
        command = "INSERT INTO rolloc VALUES (?,?)" if addRole else "DELETE FROM rolloc WHERE Rmember_id=? AND Rrole_id=?"
        self.database.execute(str(command),str(memId),str(rolId))

        return self.safeCommit()

    def resetRoles(self,name):
        #reset the roles of the member back to default (given their rankingscore) ((((do not remove member added roles))))
        shouldHave = self.getRoles(name)

        command = "SELECT member_id FROM members WHERE member_name=?"
        id = self.database.record(str(command),str(name))
        
        assert id is not None

        for role in shouldHave:#for each role that the member should have, try to insert that role into the database
            command = "INSERT OR IGNORE INTO rolloc VALUES (?,?)"
            self.database.execute(str(command),int(id[0]),int(role))
        self.database.commit()

    def getRoles(self,name,allStats=False):
        #get all roles that member "name" is authorized to have. return list of roles as tuples
        roleList = []
        memberScore = self.database.record('SELECT ranking_score FROM members WHERE member_name=?',str(name))
        result = self.database.records('SELECT role_id, role_name, role_cost FROM roles')

        if result is None or memberScore is None:
            return []

        for cell in result:#for each role that a member should have, append it to the list
            if memberScore[0] >= cell[2]:
                roleList.append(cell) if allStats else roleList.append(cell[0])

        return roleList
    
    def getRole(self,role):#get the role with role_name = "role"
        command = "SELECT * FROM roles WHERE role_name = ?"
        result = self.database.record(str(command),str(role))
        
        if result is None:
            return 1

        return result
    
    def safeCommit(self):#runs the commit command while checking if the table was altered at all. return 0 if database was saved, 1 if not
        if self.database.rowCount() == 1:
            self.database.commit()
            return 0
        return 1


class MemberModule:

    def __init__(self,database):
        self.database = database

    def updateHistory(self):

        command = "UPDATE members SET history = 1"
        self.database.execute(str(command))
        self.database.commit()
        

    def getHistory(self,name):
        command = "SELECT history FROM members WHERE member_name = ?"
        result = self.database.record(str(command),str(name))
        if result is None:
            return 0
        return result[0]
    
    def addMember(self, name):#insert a member into the members table with member_name = "name", if exists ignore this command
        command = "INSERT OR IGNORE INTO members VALUES ((SELECT max(member_id) FROM members)+1,?,0,0,0,0,0,0)"
        self.database.execute(str(command),str(name))
        return self.safeCommit()

    def removeMember(self,name):#remove a member from the members table with member_name = "name"
        command = "SELECT member_id FROM members WHERE member_name = ?"
        id = self.database.record(str(command),str(name))
        
        if id is None:
            return 1

        command = "DELETE FROM rolloc WHERE Rmember_id = ?"
        self.database.execute(str(command),id[0])

        command = "DELETE FROM members WHERE member_name = ?"
        self.database.execute(str(command),str(name))

        return self.safeCommit()

    def getMember(self,name):#get the member with member_name = "name"
        command = "SELECT * FROM members WHERE member_name = ?"
        result = self.database.record(str(command),str(name))
        
        if result is None:
            return 1

        return result
    
    def getAllMembers(self):
        command = "SELECT * FROM members"
        result = self.database.records(str(command))
        return result

    def safeCommit(self):#runs the commit command while checking if the table was altered at all. return 0 if database was saved, 1 if not
        if self.database.rowCount() != 0:
            self.database.commit()
            return 0
        return 1
    
    

class ScoreCalculator:

    def __init__(self,database):#store the word dictionary in self.wordDict in order to rank the attribute scores of each member's messages
        self.scoreModule = ScoreModule(database)

        nltk.download('vader_lexicon')
        self.analizer = SIA()
    
    def changeScore(self,name,message):#increment the member's score by the chat increment amount and increment each attribute score by the values in "attributeList"
        attributeList = self.calculateStr(message)
        self.scoreModule.adjustScore(name,attributeList)
        self.scoreModule.updateRankingScore(name,attributeList)
        return 0

    def calculateStr(self,message):#calculate the score of a specific string that a member sent
        result = self.analizer.polarity_scores(message)
        attributes = [result['neg'],result['neu'],result['pos']]

        return attributes
    

class ScoreModule:

    def __init__(self,database):
        self.database = database

    def adjustScore(self,name,aL):#adjust the ranking score of "name" by 1 and each attribute by the amount described by the list "aL"
        command = "UPDATE members SET number_messages=number_messages + 1, ranking_score=ranking_score, negative=negative + ?2, neutral=neutral + ?3, positive=positive + ?4, history=history WHERE member_name=?1"
        self.database.execute(str(command),str(name),aL[0],aL[1],aL[2])
        self.database.commit()
    
    def updateRankingScore(self,name,aL):
        
        assert all(isinstance(f, float) or isinstance (f,int) for f in aL)

        negScore = aL[0] / 3
        neuScore = aL[1]
        posScore = aL[2] * 3
        
        rankingScore = negScore + neuScore + posScore

        command = "UPDATE members SET number_messages=number_messages, ranking_score=ranking_score + ?2, negative=negative, neutral=neutral, positive=positive, history=history WHERE member_name=?1"
        self.database.execute(str(command),str(name),rankingScore)
        self.database.commit()
        

def main():
    b = BRIAN()
    result = b.shouldSearch()
    print(result)
if __name__ == "__main__":
    main()
