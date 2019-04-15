#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import * #QIcon, QPainter, QColor
import os
import time
import platform
from EvoEngine import *
from FromFileGetter import *



#--------------------------------------v--WINDOW-CLASSES--v----------------------------------------#

""" Class to inherit """
class Windower(QWidget):

	windowWidth = 700
	windowHeight = 420
	descStr = "Hello"
	deletingTurnON = False
	firstField = None
	onShowUpdateEnabled = False
	showSuccess = False

	def onShowUpdate(self):
		pass
	
	def buildInterfaceBase(self):
		""" Description """
		self.description = QTextEdit()
		self.description.setFontPointSize(10)
		self.description.setText(self.descStr)
		self.description.setReadOnly(True)

		""" Labels """
		fillLabel = QLabel("	", self)

		""" Edit fields """
		self.delField = QLineEdit()
		# Settings
		self.delField.setReadOnly(True)
		self.delField.setMaxLength(3) # ograniczenie liczby znaków
		
		""" Buttons """
		self.addButton = QPushButton("&Dodaj", self)
		self.delButton = QPushButton("Usuń", self)
		self.homeButton = QPushButton("OK", self)
		# Settings
		self.homeButton.setMinimumWidth(500)
		self.delButton.setMinimumWidth(100)
		self.delButton.setEnabled(False)

		""" Layout settings """
		primaryLayout = QGridLayout()
		middleLayout = QHBoxLayout()
		self.contentLayout = QVBoxLayout()
		self.vertiLayout = QVBoxLayout()
		endLayout = QHBoxLayout()
		# Description
		primaryLayout.addWidget(self.description, 0, 0)
		# MiddleLayout
		self.vertiLayout.addWidget(self.addButton)
		middleLayout.addLayout(self.contentLayout)
		middleLayout.addLayout(self.vertiLayout)
		primaryLayout.addLayout(middleLayout, 1, 0)
		# Wypełniacz
		primaryLayout.addWidget(fillLabel, 2, 0)
		# EndLayout
		endLayout.addWidget(self.delField)
		endLayout.addWidget(self.delButton)
		endLayout.addWidget(self.homeButton)
		primaryLayout.addLayout(endLayout, 3, 0)
		
		# Przypisanie utworzonego układu do okna
		self.setLayout(primaryLayout)

		""" przypisanie ActionListenerów """
		self.delButton.clicked.connect(self.actionDelete)
		self.homeButton.clicked.connect(self.actionBackHome)

		""" ustawienia okna """
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), QColor(157,255,170))
		self.setPalette(p)
	
	def calcInitPosition(self):
		x = int((screenAvaliableSize.width() - self.windowWidth)/2)
		y = int((screenAvaliableSize.height() - self.windowHeight)/2)
		return x,y
		
	def addWindow(self, window):
		if window.name == "saleWindow":
			self.saleWindow = window
		elif window.name == "szkoleniaWindow":
			self.szkoleniaWindow = window
		elif window.name == "uczestnicyWindow":
			self.uczestnicyWindow = window
		elif window.name == "settingsWindow":
			self.settingsWindow = window
		elif window.name == "resultWindow":
			self.resultWindow = window
		elif window.name == "homeWindow":
			self.homeWindow = window
		else :
			pass

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.close()

	def actionDelete(self):
		QMessageBox.information(self, "Sorry", "Function not avaliable yet...", QMessageBox.Ok)
		self.firstField.setFocus()
	
	def actionBackHome(self):
		self.homeWindow.showIt()
		self.hideIt()
	
	def appendFromFile(self, lastOld, classID):
		global dataBuilder
		newAmount = dataBuilder.numOf(classID)
		lastOld += 1
		while lastOld <= newAmount :
			objectDesc = dataBuilder.writeNr(lastOld, classID)
			self.description.append(objectDesc)
			self.spisStr += "\n" + objectDesc
			lastOld += 1
	
	def cleanIt(self):
		self.description.setText(self.descStr)
		if self.firstField != None : self.firstField.setText("")
	
	def showIt(self):
		global currentWindow, osName
		
		geom = currentWindow.frameGeometry()
		#print(geom)
		if osName == "Linux": geom.setTop(geom.top()+30) # Bo sie coś rozmiar zmienia nie wiem czemu
		elif osName == "Windows":
			geom.setTop(geom.top()+38)
			geom.setBottom(geom.bottom()-9)
			geom.setLeft(geom.left()+9)
			geom.setRight(geom.right()-9)
		self.setGeometry(geom)
		currentWindow = self
		if self.firstField != None : self.firstField.setFocus()
		if self.onShowUpdateEnabled : self.onShowUpdate()
		self.show()

	def hideIt(self):
		self.hide()

	def closeEvent(self, event):
		odp = QMessageBox.question(self, 'Think over it!', "Are you sure you want to close?",
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if odp == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()



class HomeWindow(Windower):

	name = "homeWindow"
	descStr = "Witamy w naszym programie!\nUłożymy dla Ciebie idealny plan szkoleń!\n\n"
	salStr = "Sal: "
	szkolenStr = "\nSzkoleń: "
	uczestnikowStr = "\nUczestników: "
	onShowUpdateEnabled = True

	def __init__(self, parent = None):
		super().__init__(parent)
		self.buildInterface()


	def onShowUpdate(self):
		global dataBuilder
		if dataBuilder.numOf(Szkolenie.ID)>0 and dataBuilder.numOf(Sala.ID)>0 and dataBuilder.numOf(Uczestnik.ID)>0 :
			self.btnGenPlan.setEnabled(True)
		else :
			self.btnGenPlan.setEnabled(False)
		if dataBuilder.numOf(Szkolenie.ID)!=0 or dataBuilder.numOf(Sala.ID)!=0 or dataBuilder.numOf(Uczestnik.ID)!=0 :
			self.btnClean.setEnabled(True)
		else :
			self.btnClean.setEnabled(False)
		self.description.setText(self.descStr + self.salStr + str(dataBuilder.numOf(Sala.ID))
			+ self.szkolenStr + str(dataBuilder.numOf(Szkolenie.ID)) + self.uczestnikowStr + str(dataBuilder.numOf(Uczestnik.ID)))

		
	def buildInterface(self):
		""" Description """
		self.description = QTextEdit()
		self.description.setReadOnly(True)
		self.description.setFontPointSize(13)

		""" Buttons """
		btnSala = QPushButton("&Sale", self)
		btnSzkolenie = QPushButton("S&zkolenia", self)
		btnUczestnik = QPushButton("U&czestnicy", self)
		self.btnClean = QPushButton("Czyść", self)
		btnfromFile = QPushButton("Załaduj z pliku", self)
		btnUstawienia = QPushButton("Ustawienia", self)
		self.btnGenPlan = QPushButton("GENERUJ PLAN", self)
		# Settings
		self.btnClean.setMinimumWidth(int(self.windowWidth*2/50))
		btnfromFile.setMinimumWidth(int(self.windowWidth*2/5))
		btnUstawienia.setMinimumWidth(int(self.windowWidth*2/5))
		
		""" Layout settings """
		primaryLayout = QGridLayout()
		horizontalLayout1 = QHBoxLayout()
		horizontalLayout2 = QHBoxLayout()
		
		# Description
		primaryLayout.addWidget(self.description, 0, 0)
		
		# Buttons
		horizontalLayout1.addWidget(btnSala)
		horizontalLayout1.addWidget(btnSzkolenie)
		horizontalLayout1.addWidget(btnUczestnik)
		horizontalLayout2.addWidget(self.btnClean)
		horizontalLayout2.addWidget(btnfromFile)
		horizontalLayout2.addWidget(btnUstawienia)
		primaryLayout.addWidget(self.btnGenPlan, 3, 0)
		
		# Layouts
		primaryLayout.addLayout(horizontalLayout1, 1, 0)
		primaryLayout.addLayout(horizontalLayout2, 2, 0)
		
		# przypisanie utworzonego układu do okna
		self.setLayout(primaryLayout)

		""" przypisanie ActionListenerów """
		btnSala.clicked.connect(self.actionManager)
		btnSzkolenie.clicked.connect(self.actionManager)
		btnUczestnik.clicked.connect(self.actionManager)
		self.btnClean.clicked.connect(self.reset)
		btnfromFile.clicked.connect(self.fromFileAction)
		btnUstawienia.clicked.connect(self.actionManager)
		self.btnGenPlan.clicked.connect(self.generatePlanAction)

		""" ustawienia okna """
		[x,y] = self.calcInitPosition()
		self.setGeometry(x, y, self.windowWidth, self.windowHeight)
		self.setWindowTitle("Generator Planów Szkoleń")
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), QColor(245,161,0))
		self.setPalette(p)


	def actionManager(self):
		global dataBuilder
		nadawca = self.sender()
		if nadawca.text() == "&Sale":
			self.saleWindow.showIt()
			self.hideIt()
		elif nadawca.text() == "S&zkolenia":
			self.szkoleniaWindow.showIt()
			self.hideIt()
		elif nadawca.text() == "U&czestnicy":
			if dataBuilder.numOf(Szkolenie.ID) == 0:
				QMessageBox.information(self, "Nie tak szybko!", "Aby dodać uczestników, musisz najpierw\ndodać jakieś szkolenia.", QMessageBox.Ok)
			else :
				self.uczestnicyWindow.showIt()
				self.hideIt()
		elif nadawca.text() == "Ustawienia":
			self.settingsWindow.showIt()
			self.hideIt()
		else:
			pass
	
	
	def fromFileAction(self):
		global programPath, dataBuilder
		#if self.btnClean.isEnabled():
		odp1 = QMessageBox.information(self, "Parę informacji...",
			"Dane będą pobrane z pliku \"data.txt\" z folderu, w którym znajduje się ten program:\n"+programPath, QMessageBox.Ok | QMessageBox.Cancel)
		if odp1 == QMessageBox.Ok:
		
			if dataBuilder.numOf(Szkolenie.ID)>0:
				odp2 = QMessageBox.warning(self, "Uważaj!",
				"Typy szkoleń są autonumerowane, dlatego dodanie z pliku może grozić utratą spójności preferencji uczestników", QMessageBox.Ok | QMessageBox.Cancel)
				if odp2==QMessageBox.Cancel: return
				
			listsFromFile = readData()
			if listsFromFile.isGood:
				a = dataBuilder.numOf(Sala.ID)
				b = dataBuilder.numOf(Szkolenie.ID)
				c = dataBuilder.numOf(Uczestnik.ID)
				dataBuilder.extendFromFile(listsFromFile)
				self.onShowUpdate()
				self.saleWindow.appendFromFile(a, Sala.ID)
				self.szkoleniaWindow.appendFromFile(b, Szkolenie.ID)
				self.uczestnicyWindow.appendFromFile(c, Uczestnik.ID)
				QMessageBox.information(self, "Sukces!", "Udało się poprawnie pobrać dane z pliku", QMessageBox.Ok)
				
			else :
				QMessageBox.critical(self, "Porażka!", "Nie udało się pobrać danyh z pliku", QMessageBox.Ok)
		else :
			pass
		
	
	def generatePlanAction(self):
		global dataBuilder, dataReceiver
		odp = QMessageBox.information(self, 'Zaczynamy?', "Na czas obliczeń okno programu zniknie.",
			QMessageBox.Ok | QMessageBox.Cancel)
		if odp == QMessageBox.Ok:
			self.hideIt()
			dataBuilder.supplyTheEngine()
			dataReceiver = DataReceiver()
			self.resultWindow.showIt()
		else:
			pass
	
	
	def reset(self, stranger = None):
		global dataBuilder
		if stranger == None or stranger == False or stranger == True: parent = self
		else : parent = stranger
		odp = QMessageBox.warning(parent, 'Jesteś pewien?', "Wszystkie dane zostaną usunięte",
			QMessageBox.Ok | QMessageBox.Cancel)
		if odp == QMessageBox.Ok:
			dataBuilder.clearAll()
			self.onShowUpdate()
			self.saleWindow.cleanIt()
			self.szkoleniaWindow.cleanIt()
			self.uczestnicyWindow.cleanIt()
			self.resultWindow.cleanIt()
		return odp



