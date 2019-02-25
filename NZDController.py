import json
import mysql
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for,jsonify
from datetime import timedelta
import reservation_check
import  api_test
import os
import random1
import  dateTimeDemo
import Integer30
import  api_openid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。\


'''员工绑定已经录好的手机号'''
# Employee binds mobile phone
@app.route('/indexTest',methods=['GET','POST'])
def indexTest():
    return render_template('indexTest.html')

'''员工绑定已经录好的手机号'''
# Employee binds mobile phone
@app.route('/EmployeeBindsMobilePhone',methods=['GET','POST'])
def EmployeeBindsMobilePhone():
    if 'verCode' in session and 'telRegister' in session:
        vcode=session.get('verCode')
        telNow=session.get('telRegister')
        print(vcode,telNow)
        telNum = request.values['telNum']
        VerificationCode=request.values['verificationCode']
        openid = request.values['openid']
        print(telNum, VerificationCode,openid)
        if str(VerificationCode)==str(vcode) and  str(telNum) == str(telNow):
            print('验证成功验证码,开始尝试绑定已有的手机号')
        telNumCount = mysql.SelectTypeValueWorker('worker_phone_num', telNum)
        b = telNumCount[0]
        print(b)
        if b == 1:
            print('手机号存在可以尝试绑定，开始绑定')
            #查找手机号对应的用户是否已经有openid 如果没有就开始绑定 如果有就绑定失败
            results=mysql.SearchOpenidByTel(telNum)
            openidNow=results[0]
            print(openidNow)
            if openidNow is None or openidNow.strip()=='':
                a='该账号无人绑定 可以进行绑定'
                print(a)
                i=mysql.EmployeeBindsExistingMobilePhoneNumber(telNum, openid)
                if i==1:
                    msg='绑定成功'
                    return out_user_info('0', msg, '1')
                else:
                    msg='绑定失败'
                    return out_user_info('0', msg, '1')
            else:
                a = '该账号已经有人了无法绑定'
                print(a)
                return out_user_info('0', a, '1')
        elif b == 0:
            msg='手机号不存在 无法绑定'
            print(msg)
            return out_user_info('0', msg, '1')
        else:
            msg = '手机号异常 请更换手机号绑定'
            print(msg)
            return out_user_info('0', msg, '1')

    else:
        return render_template('error.html')

'''更换手机方法'''
@app.route('/changeTel',methods=['GET','POST'])
def changeTel():
    if 'userId' in session and 'authority' in session:
        userId=session.get('userId')
        authority=session.get('authority')
        print(userId,authority)
        if 'verCode' in session and 'telRegister' in session:
            vcode = session.get('verCode')
            telNow = session.get('telRegister')
            print(vcode, telNow)
            telNum = request.values['telNum']
            VerificationCode = request.values['verificationCode']
            print(VerificationCode, telNum)
            if str(VerificationCode) == str(vcode) and str(telNum) == str(telNow):
                print(authority)
                print(str(authority))
                if (str(authority) == 'c'):
                    print('不是员工')
                    telNumCount = mysql.SelectTypeValue('customer_phone_num', telNum)
                    b = telNumCount[0]
                elif (str(authority) == 'sm' or (str(authority) == 'm')):
                    print('是员工')
                    telNumCount = mysql.SelectTypeValueWorker('worker_phone_num', telNum)
                    b = telNumCount[0]
                print(b)
                if b != 0:
                    msg = '手机号已经被占用'
                    session.pop('verCode', None)
                    session.pop('telRegister', None)
                    print(msg)
                    return out_user_info('0', msg, '1')
                else:
                    msg = '更换成功'
                    session.pop('verCode', None)
                    session.pop('telRegister', None)
                    print(msg)
                    if (str(authority) == 'c'):
                        mysql.changeTelBind(telNum, userId)
                    elif (str(authority) == 'sm' or (str(authority) == 'm')):
                        mysql.changeTelBindWorker(telNum, userId)
                    else:
                        msg = '权限异常'
                    return out_user_info('0', msg, '1')

        else:
            msg = '当前验证码已经过期，请重新发送'
            print(msg)
            return out_user_info('0', msg, '1')
    else:
        return render_template('error.html')



'''更换手机号页面跳转'''
@app.route('/changeTelPage',methods=['GET','POST'])
def changeTelPage():
    return render_template('changeTel.html')



