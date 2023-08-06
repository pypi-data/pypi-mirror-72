import xlsxwriter

from autotesttables import Table


class Generator:
    """
    A class used to hold Table instances and then generate the actual tables.

    This is seperate to keep the code cleaner.
    """

    # <-- Dunder Methods -->
    def __init__(
        self,
        reportTitle=None,
        reportDescription=None,
        successCount=0,
        failureCount=0,
        errorCount=0,
        mode="print",
        filename="Test Tables",
    ):
        """
        self.tables is a dict of all Table instances where table.title is the key
        """
        self.tables = {}
        self.report_title = reportTitle or "Test Tables"
        self.report_description = reportDescription or ""

        self.success_count = successCount
        self.failure_count = failureCount
        self.error_count = errorCount

        self.mode = mode
        self.filename = filename

    # <-- Class Methods -->
    def SetReportTitle(self, title):
        """
        Sets the new report title

        Params:
         - title (str) : The new report title
        """
        self.report_title = title

    def SetReportDescription(self, description):
        """
        Sets the new report description

        Params:
         - description (str) : The new report description
        """
        self.report_description = description

    def SetSuccessCount(self, count):
        """
        Sets the success count

        Params:
         - count (int) : The new count
        """
        # If not already int
        if not isinstance(count, int):
            count = int(count)

        self.success_count = count

    def SetFailureCount(self, count):
        """
        Sets the failure count

        Params:
         - count (int) : The new count
        """
        # If not already int
        if not isinstance(count, int):
            count = int(count)

        self.failure_count = count

    def SetErrorCount(self, count):
        """
        Sets the error count

        Params:
         - count (int) : The new count
        """
        # If not already int
        if not isinstance(count, int):
            count = int(count)

        self.error_count = count

    def SetMode(self, mode):
        """
        Sets the current mode

        Params:
         - mode (print/save) : The mode for Build()
        """
        if not mode.lower() in ["print", "save"]:
            raise Exception(f"Invalid mode: {mode}. Expected print or save")

        self.mode = mode.lower()

    def SetFilename(self, filename):
        """
        Sets the filename for saving
        """
        self.filename = filename

    def GetReportTitle(self):
        """
        Returns this instances report title
        """
        return self.report_title

    def GetReportDescription(self):
        """
        Returns this instances report description
        """
        return self.report_description

    def GetSuccessCount(self):
        """
        Returns this instances success count
        """
        return self.success_count

    def GetFailureCount(self):
        """
        Returns this instances failure count
        """
        return self.failure_count

    def GetErrorCount(self):
        """
        Returns this instances error count
        """
        return self.error_count

    def GetMode(self):
        """
        Returns this instances current mode
        """
        return self.mode

    def GetFilename(self):
        """
        Returns this instances current filename for excel sheets
        """
        return self.filename

    def AddTable(self, table):
        """
        Adds a new table to our instance list

        Params:
         - table (Table instance)
        """
        if not isinstance(table, Table):
            raise Exception("Expected Table instance")

        if table.GetTitle() in self.tables:
            raise KeyError(f"Table with title ({table.GetTitle()}) already exists")

        self.tables[table.GetTitle()] = table

    def GetTable(self, tableName):
        """
        Get the object instance for a table

        Params:
         - tableName (str) : The table to return
        """
        # Check the table exists
        if not self.tables[tableName]:
            raise KeyError("Table not found")

        return self.tables[tableName]

    def PrintTableOutput(self, tableName):
        """
        Used to generate a nice output and print to stdout

        Ideally this is an internal method

        Params:
         - tableName (str) : The table to output
        """
        # Check the table exists
        if not self.tables[tableName]:
            raise KeyError("Table not found")

        # Get our instance and data dict
        table = self.tables[tableName]
        data = table.Build()

        # Build output here
        for key, value in data.items():
            print(f"{key}: {value}")

        print("\n")

    def BuildTablesToExcel(self, filename):
        """
        Builds the current tables to the supplied excel file path

        Params:
         - filename (str) : Excel filename
        """
        # Time to start excel stuff
        # Create workbook
        workbook = xlsxwriter.Workbook(f"{filename}.xlsx")
        worksheet = workbook.add_worksheet()

        # Modify our column width
        worksheet.set_column(0, 0, width=25)
        worksheet.set_column(1, 1, width=50)

        # Here are some formatting variables we can use
        # BOLD
        bold = workbook.add_format({"bold": True})
        boldUnderline = workbook.add_format({"bold": True, "underline": True})
        leftAlign = workbook.add_format()
        leftAlign.set_align("left")

        # Starting index's
        row = 0
        col = 0

        # Write in our headers
        worksheet.write(row, col, self.report_title, boldUnderline)
        row += 1

        worksheet.write(row, col, self.report_description)
        row += 2

        # Write our actual tests into the file
        for tableName in self.tables:
            data = self.tables[tableName].Build()
            for key, value in data.items():
                worksheet.write(row, col, key, bold)
                worksheet.write(row, col + 1, value)
                row += 1
            row += 1

        # Write footers into the file
        worksheet.write(row, col, "Total Tests:", bold)
        worksheet.write(
            row,
            col + 1,
            self.success_count + self.failure_count + self.error_count,
            leftAlign,
        )
        row += 1

        worksheet.write(row, col, "Total Successful Tests:", bold)
        worksheet.write(row, col + 1, self.success_count, leftAlign)
        row += 1

        worksheet.write(row, col, "Total Failed Tests:", bold)
        worksheet.write(row, col + 1, self.failure_count, leftAlign)
        row += 1

        worksheet.write(row, col, "Total Errored Tests:", bold)
        worksheet.write(row, col + 1, self.error_count, leftAlign)
        row += 1

        workbook.close()

    def Build(self):
        """
        Essentially generates the tables for every currently stored test

        Optional Param:
         - filename (str) : If mode is save this is needed
        """
        if self.mode.lower() == "save":
            self.BuildTablesToExcel(self.filename)
        else:
            count = 0
            for key in self.tables.keys():
                self.PrintTableOutput(key)
                count += 1
            print(
                f"Total Tests: {self.success_count + self.failure_count + self.error_count}",
                f"Total Successful Tests: {self.success_count}",
                f"Total Failed Tests: {self.failure_count}",
                f"Total Error'ed Tests: {self.error_count}",
                sep="\n",
            )
