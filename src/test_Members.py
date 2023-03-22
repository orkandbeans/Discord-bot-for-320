import unittest
import Ranking
from db import db as database



class TestMemberModule(unittest.TestCase):

    def test_safeCommit(self):
        dropDB(True)
        m = Ranking.MemberModule()
        database.execute("INSERT INTO members VALUES (0,'testPerson',0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,0)

    def test_add_member(self): #like this?
        dropDB()
        b = Ranking.BRIAN()
        result = b.newMember("testPerson")
        self.assertEqual(result,0)

        command = "SELECT * FROM members WHERE member_name='testPerson'"
        result2 = database.record(command)
        self.assertEqual(result2,(1,"testPerson",0,0,0,0,0))


    def test_remove_member(self):
        dropDB()
        b = Ranking.BRIAN()
        m = Ranking.MemberModule()

        database.execute("INSERT INTO members VALUES (0,'testPerson',0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,0)

        result = b.removeMember("testPerson")
        self.assertEqual(result,0)

    @unittest.expectedFailure
    def test_remove_member_invalid(self):
        dropDB()
        b = Ranking.BRIAN()
        m = Ranking.MemberModule()

        database.execute("INSERT INTO members VALUES (0,'testPerson',0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,0)

        result = b.removeMember("invalidName")
        self.assertEqual(result,1)

    def test_get_member(self):
        dropDB(True)
        m = Ranking.MemberModule()

        database.execute("INSERT INTO members VALUES (0,'testPerson2',0,0,0)")
        database.execute("INSERT INTO members VALUES (1,'testPerson',0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,0)

        result = m.getMember("testPerson")
        self.assertEqual(result,(1,"testPerson",0,0,0))

    @unittest.expectedFailure
    def test_get_member_invalid(self):
        dropDB(True)
        m = Ranking.MemberModule()

        database.execute("INSERT INTO members VALUES (0,'testPerson',0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,0)

        result = m.getMember("invalidName")
        self.assertEqual(result,1)

    def test_integrationMemberModule(self):
        #use all methods (or some)
        pass

class TestRoleModule(unittest.TestCase):

    def test_new_role(self):
        pass

    def test_delete_role(self):
        pass

    def test_add_role(self):
        pass

    def test_remove_role(self):
        pass

    def test_add_role_invalid(self):
        pass

    def test_remove_role_invalid(self):
        pass


class TestBot(unittest.TestCase): #how the what do i do in the world

    def what():
        pass


class TestScore(unittest.TestCase): #does this work????????

    def test_white_updateRanking(self):
        pass



def createDB():
    createCommand = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY, member_name TEXT UNIQUE, number_messages INTEGER, ranking_score INTEGER, negative REAL, neutral REAL, Positive REAL)"
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

def dropDB(reset=False):
    
    database.execute("DROP TABLE IF EXISTS rolloc")
    database.execute("DROP TABLE IF EXISTS roles")
    database.execute("DROP TABLE IF EXISTS members")
    database.commit()

    if reset:
        createDB()




if __name__ == '__main__':
    unittest.main()