'''验证验证码'''
@app.route('/comparisonVerificationCode',methods=['GET','POST'])
def comparisonVerificationCode():
    if 'verCode' in session and 'telRegister' in session:
        vcode=session.get('verCode')
        telNow=session.get('telRegister')
        #print(vcode,telNow)
        telNum = request.values['telNum']
        VerificationCode=request.values['verificationCode']
        openid=request.values['openid']
        name=request.values['name']
        #print(VerificationCode,telNum,openid)
        if str(VerificationCode)==str(vcode) and  str(telNum) == str(telNow):
            print('验证成功验证码,开始绑定')
            telNumCount=mysql.SelectTypeValue('customer_phone_num',telNum)
            b=telNumCount[0]
            print(b)
            if b!=0:
                msg='手机号已经被占用'
                session.pop('verCode', None)
                session.pop('telRegister', None)
                print(msg)
                return out_user_info('0', msg, '1')
            else:
                nameCount = mysql.SelectTypeValue('customer_name', name)
                c=nameCount[0]
                print(c)
                if c!=0:
                    msg='该姓名已经被占用'
                    session.pop('verCode', None)
                    session.pop('telRegister', None)
                    print(msg)
                    return out_user_info('0', msg, '1')
                else:
                    msg = '注册成功'
                    session.pop('verCode', None)
                    session.pop('telRegister', None)
                    print(msg)
                    mysql.telBind(openid,telNum,name)
                    return out_user_info('0', msg, '1')
        else:
            msg='验证失败'
            print(msg)
            return out_user_info('0', msg, '1')
    else:
        msg='当前验证码已经过期，请重新发送'
        print(msg)
        return out_user_info('0', msg, '1')

'''发送验证码'''

@app.route('/sMSVerificationCode',methods=['GET','POST'])
def sMSVerificationCode():
    telNum = request.values['telNum']
    print(telNum)
    url2 = 'http://wcphp172.xinhaimobile.cn/xh_sms/sms/sms_qcloud.php'
    phone = '18395806960'
    name = '奶珍多用户'
    # content = '9588'
    content=random1.randomFour()
    print(content)
    templId = '278738'  # 模板id 32518预警模板
    operation = 'onesms'  # onesms单条
    session.permanent = True  # 默认session的时间持续31天
    session['verCode'] = content
    session['telRegister'] = telNum
    results=api_test.api_func(url2,telNum,name,content,templId,operation)
    vcode = session.get('verCode')
    telNow=session.get('telRegister')
    print(vcode)
    print(telNow)
    #print('------------'+results)
    return out_user_info('0', results, '1')
    # if 'code' in session:
    #     telNum = request.values['telNum']
    #     verificationCode = request.values['verificationCode']
    #     print()
    # else:


'''个人详情记录时间搜索'''
# reservationPersonRecordPage
@app.route('/reservationPersonRecordPage',methods=['GET','POST'])
def reservationPersonRecordPage():
    if 'userId' in session:
        userId = session.get('userId')
        startTime=request.args.get('startTime')
        endTime=request.args.get('endTime')
        # startTime=request.values['startTime']
        # endTime=request.values['endTime']
        # startTime = request.form['startTime']
        # endTime = request.form['endTime']
        print('startTime:',startTime,' endTime:',endTime)
        sqlJoint=''
        if not startTime is None:
            if startTime.strip() != '':
                sqlJoint= sqlJoint+" and nzdr.resv_time >= '%s' "%(startTime)
                print('开始条件',sqlJoint)
        if not endTime is None:
            if endTime.strip() != '':
                sqlJoint= sqlJoint+" and nzdr.resv_time <= '%s' "%(endTime)
                print('结束条件', sqlJoint)
        if not endTime is None and startTime is None :
            if endTime.strip() == ''and startTime.strip() == '':
                sqlJoint = "and nzdr.resv_time =curdate()"
        print(sqlJoint)
        results = mysql.SearchPersonRecordDetailsByDate(userId,sqlJoint)
        print(results)
        return render_template('personOrderRecord.html', results=results)
    else:
        return render_template('error.html')

'''个人预约记录详情'''
@app.route('/PersonRecordDetails',methods=['GET','POST'])
def PersonRecordDetails():
    id=request.values['num']
    results = mysql.SearchPersonRecordDetails(id)
    print(results)
    #print(results['storeName'])
    #return render_template('personOrderRecord.html', results=results)
    return out_user_info('0', results, '1')
'''个人预约记录'''
@app.route('/PersonalOrderRecordPage',methods=['GET','POST'])
def PersonalOrderRecordPage():
    if 'userId' in session:
        userId = session.get('userId')
        print(userId)
        results = mysql.SearchPersonalOrderRecord(userId)
        print(results)
        return render_template('personOrderRecord.html', results=results)
    else:
        return render_template('error.html')



