from PySide2 import QtWidgets
import currency_converter
import json
import convert

app = QtWidgets.QApplication([])
win = convert.App()
win.show()
app.exec_()
