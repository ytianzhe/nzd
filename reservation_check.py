import pymysql
from datetime import datetime, date, timedelta

def get_dbconnect():
    host_add = '192.168.0.100'
    port_num = 3306
    user_name = 'xh_ytz'
    pw = 'xinhai0574'
    db = 'xh_ytz'
    return pymysql.connect(host=host_add, port=port_num, user=user_name, password=pw, database=db)

#获取某天某店的工作表
def get_resv(data):
    conn = get_dbconnect()
    c = conn.cursor(cursor=pymysql.cursors.DictCursor)
    c.execute("select start_time, end_time from naizhenduo_reservation where resv_time='%s' and location=%d and state=1"%(
            data['resv_time'], data['location']))
    result = c.fetchall()
    c.close()
    conn.close()
    return sort_dict(result)

#查看时间点被预约数
def check(data):
    shift = {"08:00": 0, "08:30": 0, "09:00": 0, "09:30": 0, "10:00": 0, "10:30": 0, "11:00": 0, "11:30": 0,
             "12:00":0, "12:30":0, "13:00":0,"13:30":0,"14:00":0,"14:30":0,"15:00":0, "15:30":0, "16:00":0,
             "16:30":0, "17:00":0, "17:30":0, "18:00":0, "18:30":0,"19:00":0}
    start_time = datetime.strptime("08:00","%H:%M")
    # print(len(data))
    if len(data)!=0:
        for i in data:
            # end_time = (start_time+timedelta(minutes=cust_resv['duration'])).strftime("%H:%M")
            st_time = start_time.strftime("%H:%M")
            # print(i['start_time'])
            shift[i['start_time']]+=1
            time_dif = time_difference(i['start_time'],i['end_time'])
            if  time_dif >30 and st_time!="19:00":
                # print('test')
                tmp = start_time
                # print(int(time_dif/30))
                for i in range(0,int(time_dif/30)):
                    tmp += timedelta(minutes=30)

                    shift[tmp.strftime("%H:%M")]+=1
    return shift

#哪些时间段可预约，若没有人员安排表则默认为在店3人
def available(data, shift,cust_resv):
    conn = get_dbconnect()
    a = {}
    c = conn.cursor(cursor=pymysql.cursors.DictCursor)
    c.execute("select morning_shift, afternoon_shift from naizhenduo_workshift where work_date='%s' and store_id=%d"%(data['resv_time'],data['location']))
    result = c.fetchone()
    union={}
    if result is not None:
        morning = {k:v for k,v in shift.items() if k<="11:30"and v<result['morning_shift']}
        afternoon = {k:v for k,v in shift.items() if k >="12:00" and v<result['afternoon_shift']}
        union.update(morning)
        union.update(afternoon)

    else:
        morning = {k: v for k, v in shift.items() if k <= "11:30" and v < 3}
        afternoon = {k: v for k, v in shift.items() if k >= "12:00" and v < 3}
        union.update(morning)
        union.update(afternoon)

    if cust_resv['duration']<=30:
        tmp = list(union.keys())
        tmp.remove('19:00')
        return tmp

    else:
        union_list = list(union.keys())
        print(union_list)
        final_list = []
        for k,v in union.items():
            if k=='19:00':
                break
            start_time = datetime.strptime(k,"%H:%M")
            end_time = (start_time+timedelta(minutes=cust_resv['duration']))
            str_end_time = end_time.strftime("%H:%M")
            try:
                mutiplier = int(cust_resv['duration']/30)
                if str_end_time>"19:00":
                    for i in range(1,mutiplier):
                        next_point = start_time + timedelta(minutes=30)
                        if next_point.strftime("%H:%M")=="19:00":
                            break
                        union_list.index(next_point.strftime("%H:%M"))
                    final_list.append(k)
                else:
                    for i in range(1,mutiplier):

                        # print(i)
                        next_point = start_time + timedelta(minutes=30)
                        if k == "16:00":
                            print(next_point.strftime("%H:%M"))
                        union_list.index(next_point.strftime("%H:%M"))
                        start_time=next_point
                    final_list.append(k)
            except:
                # print(k)
                continue
        return final_list

#计算时间差
def time_difference(time1,time2):
    return ((datetime.strptime(time2,"%H:%M")-datetime.strptime(time1,"%H:%M")).seconds/60)

#字典排序，先按照start_time再按照end_time
def sort_dict(data):
    sorted_dict = sorted(data,key=lambda k:(k['start_time'],k['end_time']))
    return sorted_dict


# data = {"resv_time":"2019-01-28","location":1}
# cust_resv = {"duration":90}
# a=get_resv(data)
# b=check(a)
# b['14:30']+=3
# b['15:00']+=3
# b['15:30']+=3
# b['16:30']+=3
# b['18:30']+=3
# # print(b)
# c = available(data,b,cust_resv)
# print(c)