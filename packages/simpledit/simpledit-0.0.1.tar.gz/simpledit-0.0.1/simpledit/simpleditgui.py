from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PIL import Image, ImageQt
import sys
import os
import im_functions
import time
import copy

widgetList = []
pixelArrayRGBA = []
pixelArrayRGBAOriginal = []
pyqtPixelArray = []
bugReportText = ''
feedbackText = ''
originalLabelWidget = []
switchOrder = False

save_state = []
ssptr = -1


class Ui_MainWindow(object):

    def setup_ui(self, MainWindow):

        MainWindow.setWindowTitle("SimplEdit")
        MainWindow.resize(1200, 850)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowIcon(QtGui.QIcon("images/icon.png"))

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.central_widget(MainWindow)
        self.tab_widget(MainWindow)
        self.tab_elements(MainWindow)
        self.label_widget(MainWindow)
        self.layouts(MainWindow)

    def central_widget(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setToolTipDuration(0)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        MainWindow.setCentralWidget(self.centralwidget)

    def label_widget(self, MainWindow):
        global pixelArrayRGBA
        global pyqtPixelArray
        global originalLabelWidget
        img = Image.open(os.path.abspath(os.path.dirname(__file__)) + '/images/open_file.png')
        pixels = list(img.getdata())
        width, height = img.size
        pixelArrayRGBA = [pixels[i * width:(i + 1) * width] for i in range(height)]
        pyqtPixelArray = QtGui.QPixmap('images/open_file.png')
        self.labelWidget = QtWidgets.QLabel(self.frame)
        self.labelWidget.setPixmap(pyqtPixelArray)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.labelWidget.setSizePolicy(sizePolicy)
        self.labelWidget.setMinimumSize(QtCore.QSize(200, 200))
        self.labelWidget.setMouseTracking(False)
        self.labelWidget.setAutoFillBackground(True)

    def tab_widget(self, MainWindow):
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(3000, 70))

        self.tab_home = QtWidgets.QWidget()
        self.tab_edit = QtWidgets.QWidget()
        self.tab_color = QtWidgets.QWidget()
        self.tab_filters = QtWidgets.QWidget()
        self.tab_effects = QtWidgets.QWidget()
        self.tab_creative = QtWidgets.QWidget()

        self.tabWidget.addTab(self.tab_home, "Home")
        self.tabWidget.addTab(self.tab_edit, "Edit")
        self.tabWidget.addTab(self.tab_color, "Color")
        self.tabWidget.addTab(self.tab_effects, "Effects")
        self.tabWidget.addTab(self.tab_filters, "Filters")
        self.tabWidget.addTab(self.tab_creative, "Creative")

        self.tabWidget.setCurrentIndex(0)

    def tab_elements(self, MainWindow):
        # Home Buttons
        self.tab_button(self, self.tab_home,
                        (0, 0, 40, 40), "Open an Image")
        self.button.clicked.connect(self.OpenImage)
        self.button.setIcon(QtGui.QIcon("images/open.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_home,
                        (45, 0, 40, 40), "Save a file")
        self.button.clicked.connect(self.SaveFile)
        self.button.setIcon(QtGui.QIcon("images/save_file.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Edit Buttons

        self.tab_button(self, self.tab_edit,
                        (0, 0, 40, 40), "Undo the last operation")
        self.button.clicked.connect(self.Undo)
        self.button.setIcon(QtGui.QIcon("images/undo.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (45, 0, 40, 40), "Redo the last operation")
        self.button.clicked.connect(self.Redo)
        self.button.setIcon(QtGui.QIcon("images/redo.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (90, 0, 40, 40), "Rotate the image Left")
        self.button.clicked.connect(self.RotateL)
        self.button.setIcon(QtGui.QIcon("images/rotate_left.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_edit,
                        (135, 0, 40, 40), "Rotate the image Right")
        self.button.clicked.connect(self.RotateR)
        self.button.setIcon(QtGui.QIcon("images/rotate_right.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Color Buttons

        self.tab_button(self, self.tab_color,
                        (0, 0, 40, 40), "Brighten or darken colors")
        self.button.clicked.connect(self.Brighten)
        self.button.setIcon(QtGui.QIcon("images/brightness.png"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_color,
                        (45, 0, 40, 40), "Change image transparency")
        self.button.clicked.connect(self.ChangeTransparency)
        self.button.setIcon(QtGui.QIcon("images/transparency.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Effects Buttons

        self.tab_button(self, self.tab_effects,
                        (0, 0, 40, 40), "Create a swirl effect")
        self.button.clicked.connect(self.Swirl)
        self.button.setIcon(QtGui.QIcon("images/swirl.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Filter Buttons

        self.tab_button(self, self.tab_filters,
                        (0, 0, 40, 40), "Invert all colors")
        self.button.clicked.connect(self.InvertColors)
        self.button.setIcon(QtGui.QIcon("images/invert.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (45, 0, 40, 40), "Add a light yellow tint")
        self.button.clicked.connect(self.YellowTint)
        self.button.setIcon(QtGui.QIcon("images/yellow_tint.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        self.tab_button(self, self.tab_filters,
                        (90, 0, 40, 40), "Add shades of maroon")
        self.button.clicked.connect(self.Redwood)
        self.button.setIcon(QtGui.QIcon("images/redwood.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Creative Buttons

        self.tab_button(self, self.tab_creative, (0, 0, 40, 40), "Before and After")
        self.button.clicked.connect(self.BeforeAndAfter)
        self.button.setIcon(QtGui.QIcon("images/before_after.svg"))
        self.button.setIconSize(QtCore.QSize(40, 40))

        # Button Separators

        self.tab_frame(self, self.tab_home, (90, 0, 3, 61))
        self.tab_frame(self, self.tab_edit, (180, 0, 3, 61))
        self.tab_frame(self, self.tab_color, (90, 0, 3, 61))
        self.tab_frame(self, self.tab_effects, (45, 0, 3, 61))
        self.tab_frame(self, self.tab_filters, (135, 0, 3, 61))
        self.tab_frame(self, self.tab_creative, (45, 0, 3, 61))

    def tab_button(self, MainWindow, widget_parent, position, status_tip):
        x, y, z, k = position
        self.button = QtWidgets.QToolButton(widget_parent)
        self.button.setGeometry(QtCore.QRect(x, y, z, k))
        self.button.setStatusTip(status_tip)

    def tab_frame(self, MainWindow, widget_parent, position):
        x, y, z, k = position
        self.separator = QtWidgets.QFrame(widget_parent)
        self.separator.setGeometry(QtCore.QRect(x, y, z, k))
        self.separator.setFrameShape(QtWidgets.QFrame.VLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)

    def layouts(self, MainWindow):
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.addWidget(self.labelWidget)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

    def on_change(self, arr):
        global ssptr
        global save_state
        save_state = save_state[0:ssptr + 1]
        ssptr += 1
        arr2 = []
        count = -1
        for i in arr:
            arr2.append([])
            count += 1
            for j in i:
                arr2[count].append((j[0], j[1], j[2], j[3]))
        save_state.append(arr2)

    def OpenImage(self):
        global pixelArrayRGBA
        global pyqtPixelArray
        global img
        global originalLabelWidget
        global switchOrder
        global ssptr
        global save_state
        global pixelArrayRGBAOriginal
        if (switchOrder):
            self.SwitchOrderAndRescale()
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName()
            imagePath = filename[0]
            pixmap = QtGui.QPixmap(imagePath)
            img = Image.open(imagePath).convert("RGBA")
            pixels = list(img.getdata())
            width, height = img.size
            pixelArrayRGBA = [pixels[i * width:(i + 1) * width] for i in range(height)]
            pyqtPixelArray = pixmap
            originalLabelWidget = pixmap
            pixelArrayRGBAOriginal = [pixels[i * width:(i + 1) * width] for i in range(height)]
            save_state = [[pixels[i * width:(i + 1) * width] for i in range(height)]]
            ssptr = 0

        except:
            return

        self.labelWidget.setPixmap(QtGui.QPixmap(pixmap.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

    def SaveFile(self):
        filePath = QtWidgets.QFileDialog.getSaveFileName()
        if filePath == "":
            return
        if (switchOrder):
            self.SwitchOrderAndRescale()
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

        img = im_functions.rgba2QImage(pixelArrayRGBA)
        QtGui.QPixmap.fromImage(img).save(filePath[0], "PNG")

    # to do
    def Undo(self):
        global ssptr
        global pixelArrayRGBA
        global save_state
        global pixelArrayRGBAOriginal
        if ssptr == 1:
            save_state[0] = copy.deepcopy(pixelArrayRGBAOriginal)
        if ssptr > 0:
            ssptr -= 1
            disp = im_functions.rgba2QImage(save_state[ssptr])
            if (switchOrder):
                self.labelWidget.setPixmap(
                    QtGui.QPixmap.fromImage(disp.scaled(QtCore.QSize(550, 700), QtCore.Qt.KeepAspectRatio)))
            else:
                self.labelWidget.setPixmap(
                    QtGui.QPixmap.fromImage(disp.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))
            pixelArrayRGBA = save_state[ssptr]
        else:
            print('cannot go back any further')
            # after undo operation is done, we want to take the user back
        # to the method they were working in before

    # to do
    def Redo(self):
        global ssptr
        global pixelArrayRGBA
        global save_state

        if ssptr < len(save_state) - 1:
            ssptr += 1
            disp = im_functions.rgba2QImage(save_state[ssptr])
            if (switchOrder):
                self.labelWidget.setPixmap(
                    QtGui.QPixmap.fromImage(disp.scaled(QtCore.QSize(550, 700), QtCore.Qt.KeepAspectRatio)))
            else:
                self.labelWidget.setPixmap(
                    QtGui.QPixmap.fromImage(disp.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))
            pixelArrayRGBA = save_state[ssptr]
        else:
            print('cant go ahead')
            # after redo operation is done, we want to take the user back
        # to the method they were working in before

    # To Do
    def RotateL(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

        a = im_functions.LRotate(pixelArrayRGBA)
        im_qt = a[0]
        pixelArrayRGBA = a[1]
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

        self.on_change(pixelArrayRGBA)

    # To Do
    def RotateR(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

        a = im_functions.RRotate(pixelArrayRGBA)
        im_qt = a[0]
        pixelArrayRGBA = a[1]
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

        self.on_change(pixelArrayRGBA)

    def img_to_pixmap(self, convert_img):
        data = convert_img.convert("RGBA").tobytes("raw", "RGBA")
        qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_RGBX8888)
        pixmap = QtGui.QPixmap.fromImage(qim)
        return pixmap

    def Brighten(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        # Finish Method
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

        slider = QtWidgets.QSlider()
        self.horizontalLayout.addWidget(slider)
        
        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.valueChanged.connect(self.updateLabel)
        
        submit_brightness = QtWidgets.QPushButton('Submit')
        self.horizontalLayout.addWidget(submit_brightness)
        
        submit_brightness.clicked.connect(self.updateBrightness)

    def updateBrightness(self):
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i+1).widget().setParent(None)
        im_qt = im_functions.AdjustBrightness(pixelArrayRGBA, slider_value)
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

        self.on_change(pixelArrayRGBA)

    def updateLabel(self, value):
        global slider_value
        slider_value = value

    # To Do
    def ChangeTransparency(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        # Finish Method
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
        
        slider = QtWidgets.QSlider()
        self.horizontalLayout.addWidget(slider)

        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.valueChanged.connect(self.updateLabel)
        
        submit_transparency = QtWidgets.QPushButton('Submit')
        self.horizontalLayout.addWidget(submit_transparency)
        
        submit_transparency.clicked.connect(self.updateBrightness)
    
    def updateTransparency(self):
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
        im_qt = im_functions.AdjustTransparency(pixelArrayRGBA, slider_value)
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

    # To Do
    def Swirl(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        # This messy for loop is to remove any widgets in horizontalLayout created by other methods
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
        # Finish Method
        im_qt = im_functions.Swirl(pixelArrayRGBA)
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

        self.on_change(pixelArrayRGBA)

    def InvertColors(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

        im_qt = im_functions.invert_filter(pixelArrayRGBA)
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

        self.on_change(pixelArrayRGBA)

    def YellowTint(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

        im_qt = im_functions.yellow_tint_filter(pixelArrayRGBA)
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

        self.on_change(pixelArrayRGBA)

    def Redwood(self):
        if ssptr < 0:
            return
        global pixelArrayRGBA
        global switchOrder

        if (switchOrder):
            self.SwitchOrderAndRescale()
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)

        im_qt = im_functions.redwood_filter(pixelArrayRGBA)
        self.labelWidget.setPixmap(
            QtGui.QPixmap.fromImage(im_qt.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))

        self.on_change(pixelArrayRGBA)

    def BeforeAndAfter(self):
        global switchOrder
        global originalLabelWidget
        global switchOrder
        if (switchOrder):
            self.SwitchOrderAndRescale()
        # This messy for loop is to remove any widgets in horizontalLayout created by other methods
        for i in reversed(range(self.horizontalLayout.count() - 1)):
            self.horizontalLayout.itemAt(i + 1).widget().setParent(None)
        # x = (self.horizontalLayout.itemAt(0))
        # self.horizontalLayout.itemAt(0).widget().setParent(None)
        try:
            self.labelWidget2 = QtWidgets.QLabel(self.frame)
            self.labelWidget2.setPixmap(originalLabelWidget)

            self.labelWidget.setPixmap(
                QtGui.QPixmap(self.labelWidget.pixmap().scaled(QtCore.QSize(550, 700), QtCore.Qt.KeepAspectRatio)))
            self.horizontalLayout.itemAt(0).widget().setParent(None)
            self.labelWidget2.setPixmap(
                QtGui.QPixmap(originalLabelWidget.scaled(QtCore.QSize(550, 700), QtCore.Qt.KeepAspectRatio)))
            # Finish Method
            self.horizontalLayout.addWidget(self.labelWidget2)
            self.horizontalLayout.addWidget(self.labelWidget)
            switchOrder = True
        except:
            print('No image loaded yet')

    def SwitchOrderAndRescale(self):
        global switchOrder
        switchOrder = False
        self.horizontalLayout.itemAt(1).widget().setParent(None)
        self.horizontalLayout.itemAt(0).widget().setParent(None)
        image = self.labelWidget.pixmap()
        self.labelWidget.setPixmap(QtGui.QPixmap(image.scaled(QtCore.QSize(1100, 700), QtCore.Qt.KeepAspectRatio)))
        self.horizontalLayout.addWidget(self.labelWidget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qss_file = open('styling/style.qss').read()
    app.setStyleSheet(qss_file)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())