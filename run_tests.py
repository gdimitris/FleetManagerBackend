import unittest
import time
from coverage import coverage

cov = coverage(branch=True, source=['Application'])
cov.start()

from Tests.db_operation_tests import DBOperationsTests
from Tests.view_test import ViewTests


test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(DBOperationsTests))
test_suite.addTest(unittest.makeSuite(ViewTests))

runner = unittest.TextTestRunner()
runner.run(test_suite)

cov.stop()
cov.save()

time.sleep(0.1)
print "\n\n Coverage Report: \n"
cov.report()
print "Report in HTML: http://localhost:5050/FleetManagerBackend/tmp/coverage/index.html"
cov.html_report(directory='tmp/coverage')
cov.erase()