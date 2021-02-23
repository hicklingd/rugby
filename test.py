from datetime import datetime
p='Sat, Feb 20'
d=datetime.strptime(p, "%a, %b %d")
print(d.strftime("%d/%m"))



#datetime_object = datetime.datetime.strptime(p)