class SaleWindow(Windower):

	name = "saleWindow"
	descStr = "Jesteś w trybie dodawania sal. Aby dodać salę, musisz podać jej pojemność wyrażoną w ilości miejsc.\n"
	spisStr = ""
	
	def __init__(self, parent = None):
		super().__init__(parent)
		self.buildInterface()

	
	def buildInterface(self):
		self.buildInterfaceBase()
		
		""" Labels """
		pojeLabel = QLabel("Pojemność:", self)
		# Settings
		pojeLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		
		""" Edit fields """
		self.pojeField = QLineEdit()
		# Settings
		self.pojeField.setToolTip('Wpisz <b>liczbę</b> i wciśnij [Enter]')
		self.pojeField.setMaxLength(2) # ograniczenie liczby znaków
		self.firstField = self.pojeField
		
		""" Layout settings """
		# hori 1
		horiLayout1 = QHBoxLayout()
		horiLayout1.addWidget(pojeLabel)
		horiLayout1.addWidget(self.pojeField)
		self.contentLayout.addLayout(horiLayout1)
		
		""" przypisanie ActionListenerów """
		self.addButton.clicked.connect(self.actionAdd)
		
		""" ustawienia okna """
		self.setWindowTitle("Dodawanie sal")
	
		
	def actionAdd(self):
		global dataBuilder
		if self.pojeField.text() == "":
			QMessageBox.warning(self, "Coś nie tak", "Brakuje danych...", QMessageBox.Ok)
			self.firstField.setFocus()
			return
		try:
			pojemnosc = int(self.pojeField.text())
			dataBuilder.addNew(Sala(pojemnosc), Sala.ID)
			self.pojeField.setText("")
			salaDesc = dataBuilder.writeNr(dataBuilder.numOf(Sala.ID), Sala.ID)
			self.description.append(salaDesc)
			self.spisStr += "\n"+ salaDesc
			if self.deletingTurnON:
				self.delButton.setEnabled(True)
				self.delField.setReadOnly(True)
				deletingTurnON = False
			if self.showSuccess: QMessageBox.information(self, "Sukces!", "Pomyślnie dodano salę.", QMessageBox.Ok)
		except ValueError:
			QMessageBox.warning(self, "Error", "Wrong data type", QMessageBox.Ok)
			self.firstField.selectAll()
		self.firstField.setFocus()

		
	def keyPressEvent(self, e):
		super().keyPressEvent(e)
		if e.key() == Qt.Key_Enter:
			if self.pojeField.hasFocus(): self.actionAdd()
			elif self.homeButton.hasFocus(): self.actionBackHome()

	
			
