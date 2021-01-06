from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QFont


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super(Highlighter, self).__init__(document)
        color = QColor()
        color.setNamedColor('yellow')
        self.format = QTextCharFormat()
        self.format.setBackground(color)
        self.focousArea = None

        fcolor = QColor()
        fcolor.setNamedColor('magenta')
        self.focousFormat = QTextCharFormat()
        self.focousFormat.setBackground(fcolor)

        white = QColor()
        white.setNamedColor('white')
        self.normalFormat = QTextCharFormat()
        self.normalFormat.setBackground(white)

        self.expression = QRegularExpression()

    def setExpression(self, exp, caseSensitive, wholeWord):
        if wholeWord:
            exp = "\\b" + exp + "\\b"
            print(exp)
        if caseSensitive:
            self.expression = QRegularExpression(exp)
        else:
            self.expression = QRegularExpression(exp, QRegularExpression.CaseInsensitiveOption)

    def currentFocoused(self, start, size):
        if self.focousArea:
            self.setFormat(self.focousArea[0], self.focousArea[1], self.normalFormat)
        self.focousArea = (start, size)
        self.rehighlight()

    def highlightBlock(self, text):
        matches = self.expression.globalMatch(text)
        while matches.hasNext():
            match = matches.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.format)

        if self.focousArea:
            self.setFormat(self.focousArea[0], self.focousArea[1], self.focousFormat)
        # print("starting at ", match.capturedStart())
        # print(f"lenght = {match.capturedLength()}")

    def unformat(self, text):
        self.setFormat(0, len(text), self.normalFormat)
