
import sys
from PySide2.QtCore import Qt,QStringListModel
from PySide2.QtWidgets import QLineEdit, QCompleter

# class delegate(QItemDelegate):
#     def __init__(self):
#         QItemDelegate.__init__(self)
# class items(QAbstractItemView):
#     def __init__(self):
#         QAbstractItemView.__init__(self)   

class AutoCompleteLineEdit(QLineEdit):
    def __init__(self, path, parent=None):
        super(AutoCompleteLineEdit, self).__init__(parent)
        self.path = path
        with open(self.path,"r") as f: self.list= f.read().split('\n')
        self.__items = QStringListModel(self.list)
        self.__separators = [",", " "]
        self.textChanged.connect(self.__updateModel)
        self.__completer = QCompleter(self.__items, self)
        self.__completer.setWidget(self)
        self.setAlignment(Qt.AlignLeft)
        # self.__completer.setPopup(items().setItemDelegate(delegate()))
        self.__completer.activated[str].connect(self.__insertCompletion)
        self.__completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.__keysToIgnore = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab]

    def __insertCompletion(self, completion):
        extra = len(completion) - len(self.__completer.completionPrefix())
        extra_text = completion[-extra:]
        extra_text += " "
        self.setText(self.text() + extra_text)

    def setGeometry(self, x: int, y: int, w: int, h: int) -> None:
        return super().setGeometry(x, y, w, h)
    def __updateModel(self):
        if self.text()[-1] == " ":
            if self.text().split()[-1] not in self.__items.stringList():
                self.__items.setStringList(self.__items.stringList()+[self.text().split()[-1]])
                self.appendToFile(self.__items.stringList())
                self.__completer.setModel(self.__items)

    def appendToFile(self,items):
        with open(self.path,'w') as f:
            for ele in items: 
                f.write(ele+'\n')


    def textUnderCursor(self):
        text = self.text()
        text_under_cursor = ''
        i = self.cursorPosition() - 1
        while i >=0 and text[i] not in self.__separators:
            text_under_cursor = text[i] + text_under_cursor
            i -= 1
        return text_under_cursor


    def keyPressEvent(self, event):
        if self.__completer.popup().isVisible():
            if event.key() in self.__keysToIgnore:
                event.ignore()
                return

        super(AutoCompleteLineEdit, self).keyPressEvent(event)

        completion_prefix = self.textUnderCursor()
        if completion_prefix != self.__completer.completionPrefix():
            self.__updateCompleterPopupItems(completion_prefix)
        if len(event.text()) > 0 and len(completion_prefix) > 0:
            self.__completer.complete()
        if len(completion_prefix) == 0:
            self.__completer.popup().hide()


    def __updateCompleterPopupItems(self, completionPrefix):
        self.__completer.setCompletionPrefix(completionPrefix)
        self.__completer.popup().setCurrentIndex(self.__completer.completionModel().index(0,0))
