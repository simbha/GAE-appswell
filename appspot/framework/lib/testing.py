"""
    Appswell Testing Library

    Tools used in testing

    USAGE
    import lib.utilities as ut
    ut.append_syspath(ut.PROJECT_PATH, 'test')

    REFERENCES
    http://docs.python.org/library/unittest.html
    http://docs.python.org/library/traceback.html
    http://tungwaiyip.info/software/HTMLTestRunner.html
"""
#
# Imports
#
# Python
import sys, os, logging, inspect
from os.path import (abspath, dirname, join as pathjoin)
from unittest import (TestCase, TestLoader, TextTestRunner, TestResult)
from traceback import (extract_stack, format_tb, format_exc)
from datetime import (datetime)
import time

# Appswell


#
# Constants
#
PROJECT_PATH = abspath(pathjoin(dirname(__file__), '..'))


#
# Module Functions
#
def run_test_from_command_line(TestClass):
    suite = TestLoader().loadTestsFromTestCase(TestClass)
    print "\n%s START TEST: %s %s\n" % ("*"*5, datetime.now(), "*"*5)
    TextTestRunner(verbosity=2).run(suite)
    print "\n%s END TEST: %s %s\n" % ("*"*5, datetime.now(), "*"*5)


#
# Classes
#
class AppswellUnitTest(TestCase):
    """adds a note log that can be used to capture information within a test
    for display in output"""
    note_log = []

    def __init__(self, methodName=None):
        TestCase.__init__(self, methodName)
        self.note_log = []

    def note(self, note):
        """logs notes during test along with time and trace information in a
        dict of tuples:
        { datetime : ( note, traceback ), ... }"""
        stack_list = extract_stack()
        self.note_log.append(( datetime.now(), str(note), stack_list ))
        return stack_list


class AppswellTestRunner:
    def run(self, test):
        self.result = AppswellTestResult()
        test(self.result)
        return self.result


class AppswellTestResult(TestResult):
    testSuccess = []
    all_tests = {}      # name -> result
    results_log = {}    # id -> result, trace, duration, start_time, test_num, desc
    note_log = []       # (datetime, m, trace)

    # result code
    passed = 'PASS'
    failed = 'FAIL'
    erred  = 'ERROR'

    def __init__(self):
        TestResult.__init__(self)
        self.start_at = time.time()
        self.testSuccess = []
        self.all_tests = {}
        self.results_log = {}
        self.note_log = []

    def update_logs(self, id, result, note_logs, err=None):
        """called just by addSuccess, addFailure, and addError"""
        self.note_log.extend(note_logs)
        self.all_tests[id] = result
        self.results_log[id][0] = result
        if err:
            self.results_log[id][5] = '%s (l. %s)' % (err[1], err[2].tb_next.tb_lineno)

    def startTest(self, test):
        self.test_start_at = time.time()
        self.all_tests[test.id()] = None
        self.results_log[test.id()] = [None, None, 0, datetime.now(),
            self.testsRun, test.shortDescription() or str(test)]
        return TestResult.startTest(self, test)

    def stopTest(self, test):
        self.results_log[test.id()][2] = time.time() - self.test_start_at
        return TestResult.stopTest(self, test)

    def addSuccess(self, test):
        self.update_logs(test.id(), self.passed, test.note_log)
        self.testSuccess.append(str(test))
        return TestResult.addSuccess(self, test)

    def addFailure(self, test, err):
        self.results_log[test.id()][1] = format_exc()
        self.update_logs(test.id(), self.failed, test.note_log, err)
        return TestResult.addFailure(self, test, err)

    def addError(self, test, err):
        self.results_log[test.id()][1] = format_exc()
        self.update_logs(test.id(), self.erred, test.note_log, err)
        return TestResult.addError(self, test, err)

    def get_detail(self):
        num_tests = len(self.all_tests)
        num_passed = sum([1 for r in self.all_tests.values() if r == self.passed])
        return {
            'runs'      : self.testsRun,
            'all'       : self.all_tests,
            'total'     : num_tests,
            'passed'    : num_passed,
            'success'   : num_passed == num_tests,
            'notes'     : self.note_log,
            'results'   : self.results_log,
            'duration'  : time.time() - self.start_at,
        }

    def _list(self, list):
        dict = []
        for test, err in list:
            d = {
              'desc': test.shortDescription() or str(test),
              'detail': err,
            }
            dict.append(d)
        return dict
