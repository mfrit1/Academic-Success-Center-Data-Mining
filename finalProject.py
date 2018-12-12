import pandas as pd 
import numpy as np 
import re
import matplotlib.pyplot as plt
from datetime import datetime as dt
import math


#Open the new data file.
f = open("NewCheckIn.txt", "w+")


#Filter out all files from origional data that are sign out, no 
#log out data or not math tutoring.
delimiter='	'
count = 0;
with open("CheckIn.txt") as input_file:
	for line in input_file:
		if count == 0:
			f.write(line)
			count = count + 1
		if "No Log Out Data" not in line and 'Signing Out' not in line and 'Math Tutoring' in line:
			f.write(line)

f.close()

 
#Importing filtered data.
df = pd.read_csv('NewCheckIn.txt', sep='	')


#Remove the uneccesary columns.
badColumnList = list(df)
badColumnList.remove("StartDate") 
badColumnList.remove("Time in Center")
df.drop(badColumnList, axis=1, inplace=True)


#remove rown where the time in the center is ######## (rare case).
for index, row in df.iterrows():
	if ':' not in row['Time in Center'] or row['Time in Center'] == '0:00':
		df.drop(df.index[index])

		
#Split the Date Time column into Date and Time
new = df['StartDate'].str.split(" ", 1, expand=True)
df['Date'] = new[0]
df['Time'] = new[1]


#Remove any dates that are weekends because we do not need tutors for those dates (online tutoring).
for index, row in df.iterrows():
	d = dt.strptime(row['Date'], '%m/%d/%Y')
	if d.weekday() > 4:
		df.drop(df.index[index])


#Take each unique date in the dataframe and put them into an array
df2 = df
dateArray = df2.Date.unique()
newDateArray = []
countForDay = []
for x in dateArray:
		date = x.split('/')
		newDateArray.append(date[0] + '/' + date[1] + '/' + date[2])
		countForDay.append(0)


#Log the number of people in the center for each date into the corresponding 
#position of the countForDay array
for index, row in df2.iterrows():
	date1 = row['Date']
	countForDayIndex = newDateArray.index(date1)
	countForDay[countForDayIndex] = countForDay[countForDayIndex] + 1


#Takes the first quarter of all the dates, enumerates them, and makes those the x coordinates.
Quarter = math.floor(len(newDateArray)/4)
GraphX = []
for x in newDateArray[:Quarter]:
	GraphX.append(newDateArray.index(x))


#Takes the first quarter of countForDay array, averages the number of people 
#across all days, and prints it.
GraphY = countForDay[:Quarter]
count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1
print('The average people per day in Quarter 1 is:   ' + str(average/count))


#Plots the enumerated dates with the number of students present 
#each date for the first quarter and shows the graph.
plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 1')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()



#Takes the second quarter of all the dates, enumerates them, and makes those the x coordinates.
GraphX=[]
for x in newDateArray[Quarter:2*Quarter]:
	GraphX.append(newDateArray.index(x))


#Takes the second quarter of countForDay array, averages the number of people 
#across all days, and prints it.
GraphY = countForDay[Quarter:2*Quarter]
count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1
print('The average people per day in Quarter 2 is:   ' + str(average/count))



#Plots the enumerated dates with the number of students present 
#each date for the second quarter and shows the graph.
plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 2')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()



#Takes the third quarter of all the dates, enumerates them, and makes those the x coordinates.
GraphX=[]
for x in newDateArray[2*Quarter:3*Quarter]:
	GraphX.append(newDateArray.index(x))



#Takes the third quarter of countForDay array, averages the number of people 
#across all days, and prints it.
GraphY = countForDay[2*Quarter:3*Quarter]
count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1
print('The average people per day in Quarter 3 is:   ' + str(average/count))


#Plots the enumerated dates with the number of students present 
#each date for the third quarter and shows the graph.
plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 3')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()



#Takes the fourth quarter of all the dates, enumerates them, and makes those the x coordinates.
GraphX=[]
for x in newDateArray[3*Quarter:4*Quarter]:
	GraphX.append(newDateArray.index(x))



