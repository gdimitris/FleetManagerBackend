import unittest
from Application import app, db
from Application.db_operations import *


class DBOperationsTests(unittest.TestCase):
    def setUp(self):
        self.existing_researcher = Researchers(phone_id='123', name='test', surname='test')
        app.config.from_pyfile('../Tests/testing_conf.py')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testCommitsResearcher(self):
        commit_and_flush(self.existing_researcher)
        actual = self.get_test_researcher()
        self.assertIsNotNone(actual)
        self.assertIsInstance(actual, Researchers)

    def testCreatesNewResearcher(self):
        should_be_none = self.get_test_researcher()
        self.assertIsNone(should_be_none)
        insert_or_update_existing_researcher('123', 'test', 'test')
        should_exist = self.get_test_researcher()
        self.assertIsNotNone(should_exist)
        self.assertIsInstance(should_exist, Researchers)

    def testUpdatesExistingResearcher(self):
        commit_and_flush(self.existing_researcher)
        insert_or_update_existing_researcher('123', 'nottest', 'nottesttoo')
        actual = self.get_test_researcher()
        self.assertIsInstance(actual, Researchers)
        self.assertIsNotNone(actual)
        self.assertEqual(actual.name, 'nottest')
        self.assertEqual(actual.surname, 'nottesttoo')

    def testUpdatesResearcherTimestamp(self):
        commit_and_flush(self.existing_researcher)
        res = self.get_test_researcher()
        self.assertIsNone(res.last_updated)
        timestamp = datetime.now()
        update_researcher_timestamp('123', timestamp)
        res = self.get_test_researcher()
        self.assertEqual(timestamp, res.last_updated)

    def testUpdateTimestampOfNonExistingResearcher(self):
        timestamp = datetime.now()
        update_researcher_timestamp('123', timestamp)
        res = self.get_test_researcher()
        self.assertIsNotNone(res)
        self.assertEqual(res.last_updated, timestamp)
        self.assertEqual(res.phone_id, '123')
        self.assertEqual(res.name, 'None')
        self.assertEqual(res.surname, 'None')

    def testGetsAllResearchersFromDB(self):
        self.commit_four_researchers_in_db()
        res = get_all_researchers_from_db()
        self.assertEqual(4, len(res))

    def testInsertsLocationPointsInDB(self):
        should_be_empty = LocationPoints.query.filter(LocationPoints.phone_id == '123').all()
        self.assertEqual(0, len(should_be_empty))

        stamp = datetime.now()
        insert_location_point_in_db('123', '32.333', '33.333', stamp)
        should_not_be_empty = LocationPoints.query.filter(LocationPoints.phone_id == '123').all()
        self.assertEqual(1, len(should_not_be_empty))

    def testGetsLocationsWithID(self):
        self.commit_ten_locations_in_db()
        res = get_entries_with_phone_id('456')
        self.assertEqual(5, len(res))

    def testGetsLocationsForMultipleIDs(self):
        self.commit_ten_locations_in_db()
        res = get_locations_for_phone_ids(['789', '444'])
        self.assertEqual(5, len(res))

    def commit_four_researchers_in_db(self):
        commit_and_flush(self.existing_researcher)
        commit_and_flush(Researchers(phone_id='456', name='test2', surname='test2'))
        commit_and_flush(Researchers(phone_id='789', name='test3', surname='test3'))
        commit_and_flush(Researchers(phone_id='444', name='test4', surname='test4'))

    def commit_ten_locations_in_db(self):
        commit_and_flush(LocationPoints(phone_id='456', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='456', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='456', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='456', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='456', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='789', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='789', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='444', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='444', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))
        commit_and_flush(LocationPoints(phone_id='444', timestamp=datetime.now(), latitude='32.333', longitude='33.333'))

    def get_test_researcher(self):
        return Researchers.query.filter(Researchers.phone_id == '123').first()

