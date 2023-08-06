#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from rawprasslib import load_raw
from prasopes.predictmz import predict as getmzpattern
try:
    from rawautoparams import load_params
    import rawautoparams
    autoparams = True
except ImportError:
    autoparams = False
import rawprasslib
import numpy as np
import prasopes.config as cf
import prasopes.datatools as dt
import prasopes.drltools_gui as drlgui
import prasopes.filetools as ft
import prasopes.graphtools as gt
import prasopes.imagetools as imgt
import prasopes.zcetools as zce
import prasopes.docks as docks
import prasopes.tangoicons
import sys
import logging
import os.path


class update_signal(QtCore.QObject):
    signal = QtCore.pyqtSignal()


class QStatusBarLogger(logging.Handler):
    def __init__(self, parent=None):
        super().__init__()
        self.statusBar = QtWidgets.QStatusBar(parent)
        self.trigger = update_signal()
        self.msg = str("")

    def emit(self, record):
        self.msg = self.format(record)
        self.trigger.signal.emit()


def show_exception_and_exit(exc_type, exc_value, tb):
    if "figure size must be positive finite not" in str(exc_value):
        return
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    details = "\n".join(traceback.format_exception(exc_type, exc_value, tb))
    errmsg = "\n".join(traceback.format_exception_only(exc_type, exc_value))\
            + ("\n The program might misbehave, do you want to continue?")
    msgbox = QtWidgets.QMessageBox(
        3, "Exception!", errmsg,
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msgbox.setDetailedText(details)
    outvalue = msgbox.exec_()
    if outvalue != QtWidgets.QMessageBox.Yes:
        sys.exit(-1)


def load_file(parent, augCanvas, update, settings, loadthread, filename=None):
    """populates dataset and plots it"""
    directory = augCanvas.filename or settings.value("open_folder")
    filename = filename or QtWidgets.QFileDialog.getOpenFileName(
            caption="Open spectrum", directory=directory,
            filter="Finnigan RAW files (*.raw, *.RAW)")[0]
    if filename != '' and os.path.isfile(filename)\
            and not os.path.isdir(filename):
        error = update_signal()
        errormsg = []

        def runfnc():
            try:
                [i.clear() for i in (
                    augCanvas.ds, augCanvas.chrom['timesarg'],
                    augCanvas.ms['params'], augCanvas.ms['headers'])]
                [augCanvas.ds.append(dict(
                    chrom_dat=i[0], masses=i[1], matrix=i[2]))
                 for i in load_raw(filename, settings.value("tmp_location"))]
            except rawprasslib.ParsingException as pex:
                errormsg.append("Opening of the file has failed!")
                errormsg.append(
                    "File is incompatible with the rawprasslib, "
                    "canceling request!\n\n"
                    "Error message:\n{}".format(pex.args[0]))
                error.signal.emit()
                return
            if autoparams:
                try:
                    (augCanvas.ms['params'], rawheaders,
                        augCanvas.chrom['machtype']) = load_params(
                                filename, settings.value("tmp_location"))
                    segments = [len(subset['chrom_dat'][0])
                                for subset in augCanvas.ds]
                    indicies = [sum(segments[:i+1])
                                for i in range(len(segments))]
                    augCanvas.ms['headers'] = np.split(
                            rawheaders, indicies)[:-1]
                except Exception as pex:
                    errormsg.append(
                            "File is incompatible with the rawautoparams,")
                    errormsg.append(
                            "no parameters loaded!\n\n"
                            "Error message:\n{}".format(pex.args[0]))
                    error.signal.emit()
            gt.populate(augCanvas)
            augCanvas.filename = filename
            oldrecents = settings.value("recents")
            oldrecents.remove(filename) if filename in oldrecents else None
            settings.setValue("recents", [filename, *oldrecents])
            update.signal.emit()
        error.signal.connect(lambda: QtWidgets.QMessageBox.critical(
            parent, errormsg[0], errormsg[1]))
        loadthread.run = runfnc
        loadthread.start()


def print_graph(augCanvas):
    def printimage(printdevice, img):
        printer.setResolution(600)
        painter = QtGui.QPainter(printdevice)
        font = painter.font()
        linesize = printer.resolution()/15
        font.setPixelSize(linesize)
        painter.setFont(font)
        painter.drawImage(0, 0, img)
        offset = img.size().height()
        line = 1
        spacing = 1.5
        for row in range(augCanvas.paramstable.rowCount()):
            if augCanvas.paramstable.cellWidget(row, 0).checkState() == 2:
                text = augCanvas.paramstable.item(row, 1).text() +\
                       augCanvas.paramstable.item(row, 2).text()
                painter.drawText(300, int(offset+line*linesize*spacing), text)
                line += 1
        painter.end()
    # TODO: substitute the QPrintPreviewDialog with QPrintPreviewWidget
    printPreview = QtPrintSupport.QPrintPreviewDialog()
    printer = printPreview.printer()
    printer.setPageSize(printer.A5)
    printer.setDuplex(printer.DuplexNone)
    image = imgt.paint_image(augCanvas.ms, augCanvas.spectplot,
                             augCanvas.filename, printer)
    printPreview.paintRequested.connect(lambda:
                                        printimage(printer, image))
    printPreview.exec()


def update_spectrum(augCanvas, config):
    if augCanvas.filename:
        slims = [augCanvas.spectplot.get_xlim(),
                 augCanvas.spectplot.get_ylim()]
        augCanvas.ds.clear()
        [augCanvas.ds.append(dict(chrom_dat=i[0], masses=i[1], matrix=i[2]))
         for i in load_raw(augCanvas.filename, config.value("tmp_location"))]
        if autoparams:
            try:
                (augCanvas.ms['params'], rawheaders,
                    augCanvas.chrom['machtype']) = load_params(
                            augCanvas.filename, config.value("tmp_location"))
                segments = [len(subset['chrom_dat'][0])
                            for subset in augCanvas.ds]
                indicies = [sum(segments[:i+1])
                            for i in range(len(segments))]
                augCanvas.ms['headers'] = np.split(
                        rawheaders, indicies)[:-1]
            except Exception as pex:
                QtWidgets.QMessageBox.critical(None,
                        "File is incompatible with the rawautoparams",
                        "no parameters loaded!\n\n"
                        "Error message:\n{}".format(pex))
        gt.populate(augCanvas)
        augCanvas.spectplot.set_xlim(slims[0])
        augCanvas.spectplot.set_ylim(slims[1])
        gt.ann_spec(augCanvas.spectplot, augCanvas.ms)
        augCanvas.draw()


def update_recents(rcm, main_window, augCanvas, update, config, loadthread):
    """updates recents_menu (rcm)"""
    rcm.clear()
    # Actions need to be stored somewhere. Otherwise they end up in garbage.
    rcm.actionCache = []
    for i, j in enumerate(config.value("recents"), start=1):
        rcm.actionCache.append(QtWidgets.QAction("&{}. {}".format(i, j), None))
        rcm.actionCache[-1].triggered.connect(lambda _, fn=j: load_file(
            main_window, augCanvas, update, config, loadthread, filename=fn))
    rcm.actionCache.append(rcm.addSeparator())
    rcm.actionCache.append(QtWidgets.QAction("Clear Recents", None))
    [rcm.actionCache[-1].triggered.connect(i) for i in (
         lambda: config.setValue("recents", ""), lambda: update_recents(
             rcm, main_window, augCanvas, update, config, loadthread))]
    rcm.addActions(rcm.actionCache)


def dropped(event, parent, augCanvas, update, config, loadthread):
    dropurl = event.mimeData().urls()[0].toLocalFile()
    load_file(parent, augCanvas, update, config, loadthread, filename=dropurl)


def drag_entered(event):
    if event.mimeData().hasUrls() and event.mimeData().urls()[0]\
            .toLocalFile().lower().endswith('.raw'):
        event.accept()


def predictmz(form, augCanvas):
    text = form.text()
    if text == "":
        augCanvas.ms["predict"] = None
        return
    slims = [augCanvas.spectplot.get_xlim(),
             augCanvas.spectplot.get_ylim()]
    augCanvas.ms["predict"] = getmzpattern(text)
    gt.populate(augCanvas)
    augCanvas.spectplot.set_xlim(slims[0])
    augCanvas.spectplot.set_ylim(slims[1])
    augCanvas.draw()


def oddeven_changed(augCanvas, config, oddevenact):
    config.setValue("view/oddeven", oddevenact.isChecked())
    update_spectrum(augCanvas, config)


def key_pressed(event, augCanvas, config, update):
    if event.key() == QtCore.Qt.Key_F5:
        update_spectrum(augCanvas, config)
        if augCanvas.filename:
            update.signal.emit()
    if event.key() == QtCore.Qt.Key_C:
        if event.modifiers().__int__() == QtCore.Qt.ControlModifier:
            if augCanvas.paramstable.underMouse():
                dt.clip_tablestr(augCanvas)
            else:
                imgt.clip_spect_img(augCanvas.ms, augCanvas.spectplot,
                                    augCanvas.filename)
        if event.modifiers().__int__() == QtCore.Qt.ControlModifier + \
                QtCore.Qt.ShiftModifier:
            dt.clip_spectstr(augCanvas)
    if event.key() in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Right):
        gt.shift_times(event, augCanvas)


