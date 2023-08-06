import re
import sys
import time
import unittest
import datetime

try:
    from StringIO import StringIO  # Py 2
except ImportError:
    from io import StringIO  # Py 3

from autotesttables import Generator, Table

# from table import Table
# from generator import Generator

"""
I did not build the base test runner myself, I simply used someone else's
to then further build upon it myself and include my own things


Ethan M-H (github.com/skelmis) | 2020
"""

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ""))
        if self.verbosity > 1:
            sys.stderr.write("ok ")
            sys.stderr.write(str(test))
            sys.stderr.write("\n")
        else:
            pass  # sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write("E  ")
            sys.stderr.write(str(test))
            sys.stderr.write("\n")
        else:
            pass  # sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write("F  ")
            sys.stderr.write(str(test))
            sys.stderr.write("\n")
        else:
            pass  # sys.stderr.write('F')


class TestRunner:
    def __init__(self, stream=sys.stdout, verbosity=1):
        self.stream = stream
        self.verbosity = verbosity

        self.generator = Generator()

    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity)
        test(result)

        self.BuildGenerator(test, result)

        return result

    def BuildGenerator(self, test, result):
        """
        Builds the generator class object for all of our tests

        Params:
         - test () : Somethin
         - result (2d list) : our tests
        """
        # Setup our generator values
        self.generator.SetSuccessCount(result.success_count)
        self.generator.SetFailureCount(result.failure_count)
        self.generator.SetErrorCount(result.error_count)

        # Get all our tests sorted by class
        sortedTests = self.SortResult(result.result)

        # Make Table instances for all of our tests
        for tupleIndex in range(len(sortedTests)):
            for testIndex in range(len(sortedTests[tupleIndex][1])):
                # initialize variables
                testTitle = (
                    docString
                ) = inputDoc = outputDoc = testStatus = testStack = ""

                curTest = sortedTests[tupleIndex][1][testIndex]
                curTestObject = curTest[1]

                testTitle = curTestObject.__str__().split(" ")[0]

                # Begin parsing docstring
                docString = curTestObject._testMethodDoc
                docString = docString.replace("\n", "")  # Remove newlines
                docString = str.lower(docString)

                # See if input is provided and do stuff
                if "input:" in docString:
                    docString = docString.split("input:")
                    # ("description", 'input/(Maybe output)')

                # See if output is provded and do stuff
                if isinstance(docString, str):
                    # I.E `input:`` was not found
                    if "output:" in docString:
                        docString = docString.split("output:")
                elif isinstance(docString, list):
                    # If `input:` was found, check the last item in the list
                    if "output:" in docString[len(docString) - 1]:
                        inputDoc, outputDoc = docString[len(docString) - 1].split(
                            "output:"
                        )

                # Ensure docstring is now only the actual docstring
                if isinstance(docString, list):
                    docString = docString[0]

                # Strip all 3 to ensure they look good and dont take excessive space
                docString = docString.strip()
                inputDoc = inputDoc.strip()
                outputDoc = outputDoc.strip()

                # Make it look nice again
                docString = docString.capitalize()

                # Set test status
                testStatus = True if curTest[0] == 0 else False

                # Parse our stack if it exists
                if curTest[2] == "":
                    testStack = ""
                else:
                    # We have a stack to parse
                    # this works off finding the last semicolon in the
                    # error message
                    testStack = curTest[2]
                    placeholderStack = curTest[2][::-1]
                    semiIndex = placeholderStack.index(":")
                    # we have the reverse index, now we need to find the
                    # index of the next space so we can include the exception
                    # within our stack message
                    for i in range(semiIndex, len(placeholderStack)):
                        if placeholderStack[i] in [" ", "\n"]:
                            # We found the end of the exception word
                            semiIndex = i
                            break

                    # Get the index in non-reversed stack
                    semiIndex = len(testStack) - semiIndex

                    # Set stack to everything after said index
                    testStack = testStack[semiIndex:]

                # Make our new Table instance
                currentTable = Table(
                    testTitle, docString, inputDoc, outputDoc, testStatus, testStack
                )

                # Add it into our generator
                self.generator.AddTable(currentTable)

        # All tests are now in the generator so make the test tables
        self.generator.Build()

    def SortResult(self, result_list):
        """
        unittest does not seems to run in any particular order.
        Here at least we want to group them together by class.

        Dictionary where keys are class names,
        values are a list of all tests for that class in the format
        [Test status, test class instance, traceback]

        Test status:
        0: Pass
        1: Fail
        2: Error
        """
        rmap = {}
        classes = []
        for n, test, output, error in result_list:
            testClass = test.__class__
            if testClass not in rmap:
                rmap[testClass] = []
                classes.append(testClass)
            rmap[testClass].append((n, test, error))
        r = [(testClass, rmap[testClass]) for testClass in classes]
        return r


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """

    def RunTests(self):
        # Pick TestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate TestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = TestRunner()
        unittest.TestProgram.runTests(self)