'''提交预约'''
@app.route('/addOrder',methods=['GET','POST'])
def addOrder():
    if 'userId' in session:
        userId=session.get('userId')
        if request.method == 'POST':
            startTime = request.form['Time']
            res = request.form['res']
            print(startTime)
            print(res)
            res_dict = json.loads(res)
            projectIdList=res_dict['projectIdList']
            print(projectIdList)
            orderDate=res_dict['orderDate']
            print(orderDate)
            duration=res_dict['duration']
            print(duration)
            location=res_dict['location']
            print(location)
            print(userId)

            # projectIdList
            for value in projectIdList.values():
                print('{}'.format(value))
                projectId='{}'.format(value)
                if not projectId=='0':
                    print(projectId)
                    duration=mysql.SearchDurationByProjectId(projectId)[0]
                    print(duration)
                    duration=Integer30.IntegerChange(int(duration))
                    print(duration)
                    print(startTime)
                    endTime=dateTimeDemo.dateCalculate(str(startTime),int(duration))
                    print(endTime)
                    # mysql.addOrder(userId,orderDate,startTime,'10:00',projectId,location)

                    mysql.addOrder(userId,orderDate,startTime,endTime,projectId,location)
                    startTime=endTime
            # 进行增加sql
            # rowCount = mysql.addbaby(addBabyName, addBabyBirth, id)
            # if rowCount == 1:
            #     msg = '添加成功'
            # else:
            #     msg = '添加异常 '
            # # return out_user_info('0', '1', '1')
            # return out_user_info('0', msg, rowCount)
            return out_user_info('0', '预约成功', '2')
    else:
        return render_template('error.html')

'''跳转预约界面'''
@app.route('/TimeListPage/<results>',methods=['GET','POST'])
def TimeListPage(results):
    res=results
    print(res)
    TestData=json.loads(res)['data']
    print(TestData)
    return render_template('timeList.html',TimeList=TestData,res=res)


