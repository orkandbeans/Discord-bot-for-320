from db import db as database



class BRIAN():

    def __init__(self):
        self.scoreCalculator = ScoreCalculator()
        self.roleController = RoleController()




    
        


class RoleController():





    pass


class RoleModule():

    def addMember(self, id):

        command = "INSERT INTO members VALUES ((SELECT max(member_id) FROM members)+1,?,0)"
        database.execute(command,id)
        database.commit()

    def removeMember(self,id):

        command = "DELETE FROM members WHERE member_name = ?"
        database.execute(command,id)
        database.commit()

    def createDb(self):

        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT, ranking_score INTEGER)"
        database.execute(createCommand)
        database.commit()

    def dropDb(self):

        dropCommand = "DROP TABLE members"
        database.execute(dropCommand)
        database.commit()



class ScoreCalculator():

    
    pass

class ScoreModule():
    
    pass

class WordDict():

    pass



def main():

    
    brian = RoleModule()
    #brian.dropDb()
    brian.createDb()
    brian.removeMember("jimmy")
    #brian.addMember("jimmy")
    #brian.addMember("jaden")
   
   
if __name__ == "__main__":
    main()
