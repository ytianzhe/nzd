
import NZDMySqlConnect
import datetime

def TableToJson():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "SELECT * FROM `naizhenduo_babylist`"
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        print
        u'fetchall()返回的数据：', results
        c.close()
        conn.close()
        jsonData = []
        for row in results:
            json_dict = {}
            json_dict['babyName'] = row[0]
            json_dict['babyBirthday'] = row[1]
            json_dict['CustomerName'] = row[2]
            json_dict['CustomerWechat'] = row[3]
            json_dict['phone'] = row[4]
            jsonData.append(json_dict)
        return jsonData
    except:
        print
        'MySQL connect fail...'



def workerInfo(openid):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "SELECT * FROM `naizhenduo_worker_info` where worker_wechat="+openid
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        # print
        # u'fetchall()返回的数据：', results
        c.close()
        conn.close()
        # jsonData = []
        worker_dict = {}
        worker_dict['id'] = results[0]
        worker_dict['workerOpenId'] = results[1]
        worker_dict['workerName'] = results[2]
        worker_dict['workerPhoneNum'] = results[3]
        worker_dict['location'] = results[4]
        worker_dict['note'] = results[6]
        worker_dict['authority'] = results[7]
        # jsonData.append(customer_dict)
        return worker_dict
    except:
        print
        'MySQL connect fail...'





def customerInfo(openid):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "SELECT * FROM `naizhenduo_customer_info` nzdc where nzdc.customer_wechat= '%s'" % (openid)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        # print
        # u'fetchall()返回的数据：', results
        c.close()
        conn.close()
        # jsonData = []
        customer_dict = {}
        customer_dict['id'] = results[0]
        customer_dict['customerOpenid'] = results[1]
        customer_dict['customerName'] = results[2]
        customer_dict['customerPhone'] = results[3]
        customer_dict['visitedTime'] = results[4]
        customer_dict['note'] = results[6]
        customer_dict['authority'] = results[7]
        # jsonData.append(customer_dict)
        return customer_dict
    except:
        print
        'MySQL connect fail...'

def customerInfoById(id):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "SELECT nci.id,nci.customer_name,nci.customer_phone_num FROM `naizhenduo_customer_info`  nci  where id='%s'"% (id)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        c.close()
        conn.close()
        # jsonData = []
        customer_dict = {}
        customer_dict['id'] = results[0]
        customer_dict['customerName'] = results[1]
        customer_dict['customerPhoneNum'] = results[2]
        return customer_dict
    except:
        print
        'MySQL connect fail...'

'''添加员工'''
def insertWorker(Name,Authority,Location,tel):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "insert  into naizhenduo_worker_info \
        (worker_name,authority, location, worker_phone_num) \
        VALUES  ('%s',\'%s\', \'%s\', \'%s\')" % \
        (Name, Authority, Location, tel)
        print(sql)
        i=c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        # dict={'code':0,'msg':'insert succeed','i':i}
        return i
    except:
        print
        'MySQL connect fail...'
        conn.rollback()
    conn.close()


'''查询员工'''
def selectworkerInfo():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "SELECT nzdwi.*,nzdsi.store_name FROM `naizhenduo_worker_info` nzdwi left join naizhenduo_store_info nzdsi  on nzdsi.id=nzdwi.location"
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        print
        u'fetchall()返回的数据：', results
        c.close()
        conn.close()

        return results
    except:
        print
        'MySQL connect fail...'