def about(parent):
    """constructs window with "about" info"""
    rawparver = rawautoparams.__version__ if autoparams else\
            "library not found"

    QtWidgets.QMessageBox.information(
            parent, "About Prasopes",
            "Prasopes Finnigan raw file viewer\n\n"
            "Version: {} (alpha)\n\n"
            "Rawprasslib version: {}\n"
            "Rawautoparams version: {}".format(
                prasopes.__version__, rawprasslib.__version__, rawparver))


def main():
    # thx to: https://stackoverflow.com/questions/779675/stop-python-from-closing-on-error/781074#781074
    sys.excepthook = show_exception_and_exit

    app = QtWidgets.QApplication(sys.argv)
    loadthread = QtCore.QThread()

    augCanvas = gt.AugFigureCanvas()
    update = update_signal()

    config = cf.settings()

    barHandler = QStatusBarLogger()
    barHandler.trigger.signal.connect(
        lambda: barHandler.statusBar.showMessage(barHandler.msg))

    p_logger = logging.getLogger('parseLogger')
    params_logger = logging.getLogger('acqLogLogger')
    drl_logger = logging.getLogger('drlLogger')
    zce_logger = logging.getLogger('zcelogger')
    rxn_logger = logging.getLogger('reactivityLogger')
    logging.basicConfig()
    # p_logger.setLevel("WARN")
    p_logger.setLevel("DEBUG")
    rxn_logger.setLevel("DEBUG")
    # drl_logger.setLevel("INFO")
    drl_logger.setLevel("DEBUG")
    zce_logger.setLevel("DEBUG")
    # params_logger.setLevel("DEBUG")
    p_logger.addHandler(barHandler)
    zce_logger.addHandler(barHandler)
    params_logger.addHandler(barHandler)
    barHandler.setLevel("DEBUG")

    main_window = QtWidgets.QMainWindow(windowTitle="Prasopes")
    update.signal.connect(lambda: main_window.setWindowTitle(
        "Prasopes - {}".format(os.path.basename(augCanvas.filename))))

    if QtGui.QIcon.themeName() == "":
        QtGui.QIcon.setThemeName("TangoMFK")

    consoledock = docks.consoleDockWidget(
            locals(), "&Console", "view/consolevisible")
    treedock = docks.treeDockWidget(
            "&File browser", "view/filebrowservisible", update, load_file,
            main_window, augCanvas, config, loadthread)
    paramsdock = docks.AugDock("Acquisition parameters", "&Acq parameters",
                               "view/acqparvisible")
    update.signal.connect(lambda: gt.update_paramstable(augCanvas))
    paramsdock.setWidget(augCanvas.paramstable)

    openact = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "document-open"), "&Open...", None)
    openact.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_O)
    openact.triggered.connect(lambda: load_file(
        main_window, augCanvas, update, config, loadthread))
    exportact = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "document-save-as"), "&Export...", None)
    exportact.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
    exportact.triggered.connect(lambda: ft.export_dial(
        augCanvas, main_window))
    printact = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "document-print"), "&Print", None)
    printact.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_P)
    printact.triggered.connect(lambda: print_graph(augCanvas))
    settingsact = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "preferences-system"), "&Settings...", None)
    settingsact.triggered.connect(lambda: cf.dial(main_window))
    quitact = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "application-exit"), "&Quit", None)
    quitact.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
    quitact.triggered.connect(main_window.close)
    zceact = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "applications-utilities"), "&TSQ zce...", None)
    zceact.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_T)
    zceact.triggered.connect(lambda: zce.dialog(
        main_window, augCanvas, update))
    drlact = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "applications-utilities"), "&DRL...", None)
    drlact.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_D)
    drlact.triggered.connect(lambda: drlgui.main_window(
        main_window, augCanvas, update))
    aboutact = QtWidgets.QAction("&About Prasopes", None)
    aboutact.triggered.connect(lambda: about(main_window))
    autozoomy = QtWidgets.QAction(QtGui.QIcon.fromTheme(
        "zoom-original"), "Auto Zoom Y", None, checkable=True,
        checked=config.value("view/autozoomy", type=bool))
    autozoomy.triggered.connect(lambda: config.setValue(
                                "view/autozoomy", autozoomy.isChecked()))
    autozoomy.triggered.connect(lambda: gt.autozoomy(augCanvas.spectplot))
    intensitiesact = QtWidgets.QAction(
        "&Show intensities", None, checkable=True,
        checked=config.value("view/intensities", type=bool))
    intensitiesact.triggered.connect(lambda: config.setValue(
        "view/intensities", intensitiesact.isChecked()))
    intensitiesact.triggered.connect(lambda: gt.ann_spec(
        augCanvas.spectplot, augCanvas.ms))
    intensitiesact.triggered.connect(lambda: augCanvas.draw())
    oddevenact = QtWidgets.QAction(
            "&Odd / even", None, checkable=True,
            checked=config.value("view/oddeven", type=bool))
    oddevenact.triggered.connect(
        lambda: oddeven_changed(augCanvas, config, oddevenact))

    predictform = QtWidgets.QLineEdit(maximumWidth=150)
    predictform.editingFinished.connect(lambda: predictmz(
        predictform, augCanvas))

    recents_menu = QtWidgets.QMenu('Open &Recent', main_window)
    update_recents(recents_menu, main_window, augCanvas,
                   update, config, loadthread)
    update.signal.connect(lambda: update_recents(
        recents_menu, main_window, augCanvas, update, config, loadthread))

    file_menu = QtWidgets.QMenu('&File', main_window)
    main_window.menuBar().addMenu(file_menu)
    file_menu.addAction(openact)
    file_menu.addMenu(recents_menu)
    file_menu.addAction(exportact)
    file_menu.addSeparator()
    file_menu.addAction(printact)
    file_menu.addSeparator()
    file_menu.addAction(settingsact)
    file_menu.addSeparator()
    file_menu.addAction(quitact)
    tools_menu = QtWidgets.QMenu('&Tools', main_window)
    main_window.menuBar().addMenu(tools_menu)
    tools_menu.addAction(zceact)
    tools_menu.addAction(drlact)
    tools_menu.addSeparator()
    view_menu = QtWidgets.QMenu('&View', main_window)
    [view_menu.addAction(i.action) for i in
     (treedock, paramsdock, consoledock)]
    [view_menu.addAction(i) for i in (autozoomy, intensitiesact)]
    view_menu.addSeparator()
    view_menu.addAction(oddevenact)
    main_window.menuBar().addMenu(view_menu)
    help_menu = QtWidgets.QMenu('&Help', main_window)
    main_window.menuBar().addMenu(help_menu)
    help_menu.addAction(aboutact)

    main_window.setCentralWidget(augCanvas)

    toolBar = QtWidgets.QToolBar(main_window)
    toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
    toolBar.setFloatable(False)
    toolBar.setMovable(False)
    toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

    toolBar.addAction(openact)
    toolBar.addAction(exportact)
    toolBar.addSeparator()
    toolBar.addWidget(QtWidgets.QLabel("Predict Formula:"))
    toolBar.addWidget(predictform)
    toolBar.addSeparator()
    toolBar.addAction(zceact)
    toolBar.addAction(drlact)
    toolBar.addSeparator()
    toolBar.addAction(autozoomy)

    main_window.dragEnterEvent = lambda event: drag_entered(event)
    main_window.dropEvent = lambda event: dropped(
        event, main_window, augCanvas, update, config, loadthread)
    main_window.setAcceptDrops(True)
    main_window.keyPressEvent = lambda event: key_pressed(
            event, augCanvas, config, update)
    main_window.resizeEvent = lambda event: augCanvas.constrained_draw()
    update.signal.connect(lambda: augCanvas.constrained_draw())

    main_window.addToolBar(QtCore.Qt.TopToolBarArea, toolBar)
    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, treedock)
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, paramsdock)
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, consoledock)
    main_window.setStatusBar(barHandler.statusBar)

    main_window.setFocus()

    if len(sys.argv) == 2:
        load_file(main_window, augCanvas, update, config, loadthread,
                  filename=sys.argv[1])
    else:
        gt.pop_plot([], [], augCanvas.spectplot, augCanvas.ms)
        gt.pop_plot([], [], augCanvas.chromplot, augCanvas.chrom)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
