from db import db as database


class Calculator():

    pass


class Handler():

    def addMember(self, id):

        command = "INSERT INTO members VALUES ((SELECT max(member_id) FROM members)+1,'" + id + "',0)"
        database.execute(command)
        database.commit()

    def removeMember(self,id):

        command = "DELETE FROM members WHERE member_name = '" + id + "'"
        database.execute(command)
        database.commit()

    def createDb(self):

        createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT, ranking_score INTEGER)"
        database.execute(createCommand)
        database.commit()

    def dropDb(self):

        dropCommand = "DROP TABLE members"
        database.execute(dropCommand)
        database.commit()


class RoleManager():

    pass


class TimeMachine():

    pass



def main():

    
    handler = Handler()
    #handler.dropDb()
    handler.createDb()
    #handler.removeMember("jimmy")
    #handler.addMember("jimmy")
    #handler.addMember("jaden")
    





if __name__ == "__main__":
    main()
