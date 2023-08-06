# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from hyperborea.unit_preferences import UnitPreferencesWidget


class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        if not PreferencesDialog.objectName():
            PreferencesDialog.setObjectName(u"PreferencesDialog")
        PreferencesDialog.resize(414, 379)
        self.verticalLayout = QVBoxLayout(PreferencesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(PreferencesDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.unitTab = QWidget()
        self.unitTab.setObjectName(u"unitTab")
        self.gridLayout = QGridLayout(self.unitTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.unitsLabel = QLabel(self.unitTab)
        self.unitsLabel.setObjectName(u"unitsLabel")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.unitsLabel.setFont(font)

        self.gridLayout.addWidget(self.unitsLabel, 0, 0, 1, 2)

        self.horizontalSpacer = QSpacerItem(20, 13, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_7, 4, 0, 1, 2)

        self.unitPreferences = UnitPreferencesWidget(self.unitTab)
        self.unitPreferences.setObjectName(u"unitPreferences")

        self.gridLayout.addWidget(self.unitPreferences, 1, 1, 1, 1)

        self.tabWidget.addTab(self.unitTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.tabWidget, self.buttonBox)

        self.retranslateUi(PreferencesDialog)
        self.buttonBox.accepted.connect(PreferencesDialog.accept)
        self.buttonBox.rejected.connect(PreferencesDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PreferencesDialog)
    # setupUi

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QCoreApplication.translate("PreferencesDialog", u"Preferences", None))
        self.unitsLabel.setText(QCoreApplication.translate("PreferencesDialog", u"Display Units", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.unitTab), QCoreApplication.translate("PreferencesDialog", u"Units", None))
    # retranslateUi

