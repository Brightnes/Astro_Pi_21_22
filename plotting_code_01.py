"""
Piccolo programma per fare grafici dei dati misurati con
l'Astro Pi; edizione 2021/22.
"""
from csv import reader
from matplotlib import pyplot #as plt
from dateutil import parser
col_counter=0
#attenzione, nell'istr. seguente, il file csv deve essere nella stessa
#directory in cui ho salvato questo programma
with open('data.csv', 'r') as f:
    dat = list(reader(f))


print(type(dat))
print(len(dat))
print(type(dat[0]))
print(len(dat[0]))



for el in dat[0]:
    print(str(col_counter) + '   ' + el)
    col_counter +=1

a=int(input('Choose number for y entry (0-13)'))
#l'istr. seguente estrae le letture del parametro selezionato
#ma faccio un typecasting a float, se no i valori in y sono sballati
temp = [float(i[a]) for i in dat[1::]]
#l'istr. seguente estrae l'ora in cui ogni lettura è stata fatta
time = [parser.parse(i[0]) for i in dat[1::]]
#Time è una lista; gli elementi della lista sono
#degli oggetti di classe datetime.datetime;
#è possibile calcolare la differenza tra due elementi di time;

headers=dat[0]

start=time[0]
end=time[-1]
#time_raw = [i[19] for i in data[1::]]

pyplot.title('letture dati dal '+ str(start) + ' al ' + str(end))
pyplot.ylabel(headers[a])
"""
Usare una delle due istruzioni seguenti(si disattiva
l'altra anteponendo un simbolo #)
"""
pyplot.plot(time, temp,'.', markersize=1)
#pyplot.plot(time, temp, linewidth=1)



pyplot.show()
#plt.scatter(time,temp, s=1, marker='.')
#plt.show()