class SzkoleniaWindow(Windower):

	name = "szkoleniaWindow"
	descStr = "Jesteś w trybie dodawania szkoleń. Aby dodać szkolenie, musisz podać wymienione poniżej informacje na jego temat.\n"
	spisStr = ""
	onShowUpdateEnabled = True

	def __init__(self, parent = None):
		super().__init__(parent)
		self.buildInterface()
	
	
	def onShowUpdate(self):
		self.focus = 0
	
	
	def buildInterface(self):
		self.buildInterfaceBase()
		
		""" Labels """
		pojeLabel = QLabel("Pojemność:", self)
		czasLabel = QLabel("Czas trwania:", self)
		iloscLabel = QLabel("Ilość:", self)
		# Settings
		pojeLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		czasLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		iloscLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		
		""" Edit fields """
		self.pojeField = QLineEdit()
		self.czasField = QLineEdit()
		self.iloscField = QLineEdit()
		# Settings
		self.pojeField.setMaxLength(5) # ograniczenie liczby znaków
		self.firstField = self.pojeField
		
		""" Buttons """
		self.nextButton = QPushButton("Focus Next", self)
		
		""" Layout settings """
		# hori 2
		horiLayout2 = QHBoxLayout()
		horiLayout2.addWidget(pojeLabel)
		horiLayout2.addWidget(self.pojeField)
		# hori 3
		horiLayout3 = QHBoxLayout()
		horiLayout3.addWidget(czasLabel)
		horiLayout3.addWidget(self.czasField)
		# hori 4
		horiLayout4 = QHBoxLayout()
		horiLayout4.addWidget(iloscLabel)
		horiLayout4.addWidget(self.iloscField)
		# verti
		self.vertiLayout.addWidget(self.nextButton)
		# content
		self.contentLayout.addLayout(horiLayout2)
		self.contentLayout.addLayout(horiLayout3)
		self.contentLayout.addLayout(horiLayout4)
		
		""" przypisanie ActionListenerów """
		self.addButton.clicked.connect(self.actionAdd)
		self.nextButton.clicked.connect(self.nextAction)
		
		""" ustawienia okna """
		self.setWindowTitle("Dodawanie szkoleń")
	
	
	def actionAdd(self):
		global dataBuilder
		if self.pojeField.text() == "":
			QMessageBox.warning(self, "Zara chwila", "Brakuje danych...", QMessageBox.Ok)
			self.firstField.setFocus()
			self.focus = 0
			return
		elif self.czasField.text() == "":
			QMessageBox.warning(self, "Zara chwila", "Brakuje danych...", QMessageBox.Ok)
			self.czasField.setFocus()
			self.focus = 1
			return
		elif self.iloscField.text() == "":
			QMessageBox.warning(self, "Zara chwila", "Brakuje danych...", QMessageBox.Ok)
			self.iloscField.setFocus()
			self.focus = 2
			return
		try:
			checker = 0
			pojemnosc = int(self.pojeField.text())
			checker = 1
			czas = int(self.czasField.text())
			checker = 2
			ilosc = int(self.iloscField.text())
			
			dataBuilder.addNew(Szkolenie(pojemnosc,czas,ilosc), Szkolenie.ID)
			
			self.pojeField.setText("")
			self.czasField.setText("")
			self.iloscField.setText("")
			szkolenieDesc = dataBuilder.writeNr(dataBuilder.numOf(Szkolenie.ID), Szkolenie.ID)
			self.description.append(szkolenieDesc)
			self.spisStr += "\n"+ szkolenieDesc
			if self.deletingTurnON:
				self.delButton.setEnabled(True)
				self.delField.setReadOnly(True)
				deletingTurnON = False
			if self.showSuccess: QMessageBox.information(self, "Sukces!", "Pomyślnie dodano szkolenie.", QMessageBox.Ok)
		except ValueError:
			QMessageBox.warning(self, "Error", "Wrong data type", QMessageBox.Ok)
			if checker==0:
				self.firstField.selectAll()
				self.firstField.setFocus()
			elif checker==1:
				self.czasField.selectAll()
				self.czasField.setFocus()
			else :
				self.iloscField.selectAll()
				self.iloscField.setFocus()
			self.focus = checker
			return
		self.firstField.setFocus()
		self.focus = 0
	
	
	def nextAction(self):
		if self.focus==0: self.czasField.setFocus(); self.focus = 1
		elif self.focus==1: self.iloscField.setFocus(); self.focus = 2
		elif self.focus==2: self.firstField.setFocus(); self.focus = 0
		else: pass
	
	
	def cleanIt(self):
		super().cleanIt()
		self.czasField.setText("")
		self.iloscField.setText("")


		
