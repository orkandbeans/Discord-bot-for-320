import unittest
import os
from unittest.mock import MagicMock, patch, Mock

from jeopardy import *

class TestJeopardy(unittest.TestCase):

    def test_category(self):    #acceptance test, tests that function is able to pick out categories from the data file
        result = GameStart.randomcategory(random.randint(0, 1000))
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)



    def test_start_game(self):   #White box test with complete coverage for making database, adding users, checking users
        """
        def start_game(self, user_id, server_id):
            #Check if the user exists in the database
            rows = self.conn.execute("SELECT User_id, Server_id, isInGame FROM Jeopardy").fetchall()
            print(rows)
            if not self.user_exists(user_id, server_id):
                #If the user does not exist, add them to the database
                self.add_user(user_id, server_id)
                self.update_is_in_game(user_id, server_id, 1)
                rows = self.conn.execute("SELECT User_id, Server_id, isInGame FROM Jeopardy").fetchall()
                print(rows)
                return True
            else:
                #If the user does exist, check if isInGame is set to 1
                if self.is_in_game(user_id, server_id):
                    print("User is already in a game.")
                    return False
                else:
                    self.update_is_in_game(user_id, server_id, 1)
                    return True
        """
        self.db = JeopardyData()

        #Test starting a new game for a user that doesn't exist in the database
        result = self.db.start_game(1234, 5678)
        self.assertTrue(result)

        #Check if the user is now marked as in a game
        isInGame = \
        self.db.conn.execute("SELECT isInGame FROM Jeopardy WHERE User_id=1234 AND Server_id=5678").fetchone()[0]
        self.assertEqual(isInGame, 1)

        #Test starting a game for a user that already exists in the database and is already in a game
        result = self.db.start_game(1234, 5678)
        self.assertFalse(result)
        self.db.conn.close()



    def test_update_is_in_game(self): #white box test to test the ability to update the players status in the database
        """
        def update_is_in_game(self, user_id, server_id, value):
            try:
                self.database.execute("UPDATE Jeopardy SET isInGame = ? WHERE User_id = ? AND Server_id = ?",
                                      (value, user_id, server_id))
                self.conn.commit()
                print("isInGame value updated in Jeopardy table.")

            except sqlite3.Error as error:
                print("Error updating isInGame value for user in Jeopardy table:", error)
        """
        self.db = JeopardyData()
        #Add a test user to the Jeopardy table
        user_id = 123
        server_id = 456
        self.db.database.execute("INSERT INTO Jeopardy (User_id, Server_id, isInGame) VALUES (?, ?, ?)",
                                 (user_id, server_id, 1))
        self.db.conn.commit()

        #Call the function with a value of 0 to update the isInGame column
        self.db.update_is_in_game(user_id, server_id, 0)

        #Check that the isInGame column was updated to 0
        cur = self.db.conn.cursor()
        cur.execute("SELECT isInGame FROM Jeopardy WHERE User_id = ? AND Server_id = ?", (user_id, server_id))
        result = cur.fetchone()[0]
        self.assertEqual(result, 0)
        self.db.conn.close()



    def test_save_question(self):   #acceptance test
        #Test with a category that exists in the data
        category = "HISTORY"
        result = GameStart.savequestion(category)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for question in result:
            self.assertEqual(question["category"], category)

        #Test with a category that doesn't exist in the data
        category = "INVALID CATEGORY"
        result = GameStart.savequestion(category)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)



    def test_save_category(self):   #Integration Test, Testing the save question function paired with save category function, Big Bang Method
        self.category = "HISTORY"
        self.file_path = "jeopardydata.json"
        # Call the function to save the category
        GameStart.savecategory(self.category)

        # Check that the file was created and contains data
        self.assertTrue(os.path.exists(self.file_path))
        with open(self.file_path, "r") as file:
            data = json.load(file)
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)

            # Check that the data contains the correct category
            for question in data:
                self.assertEqual(question["category"], self.category)
        if os.path.exists(self.file_path):
            os.remove(self.file_path)



    def test_updatetable(self): #white box test, testing the ability to update the gameboard when selecting questions
        """    def updatetable(categories, category_to_remove,
                        value_to_delete):  # update the table message, save the deletions so game can progress
            values = [200, 400, 600, 800, 1000]
            value_index = values.index(value_to_delete)

            with open("categorystate.json", "r") as f:
                current_categories = json.load(f)
            current_categories[category_to_remove][value_index] = None

            with open("categorystate.json", "w") as f:
                json.dump(current_categories, f)

            message = "```\nCategories:\n"
            longest_category_length = max(len(category) for category in categories)
            for i, category in enumerate(categories):
                message += category + " " * (longest_category_length - len(category)) + "\t\t"
                for value in values:
                    if current_categories.get(category, [None, None, None, None, None])[values.index(value)] is None:
                        message += "     \t"
                    else:
                        message += str(value) + "\t"
                message += "\n"
            message += "```"
            return message
            """
        #Create a test file with some initial data
        with open("categorystate.json", "w") as file:
            categories = {"Category A": [200, 400, 600, 800, 1000], "Category B": [200, 400, 600, 800, 1000]}
            json.dump(categories, file)

        #Call the function to update the table
        categories_to_test = ["Category A", "Category B"]
        category_to_remove = "Category A"
        value_to_delete = 600
        expected_output = "```\nCategories:\nCategory A              \t\t200\t400\t    \t800\t1000\t\nCategory B              \t\t200\t400\t600 \t800\t1000\t\n```"
        output = GameBoard.updatetable(categories_to_test, category_to_remove, value_to_delete)

        #Check that the file was updated correctly
        with open("categorystate.json", "r") as file:
            current_categories = json.load(file)
            expected_categories = {"Category A": [200, 400, None, 800, 1000], "Category B": [200, 400, 600, 800, 1000]}
            self.assertEqual(current_categories, expected_categories)



    def test_pickcategory(self):    #white box testing, testing the ability for the user to pick questions
        """def pickcategory(
                input):  # verify the user picked a proper category and value, it must exist for it to return true
            try:
                categoryusermsg, valueusermsg = input.split("# ")  # user must type "Category# Value"
                #  print(categoryusermsg)
                #  print(valueusermsg)
                with open("categorystate.json", "r") as file:
                    current_categories = json.load(file)
                    # print("categories found")
                    # print(current_categories)
                    values = [200, 400, 600, 800, 1000]
                    value_index = values.index(int(valueusermsg))
                    if current_categories[categoryusermsg][
                        value_index] is None:  # make sure user picks unique categories and not a previously selected one
                        return False
                    else:
                        return True
            except:
                return False"""
        current_categories = {
            "VIETNAM": [200, 400, 600, 800, 1000]
        }
        with open("categorystate.json", "w") as file:
            json.dump(current_categories,file)
        category_name = "VIETNAM"

        #Test with valid category and value
        input_str = f"{category_name}# 200"
        print("input : " + input_str)
        result = Input.pickcategory(input_str)
        self.assertEqual(result, True)

        #Test with invalid format
        input_str = f"{category_name} 200"
        result = Input.pickcategory(input_str)
        self.assertEqual(result, False)

        #Test with invalid category
        input_str = f"Invalid Category# 200"
        result = Input.pickcategory(input_str)
        self.assertEqual(result, False)

        #Test with invalid value
        input_str = f"{category_name}# 3000"
        result = Input.pickcategory(input_str)
        self.assertEqual(result, False)

        #Test with previously selected category
        current_categories[category_name][0] = None
        input_str = f"{category_name}# 200"
        result = Input.pickcategory(input_str)
        self.assertEqual(result, True)



    def test_startgame_custom(self):    #white box test, testing the ability to collect all the chosen categories with associated values
        """def startgame(command, numberofcategories):  # , username, channel):

            command = command.lower()
            if command == 'custom':  # Custom Game Solo: In Progress
                #    print(f"{username} from: ({channel})")
                with open("jeopardydata.json", "w") as file:  # empty file first
                    myselectcategory = [None] * int(numberofcategories)
                    for i in range(int(numberofcategories)):
                        myrand = random.randint(0, 1000)
                        selectcategory = GameStart.randomcategory(myrand)
                        GameStart.savecategory(selectcategory)
                        print(str(selectcategory) + " " + str(i) + " " + str(myrand) + " " + str(numberofcategories))
                        myselectcategory[i] = str(selectcategory)
                        questions = GameStart.savequestion(selectcategory)
                return (myselectcategory)"""
        #Set up test parameters
        command = 'custom'
        numberofcategories = 5
        #Open the file and pass the file object to startgame function
        with open('jeopardydata.json', 'w') as f:
            myselectcategory = GameStart.startgame(command, numberofcategories)
        #Assert that the correct number of categories were returned
        with open("jeopardydata.json", "r") as file:
            data = json.load(file)
        category = [None] * len(data)
        for i in range(len(data)):
            if data[i]["category"] != category[i]:
                category[i] = data[i]["category"]
        print(category)
        unique_categories = len(set(category))
        self.assertEqual(unique_categories, numberofcategories)
        if os.path.exists('jeopardydata.json'):
            os.remove('jeopardydata.json')



    async def test_playgame(self):  #Integration test, test the main play function that ties all other functions together, this ties my classes for user input, database class, and game function classes
        #create mock objects
        myjeopardy_mock = MagicMock()
        ctx_mock = MagicMock()
        ctx_mock.author.id = 12345
        ctx_mock.guild.id = 67890
        bot_mock = MagicMock()

        #run the function
        await Input.playgame(myjeopardy_mock, ctx_mock, 'custom', bot_mock)

        #make assertions, check to see if calls to other functions made
        myjeopardy_mock.start_game.assert_called_once_with(12345, 67890)
        self.assertEqual(bot_mock.wait_for.call_count, 3)
        self.assertEqual(ctx_mock.send.call_count, 4)
        GameStart.gamemake.assert_called_once_with(ctx_mock)
        GameBoard.gameover.assert_called_once_with(myjeopardy_mock, ctx_mock)



    def test_drawtable(self):   #white box test, testing the feature to draw the gameboard onto the screen with formatting
        """def drawtable(categories):  # initial create the table
            values = [[200, 400, 600, 800, 1000] for i in range(len(categories))]

            message = "```\nCategories:\n"
            longest_category_length = max(len(category) for category in categories)

            for category_index, category in enumerate(categories):  # FORMATTING THE TABLE PLS DONT TOUCH
                message += category + " " * (longest_category_length - len(category)) + "\t\t"
                for value in values[category_index]:
                    if value is not None:
                        message += str(value) + "\t"
                    else:
                        message += " " * len(str(value)) + "\t"
                message += "\n"

            message += "```"
            return message"""
        #Set up test parameters
        categories = ['Category 1', 'Category 2', 'Category 3']

        #Call the function to get the output
        output = GameBoard.drawtable(categories)

        #Check that the output is formatted correctly
        expected_output = "```\nCategories:\nCategory 1\t\t200\t400\t600\t800\t1000\t\nCategory 2\t\t200\t400\t600\t800\t1000\t\nCategory 3\t\t200\t400\t600\t800\t1000\t\n```"
        self.assertEqual(output, expected_output)



    def test_initcategories(self):  #white box test, setting up the game categories, questions, and values
        """def initcategories(categories):  # initialize all categories with their values in an "array"
            with open("categorystate.json", "w") as file:
                file.close()
            try:
                with open("categorystate.json", "r") as f:
                    categories_values = json.load(f)
            except:
                categories_values = {category: [200, 400, 600, 800, 1000] for category in categories}
            with open("categorystate.json", "w") as f:
                json.dump(categories_values, f)"""
        #Set up test parameters
        categories = ["Category 1", "Category 2", "Category 3"]

        #Remove the categorystate file if it exists
        if os.path.exists("categorystate.json"):
            os.remove("categorystate.json")

        #Call the initcategories function
        GameBoard.initcategories(categories)

        #Assert that the file was created
        self.assertTrue(os.path.exists("categorystate.json"))

        #Assert that the file contains the correct data
        with open("categorystate.json", "r") as f:
            data = json.load(f)
        self.assertEqual(len(data), len(categories))
        for category in categories:
            self.assertIn(category, data)
            self.assertEqual(data[category], [200, 400, 600, 800, 1000])

        #Remove the categorystate file after the test
        os.remove("categorystate.json")



    def test_gameover(self):    #White box test, testing the ability to end the game based on either user input or the gameboard being empty
        """def gameover(myjeopardy, user):  # check to see if all values are null for game over
            if (user.content == "quit"):
                print("Quiting because user said so")
                myjeopardy.end_game(user.author.id, user.guild.id)
                return True
            with open("categorystate.json", "r") as f:
                current_categories = json.load(f)
                game_over = True
                for category_values in current_categories.values():
                    if any(value is not None for value in category_values):
                        game_over = False
                        break
                if game_over:
                    return True
                else:
                    return False"""
        #Test game over when all values are None
        myjeopardy = Mock()
        myjeopardy.end_game = Mock()
        user = Mock(content="not quit", author=Mock(id=123), guild=Mock(id=456))
        with open("categorystate.json", "r") as f:
            current_categories = {k: [None]*5 for k in ["category1", "category2", "category3"]}
            with open("categorystate.json", "w") as f:
                json.dump(current_categories, f)
        self.assertTrue(GameBoard.gameover(myjeopardy, user))
        #Test game not over when some values are not None
        myjeopardy.end_game.reset_mock()
        current_categories = {k: [None]*5 for k in ["category1", "category2", "category3"]}
        current_categories["category1"][0] = "value1"
        with open("categorystate.json", "w") as f:
            json.dump(current_categories, f)
        self.assertFalse(GameBoard.gameover(myjeopardy, user))
        myjeopardy.end_game.assert_not_called()
        #Test game not over when user types "quit"
        user.content = "quit"
        self.assertTrue(GameBoard.gameover(myjeopardy, user))
        myjeopardy.end_game.assert_called_once_with(123, 456)



if __name__ == '__main__':
    asyncio.run(unittest.main())

