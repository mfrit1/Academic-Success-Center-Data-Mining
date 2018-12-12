import pandas as pd 
import numpy as np 
import re
import matplotlib.pyplot as plt
from datetime import datetime as dt
import math

#Format the data to be usable for us.
f = open("NewCheckIn.txt", "w+")

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

 
#Importing data
df = pd.read_csv('NewCheckIn.txt', sep='	')

#remove the uneccesary columns
badColumnList = list(df)
badColumnList.remove("StartDate") 
badColumnList.remove("Time in Center")
df.drop(badColumnList, axis=1, inplace=True)

#remove rown where the time in the center is ########
for index, row in df.iterrows():
	if ':' not in row['Time in Center'] or row['Time in Center'] == '0:00':
		df.drop(df.index[index])

		
#Split the date time column into date and time
new = df['StartDate'].str.split(" ", 1, expand=True)
df['Date'] = new[0]
df['Time'] = new[1]

#Remove any dates that are weekends because we don not need tutors for those dates.
for index, row in df.iterrows():
	d = dt.strptime(row['Date'], '%m/%d/%Y')
	if d.weekday() > 4:
		df.drop(df.index[index])



df2 = df
dateArray = df2.Date.unique()
newDateArray = []
countForDay = []
for x in dateArray:

		date = x.split('/')
		#if int(date[0]) < 10:
		#	date[0] = '0' + date[0]
		#if int(date[1]) < 10:
		#	date[1] = '0' + date[1]

		#df2 = pd.DataFrame([[str(x) + ' ' + str(count) + ":00", 0]], columns=['DateTime', 'Count'])
		#dateTimeCount.append(df2)
		newDateArray.append(date[0] + '/' + date[1] + '/' + date[2])
		countForDay.append(0)

for index, row in df2.iterrows():
	date1 = row['Date']
	countForDayIndex = newDateArray.index(date1)
	countForDay[countForDayIndex] = countForDay[countForDayIndex] + 1


Quarter = math.floor(len(newDateArray)/4)
GraphX = []
for x in newDateArray[:Quarter]:
	GraphX.append(newDateArray.index(x))
GraphY = countForDay[:Quarter]

count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1

print('The average people per day in Quarter 1 is:   ' + str(average/count))

plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 1')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()




GraphX=[]
for x in newDateArray[Quarter:2*Quarter]:
	GraphX.append(newDateArray.index(x))
GraphY = countForDay[Quarter:2*Quarter]

count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1

print('The average people per day in Quarter 2 is:   ' + str(average/count))

plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 2')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()


GraphX=[]
for x in newDateArray[2*Quarter:3*Quarter]:
	GraphX.append(newDateArray.index(x))
GraphY = countForDay[2*Quarter:3*Quarter]

count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1

print('The average people per day in Quarter 3 is:   ' + str(average/count))

plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 3')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()

GraphX=[]
for x in newDateArray[3*Quarter:4*Quarter]:
	GraphX.append(newDateArray.index(x))
GraphY = countForDay[3*Quarter:4*Quarter]

count = 0
average = 0
for x in GraphY:
	average = average + x
	count = count + 1

print('The average people per day in Quarter 4 is:   ' + str(average/count))

plt.plot(GraphX,GraphY, 'o-', color='red')
plt.title('Quarter 4')
plt.ylabel('Number of Students')
plt.xlabel('Enumerated Dates')
plt.show()

dateArray = df.Date.unique()
dateTimeArray = []
countArray = []

for x in dateArray:
	count = 8
	while count <= 21:
		dateTimeArray.append(str(x) + ' ' + str(count) + ":00")
		countArray.append(0)
		#df2 = pd.DataFrame([[str(x) + ' ' + str(count) + ":00", 0]], columns=['DateTime', 'Count'])
		#dateTimeCount.append(df2)
		count = count + 1






#Go through each row to look at info
for index, row in df.iterrows():

	#Get the date of the record
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
	

data = {'DateTime' : dateTimeArray, 'Count' : countArray}
dateTimeCount2 = pd.DataFrame(data)

#This code plots all monday points.
plt.figure()

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

plt.plot(dummy,averagePeople, 'o-', color='red')
plt.show()






#Gets the number of rows
#numRow = len(dateTimeCount.index)
#split = int(numRow * 0.8)
#Divides data into train and test arrays
#train=dateTimeCount2[0:split] 
#test=dateTimeCount2[split:]

#print(dateTimeCount2.head())
#print('###################################')
#print(train.head())
#print('###################################')
#print(test.head())

#dateTimeCount2['Timestamp'] = pd.to_datetime(dateTimeCount2.DateTime,format='%m-%d-%Y %H:%M') 
#dateTimeCount2.index = dateTimeCount2.Timestamp 
#dateTimeCount2 = dateTimeCount2.resample('D').mean()
#train['Timestamp'] = pd.to_datetime(train.DateTime,format='%m-%d-%Y %H:%M') 
#train.index = train.Timestamp 
#train = train.resample('D').mean() 
#test['Timestamp'] = pd.to_datetime(test.DateTime,format='%m-%d-%Y %H:%M') 
#test.index = test.Timestamp 
#test = test.resample('D').mean()


#train.Count.plot(figsize=(15,8), title= 'Student Count', fontsize=14)
#test.Count.plot(figsize=(15,8), title= 'Student Count', fontsize=14)
#plt.show()

#dd= np.asarray(train.Count)
#y_hat = test.copy()
#y_hat['naive'] = dd[len(dd)-1]
#plt.figure(figsize=(12,8))
#plt.plot(train.index, train['Count'], label='Train')
#plt.plot(test.index,test['Count'], label='Test')
#plt.plot(y_hat.index,y_hat['naive'], label='Naive Forecast')
#plt.legend(loc='best')
#plt.title("Naive Forecast")
#plt.show()


#y_hat_avg = test.copy()
#fit1 = ExponentialSmoothing(np.asarray(train['Count']) ,seasonal_periods=5 ,trend='add', seasonal='add',).fit()
#y_hat_avg['Holt_Winter'] = fit1.forecast(len(test))
#plt.figure(figsize=(16,8))
#plt.plot( train['Count'], label='Train')
#plt.plot(test['Count'], label='Test')
#plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
#plt.legend(loc='best')