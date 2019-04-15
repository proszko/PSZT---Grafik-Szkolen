#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import platform

class ListsFromFile():
	isGood = False
	ffList1 = []
	ffList2 = []
	ffList3 = []
	ffList4 = []
	ffList5 = []

""" Provides 'from file Lists' with data ready to use """
def readData():
	listsFromFile = ListsFromFile()
	
	fileName = "data.txt"
	filePath = os.path.dirname(__file__)
	osName = platform.system()
	
	try :
		if osName == "Windows":
			file = open(filePath+"\\"+fileName, 'r')
		else :
			file = open(filePath+"/"+fileName, 'r')
		
		ffList1 = toIntsList(file.readline()) # pojemności sal
		ffList2 = toIntsList(file.readline()) # pojemność szkoleń
		ffList3 = toIntsList(file.readline()) # czas trwania szkoleń
		ffList4 = toIntsList(file.readline()) # liczba szkoleń
		ffList5 = toListOfIntsLists(file.readline()) # preferencje uczestników

		file.close()
		
	except :
		print("Nie pykło")
		return listsFromFile
	
	if len(ffList2) != len(ffList3):
		return listsFromFile
	
	listsFromFile.isGood = True
	listsFromFile.ffList1 = ffList1.copy()
	listsFromFile.ffList2 = ffList2.copy()
	listsFromFile.ffList3 = ffList3.copy()
	listsFromFile.ffList4 = ffList4.copy()
	listsFromFile.ffList5 = ffList5.copy()
	
	return listsFromFile


def toIntsList(line):
	list = line.replace("\n","").split(',')
	for i in range(len(list)):
		list[i] = int(list[i])
	return list

	
def toListOfIntsLists(line):
	list = line.replace("\n","").split('|')
	for i in range(len(list)):
		list[i] = toIntsList(list[i])
	return list

