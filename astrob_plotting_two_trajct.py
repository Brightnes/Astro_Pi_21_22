"""
Code used for plotting purpose of
2021/2022 ed of Astropi challenge, team astrob.
Code plots two trajectories, from two available data sets
data.csv (21/22 ed) and a second data set with its own path.
This program and  the first data file data.csv must be saved in the same directory
"""
from csv import reader
from matplotlib import pyplot #as plt
from dateutil import parser
col_counter=0

#Edit the following line with the path to the second data file
path_to_file = '/Users/lorenzotruffagiachet/Documents/astro_pi/edizione_20_21/eposat/eposat_data/data01.csv'#Edit with path to second data set

# First create data lists:
with open('data.csv', 'r') as f:
    dat = list(reader(f))
with open(path_to_file, 'r') as g:
    dat1 = list(reader(g))



#Now print info and enter data sets reference:
print(type(dat))
print(len(dat))
print(type(dat[0]))
print(len(dat[0]))



for el in dat[0]:
    print(str(col_counter) + '   ' + el)
    col_counter +=1

a=int(input('Please enter latitude line number'))
b=int(input('Please enter longitude line number'))

print(type(dat1))
print(len(dat1))
print(type(dat1[0]))
print(len(dat1[0]))

# Now reset col_counter value:
col_counter=0



for el in dat1[0]:
    print(str(col_counter) + '   ' + el)
    col_counter +=1

c=int(input('Please enter latitude line number'))
d=int(input('Please enter longitude line number'))


#Now, get lat, long values from dat lists:
#l'istr. seguente estrae le letture del parametro selezionato
#ma faccio un typecasting a float, se no i valori in y sono sballati
lat = [float(i[a]) for i in dat[1::]]
lat1 = [float(i[c]) for i in dat1[1::]]
#l'istr. seguente estrae l'ora in cui ogni lettura è stata fatta
long = [float(i[b]) for i in dat[1::]]
long1 = [float(i[d]) for i in dat1[1::]]

# now some silly stuff to print plot headers:
headers=dat[0]

#start=lat[0]
#end=lat[-1]
#time_raw = [i[19] for i in data[1::]]

pyplot.title('Traiettoria da '+ str(round(lat[0],2)) + ' , '+str(round(long[0],2)) + ' a ' + str(round(lat[-1],2)) + ' , ' +str(round(long[-1],2)))
pyplot.ylabel(headers[a])
pyplot.xlabel(headers[b])


# Finally plot the two trajectories:
"""
Usare una delle due istruzioni seguenti
"""
pyplot.plot(long, lat,'.', markersize=1)
#pyplot.plot(time, temp, linewidth=1)

"""
Usare una delle due istruzioni seguenti
"""
pyplot.plot(long1, lat1,'.', markersize=1)
#pyplot.plot(time, temp, linewidth=1)


pyplot.show()
#plt.scatter(time,temp, s=1, marker='.')
#plt.show()
