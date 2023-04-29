"""
Test Cases TestAccountModel
"""
import json
from unittest import TestCase
from models import app, db
from models.account import Account, DataValidationError
import random as rand

ACCOUNT_DATA = {}
app.app_context().push()

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        db.create_all()
        global ACCOUNT_DATA
        with open("tests/fixtures/account_data.json") as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.random = rand.randint(0, len(ACCOUNT_DATA) -1)
        db.session.query(Account).delete()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_account(self):
        """ Test creating an account """
        data = ACCOUNT_DATA[self.random]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_creating_accounts(self):
        """ Test creating multiple accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_represent_as_string(self):
        """ Test repr function """
        account = Account()
        account.name = 'Foo'
        self.assertEqual(str(account), "<Account 'Foo'>")
    
    def test_to_dict(self):
        """ Test turn object into a dictionary """
        data = ACCOUNT_DATA[self.random]
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(result["name"], account.name)
        self.assertEqual(result["phone_number"], account.phone_number)
        self.assertEqual(result["email"], account.email)
        self.assertEqual(result["disabled"], account.disabled)

    def test_from_dict(self):
        """ Test create an account from a dictionary """
        data = ACCOUNT_DATA[self.random]
        account = Account()
        account.from_dict(data)
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["phone_number"], account.phone_number)
        self.assertEqual(data["email"], account.email)
        self.assertEqual(data["disabled"], account.disabled)

    def test_update_an_account(self):
        """ Test update an account """
        data = ACCOUNT_DATA[self.random]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.name = "Foo"
        account.update()
        found = Account.find(account.id)
        self.assertEqual(found.name, "Foo")

    def test_update_without_id(self):
        account = Account()
        self.assertRaises(DataValidationError, account.update)

    def test_delete_an_account(self):
        """ Test account deletion """
        data = ACCOUNT_DATA[self.random]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

        
    



        