'''提交到可预约时间点查询'''
@app.route('/SearchTimeList',methods=['GET','POST'])
def SearchTimeList():
    storeName = request.form['express_name']
    orderDate = request.form['orderDate']
    project1 = None
    project2 = None
    project3 = None
    sum=0
    projectlist={1:'0',2:'0',3:'0'}
    if not request.form['express_project1'] is None:
        if not (request.form['express_project1']).strip() == '':
            print('project1',request.form['express_project1'])
            project1 = request.form['express_project1']
            pr1Time = mysql.SearchBussinessTime(project1)['business_duration']
            pr1Int = 0
            if not int(pr1Time) % 30 == 0:
                pr1Int = ((int(pr1Time) // 30) + 1) * 30
            else:
                pr1Int = int(pr1Time)
            sum = sum + int(pr1Time)
            projectlist[1] = mysql.SearchBussinessTime(project1)['id']
        else:
            print('project为空')

    if not  request.form['express_project2'] is None:
        if not (request.form['express_project2']).strip() == '':
            project2 = request.form['express_project2']
            pr2Time = mysql.SearchBussinessTime(project2)['business_duration']
            sum = sum + int(pr2Time)
            pr1Int = 0
            if not int(pr2Time) % 30 == 0:
                pr1Int = ((int(pr2Time) // 30) + 1) * 30
            else:
                pr1Int = int(pr2Time)
            sum = sum + int(pr2Time)
            projectlist[2] = mysql.SearchBussinessTime(project2)['id']
    if not request.form['express_project3'] is None:
        if not( request.form['express_project3']).strip()=='':
            project3 = request.form['express_project3']
            pr3Time = mysql.SearchBussinessTime(project3)['business_duration']
            sum = sum + int(pr3Time)
            pr1Int = 0
            if not int(pr3Time) % 30 == 0:
                pr1Int = ((int(pr3Time) // 30) + 1) * 30
            else:
                pr1Int = int(pr3Time)
            sum = sum + int(pr3Time)
            projectlist[3] = mysql.SearchBussinessTime(project3)['id']
    # print(storeName, orderDate, project1, project2, project3)
    # results = reservation_check.SearchMsg()
    # print(results)
    print(projectlist)
    storeId=mysql.SearchStoreIdByName(storeName)['id']

    # print(storeId)
    # print(orderDate)
    data = {"resv_time": str(orderDate), "location":storeId}

    # print(data)
    # print(sum)
    cust_resv = {"duration": sum}
    print(cust_resv)
    a = reservation_check.get_resv(data)
    print(1)
    b = reservation_check.check(a)
    print(2)
    b['14:30'] += 3
    b['15:00']+=3
    b['15:30']+=3
    b['16:30']+=3
    b['18:30']+=3
    # print(b)
    c = reservation_check.available(data,b,cust_resv)
    print(c)
    # data = {"resv_time":"2019-01-28","location":1}
    # data = {"resv_time":orderDate,"location":storeName}
    # print(data)
    # cust_resv = {"duration":90}
    # a=reservation_check.get_resv(data)
    # b=reservation_check.check(a)
    # b['14:30']+=3
    # b['15:00']+=3
    # b['15:30']+=3
    # b['16:30']+=3
    # b['18:30']+=3
    # # print(b)
    # c = reservation_check.available(data,b,cust_resv)
    # print(c)
    # # timeList=['08:00','08:30']
    # (code, msg, data, projectIdList, orderDate, duration, lcocation):
    return out_TimeList_info(0, '时间列表', c, projectlist, orderDate, sum, storeId)
'''跳转预约界面'''
@app.route('/orderPage',methods=['GET','POST'])
def orderPage():
    # return render_template('newOrder.html')
    results=mysql.selectBusiness()
    results2=mysql.selectStoreList()
    print(results)
    list = []
    for i in results:
        #print(i[0])
        list.append(i[0])
        #print(len(i[0]))
    print(list)

    storeList=[]
    for i in results2:
        storeList.append(i[0])
    print(storeList)

    #projectDemo="['二','二','二','一']"
   # s2=unicode(list, "utf-8")
    return render_template('order.html',projectList=list,storeList=storeList)





'''消息记录'''
@app.route('/msgPage',methods=['GET','POST'])
def msgPage():
    results = mysql.SearchMsg()
    print(results)
    return render_template('msg.html', results=results)
'''禁用宝宝'''
@app.route('/delBaby',methods=['GET','POST'])
def delBaby():
    if request.method =='POST':
        delId=request.values['delId']
        print(delId)
        rowCount = mysql.DelBabyByUserId(delId)
        if rowCount == 1:
            msg = 'del succeed'
        else:
            msg='del error'
    return out_user_info('0', msg, rowCount)
    # return out_user_info('0', '1', '3')



''' 编辑宝宝 '''
@app.route("/editBaby",methods=['GET','POST'])
def editBaby():
    updatekey=0
    print(updatekey)
    if 'userId' in session:
        id = session.get('userId')
        if request.method =='POST':
            editBabyName = request.form['editbabyName']
            editBabyBirth = request.form['editbabyBirth']
            editId = request.form['babyId']

            resultss=mysql.SearchBabyNameBybabyId(editId)
            oldEditBabyName=resultss[0]
            oldEditBabyBirth=resultss[1]
            print(editBabyName,oldEditBabyName)
            if(str(editBabyName)==str(oldEditBabyName)):
                print('名字和旧名字相同 ')
                updatekey=1
                print(updatekey)
                if(str(editBabyBirth)==str(oldEditBabyBirth)):
                    updatekey = 0
                    msg = '无修改'
                    print(updatekey)
                    return out_user_info('0', msg, 1)
            else:
                print('名字和旧名字不相同')
                results = mysql.SearchAddBabyNameByUserId(id, editBabyName)
                editBabyNameCount = results[0]
                if (editBabyNameCount == 0):
                    # 该孩子名字没有被注册可以进行更新
                    updatekey = 1
                    print(updatekey)
                else:
                    msg = '添加失败,请不要重复添加相同的孩子姓名 '
                    print(updatekey)
                    print(msg)
                    return out_user_info('0', msg, 1)

            if updatekey == 1:
                rowCount = mysql.editBaby(editBabyName,editBabyBirth,editId)
                if rowCount == 1:
                    msg = 'update succeed'
                else:
                    msg='update error'
                return out_user_info('0', msg, rowCount)
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')




'''增加宝宝'''
@app.route("/addBaby",methods=['GET','POST'])
def addBaby():
    if 'userId' in session:
        id=session.get('userId')
        if request.method == 'POST':
            addBabyName = request.form['addBabyName']
            addBabyBirth = request.form['addBabyBirth']
            print(addBabyName + "----" + addBabyBirth )
            # 进行增加sql

            results=mysql.SearchAddBabyNameByUserId(id,addBabyName)
            addBabyNameCount=results[0]


            print(addBabyNameCount)
            if(addBabyNameCount==0):
                #该孩子名字没有被注册可以进行添加
                rowCount = mysql.addbaby(addBabyName, addBabyBirth, id)
                if rowCount == 1:
                    msg = '添加成功'
                else:
                    msg = '添加异常 '
                # return out_user_info('0', '1', '1')
                return out_user_info('0', msg, rowCount)
            else:
                msg = '添加失败,请不要重复添加相同的孩子姓名 '
                print(msg)
                return out_user_info('0', msg, 1)

    else:
        return render_template('error.html')










'''跳转宝宝页面'''
@app.route('/babyPage',methods=['GET','POST'])
def babyPage():
    if 'userId' in session:
        print(session.get('userId'))
        id=session.get('userId')
        #查询所有的客户宝宝
        results=mysql.SearchBabyByUserId(id)
        print(results)
        return render_template('baby.html',results=results)
    else:
        print('Session中没有userId')
        return render_template('error.html')

'''增加人数'''
@app.route('/addWorkerNumber',methods=['GET','POST'])
def addWorkerNumber():
    if 'userId' in session:
        userId = session.get('userId')
        location = session.get('location')
        print('id 地点')
        print(userId,location)
        morining = request.form['addMorning']
        print(1)
        afternoon=request.form['addAfternoon']
        print(2)
        evening=request.form['addEvening']
        print(3)
        print('早中晚:'+morining,afternoon,evening)
        results=mysql.addWorkNumber(morining,afternoon,evening,location)
        print(results)
        return redirect(url_for('workNumberPage'))
        # return render_template('/workNumberPage')
    else:
        return render_template('error.html',msg='userId 异常')

'''更新人数'''
@app.route('/editWorkerNumber',methods=['GET','POST'])
def editWorkerNumber():
    if 'userId' in session:
        userId = session.get('userId')
        morining = request.form['editMorning']
        print(1)
        afternoon=request.form['editAfternoon']
        print(2)
        evening=request.form['editEvening']
        print(3)
        id=request.form['editId']
        print('早中晚:'+morining,afternoon,evening)
        results=mysql.editWorkNumber(morining,afternoon,evening,id)
        print(results)
        return redirect(url_for('workNumberPage'))
        # return render_template('/workNumberPage')
    else:
        return render_template('error.html',msg='userId 异常')


'''跳转人数管理'''
@app.route('/workNumberPage',methods=['GET','POST'])
def workNumberPage():
    if 'authority' in session:
        au=session.get('authority')
        print(au)
        location=session.get('location')
        results = mysql.selectWorkNumberPage(location)
        if results is None:
            # results = (1, 1, 3, 3, 3, '2019-01-26')
            return render_template('workerNumber.html')
        else:
            return render_template('workerNumber.html', results=results)
        # if au=='c':
        #     print('顾客,拒绝操作，权限不足');
        #     msg='权限不足,无法访问'
        #     return render_template('index.html',msg=msg)
        # elif au=='m' or au=='sm':
        #     print('操作员')
        #     results = mysql.selectWorkNumberPage()
        #     if results is None:
        #         results=(1, 1, 3, 3, 3, '2019-01-26')
        #         return render_template('workerNumber.html',results=results)
        #     else:
        #         return render_template('workerNumber.html',results=results)

        return out_user_info('0', '1', 'error')


'''禁用店面'''
@app.route('/delStore',methods=['GET','POST'])
def delStore():
    if request.method =='POST':
        delId=request.values['delId']
        print(delId)
        rowCount = mysql.delStore(delId)
        if rowCount == 1:
            msg = 'del succeed'
        else:
            msg='del error'
    return out_user_info('0', msg, rowCount)
    # return out_user_info('0', '1', '3')





'''增加店面'''
@app.route("/addStore",methods=['GET','POST'])
def addStore():
    if request.method =='POST':
        addStoreName = request.form['addStoreName']
        addStoreAddress = request.form['addStoreAddress']
        addSmName = request.form['addSmName']
        addTel = request.form['addTel']
        addStoreTel = request.form['addStoreTel']
        print(addStoreName + "----" + addStoreAddress + '----' + addSmName + '----' + addTel + '----' + addStoreTel )
        #进行增加sql
        rowCount=mysql.addStore(addStoreName,addStoreAddress,addSmName,addTel ,addStoreTel)
        if rowCount == 1:
            msg = '添加成功'
        else:
            msg='添加异常 '
        #return out_user_info('0', '1', '1')
        return out_user_info('0', msg, rowCount)
''' 编辑店面 '''
@app.route("/editStore",methods=['GET','POST'])
def editStore():
    if request.method =='POST':
        editStoreName = request.form['editStoreName']
        editStoreAddress = request.form['editStoreAddress']
        editSmName = request.form['editSmName']
        editTel = request.form['editTel']
        editStoreTel = request.form['editStoreTel']
        storeId = request.form['storeId']
        print(editStoreName+"----"+editStoreAddress+'----'+editSmName+'----'+editTel+'----'+editStoreTel+'----'+storeId)
        rowCount = mysql.editStore(editStoreName,editStoreAddress,editSmName,editTel,editStoreTel,storeId)
        if rowCount == 1:
            msg = 'update succeed'
        else:
            msg='update error'
        #return out_user_info('0', '1', '1')
        return out_user_info('0', msg, rowCount)



'''跳转到页面的店铺'''
@app.route('/storePage',methods=['GET','POST'])
def storePage():
    results = mysql.selectStorePage()
    print(results)
    return render_template('store.html', results=results)




'''删除员工'''
@app.route('/delBussinessList',methods=['GET','POST'])
def delBussinessList():
    if request.method =='POST':
        delId=request.values['delId']
        print(delId)
        rowCount = mysql.DelBussinessList(delId)
        if rowCount == 1:
            msg = 'del succeed'
        else:
            msg='del error'
    return out_user_info('0', msg, rowCount)
    # return out_user_info('0', '1', '3')



''' 编辑项目 '''
@app.route("/editBussinessList",methods=['GET','POST'])
def editBussinessList():
    if request.method =='POST':
        editlistName = request.form['editlistName']
        editTime = request.form['editTime']
        editId = request.form['editId']
        print(editlistName+"----"+editTime+'----'+editId)
        rowCount = mysql.EditBussinessList(editlistName, editTime,editId)
        if rowCount == 1:
            msg = 'update succeed'
        else:
            msg='update error'
        return out_user_info('0', '1', '1')


'''增加项目'''
@app.route("/addBussinessList",methods=['GET','POST'])
def addBussinessList():
    if request.method =='POST':
        addlistName = request.form['addlistName']
        addtime = request.form['addtime']
        print(addlistName+"----"+addtime)
        #进行增加sql
        rowCount=mysql.addBussinessList(addlistName, addtime)
        if rowCount == 1:
            msg = '添加成功'
        else:
            msg='添加异常 '
        return out_user_info('0', msg, rowCount)

'''跳转到项目管理'''
# businessListPage
@app.route('/businessListPage',methods=['GET','POST'])
def businessListPage():
    results=mysql.selectBusinessListPage()
    print(results)
    return render_template('businessList.html',results=results)
'''跳转到管理中心预约记录'''
@app.route('/reservationRecordPage',methods=['GET','POST'])
def reservationRecordPage():
    sqlJoint=""
    if request.method =='POST':
        startTime=request.values['startTime']
        endTime=request.values['endTime']
        # startTime = request.form['startTime']
        # endTime = request.form['endTime']
        print('startTime:',startTime,' endTime:',endTime)
        if startTime.strip() != '':
            sqlJoint="and nzdr.resv_time >= '%s'"%(startTime)
        print('1')
        if endTime.strip() != '':
            sqlJoint="and nzdr.resv_time <= '%s'"%(endTime)
        print('2')
        if endTime.strip() == ''and startTime.strip() == '':
            sqlJoint = "and nzdr.resv_time =curdate()"
            print(sqlJoint)
        results = mysql.selectReservationRecord(sqlJoint)
        return render_template('reservationRecord.html', results=results)
            # return out_user_info('0', 'succeed', results)
            # return jsonify(results)
    else :
        sqlJoint = "and nzdr.resv_time =curdate()"
        print(sqlJoint)
        results = mysql.selectReservationRecord(sqlJoint)
        return render_template('reservationRecord.html', results=results)
'''跳转到人员管理'''
@app.route('/manageEditPage',methods=['GET','POST'])
def manageEditPage():
    results=mysql.selectworkerInfo()
    print(results)
    return render_template('employeeManagement.html',results=results)

'''删除员工'''
@app.route('/delEmployee',methods=['GET','POST'])
def delEmployee():
    if request.method =='POST':
        delId=request.values['delId']
        print(delId)
        rowCount = mysql.DelWorker(delId)
        if rowCount == 1:
            msg = 'del succeed'
        else:
            msg='del error'
        return out_user_info('0', msg, rowCount)
        # return out_user_info('0', '1', '3')

''' 编辑员工 '''
@app.route("/editEmployee",methods=['GET','POST'])
def editEmployee():
    if request.method =='POST':
        editName = request.form['editName']
        editAu = request.form['editAu']
        editTel = request.form['editTel']
        editLocation = request.form['editLocation']
        editId = request.form['editId']
        print(editName+"----"+editAu+"---"+editTel+"---"+editLocation+'---'+editId)
        rowCount = mysql.EditWorker(editName, editAu, editTel, editLocation,editId)
        if rowCount == 1:
            msg = 'update succeed'
        else:
            msg='update error'
        return out_user_info('0', msg, rowCount)
    # return out_user_info('0', '1', '2')



'''添加员工'''
@app.route("/addEmployeeManagement",methods=['GET','POST'])
def addEmployeeManagement():
    if request.method =='POST':
        employeeName = request.form['employeeName']
        authCode = request.form['authCode']
        tel = request.form['tel']
        Location = request.form['location']
        print(employeeName+"----"+authCode+"---"+tel+"---"+Location)
        #进行增加sql
        rowCount=mysql.insertWorker(employeeName, authCode, Location, tel)
        if rowCount == 1:
            msg = 'insert succeed'
        else:
            msg='error '
        return out_user_info('0', msg, rowCount)
'''客户登入'''
@app.route('/HomeLogin',methods=['GET','POST'])
def HomeLogin():
    openid = request.args.get('openid')
    print('获取的openid：'+openid)
    results=mysql.customerInfo(openid)
    if not results is None:
        customerName = results['customerName']
        customerId = results['id']
        customerAuthority = results['authority']
        print(customerId)
        print(customerName)
        print(customerAuthority)
        session.permanent = True  # 默认session的时间持续31天
        session['userId'] = customerId
        session['authority'] = customerAuthority
        print(session.get('userId'))
        storeList = mysql.selectStoreList()
        list = []
        for i in storeList:
            # print(i[0])
            list.append(i[0])
            # print(len(i[0]))
        print(list)
        return render_template('index.html', cN=customerName, ID=customerId,storeList=list)
    else:
        return render_template('telBinding.html',results=openid)


'''员工登入'''
@app.route('/WorkerLogin',methods=['GET','POST'])
def WorkerLogin():
    openid = request.args.get('openid')
    print('获取的openid：'+openid)
    results=mysql.workerInfo(openid)
    if results is None:
        # return render_template('error.html', msg='没有登入权限')
        #转入注册页面
        return render_template('register.html', openid=openid)
    else:
        WorkerName = results['workerName']
        WorkerId = results['id']
        WorkerAuthority = results['authority']
        WorkerLocation=results['location']
        print(WorkerName, WorkerId, WorkerAuthority)
        session.permanent = True  # 默认session的时间持续31天
        session['userId'] = WorkerId
        session['authority'] = WorkerAuthority
        session['location'] = WorkerLocation
        print(session.get('userId'))
        storeList=mysql.selectStoreList()
        list = []
        for i in storeList:
            # print(i[0])
            list.append(i[0])
            # print(len(i[0]))
        print(list)
        return render_template('index.html',storeList=list)







# '''客户登入'''
# @app.route('/WorkerLogin',methods=['GET','POST'])
# def WorkerLogin():
#     openid = request.args.get('openid')
#     print('获取的openid：'+openid)
#     results = mysql.workerInfo(openid)
#     workerName = results['customerName']
#     workerId = results['id']
#     workerAuthority = results['authority']
#     if results is None:
#         return render_template('error.html', msg='没有登入权限')
#     else:
#         print(workerAuthority)
#         session.permanent = True  # 默认session的时间持续31天
#         session['userId'] = workerId
#         session['authority'] = workerAuthority
#         print(session.get('userId'))
#         return render_template('index.html',cN=workerName,ID=workerId)

'''管理中心申请跳转'''
@app.route('/managePage',methods=['GET','POST'])
def managePage():
    if 'userId' in session:
        print(session.get('userId'))
        if 'authority' in session:
            print(session.get('authority'))
            results = mysql.selectToDayOrderRecord()
            authority= session.get('authority')
            print(authority)
            if authority == 'c':
                print('顾客,拒绝操作，权限不足');
                msg = '用户权限不足,无法访问'
                return render_template('index.html', msg=msg)

            elif authority == 'm'or authority=='sm':

                return render_template('Management.html',results=results)
            else:
                return render_template('error.html',msg='用户异常 请重新加载')
        else:
            return render_template('error.html',msg='无合法权限 登入管理中心')
    else:
        print('Session中没有userId')
        return render_template('error.html',msg='用户id异常')



'''主页跳转'''
@app.route('/HomePage',methods=['GET','POST'])
def HomePage():
    if 'userId' in session:
        print(session.get('userId'))
        userId = session.get('userId')
        if 'authority' in session:
            authority=session.get('authority')
            if authority == 'c':
                results=mysql.customerInfoById(userId)
                name=results['customerName']
                tel=results['customerPhoneNum']
                id=results['id']
            elif authority == 'm' or authority=='sm':
                results=mysql.workerById(userId)
                name=results['workerName']
                tel=results['workerPhoneNum']
                id=results['id']
            print(name+'--------'+tel)
            return render_template('index.html', cN=name, ID=id)
        else:
            print('authority')
            return render_template('error.html')
    else:
        print('Session中没有userId')
        return render_template('error.html')




@app.route('/personPage',methods=['GET','POST'])
def peresonPage():
    if 'userId' in session:
        userId=session.get('userId')
        if 'authority' in session:
            print(session.get('authority'))
            authority=session.get('authority')
            print(authority)
            if authority == 'c':
                print(userId)
                id = str(userId)
                name = mysql.customerInfoById(id)['customerName']
                tel = mysql.customerInfoById(id)['customerPhoneNum']
                print(name + '--------' + tel)
                #return render_template('person.html', userName=name, phoneNumber=tel)
                return render_template('person.html', userName=name, phoneNumber=tel)
            elif authority != 'c':
                print(userId)
                id = str(userId)
                name = mysql.workerById(id)['workerName']
                tel = mysql.workerById(id)['workerPhoneNum']
                print(name + '--------' + tel)
                # return render_template('workerPerson.html', userName=name, phoneNumber=tel)
                return render_template('workerPerson.html', userName=name, phoneNumber=tel)
            else :
                return render_template('error.html')

    else:
        print('Session中没有userId')
        return render_template('error.html',msg='用户id异常')



def out_user_info(code, msg, data):
    out_info = {}
    out_info['code'] = code
    out_info['msg'] = msg
    out_info['data'] = data


    return json.dumps(out_info)

def out_TimeList_info(code, msg, data,projectIdList,orderDate,duration,location):
    out_info = {}
    out_info['code'] = code
    out_info['msg'] = msg
    out_info['data'] = data
    out_info['projectIdList']=projectIdList
    out_info['orderDate'] = orderDate
    out_info['duration'] = duration
    out_info['location'] = location
    return json.dumps(out_info)


'''员工登入'''
@app.route('/workerLogin/<openid>',methods=['GET','POST'])
def workerLogin(openid):
    print(openid)
    return openid

'''客户登入2 最新版'''
@app.route('/customerLogin2',methods=['GET','POST'])
def customerLogin2():
    openid = request.args.get('openid')
    print(openid)
    print(mysql.customerInfo(openid))
    return out_user_info('0', '客户信息', mysql.customerInfo(openid))





# #获取session
# @app.route('/getSession/')
# def getSession():
#     return  Session.get('userId')
#
#
#  #删除session
# @app.route('/delete/')
# def delete():
#      print(Session.get('userId'))
#      Session.pop('userId')
#      print(Session.get('userId'))
#      return 'delete'
#
# #清楚session
# @app.route('/clear/')
# def clear():
#      print(Session.get('userId'))
#      Session.clear()
#      print(Session.get('userId'))
#      return 'clear'



@app.route("/da",methods=['GET','POST'])
def a():
    return out_user_info('0', '奶珍多表', mysql.TableToJson())



@app.route("/user",methods=['GET','POST'])
def user():
    return 'hello user'


@app.route("/users/<id>",methods=['GET','POST'])
def users(id):
    return 'hello user:'+id




@app.route("/query_user",methods=['GET','POST'])
def query_user():
    id=request.args.get('id')
    return 'query_user:'+id

@app.route("/query_url")
def query_url():
    return 'query_url:'+url_for('query_user')

@app.route("/query_login" ,methods=['GET','POST'])
def query_login():
    return render_template('index.html')



@app.route("/t/" ,methods=['GET','POST'])
def t():
    code = request.args.get('code')
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    appid = 'wxbce3138d5425b8f6'
    secret = '11e3986e750779b705904cb70ede345a'
    print(code)
    result=api_openid.api_func(url,appid,secret,code)
    openid=result["openid"]
    print(openid)
    results = mysql.customerInfo(openid)
    if not results is None:
        customerName = results['customerName']
        customerId = results['id']
        customerAuthority = results['authority']

        print('当前用户id')
        print(customerId)
        # print(customerName)
        print(customerAuthority)
        session.permanent = True  # 默认session的时间持续31天
        session['userId'] = customerId
        session['authority'] = customerAuthority
        print(session.get('userId'))
        storeList = mysql.selectStoreList()
        list = []
        for i in storeList:
            # print(i[0])
            list.append(i[0])
            # print(len(i[0]))
        print(list)
        # return render_template('index.html, cN=customerName, ID=customerId, storeList=list)
        return render_template('index.html?state=' + random1.randomFour(), cN=customerName, ID=customerId,storeList=list)
    else:
        return render_template('telBinding.html', results=openid)
    # NewUrl=url_for('HomeLogin', openid=openid)
    # print(NewUrl)
    # return  redirect(url_for('HomeLogin', openid=openid))



    #return NewUrl
    # return code


# @app.route("/a/",methods=['GET','POST'])
# def a():
#     code = request.args.get('code')
#     url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
#     appid  =  'wxbce3138d5425b8f6'
#     secret = '11e3986e750779b705904cb70ede345a'
#     print(code)
#     result=api_openid.api_func(url,appid,secret,code)
#     openid=result["openid"]
#     print(openid)
#     results = mysql.workerInfo(openid)
#     if results is None:
#         return render_template('register.html', openid=openid)
#     else:
#         WorkerName = results['workerName']
#         WorkerId = results['id']
#         WorkerAuthority = results['authority']
#         WorkerLocation = results['location']
#         print(WorkerName, WorkerId, WorkerAuthority)
#         session.permanent = True  # 默认session的时间持续31天
#         session['userId'] = WorkerId
#         session['authority'] = WorkerAuthority
#         session['location'] = WorkerLocation
#         print(session.get('userId'))
#         storeList = mysql.selectStoreList()
#         list = []
#         for i in storeList:
#             # print(i[0])
#             list.append(i[0])
#             # print(len(i[0]))
#         print(list)
#         return render_template('index.html', storeList=list)













if __name__ == '__main__':
    # app.run("10.168.20.186","5000",debug=True)
    # app.run("127.0.0.1", port=5000)
    # app.run("127.0.0.1",port=8080)
    # app.run("10.168.20.183",port=8081)
    app.run("192.168.6.35",port=8081)