class UczestnicyWindow(Windower):

	name = "uczestnicyWindow"
	descStr = "Jesteś w trybie dodawania uczestników. Aby dodać uczestnika, musisz podać jego preferencje odnośnie typów szkoleń.\n\nAktualnie dostępne są szkolenia typu: "
	prefStr = "Preferencje:"
	spisStr = ""
	preferencje = []
	onShowUpdateEnabled = True

	def __init__(self, parent = None):
		super().__init__(parent)
		self.buildInterface()

		
	def onShowUpdate(self):
		global dataBuilder
		self.szkoStr = "1"
		for i in range(dataBuilder.numOf(Szkolenie.ID)-1):
			self.szkoStr = self.szkoStr + ", " + str(i+2)
		self.description.setText(self.descStr + self.szkoStr +"\n"+ self.spisStr)

		
	def buildInterface(self):
		self.buildInterfaceBase()
		
		""" Labels """
		self.prefLabel = QLabel(self.prefStr, self)
		# Settings
		self.prefLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		
		""" Edit fields """
		self.prefField = QLineEdit()
		# Settings
		self.prefField.setMaxLength(2) # ograniczenie liczby znaków
		self.firstField = self.prefField
		
		""" Buttons """
		self.prefButton = QPushButton("Dodaj preferencję", self)
		# Settings
		self.addButton.setEnabled(False)
		
		""" Layout settings """
		# hori 1
		horiLayout1 = QHBoxLayout()
		horiLayout1.addWidget(self.prefLabel)
		horiLayout1.addWidget(self.prefField)
		horiLayout1.addWidget(self.prefButton)
		self.contentLayout.addLayout(horiLayout1)
		
		""" przypisanie ActionListenerów """
		self.prefButton.clicked.connect(self.actionAddPreferencja)
		self.addButton.clicked.connect(self.actionAddUczestnik)
		
		""" ustawienia okna """
		self.setWindowTitle("Dodawanie uczestników")
	
	
	def actionAddPreferencja(self):
		if self.prefField.text() == "":
			QMessageBox.warning(self, "Zara chwila", "Brakuje danych...", QMessageBox.Ok)
			self.firstField.setFocus()
			return
		try:
			typ = int(self.prefField.text())-1
			if typ < 0 or typ > dataBuilder.numOf(Szkolenie.ID)-1:
				QMessageBox.warning(self, "Błąd", "Nie zdefiniowano takiego szkolenia", QMessageBox.Ok)
				self.firstField.selectAll()
			elif self.preferencje.count(typ)!=0 :
				QMessageBox.warning(self, "Błąd", "Na to szkolenie uczestnik już się zgłosił", QMessageBox.Ok)
				self.firstField.selectAll()
			else :
				self.preferencje.append(typ)
				self.prefField.setText("")
				if self.prefLabel.text() == self.prefStr :
					self.prefLabel.setText(self.prefLabel.text()+" "+str(typ+1))
				else :
					self.prefLabel.setText(self.prefLabel.text()+", "+str(typ+1))
		except ValueError:
			QMessageBox.warning(self, "Error", "Wrong data type", QMessageBox.Ok)
			self.firstField.selectAll()
		if len(self.preferencje)!=0 : self.addButton.setEnabled(True)
		self.firstField.setFocus()
	
	
	def actionAddUczestnik(self):
		global dataBuilder
		dataBuilder.addNew(Uczestnik(self.preferencje.copy()), Uczestnik.ID)
		
		self.preferencje.clear()
		self.addButton.setEnabled(False)
		self.prefField.setText("")
		self.prefLabel.setText(self.prefStr)
		uczestnikDesc = dataBuilder.writeNr(dataBuilder.numOf(Uczestnik.ID), Uczestnik.ID)
		self.description.append(uczestnikDesc)
		self.spisStr = self.spisStr +"\n"+ uczestnikDesc
		if self.deletingTurnON:
			self.delButton.setEnabled(True)
			self.delField.setReadOnly(True)
			deletingTurnON = False
		if self.showSuccess: QMessageBox.information(self, "Sukces!", "Pomyślnie dodano uczestnika.", QMessageBox.Ok)
		self.firstField.setFocus()

	
	def cleanIt(self):
		super().cleanIt()
		self.preferencje.clear()
		self.addButton.setEnabled(False)
		self.prefField.setText("")
		self.prefLabel.setText(self.prefStr)
		self.spisStr = ""
		

	
