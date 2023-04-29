"""
Test Cases TestAccountModel
"""
import json
from unittest import TestCase
from models import app, db
from models.account import Account
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
        db.session.query(Account).delete()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_account(self):
        """ Test creating an account """
        random = rand.randint(0, len(ACCOUNT_DATA))
        data = ACCOUNT_DATA[random]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

