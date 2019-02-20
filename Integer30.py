
import  math

def  IntegerChange(duration):
    print(duration)
    if(duration%30!=0):
        a=duration/30
        # print(a)
        # print('向上取整')
        b=math.ceil(a)*30

    else:
        # print('不需要变化')
        b=duration
    return b



# print(quzheng30(40))