class SettingsWindow(Windower):

	name = "settingsWindow"
	descStr = "Jesteś w trybie ustawień dodatkowych.\n"

	def __init__(self, parent = None):
		super().__init__(parent)
		self.buildInterface()

		
	def buildInterface(self):
		""" Description """
		self.description = QLabel(self.descStr, self)
		
		""" Labels """
		dayLenLabel = QLabel("Długość dnia:", self)
		numOfDaysLabel = QLabel("Ilość dni:", self)
		iloPokoLabel = QLabel("Ilość pokoleń:", self)
		liczePokoLabel = QLabel("Liczebność pokoleń:", self)
		mutaChaLabel = QLabel("Szansa mutacji:", self)
		fillLabel = QLabel("			", self)
		
		pictureLabel = QLabel(self)
		pixmap = QPixmap('cogwheel.jpg')
		pictureLabel.setPixmap(pixmap)
		# Settings
		dayLenLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		numOfDaysLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		iloPokoLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		liczePokoLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		mutaChaLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
		pictureLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)

		""" Edit fields """
		self.dayLenField = QLineEdit()
		self.numOfDaysField = QLineEdit()
		self.iloPokoField = QLineEdit()
		self.liczePokoField = QLineEdit()
		self.mutaChaField = QLineEdit()
		# Settings
		self.firstField = self.dayLenField
		self.dayLenField.setText(str(DataBuilder.dayLength))
		self.numOfDaysField.setText(str(DataBuilder.numOfDays))
		self.iloPokoField.setText(str(DataBuilder.ilosc_pokolen))
		self.liczePokoField.setText(str(DataBuilder.liczebnosc))
		self.mutaChaField.setText(str(DataBuilder.mutate_chance))

		""" Buttons """
		homeButton = QPushButton("OK", self)

		""" Layout settings """
		primaryLayout = QGridLayout()
		primaryLayout.addWidget(self.description, 0, 0, 1, 3)
		primaryLayout.addWidget(dayLenLabel, 1, 0)
		primaryLayout.addWidget(self.dayLenField, 1, 1)
		primaryLayout.addWidget(numOfDaysLabel, 2, 0)
		primaryLayout.addWidget(self.numOfDaysField, 2, 1)
		primaryLayout.addWidget(fillLabel, 3, 0, 1, 3)
		primaryLayout.addWidget(iloPokoLabel, 4, 0)
		primaryLayout.addWidget(self.iloPokoField, 4, 1)
		primaryLayout.addWidget(liczePokoLabel, 5, 0)
		primaryLayout.addWidget(self.liczePokoField, 5, 1)
		primaryLayout.addWidget(mutaChaLabel, 6, 0)
		primaryLayout.addWidget(self.mutaChaField, 6, 1)
		primaryLayout.addWidget(fillLabel, 7, 0, 1, 3)
		primaryLayout.addWidget(homeButton, 8, 0, 1, 3)
		
		primaryLayout.addWidget(pictureLabel, 1, 2, 5, 1)
		
		# Przypisanie utworzonego układu do okna
		self.setLayout(primaryLayout)

		""" przypisanie ActionListenerów """
		homeButton.clicked.connect(self.actionBackHome)

		""" ustawienia okna """
		self.setWindowTitle("Ustawienia")
		
		
	def actionBackHome(self):
		global dataBuilder
		try:
			checker = 0
			dataBuilder.dayLength = int(self.dayLenField.text())
			checker = 1
			dataBuilder.numOfDays = int(self.numOfDaysField.text())
			checker = 2
			dataBuilder.ilosc_pokolen = int(self.iloPokoField.text())
			checker = 3
			dataBuilder.liczebnosc = int(self.liczePokoField.text())
			checker = 4
			dataBuilder.mutate_chance = float(self.mutaChaField.text())
			self.homeWindow.showIt()
			self.hideIt()
		except ValueError:
			QMessageBox.warning(self, "Error", "Wrong data type", QMessageBox.Ok)
			if checker==0:
				self.firstField.selectAll()
				self.firstField.setFocus()
			elif checker==1:
				self.numOfDaysField.selectAll()
				self.numOfDaysField.setFocus()
			elif checker==2:
				self.iloPokoField.selectAll()
				self.iloPokoField.setFocus()
			elif checker==3:
				self.liczePokoField.selectAll()
				self.liczePokoField.setFocus()
			else :
				self.mutaChaField.selectAll()
				self.mutaChaField.setFocus()
		

		
