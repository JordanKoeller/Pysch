from unittest import TestCase

from pysh.terminal import StatementProcessor

class TestStatementProcessor(TestCase):

    def setUp(self):
        self.processor = StatementProcessor()
        self.processor._flush_statement()

    def testTrimsCommentsReturnsEmptystringForFullyCommentedLine(self):
        line = "    # This is a full-line comment"
        self.assertEqual(self.processor._trim_comments(line), '')

    def testTrimsCommentsReturnsFragmentBeforeThePoundSymbol(self):
        line = "This is some code before a# This is a comment"
        self.assertEqual(self.processor._trim_comments(line), "This is some code before a")

    def testTrimsCommentsRStripsWhitespaceFromLine(self):
        line = "This     # has white space before the pound"
        self.assertEqual(self.processor._trim_comments(line), "This")

    def testStatementProcessorIngestsSingleLines(self):
        line = "Here is a line of code"
        result = self.processor.process_line(line)
        self.assertEqual(line, result)
        self.assertProcessorIsFlushed()

    def testStatementProcessorIncrementsIndentionLevel(self):
        self.processor.process_line("for i in range(10):")
        self.assertProcessorIsNotFlushed()
        self.assertEqual(self.processor._indention_level, 1)
        self.processor.process_line("    print(i)")
        self.assertProcessorIsNotFlushed()
        self.assertEqual(self.processor._indention_level, 1)
        self.processor.process_line("")
        self.assertProcessorIsFlushed()

    def testStatementProcessorDoesNotResolveUntilBackticksAreClosed(self):
        ret = self.processor.process_line("`ls -al")
        self.assertEqual(ret, None)
        self.assertProcessorIsNotFlushed()
        ret = self.processor.process_line("`")
        self.assertCountEqual(ret, "`ls -al\n`")
        self.assertProcessorIsFlushed()

    def testStatementProcessorReturnsFullStatementOnFlush(self):
        statement = self.processor.process_line("for i in range(10):")
        self.assertEqual(statement, None)
        self.assertProcessorIsNotFlushed()
        self.assertEqual(self.processor._indention_level, 1)
        statement = self.processor.process_line("    print(i)")
        self.assertEqual(statement, None)
        self.assertProcessorIsNotFlushed()
        self.assertEqual(self.processor._indention_level, 1)
        statement = self.processor.process_line("")
        self.assertEqual(statement, """for i in range(10):
    print(i)
""")
        self.assertProcessorIsFlushed()
    ##################
    # Custom Asserts #
    ##################

    def assertProcessorIsNotFlushed(self):
        summation = self.processor._backtick_count + self.processor._indention_level
        self.assertNotEqual(summation, 0)
        self.assertNotEqual(self.processor._statement_lines, [])

    def assertProcessorIsFlushed(self):
        self.assertEqual(self.processor._backtick_count, 0)
        self.assertEqual(self.processor._indention_level, 0)
        self.assertEqual(self.processor._statement_lines, [])