#!/usr/bin/env python3
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


def settings():
    settings = QtCore.QSettings("Yansoft", "Prasopes")
    defvals = {("view/autozoomy", True),
               ("view/filebrowservisible", True),
               ("view/consolevisible", True),
               ("view/acqparvisible", True),
               ("view/intensities", False),
               ("view/oddeven", False),
               ("print/xinch", 10),
               ("print/yinch", 4),
               ("print/dpi", 300),
               ("print/xtics", 5),
               ("imggen/xinch", 10),
               ("imggen/yinch", 4),
               ("imggen/dpi", 300),
               ("imggen/xtics", 5),
               ("imggen/onlymanann", False),
               ("reactivity/index", 0),
               ("recents", "")}
    [settings.setValue(*i)
     for i in defvals if not settings.contains(i[0])]
    return settings


def pathsearch(text, value, config):
    filename = QtWidgets.QFileDialog.getExistingDirectory()
    if filename != '':
        text.setText(filename)
        config.setValue(value, filename)


def pathlineconf(label, value, config):
    """adds generic filepath config line"""
    textfield = QtWidgets.QLineEdit(str(config.value(value)))
    textfield.editingFinished.connect(lambda: config.setValue(
        value, textfield.text()))
    browse_button = QtWidgets.QPushButton("Browse..")
    browse_button.clicked.connect(lambda: pathsearch(
        textfield, value, config))
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel(str(label)))
    layout.addWidget(textfield)
    layout.addWidget(browse_button)
    return layout


def posvarconf(label, value, config, num="int"):
    """adds generic positive integer config line"""
    textfield = QtWidgets.QLineEdit(str(config.value(value)))
    textfield.editingFinished.connect(lambda: config.setValue(
        value, textfield.text()))
    validator = QtGui.QIntValidator() if num == "int"\
        else QtGui.QDoubleValidator()
    validator.setBottom(0)
    textfield.setValidator(validator)
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel("{}:".format(label)))
    layout.addStretch()
    layout.addWidget(textfield)
    return layout


def checkboxconf(label, value, config):
    checkbox = QtWidgets.QCheckBox(label)
    checkbox.setChecked(config.value(value,type=bool))
    checkbox.stateChanged.connect(lambda: config.setValue(
        value, checkbox.checkState()))
    return checkbox


def dial(parent):
    """constructs a dialog window"""
    dialog = QtWidgets.QDialog(
        parent, windowTitle='Settings')
    dialog.resize(600, -1)

    config = settings()

    tabs = QtWidgets.QTabWidget()

    pathtab = QtWidgets.QWidget()
    pathlayout = QtWidgets.QVBoxLayout(pathtab)
    pathlayout.addLayout(pathlineconf(
        "Acquisition temp folder", "tmp_location", config))
    pathlayout.addLayout(pathlineconf(
        "Default open folder", "open_folder", config))
    tabs.addTab(pathtab, "Paths")

    printtab = QtWidgets.QWidget()
    printlayout = QtWidgets.QVBoxLayout(printtab)
    printlayout.addLayout(posvarconf(
        "Figure width (inch)", "print/xinch", config, "nonint"))
    printlayout.addLayout(posvarconf(
        "Figure height (inch)", "print/yinch", config, "nonint"))
    printlayout.addLayout(posvarconf(
        "Figure dpi", "print/dpi", config))
    printlayout.addLayout(posvarconf(
        "Figure x axis major ticks count", "print/xtics", config))
    tabs.addTab(printtab, "Printing")

    imggentab = QtWidgets.QWidget()
    imggenlayout = QtWidgets.QVBoxLayout(imggentab)
    imggenlayout.addLayout(posvarconf(
        "Figure width (inch)", "imggen/xinch", config, "nonint"))
    imggenlayout.addLayout(posvarconf(
        "Figure height (inch)", "imggen/yinch", config, "nonint"))
    imggenlayout.addLayout(posvarconf(
        "Figure dpi", "imggen/dpi", config))
    imggenlayout.addLayout(posvarconf(
        "Figure x axis major ticks count", "imggen/xtics", config))
    imggenlayout.addWidget(checkboxconf(
        "Manual annotation only", "imggen/onlymanann", config))
    tabs.addTab(imggentab, "Image clip/export")

    close_button = QtWidgets.QPushButton("Close")
    close_button.clicked.connect(dialog.close)

    butt_layout = QtWidgets.QHBoxLayout()
    butt_layout.addWidget(close_button)
    butt_layout.addStretch(1)

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.addWidget(QtWidgets.QLabel("Changes are saved automatically"))
    layout.addWidget(tabs)
    layout.addStretch(1)
    layout.addLayout(butt_layout)

    dialog.show()