class ResultWindow(Windower):
	name = "resultWindow"
	descStr = "Plan został ułożony!\nMożesz zobaczyć go z perspektywy poszczególnych sal bądź uczestników.\n"
	separateStr = "\n\n--------------------------------------------------\n"
	
	def __init__(self, parent = None):
		super().__init__(parent)
		self.buildInterface()

		
	def buildInterface(self):
		""" Description """
		self.description = QTextEdit()
		self.description.setReadOnly(True)
		self.description.setFontPointSize(10)
		self.description.setText(self.descStr)

		""" Buttons """
		btnSala = QPushButton("Sale", self)
		btnUczestnik = QPushButton("Uczestnicy", self)
		btnForNerds = QPushButton("Dla nerdów", self)
		btnToFile = QPushButton("Podgląd danych", self)
		#btnToFile.setEnabled(False)
		self.btnGenPlan = QPushButton("Nowy plan", self)
		
		""" Layout settings """
		primaryLayout = QGridLayout()
		horizontalLayout1 = QHBoxLayout()
		horizontalLayout2 = QHBoxLayout()
		
		# Description
		primaryLayout.addWidget(self.description, 0, 0)
		
		# Buttons
		horizontalLayout1.addWidget(btnSala)
		horizontalLayout1.addWidget(btnUczestnik)
		horizontalLayout1.addWidget(btnForNerds)
		horizontalLayout2.addWidget(btnToFile)
		horizontalLayout2.addWidget(self.btnGenPlan)
		
		# Layouts
		primaryLayout.addLayout(horizontalLayout1, 1, 0)
		primaryLayout.addLayout(horizontalLayout2, 2, 0)
		
		# przypisanie utworzonego układu do okna
		self.setLayout(primaryLayout)

		""" przypisanie ActionListenerów """
		btnSala.clicked.connect(self.actionManager)
		btnUczestnik.clicked.connect(self.actionManager)
		btnForNerds.clicked.connect(self.actionManager)
		btnToFile.clicked.connect(self.actionManager)
		self.btnGenPlan.clicked.connect(self.actionManager)

		""" ustawienia okna """
		[x,y] = self.calcInitPosition()
		self.setGeometry(x, y, self.windowWidth, self.windowHeight)
		self.setWindowTitle("PLAN SZKOLEŃ")
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), QColor(145,0,0))
		self.setPalette(p)


	def actionManager(self):
		global dataReceiver
		nadawca = self.sender()
		if nadawca.text() == "Sale":
			self.description.setText("PLAN DLA SAL:" + dataBuilder.writePlan(Sala.ID))
		elif nadawca.text() == "Uczestnicy":
			self.description.setText("PLAN DLA UCZESTNIKÓW:" + dataBuilder.writePlan(Uczestnik.ID))
			#self.description.scrollToAnchor("PLAN DLA UCZESTNIKÓW:")
		elif nadawca.text() == "Dla nerdów":
			self.description.setText("Statystyki dla nerdów:\n\n" + dataReceiver.writeForNerds())
		elif nadawca.text() == "Podgląd danych":
			self.description.setText("UŻYTE DANE:\n"
									+self.saleWindow.spisStr + self.separateStr
									+self.szkoleniaWindow.spisStr + self.separateStr
									+self.uczestnicyWindow.spisStr)
		elif nadawca.text() == "Nowy plan":
			odp = QMessageBox.question(self, 'Zaczynamy?', "Wyczyścić poprzednie dane?",
				QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
			if odp == QMessageBox.Yes:
				odp2 = self.homeWindow.reset(self)
				if odp2 == QMessageBox.Ok:
					self.homeWindow.showIt()
					self.hideIt()
			elif odp == QMessageBox.No:
				self.homeWindow.showIt()
				self.hideIt()
				self.cleanIt()
			else:
				pass
		else:
			pass
	
	
#---------------------------------------v--DATA-CLASSES--v-----------------------------------------#
		
class Sala():
	
	ID = 0
	descStr = "Sala nr %s.  Liczba miejsc: %s"
	nrStr = "Sala nr %s:\n"
	dayStr = "      Dzień %s:\n"
	planStr = "            %s - %s: szkolenie typu %s\n" #.  Uczestnicy: %s
	startDict = 'Start'
	koniecDict = 'Koniec'
	szkoleDict = 'Szkolenie'
	uczestDict = 'Uczestnicy'
	grafikDni = []
	
	def __init__(self, pojemnosc):
		self.pojemnosc = pojemnosc
		

class Szkolenie():
	
	ID = 1
	descStr = "Szkolenie typu: %s.  Liczba miejsc: %s.  Długość: %s h.  Ilość: %s."
	
	def __init__(self, pojemnosc, czas_trwania, ilosc):
		self.pojemnosc = pojemnosc
		self.czas_trwania = czas_trwania
		self.ilosc = ilosc


class Uczestnik():
	
	ID = 2
	descStr = "Uczestnik nr %s.  Preferowane szkolenia: %s"
	nrStr = "Uczestnik nr %s:\n"
	dayStr = "      Dzień %s:\n"
	planStr = "            %s - %s: szkolenie typu %s. Sala nr %s\n"
	startDict = 'Godzina rozpoczecia'
	koniecDict = 'Godzina zakonczenia'
	szkoleDict = 'Szkolenie'
	salaDict = 'Sala'
	grafikDni = []
	
	def __init__(self, preferencje):
		self.preferencje = preferencje

		
	
class DataBuilder():

	ilosc_pokolen = 60
	liczebnosc = 60
	mutate_chance = 0.1
	
	dayStart = 8
	dayLength = 8
	numOfDays = 3
	
	
	sale = []
	szkolenia = []
	uczestnicy = []
	

	#-----------SALE-----SZKOLENIA-----UCZESTNICY----------#
	def addNew(self, newData, id):
		if id == Sala.ID:
			self.sale.append(newData)
		elif id == Szkolenie.ID:
			self.szkolenia.append(newData)
		elif id == Uczestnik.ID:
			self.uczestnicy.append(newData)
		else :
			return 0
	
	def numOf(self, id):
		if id == Sala.ID:
			return len(self.sale)
		elif id == Szkolenie.ID:
			return len(self.szkolenia)
		elif id == Uczestnik.ID:
			return len(self.uczestnicy)
		else :
			return 0
	
	def writeNr(self, nr, id):
		if id == Sala.ID:
			return Sala.descStr %(nr, dataBuilder.sale[nr-1].pojemnosc)
		elif id == Szkolenie.ID:
			szkolenie = self.szkolenia[nr-1]
			return Szkolenie.descStr %(nr, szkolenie.pojemnosc, szkolenie.czas_trwania, szkolenie.ilosc)
		elif id == Uczestnik.ID:
			prefy = self.uczestnicy[nr-1].preferencje.copy()
			for p in range(len(prefy)):
				prefy[p] = prefy[p] + 1
			return Uczestnik.descStr %(nr, prefy)
		else :
			return 0
	
	def writePlan(self, id):
		wholeGraphic = ""
		if id == Sala.ID:
			for s in range(len(self.sale)):
				#wholeGraphic += "\n\n"+ Sala.nrStr%(s+1) + str(self.sale[s].grafikDni)
				wholeGraphic += "\n\n"+ Sala.nrStr%(s+1)
				for d in range(len(self.sale[s].grafikDni)):
					wholeGraphic += Sala.dayStr%(d+1)
					for p in range(len(self.sale[s].grafikDni[d])):
						wholeGraphic += Sala.planStr%(self.sale[s].grafikDni[d][p][Sala.startDict]+self.dayStart,
													self.sale[s].grafikDni[d][p][Sala.koniecDict]+self.dayStart,
													self.sale[s].grafikDni[d][p][Sala.szkoleDict]+1)
		elif id == Uczestnik.ID:
			for u in range(len(self.uczestnicy)):
				#wholeGraphic += "\n\n"+ Uczestnik.nrStr%(u+1) + str(self.uczestnicy[u].grafikDni)
				wholeGraphic += "\n\n"+ Uczestnik.nrStr%(u+1)
				for d in range(len(self.uczestnicy[u].grafikDni)):
					wholeGraphic += Uczestnik.dayStr%(d+1)
					for p in range(len(self.uczestnicy[u].grafikDni[d])):
						wholeGraphic += Uczestnik.planStr%(self.uczestnicy[u].grafikDni[d][p][Uczestnik.startDict]+self.dayStart,
													self.uczestnicy[u].grafikDni[d][p][Uczestnik.koniecDict]+self.dayStart,
													self.uczestnicy[u].grafikDni[d][p][Uczestnik.szkoleDict]+1,
													self.uczestnicy[u].grafikDni[d][p][Uczestnik.salaDict]+1)
		return wholeGraphic

	
	#----------------------INNE----------------------------#
	def extendFromFile(self, lFF):
		for x in lFF.ffList1 :
			self.sale.append(Sala(x))
		for y in range(len(lFF.ffList2)) :
			self.szkolenia.append(Szkolenie(lFF.ffList2[y], lFF.ffList3[y], lFF.ffList4[y]))
		for z in lFF.ffList5 :
			self.uczestnicy.append(Uczestnik(z))
		
	
	def supplyTheEngine(self):
		simpleDataList = [
			self.ilosc_pokolen, self.liczebnosc, self.mutate_chance,
			self.dayLength, self.numOfDays,
			len(self.sale), len(self.szkolenia), len(self.uczestnicy)]

		pojemnosc_sal=[]
		for s in self.sale:
			pojemnosc_sal.append(s.pojemnosc)
		
		poj_szkolen=[]
		t_szkolen=[]
		max_szkolen=[]
		for sz in self.szkolenia:
			poj_szkolen.append(sz.pojemnosc)
			t_szkolen.append(sz.czas_trwania)
			max_szkolen.append(sz.ilosc)
		
		preferencje_ucz=[]
		for u in self.uczestnicy:
			preferencje_ucz.append(u.preferencje.copy())
		
		listedDataList = [pojemnosc_sal, poj_szkolen, t_szkolen, max_szkolen, preferencje_ucz]
		
		dataAssignment(simpleDataList.copy(), listedDataList.copy())
	
	
	def clearAll(self):
		self.sale.clear()
		self.szkolenia.clear()
		self.uczestnicy.clear()
		

		
class DataReceiver():

	def __init__(self):
		[self.grafikSal, self.grafikUczestnikow, self.forNerds] = runTheCode()
		self.extractData()
		
	
	def writeForNerds(self):
		return str(self.forNerds)
	
	
	def extractData(self):
		global dataBuilder
		for s in range(len(self.grafikSal)):
			dataBuilder.sale[s].grafikDni = self.grafikSal[s]
		for u in range(len(self.grafikUczestnikow)):
			dataBuilder.uczestnicy[u].grafikDni = self.grafikUczestnikow[u]
		
	
#-----------------------------------------END-OF-CLASSES-------------------------------------------#


def getScreenSize(app):
	global screenAvaliableSize
	screen = app.primaryScreen()
	screenAvaliableSize = screen.availableGeometry()


if __name__ == '__main__':
	import sys
	global currentWindow, osName, programPath, dataBuilder
	
	app = QApplication(sys.argv)
	getScreenSize(app)
	osName = platform.system()
	programPath = os.path.dirname(__file__)
	print("I'm working on:", osName)
	print("My directory is:", programPath)
	
	""" utworzenie okien programu """
	homeWindow = HomeWindow()
	saleWindow = SaleWindow()
	szkoleniaWindow = SzkoleniaWindow()
	uczestnicyWindow = UczestnicyWindow()
	settingsWindow = SettingsWindow()
	resultWindow = ResultWindow()
	
	""" dodanie wzajemnych referencji """
	homeWindow.addWindow(saleWindow)
	homeWindow.addWindow(szkoleniaWindow)
	homeWindow.addWindow(uczestnicyWindow)
	homeWindow.addWindow(settingsWindow)
	homeWindow.addWindow(resultWindow)
	saleWindow.addWindow(homeWindow)
	szkoleniaWindow.addWindow(homeWindow)
	uczestnicyWindow.addWindow(homeWindow)
	settingsWindow.addWindow(homeWindow)
	resultWindow.addWindow(homeWindow)
	resultWindow.addWindow(saleWindow)
	resultWindow.addWindow(szkoleniaWindow)
	resultWindow.addWindow(uczestnicyWindow)
	
	""" jedziemy z koksem """
	dataBuilder = DataBuilder()
	currentWindow = homeWindow
	homeWindow.showIt()
	
	sys.exit(app.exec_())


