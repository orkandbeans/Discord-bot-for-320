import unittest
import Ranking
from db import dbFT as database



class TestMemberModule(unittest.TestCase):

    def test_white_safeCommit(self):
        #whitebox test with complete coverage
        """
        def safeCommit(self):#runs the commit command while checking if the table was altered at all. return 0 if database was saved, 1 if not
            if self.database.rowCount() != 0:
                self.database.commit()
                return 0
            return 1
        """
        #insert a member into the database, commit if the row count changed
        dropDB(reset=True)
        m = Ranking.MemberModule(database)
        database.execute("INSERT INTO members VALUES (0,'testPerson',0,0,0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,0)#A value of 0 should be returned if the database was changed and commited

        #insert the same values into the database (violating the unique constraint) which will not change the database
        database.execute("INSERT OR IGNORE INTO members VALUES (0,'testPerson',0,0,0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,1)#A value of 1 should be returned if the database was not changed at all

    def test_new_member(self):
        #acceptance test
        dropDB()
        b = Ranking.BRIAN(testMode=True)
        result = b.newMember("testPerson")
        self.assertEqual(result,0)#return 0 on successeful add and commit of the database

        #this will directly check if the database added the member correctly
        command = "SELECT * FROM members WHERE member_name='testPerson'"
        result2 = database.record(command)
        self.assertEqual(result2,(1,"testPerson",0,0,0,0,0))


    def test_delete_member(self):
        #acceptance test
        dropDB()
        b = Ranking.BRIAN(testMode=True)

        #use sqlite code to insert a member
        database.execute("INSERT INTO members VALUES (0,'testPerson',0,0,0,0,0)")
        database.commit()

        #delete member with my method
        result = b.deleteMember("testPerson")
        self.assertEqual(result,0)#should return a 0 for success

        #remove a member that does not exists for an error
        result = b.deleteMember("invalidName")
        self.assertEqual(result,1)

        #select the member to see if it is in the database or not (None)
        command = "SELECT * FROM members WHERE member_name='testPerson'"
        result2 = database.record(command)
        self.assertEqual(result2,None)

        #remove a member that does not exists for an error
        result = b.deleteMember("invalidName")
        self.assertEqual(result,1)


    def test_get_member(self):
        #whitebox test with complete coverage
        """
        def getMember(self,name):#get the member with member_name = "name"
            command = "SELECT * FROM members WHERE member_name = ?"
            result = self.database.record(str(command),str(name))
            
            if result is None:
                return 1

            return result
        """
        dropDB(True)
        m = Ranking.MemberModule(database)

        #insert two members into the database
        database.execute("INSERT INTO members VALUES (0,'testPerson2',0,0,0,0,0)")
        database.execute("INSERT INTO members VALUES (1,'testPerson',0,0,0,0,0)")
        result = m.safeCommit()
        self.assertEqual(result,0)

        #get the data of testPerson and verify the results
        result = m.getMember("testPerson")
        self.assertEqual(result,(1,"testPerson",0,0,0,0,0))

        #get a fake member from the database to reach the if statement
        result = m.getMember("invalidName")
        self.assertEqual(result,1)
        
    def test_isMember(self):
        #whitebox test with complete coverage
        """
        def isMember(self,name):
            #check if name is a member in the database
            result = self.memberModule.getMember(name)
            return True if result != 1 else False
        """
        dropDB(True)
        mc = Ranking.MemberController(database)

        result = mc.isMember("testPerson")
        self.assertFalse(result)

        #insert two members into the database
        database.execute("INSERT INTO members VALUES (0,'testPerson2',0,0,0,0,0)")
        database.execute("INSERT INTO members VALUES (1,'testPerson',0,0,0,0,0)")
        database.commit()

        result = mc.isMember("testPerson")
        self.assertTrue(result)

        result = mc.isMember("testPerson2")
        self.assertTrue(result)

        result = mc.isMember("invalidName")
        self.assertFalse(result)

              

class TestRoleModule(unittest.TestCase):

    def test_getNewRoleScore(self):
        #whitebox test with complete coverage
        """
        def getNewRoleScore(self):
            check = "SELECT role_cost FROM roles"
            result = self.database.record(check)
            if result is None:
                return 0
            
            command = "SELECT MAX(role_cost) FROM roles"
            result = self.database.record(command)
            
            return result[0] + 20
        """
        dropDB(True)
        rm = Ranking.RoleModule(database)

        #with nothing in the database, 0 should be returned
        result = rm.getNewRoleScore()
        self.assertEqual(result,0)

        #use sqlite code to insert a member
        database.execute("INSERT INTO roles VALUES (1,'testRole',1)")
        database.execute("INSERT INTO roles VALUES (2,'testRole2',12)")
        database.commit()

        #with something in the database, the highest score + 20 should be returned
        result = rm.getNewRoleScore()
        self.assertEqual(result,32)

    def test_new_role(self):
        #acceptance test
        dropDB()
        b = Ranking.BRIAN(testMode=True)
        
        #add roles to the database
        result = b.newRole("testRole",10)
        self.assertEqual(result,0)

        result = b.newRole("testRole2",-1)
        self.assertEqual(result,0)

        #this will directly check if the database added the role correctly
        command = "SELECT * FROM roles WHERE role_name='testRole'"
        result2 = database.record(command)
        self.assertEqual(result2,(1,'testRole',10))

        command = "SELECT * FROM roles WHERE role_name='testRole2'"
        result2 = database.record(command)
        self.assertEqual(result2,(2,'testRole2',30))

    def test_delete_role(self):
        #acceptance test
        dropDB()
        b = Ranking.BRIAN(testMode=True)

        #use sqlite code to insert a role
        database.execute("INSERT INTO roles VALUES (0,'testRole',0)")
        database.commit()

        #delete role with my method
        result = b.deleteRole("testRole")
        self.assertEqual(result,0)#should return a 0 for success

        #select the role to see if it is in the database or not (None)
        command = "SELECT * FROM roles WHERE role_name='testRole'"
        result2 = database.record(command)
        self.assertEqual(result2,None)

    def test_add_role(self):
        #acceptance test
        dropDB()
        b = Ranking.BRIAN(testMode=True)

        #use sqlite to inssert a member and role
        database.execute("INSERT INTO members VALUES (0,'testMember',0,0,0,0,0)")
        database.execute("INSERT INTO roles VALUES (1,'testRole',0)")
        database.commit()

        #check that no invalid configurations will add the role
        result = b.addMemberRole("InvalidName","testMember")
        self.assertEqual(result,1)

        result = b.addMemberRole("testRole","InvalidName")
        self.assertEqual(result,1)

        result = b.addMemberRole("InvalidName","InvalidName2")
        self.assertEqual(result,1)
        
        #should return None from no role being added
        command = "SELECT * FROM rolloc WHERE Rmember_id = 0"
        result2 = database.record(command)
        self.assertEqual(result2,None)

        #allocate that role to the member 
        result = b.addMemberRole("testRole","testMember")
        self.assertEqual(result,0)

        #check if the member has the role in the database
        command = "SELECT * FROM rolloc WHERE Rmember_id = 0"
        result2 = database.record(command)
        self.assertEqual(result2,(0,1))

    def test_remove_role(self):
        #acceptance test
        dropDB()
        b = Ranking.BRIAN(testMode=True)

        #use sqlite to insert a member,role, and give the member that role
        database.execute("INSERT INTO members VALUES (0,'testMember',0,0,0,0,0)")
        database.execute("INSERT INTO roles VALUES (1,'testRole',0)")
        database.execute("INSERT INTO rolloc VALUES (0,1)")
        database.commit()

        #try to remove the role from the member with invalid names
        result = b.removeMemberRole("InvalidName","testMember")
        self.assertEqual(result,1)

        result = b.removeMemberRole("testRole","InvalidName")
        self.assertEqual(result,1)

        result = b.removeMemberRole("InvalidName","InvalidName2")
        self.assertEqual(result,1)

        #check to see if it was removed
        command = "SELECT * FROM rolloc WHERE Rmember_id = 0"
        result2 = database.record(command)
        self.assertEqual(result2,(0,1))

        #try to remove that role allocation from the member correctly
        result = b.removeMemberRole("testRole","testMember")
        self.assertEqual(result,0)

        #check that the role is not allocated to the member
        command = "SELECT * FROM rolloc WHERE Rmember_id = 0"
        result2 = database.record(command)
        self.assertEqual(result2,None)

    def test_integration_newrole(self):
        #this is a bottom up integration test that has full coverage of the newRole 
        #   method in class MemberController and complete coverage of the getNewRoleScore 
        #   method in the class RoleModule 
        dropDB()
        b = Ranking.BRIAN(testMode=True)

        result = b.newRole("testRole",10)
        self.assertEqual(result,0)#return 0 on successeful add and commit of the database

        #this will directly check if the database added the member correctly
        command = "SELECT * FROM roles WHERE role_name='testRole'"
        result2 = database.record(command)
        self.assertEqual(result2,(1,'testRole',10))

        result = b.newRole("testRole2",-1)
        self.assertEqual(result,0)#return 0 on successeful add and commit of the database

        #this will directly check if the database added the member correctly
        command = "SELECT * FROM roles WHERE role_name='testRole2'"
        result2 = database.record(command)
        self.assertEqual(result2,(2,'testRole2',30))

        dropDB(True)
        result = b.newRole("testRole3",-1)
        self.assertEqual(result,0)#return 0 on successeful add and commit of the database

    def test_getRoles(self):
        #acceptance test
        dropDB(True)
        rm = Ranking.RoleModule(database)

        #test for nothing in the database, should return no roles
        result = rm.getRoles('testMember')
        self.assertEqual(result,[])

        #use sqlite to insert a member
        database.execute("INSERT INTO members VALUES (0,'testMember',0,10,0,0,0)")

        #getroles should return no viable roles
        result = rm.getRoles('testMember')
        self.assertEqual(result,[])

        #insert roles into the database
        database.execute("INSERT INTO roles VALUES (1,'testRole',0)")
        database.execute("INSERT INTO roles VALUES (2,'testRole2',5)")
        database.execute("INSERT INTO roles VALUES (3,'testRole3',50)")
        database.commit()

        #with allStats disabled, the role_id's are given, otherwise, all role information is given
        result = rm.getRoles('testMember')
        self.assertEqual(result,[1,2])

        result = rm.getRoles('testMember',allStats=True)
        self.assertEqual(result,[(1,'testRole',0),(2,'testRole2',5)])

class TestScore(unittest.TestCase): 

    def test_updateRankingScore(self):
        #acceptance test
        dropDB(True)
        sm = Ranking.ScoreModule(database)

        #use sqlite to insert a member
        database.execute("INSERT INTO members VALUES (0,'testMember',0,0,0,0,0)")
        database.commit()

        #update the ranking score, this will increase it by 11.333 repeating
        sm.updateRankingScore('testMember',[1,2,3])

        #Round 11.333 to the 15th place to match pyhton's rounding and compare the output
        result = database.record("SELECT * FROM members WHERE member_name='testMember'")
        self.assertEqual(result,(0,'testMember',0,11.333333333333334,0,0,0))

    def test_adjustScore(self):
        #acceptance test
        dropDB(True)
        sm = Ranking.ScoreModule(database)

        #use sqlite to insert a member
        database.execute("INSERT INTO members VALUES (0,'testMember',0,0,0,0,0)")
        database.commit()

        #use my method to change the database
        sm.adjustScore('testMember',[1,2,3])

        #verify the correct output of the scores
        result = database.record("SELECT * FROM members WHERE member_name='testMember'")
        self.assertEqual(result,(0,'testMember',1,0,1,2,3))

        #do it again to add to the existing score
        sm.adjustScore('testMember',[1,2,3])

        #verify the correct output of the scores
        result = database.record("SELECT * FROM members WHERE member_name='testMember'")
        self.assertEqual(result,(0,'testMember',2,0,2,4,6))

        





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
    #this is made to delete all information in the database for the tests
    database.execute("DROP TABLE IF EXISTS rolloc")
    database.execute("DROP TABLE IF EXISTS roles")
    database.execute("DROP TABLE IF EXISTS members")
    database.commit()

    if reset:
        #reset will create the tables again
        createDB()




if __name__ == '__main__':
    unittest.main()