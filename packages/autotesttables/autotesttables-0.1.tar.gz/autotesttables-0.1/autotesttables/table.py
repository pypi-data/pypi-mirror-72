class Table:
    """A class used to store information regarding a certain table"""

    # <-- Dunder Methods -->
    def __init__(
        self,
        testTitle=None,
        testDescription=None,
        testInput=None,
        testOutput=None,
        testStatus=None,
        testStack=None,
    ):
        """
        Used to set values n stuff

        Optional Params:
         - testTitle (str) : The title for this test, I.E. the function name
         - testDescription (str) : The first part of the tests docstring
         - testInput (str) : The second part of the tests docstring
         - testOutput (str) : The third part of the tests docstring
         - testStatus (bool) : True or False, True being pass, False being fail.
         - testStack (str) : If not testStatus: -> This is the first line of exception
        """
        self.title = testTitle
        self.description = testDescription
        self.input = testInput
        self.output = testOutput
        self.status = testStatus
        self.stack = testStack

    def __str__(self):
        """
        Dunder method for str(Table instance)
        """
        return f"Table({self.title})"

    def __repr__(self):
        """
        Dunder method for print(Table instance)
        """
        return f"Table({self.title})"

    # <-- Class Methods -->
    def SetTitle(self, title):
        """
        Sets self.title

        Params:
        - title (str) : The new title
        """
        self.title = title

    def SetDescription(self, description):
        """
        Sets self.description

        Params:
         - description (str) : The new description
        """
        self.description = description

    def SetInput(self, input):
        """
        Sets self.input

        Params:
         - input (str) : The new input
        """
        self.input = input

    def SetOutput(self, output):
        """
        Sets self.output

        Params:
         - output (str) : The new output
        """
        self.output = output

    def SetStatus(self, status):
        """
        Sets self.status

        Params:
         - status (bool) : The new status
        """
        self.status = status

    def SetStack(self, stack):
        """
        Sets self.stack

        Params:
         - stack (str) : The new stack
        """
        self.stack = stack

    def GetTitle(self):
        """
        Returns this instances title
        """
        return self.title

    def GetDescription(self):
        """
        Returns this instances description
        """
        return self.description

    def GetInput(self):
        """
        Returns this instances input
        """
        return self.input

    def GetOutput(self):
        """
        Returns this instances output
        """
        return self.output

    def GetStatus(self):
        """
        Returns this instances status
        """
        return self.status

    def GetStack(self):
        """
        Returns this instances stack
        """
        return self.stack

    def Build(self):
        """
        Builds and returns a dictionary of all values within
        this class instance
        """
        data = {}

        data["title"] = self.title or ""
        data["description"] = self.description or ""
        data["input"] = self.input or ""
        data["output"] = self.output or ""

        # This is a special cases that needs some logic to figure out
        if self.status:
            # The test passed
            data["status"] = "Pass"
        else:
            # The test failed
            data["status"] = "Fail"

        data["stack"] = self.stack or ""
        return data