'''编辑员工'''
def EditWorker(editName, editAu, editTel, editLocation,editId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        # sql = "SELECT * FROM `naizhenduo_worker_info`" (worker_name,authority, location, worker_phone_num) \
        sql = "UPDATE naizhenduo_worker_info SET worker_name = '%s' ,authority='%s',location='%s',worker_phone_num='%s' WHERE id = '%s'" % (editName,editAu,editLocation,editTel,editId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()

'''删除员工'''
# delWorker
def DelWorker(delId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql =" DELETE FROM naizhenduo_worker_info WHERE id= '%s'" % (delId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()

'''获取所有人当天预约记录'''
def selectReservationRecord(sqlJoint):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        # sql = "SELECT nzdr.id,nzdr.location,nzdc.customer_name,nzdr.resv_time,nzdr.start_time,nzdb.business_name,nzdc.customer_phone_num FROM  \
        #   `naizhenduo_reservation` nzdr \
        # left join naizhenduo_businesslist nzdb on nzdb.id=nzdr.resv_info  \
        # left join naizhenduo_customer_info nzdc on nzdc.id=nzdr.customer_id \
        #      where nzdr.state='1' "+sqlJoint

        sql = "SELECT nzdr.id,nzdr.location,nzdc.customer_name,nzdr.resv_time,nzdr.start_time,nzdb.business_name,nzdc.customer_phone_num ,nzds.store_name  FROM  \
                `naizhenduo_reservation` nzdr \
              left join naizhenduo_businesslist nzdb on nzdb.id=nzdr.resv_info  \
              left join naizhenduo_customer_info nzdc on nzdc.id=nzdr.customer_id \
              left join naizhenduo_store_info nzds on nzds.id=nzdr.location \
                   where nzdr.state='1' " + sqlJoint

        print(sql)
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        c.close()
        conn.close()
        # jsonData = []
        # for row in results:
        #     json_dict = {}
        #     json_dict['id'] = row[0]
        #     json_dict['location'] = row[1]
        #     json_dict['customerName'] = row[2]
        #     json_dict['resvTime'] = row[3]
        #     json_dict['startTime'] = row[4]
        #     json_dict['businessName'] = row[5]
        #     json_dict['tel'] = row[6]
        #     jsonData.append(json_dict)
        return results
    except:
        conn.rollback()
    conn.close()
'''搜索所有的项目'''
# selectBusinessListPage
def selectBusinessListPage():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT * FROM `naizhenduo_businesslist`  nzdb where nzdb.state='1' "
        print(sql)
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()

'''搜索所有的项目简表'''
# selectBusinessListPage
def selectBusiness():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdb.business_name FROM `naizhenduo_businesslist`  nzdb where nzdb.state='1' "
        print(sql)
        c.execute(sql)
        results = c.fetchall()

        # 将rows转化为数组

        # print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()

def selectStoreList():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdb.store_name FROM `naizhenduo_store_info`  nzdb where nzdb.state='1' "
        print(sql)
        c.execute(sql)
        results = c.fetchall()

        # 将rows转化为数组

        # print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()


'''增加项目'''
def addBussinessList(addlistName,addtime):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "insert  into naizhenduo_businesslist \
        (business_name,business_duration,state) \
        VALUES  ('%s',\'%s\','1')" % \
        (addlistName, addtime)
        print(sql)
        i=c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        # dict={'code':0,'msg':'insert succeed','i':i}
        return i
    except:
        print
        'MySQL connect fail...'
        conn.rollback()
    conn.close()

'''编辑项目'''
def EditBussinessList(editlistName, editTime,editId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        # sql = "SELECT * FROM `naizhenduo_worker_info`" (worker_name,authority, location, worker_phone_num) \
        sql = "UPDATE naizhenduo_businesslist SET business_name = '%s' ,business_duration='%s' WHERE id = '%s'" % (editlistName,editTime,editId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()

'''移除项目（禁用）'''
# DelBussinessList
def DelBussinessList(delId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql ="UPDATE naizhenduo_businesslist SET state = '0'  WHERE id = '%s'" % (delId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()

'''增加店铺'''
def addStore(addStoreName,addStoreAddress,addSmName,addTel ,addStoreTel):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "insert  into naizhenduo_store_info \
        (store_name,manager_name,manager_phone_num,store_location,store_phone_num,state) \
        VALUES  ('%s',\'%s\',\'%s\',\'%s\',\'%s\','1')" % \
        (addStoreName, addStoreAddress,addSmName,addTel,addStoreTel)
        print(sql)
        i=c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        # dict={'code':0,'msg':'insert succeed','i':i}
        return i
    except:
        print
        'MySQL connect fail...'
        conn.rollback()
    conn.close()


'''编辑店面'''
def editStore(editStoreName,editStoreAddress,editSmName,editTel,editStoreTel,storeId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "UPDATE naizhenduo_store_info SET store_name = '%s' ,manager_name='%s',manager_phone_num='%s',store_location='%s',store_phone_num='%s' WHERE id = '%s'" % (editStoreName,editSmName,editTel,editStoreAddress,editStoreTel,storeId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()

'''查询所有的店面'''
def selectStorePage():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzds.id,nzds.store_name,nzds.store_location,nzds.manager_name,nzds.manager_phone_num,nzds.store_phone_num FROM `naizhenduo_store_info`  nzds where nzds.state='1' "
        print(sql)
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()
'''删除店面'''
def delStore(delId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql ="UPDATE naizhenduo_store_info SET state = '0'  WHERE id = '%s'" % (delId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()



'''每天的上班人数'''

def selectWorkNumberPage(location):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT * FROM `naizhenduo_workshift`  nzdws where nzdws.work_date=curdate() and  nzdws.store_id='%s'" %(location)
        # sql = "SELECT * FROM `naizhenduo_workshift`  nzdws where nzdws.work_date='2019-01-25'"
        print(sql)
        i = c.execute(sql)
        print(i)
        results = c.fetchone()
        print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()

'''获取用户权限'''
def searchauthority(id):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdw.authority  as au FROM `naizhenduo_worker_info`  nzdw where nzdw.id='%s'" % (id)
        print(sql)
        i = c.execute(sql)
        # print(i)
        results = c.fetchone()
        # print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()

'''员工信息获取'''
def workerById(id):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "SELECT nwi.id,nwi.worker_name,nwi.worker_phone_num FROM `naizhenduo_worker_info`  nwi  where id='%s'" % (id)
        # print(sql)
        c.execute(sql)
        results = c.fetchone()
        c.close()
        conn.close()
        # jsonData = []
        worker_dict = {}
        worker_dict['id'] = results[0]
        worker_dict['workerName'] = results[1]
        worker_dict['workerPhoneNum'] = results[2]
        return worker_dict
    except:
        print
        'MySQL connect fail...'

'''获取该客户所有宝宝'''
def SearchBabyByUserId(id):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdbl.id,nzdbl.baby_name,nzdbl.baby_birthday  FROM `naizhenduo_babylist`  nzdbl where nzdbl.state='1'and  nzdbl.customer_id='%s'" % (id)
        print(sql)
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()

'''删除宝宝'''
def DelBabyByUserId(delId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql ="UPDATE naizhenduo_babylist SET state = '0'  WHERE id = '%s'" % (delId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()



'''编辑宝宝'''
def editBaby(babyName,babyBirth,babyId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "UPDATE naizhenduo_babylist SET baby_name = '%s' ,baby_birthday='%s' WHERE id = '%s'" % (babyName, babyBirth , babyId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()


'''增加宝宝'''
def addbaby(baby_name,baby_birthday,customer_id):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "insert  into naizhenduo_babylist \
        (baby_name,baby_birthday,customer_id,state) \
        VALUES  (\'%s\',\'%s\',\'%s\',\'%s\')" % \
        (baby_name, baby_birthday,customer_id,1)
        print(sql)
        i=c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        # dict={'code':0,'msg':'insert succeed','i':i}
        return i
    except:
        print
        'MySQL connect fail...'
        conn.rollback()
    conn.close()


'''今日预约记录(管理面板)'''
def selectToDayOrderRecord():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdr.*,nzdc.customer_name,nzdb.business_name,nzds.store_name FROM `naizhenduo_reservation` nzdr \
        left join naizhenduo_customer_info nzdc on nzdc.id=nzdr.customer_id \
        left join naizhenduo_businesslist nzdb on  nzdb.id=nzdr.resv_info \
        left join naizhenduo_store_info nzds on nzds.id=nzdr.location \
           where nzdr.resv_time=curdate()"
        print(sql)
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        c.close()
        conn.close()
        # jsonData = []
        # for row in results:
        #     json_dict = {}
        #     json_dict['id'] = row[0]
        #     json_dict['location'] = row[1]
        #     json_dict['customerName'] = row[2]
        #     json_dict['resvTime'] = row[3]
        #     json_dict['startTime'] = row[4]
        #     json_dict['businessName'] = row[5]
        #     json_dict['tel'] = row[6]
        #     jsonData.append(json_dict)
        return results
    except:
        conn.rollback()
    conn.close()



'''增加 当天工人人数'''
# addWorkNumber
def addWorkNumber(morining,afternoon,evening,location):
    workDate=datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "insert  into naizhenduo_workshift \
        (store_id,morning_shift,afternoon_shift,evening_shift,work_date) \
        VALUES  (\'%s\',\'%s\',\'%s\',\'%s\','%s')" % \
        (location, morining,afternoon,evening,workDate)
        print(sql)
        i=c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        # dict={'code':0,'msg':'insert succeed','i':i}
        return i
    except:
        print
        'MySQL connect fail...'
        conn.rollback()
    conn.close()


'''编辑 当天工人人数'''
def editWorkNumber(morining,afternoon,evening,editId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "UPDATE naizhenduo_workshift SET morning_shift = '%s' ,afternoon_shift='%s',evening_shift='%s'  WHERE id = '%s'" % (morining,afternoon,evening,editId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()

'''SearchMsg'''
def SearchMsg():
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdr.id,nzdr.resv_time,nzdr.start_time FROM `naizhenduo_reservation` nzdr  where nzdr.state='1' order by  resv_time  desc"
        print(sql)
        c.execute(sql)
        results = c.fetchall()
        # print(results)
        c.close()
        conn.close()
        return results
    except:
        conn.rollback()
    conn.close()

'''根据店铺查询id'''
def SearchStoreIdByName(name):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzds.id FROM `naizhenduo_store_info` nzds  where nzds.state='1' and nzds.store_name='%s'"  %(name)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        # print(results)
        Store = {}
        Store['id'] = results[0]
        return Store
        c.close()
        conn.close()
    except:
        conn.rollback()
    conn.close()


'''根据店铺查询id'''
def SearchBussinessTime(bussinessName):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdb.id,nzdb.business_duration FROM `naizhenduo_businesslist` nzdb  where nzdb.state='1' and nzdb.business_name='%s'"  %(bussinessName)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        # print(results)
        business = {}
        business['id'] = results[0]
        business['business_duration'] = results[1]
        return business
        c.close()
        conn.close()
    except:
        conn.rollback()
    conn.close()

'''预约添加'''
def addOrder(customer_id,resv_time,start_time,end_time,resv_info,location):
    workDate=datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "insert  into naizhenduo_reservation \
        (customer_id,resv_time,start_time,end_time,resv_info,location,state) \
        VALUES  (\'%s\',\'%s\',\'%s\',\'%s\','%s','%s','%s')" % \
        (customer_id, resv_time,start_time,end_time,resv_info,location,'1')
        print(sql)
        i=c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        # dict={'code':0,'msg':'insert succeed','i':i}
        return i
    except:
        print
        'MySQL connect fail...'
        conn.rollback()
    conn.close()

'''个人预约记录'''
def SearchPersonalOrderRecord(userId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        # sql = "SELECT nzds.id FROM `naizhenduo_store_info` nzds  where nzds.state='1' and nzds.store_name='%s'"  %(userId)
        sql = "SELECT nzdr.*,nzdc.customer_name,nzdb.business_name,nzds.store_name FROM `naizhenduo_reservation` nzdr \
                left join naizhenduo_customer_info nzdc on nzdc.id=nzdr.customer_id \
                left join naizhenduo_businesslist nzdb on  nzdb.id=nzdr.resv_info \
                left join naizhenduo_store_info nzds on nzds.id=nzdr.location \
                   where nzdr.customer_id='%s'" %(userId)
        print(sql)
        c.execute(sql)
        results = c.fetchall()
        # print(results)

        return results
        c.close()
        conn.close()
    except:
        conn.rollback()
    conn.close()

'''个人预约记录详情'''
# SearchPersonRecordDetails
def SearchPersonRecordDetails(id):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        # sql = "SELECT nzds.id FROM `naizhenduo_store_info` nzds  where nzds.state='1' and nzds.store_name='%s'"  %(userId)
        sql = "SELECT nzdr.resv_time,nzdr.start_time,nzdr.end_time,nzdc.customer_name,nzdb.business_name,nzds.store_name ,nzdb.business_duration FROM `naizhenduo_reservation` nzdr \
                left join naizhenduo_customer_info nzdc on nzdc.id=nzdr.customer_id \
                left join naizhenduo_businesslist nzdb on  nzdb.id=nzdr.resv_info \
                left join naizhenduo_store_info nzds on nzds.id=nzdr.location \
                   where nzdr.id='%s'" %(id)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        Details = {}
        Details['resvTime'] = results[0]
        Details['startTime'] = results[1]
        Details['endTime'] = results[2]
        Details['customerName'] = results[3]
        Details['businessName'] = results[4]
        Details['storeName'] = results[5]
        Details['projectDuration'] = results[6]
        # print(results)
        return Details
        c.close()
        conn.close()
    except:
        conn.rollback()
    conn.close()


'''查询个人预约记录详情'''
def SearchPersonRecordDetailsByDate(userId,sql):
    # print(userId)
    # print(sql)
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql="SELECT nzdr.*,nzdc.customer_name,nzdb.business_name,nzds.store_name,nzdb.business_duration FROM `naizhenduo_reservation` nzdr " \
            "left join naizhenduo_customer_info nzdc on nzdc.id=nzdr.customer_id    \
            left join naizhenduo_businesslist nzdb on  nzdb.id=nzdr.resv_info     \
        left join naizhenduo_store_info nzds on nzds.id=nzdr.location          \
        where nzdr.customer_id=%s \
        %s"%(userId, sql)

        #where nzdr.customer_id='%s' '%s' "%(userId, sql)
        print(sql)
        c.execute(sql)
        results = c.fetchall()

        return results
        c.close()
    except:
        conn.rollback()
    conn.close()

'''绑定手机和openid'''
# telBind
def telBind(openid,telNum,name):
    print(openid,telNum,name)
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "insert  into naizhenduo_customer_info \
        (customer_wechat,customer_name,customer_phone_num,authority) \
        VALUES  (\'%s\',\'%s\',\'%s\',\'%s\')" % \
        (openid, name,telNum,'c')
        print(sql)
        i=c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        # dict={'code':0,'msg':'insert succeed','i':i}
        return i
    except:
        print
        'MySQL connect fail...'
        conn.rollback()
    conn.close()

'''绑定手机检测是否重名'''
def SelectTypeValue(type,value):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT count(*) FROM `naizhenduo_customer_info` nzdc  \
        where nzdc.%s='%s'" \
         % (type, value)
        # where nzdr.customer_id='%s' '%s' "%(userId, sql)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        return results
        c.close()
    except:
        conn.rollback()
    conn.close()

'''绑定手机检测是否重名员工'''
def SelectTypeValueWorker(type,value):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT count(*) FROM `naizhenduo_worker_info` nzdw  \
        where nzdw.%s='%s'" \
         % (type, value)
        # where nzdr.customer_id='%s' '%s' "%(userId, sql)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        return results
        c.close()
    except:
        conn.rollback()
    conn.close()

'''更换手机号'''

def changeTelBind(telNum, userId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "UPDATE naizhenduo_customer_info SET customer_phone_num = '%s'   WHERE id = '%s'" % (telNum, userId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()
'''更换员工手机号'''
# changeTelBindWorker
def changeTelBindWorker(telNum, userId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "UPDATE naizhenduo_worker_info SET worker_phone_num = '%s'   WHERE id = '%s'" % (telNum, userId)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()


'''查询员工手机号对应的openid'''
# changeTelBindWorker
def SearchOpenidByTel(telNum):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdw.worker_wechat FROM `naizhenduo_worker_info` nzdw  \
              where nzdw.worker_phone_num='%s'" \
              % (telNum)
        # where nzdr.customer_id='%s' '%s' "%(userId, sql)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        return results
        c.close()
    except:
        conn.rollback()
    conn.close()


'''员工绑定已有手机号'''
# EmployeeBindsExistingMobilePhoneNumber
def EmployeeBindsExistingMobilePhoneNumber(telNum, openid):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c= conn.cursor()
        sql = "UPDATE naizhenduo_worker_info SET worker_wechat = '%s'   WHERE  worker_phone_num= '%s'" % (openid, telNum)
        print(sql)
        i = c.execute(sql)
        conn.commit()
        print(i)
        c.close()
        return i
    except:
        conn.rollback()
    conn.close()

'''查询项目id对应的时间'''

def SearchDurationByProjectId(ProjectId):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdb.business_duration FROM `naizhenduo_businesslist` nzdb  \
              where nzdb.id='%s'" \
              % (ProjectId)
        # where nzdr.customer_id='%s' '%s' "%(userId, sql)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        return results
        c.close()
    except:
        conn.rollback()
    conn.close()


'''查询该用户中 宝宝新名字的数量'''
def SearchAddBabyNameByUserId(userId,babyName):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT count(*),nzdb.baby_name FROM `naizhenduo_babylist` nzdb  \
        where nzdb.customer_id=%s and nzdb.baby_name='%s' and nzdb.state='1'"  \
         % (userId,babyName)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        return results
        c.close()
    except:
        conn.rollback()
    conn.close()


'''查询宝宝名字by babyid'''
def SearchBabyNameBybabyId(babyid):
    try:
        conn = NZDMySqlConnect.get_dbconnectYTZ()
        c = conn.cursor()
        sql = "SELECT nzdb.baby_name,nzdb.baby_birthday FROM `naizhenduo_babylist` nzdb  \
        where   nzdb.id='%s' and nzdb.state='1'"  \
         % (babyid)
        print(sql)
        c.execute(sql)
        results = c.fetchone()
        return results
        c.close()
    except:
        conn.rollback()
    conn.close()