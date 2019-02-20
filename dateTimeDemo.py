from datetime import  datetime,timedelta


def  dateCalculate(time,duration):
    print(time)
    print(duration)
    a=datetime.strptime(time,"%H:%M")
    print(a)
    b=a+timedelta(minutes=duration)
    print(b)
    c=datetime.strftime(b,"%H:%M")
    print(c)
    return c


# c=dateCalculate('08:00',120)
# print(c)