#Takes the fourth quarter of countForDay array, averages the number of people 
#across all days, and prints it.
GraphY = countForDay[3*Quarter:4*Quarter]
count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1
print('The average people per day in Quarter 4 is:   ' + str(average/count))



#Plots the enumerated dates with the number of students present 
#each date for the fourth quarter and shows the graph.
plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 4')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()


#Create an array of the DateTimes (8:00am to 9:00pm) for each date.
dateArray = df.Date.unique()
dateTimeArray = []
countArray = []
for x in dateArray:
	count = 8
	while count <= 21:
		dateTimeArray.append(str(x) + ' ' + str(count) + ":00")
		countArray.append(0)
		count = count + 1



#Finds the number of people in the Center at each time of each day.
for index, row in df.iterrows():
	date = row['Date']

	#Get the hour they logged in
	time = int(row['Time'].split(':')[0])

	#Make sure they logged in at a valid time
	if time < 8 or time > 21:
		continue

	#get The number of hours they were in the building for
	hoursInBuilding = int(row['Time in Center'].split(':')[0])

	#Find the position in the array of that login Date/Hour
	dateTimeArrayIndex = dateTimeArray.index(date +" " + str(time) + ":00")

	#add one to the corresponding count
	countArray[dateTimeArrayIndex] = countArray[dateTimeArrayIndex] + 1

	#While they were still in the center, increase array position and increase the count
	while hoursInBuilding > 0:
		time = time + 1
		hoursInBuilding = hoursInBuilding - 1
		if time > 21 or time < 8:
			continue

		dateTimeArrayIndex = dateTimeArray.index(date +" " + str(time) + ":00")
		countArray[dateTimeArrayIndex] = countArray[dateTimeArrayIndex] + 1




#Create a new dataframe object with DateTime and Number of Students columns.
#Re-format the dates and times to have leading zeroes.
data = {'DateTime' : dateTimeArray, 'Count' : countArray}
dateTimeCount = pd.DataFrame(data)

dateTimeArray = []
countArray = []
for index, row in dateTimeCount.iterrows():
	date1 = row['DateTime']
	count = row['Count']
	dateVal = date1.split(' ')[0]
	timeVal = date1.split(' ')[1]

	dateValArr = dateVal.split('/')
	if int(dateValArr[0]) < 10:
		dateValArr[0] = "0" + dateValArr[0]
	if int(dateValArr[1]) < 10:
		dateValArr[1] = "0" + dateValArr[1]

	timeValArr = timeVal.split(':')
	if int(timeValArr[0]) < 10:
		timeValArr[0] = "0" + timeValArr[0]

	date2 = dateValArr[0] + "-" + dateValArr[1] + "-" + dateValArr[2] + " " + timeValArr[0] + ":" + timeValArr[1]
	dateTimeArray.append(date2)
	countArray.append(count)
	


#Store the newly formatted data into anoter dataframe.
#Go through every day in the dataframe. Find the average 
#number of people in the center on a certain day of the week at a certain time.
data = {'DateTime' : dateTimeArray, 'Count' : countArray}
dateTimeCount2 = pd.DataFrame(data)

count = 0
dateVal1 = dt.strptime('08-31-2018', '%m-%d-%Y')
graphXPoints = []
graphYPoints = []

for index, row in dateTimeCount2.iterrows():
	dateVal2 = dt.strptime(row['DateTime'].split(' ')[0], '%m-%d-%Y')

	if dateVal2.weekday() == 4:

		if dateVal1 != dateVal2:
			count = count + 14
			dateVal1 = dateVal2

		timeVal = row['DateTime'].split(' ')[1].split(':')[0]
		graphXPoints.append(int(timeVal) -8 + count)
		graphYPoints.append(row['Count'])

averagePeople = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
count = 0

for x in graphXPoints:
	if x % 14 == 0:
		count = count + 1

	averagePeople[x % 14] = averagePeople[x % 14] + graphYPoints[x]

index = 0
for x in averagePeople:
	x = math.ceil(x / count)
	averagePeople[index] = x
	index = index + 1

dummy = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]



#Show the average number of people there at each hour of Fridays for the whole semester.
plt.figure()
plt.plot(dummy,averagePeople, 'o-', color='red')
plt.show()
