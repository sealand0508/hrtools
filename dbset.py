import traceback
import psycopg2
import xlrd
from datetime import datetime
import pprint
TcIntt = '10.2.109.89'
TcIntt14 = '10.2.111.207'
TcDataConvert = '10.2.109.152'
TcUat = '10.2.109.98'

defaultArea='台中慈院'
aliseArea = '潭子分院'
aliseArea2 = '台中慈濟'

tbl_insert_expbas_cmd ='''

'''
conn = None
book = None
cursor = None

sqlInsert ='''

INSERT INTO public.hre_expbas (hre_empbas_id, exp_seq, start_date, end_date, remark,
            comp_name, work_desc, active, quit_pos, exp_state,
             source_type, create_uid, write_uid, create_date, write_date)
VALUES (%s, %s, %s, %s, %s,
%s, %s, %s, %s, %s,
%s, %s, %s, %s, %s)
 RETURNING id; '''


def insertData(row,active,thisUid,exp_state,source_type):
    tmpEnd_Date,start_date,end_date,remark,comp_name,work_desc,quit_pos=None,None,None,None,None,None,None
    #active, #OK
    # exp_state, #OK
    # source_type, #OK
    create_uid=thisUid #OK
    write_uid=thisUid #OK
    create_date=datetime.now() #OK
    write_date=datetime.now() #OK
    '-------------------'
    hre_empbas_id = getTableField('hre_empbas', 'EMP_NO', '=', row[3], ['id'], ' last_flag=True And company_id=1 ',
                                  None, isActive=True, isMulti=False)
    if hre_empbas_id :
        sn = getseq(hre_empbas_id)
        exp_seq = sn
    tmpStart_Date = validate(row[4])
    if tmpStart_Date:
        start_date=tmpStart_Date
    if len(row)>5:
        tmpEnd_Date = validate(row[5])
    if tmpEnd_Date:
        end_date = tmpEnd_Date
    if len(row)==7 and tmpStart_Date and tmpEnd_Date:
        comp_name = ' '.join(row[6])
    if len(row) >= 8 and tmpStart_Date and tmpEnd_Date:
        comp_name = row[6]
        quit_pos = row[7]
    if   len(row) > 8 and tmpStart_Date and tmpEnd_Date:
        remark = ' '.join(row[8:])
    elif len(row)>7 and tmpStart_Date and tmpEnd_Date:
        remark = ' '.join(row[7:])
    elif len(row)>6 and tmpStart_Date and tmpEnd_Date:
        remark = ' '.join(row[6:])
    elif tmpStart_Date:
        remark = ' '.join(row[5:])
    else :
        remark = ' '.join(row[4:])
    try:
        if hre_empbas_id:
            values = (hre_empbas_id, exp_seq, start_date, end_date, remark,
                comp_name, work_desc, active, quit_pos, exp_state,
                 source_type, create_uid, write_uid, create_date, write_date)
            # print (values)
            cursor = conn.cursor()
            cursor.execute(sqlInsert, values)
            conn.commit()
    except Exception as e:
        print("insertBas 匯入錯誤錯誤訊息:", e)

def initDb(setName):  # setName = TcIntt,TcDataConvert,TcUat
    global conn
    global book
    global cursor
    try:
        strpass = 'Tzuchi520' #input('請輸入sealand密碼')
        # 109.89 intt 109.88 dataconvert
        strpass='odoo'
        conn = psycopg2.connect(database="odoo", user="odoo", password=strpass, host=setName, port="6444")
        # conn = psycopg2.connect(database="odxx", user="odoo", password='odoo', host="localhost", port="5444")
        cursor = conn.cursor()

    except Exception :
        traceback.print_exc()

    pass
mstid = {}
dtlid = {}
def getDeptNo(tmpDeptName):
    try:
        if defaultArea in tmpDeptName or aliseArea in tmpDeptName or aliseArea2 in tmpDeptName:
            DeptName = tmpDeptName
        else:
            DeptName = defaultArea + tmpDeptName
            cursor = conn.cursor()
            postgreSQL_select_Query = "select id from hre_orgbas where ch_name = %s"
            cursor.execute(postgreSQL_select_Query, [DeptName,])
            rtn = None
            mobile_records = cursor.fetchall()
            row = None
            for row in mobile_records:
                rtn = row[0]
            if rtn ==None:
                print ("搜尋不到"+DeptName)
            return rtn
    except Exception :
         print(Exception)
         traceback.print_exc()

def getIDmst(strCode): #HRA07
    global mstid
    if strCode in mstid:
        return mstid[strCode]
    cursor = conn.cursor()
    postgreSQL_select_Query = "select id from hr_codemst where code_type = %s"

    cursor.execute(postgreSQL_select_Query , [strCode,])
    rtn = None
    mobile_records = cursor.fetchall()
    # row = None
    for row in mobile_records:
        rtn=row[0]
        mstid[strCode] = rtn
    return rtn
def getResUid(login_name):

    return ''
def getIDdtlAll(strCode):
    global dtlid
    mstID = getIDmst(strCode)
    cursor = conn.cursor()
    postgreSQL_select_Query = 'select id,code_name from hr_codedtl where hr_codemst_id= %s'
    cursor.execute(postgreSQL_select_Query, [ mstID, ])
    records = cursor.fetchall()
    for row in records:
        v_id = row[0]
        v_code_name = row[1]
        dtlid[strCode+ v_code_name] = v_id
    return None

def getIDdtl(strmstCode,strdtlName):
    global dtlid
    rtn = None

    if str(strmstCode)+strdtlName in dtlid:
        rtn = dtlid(str(strmstCode)+strdtlName)
    else:
        mstID = getIDmst(strmstCode)
        if mstID:
            cursor = conn.cursor ()
            postgreSQL_select_Query = 'select id from hr_codedtl where code_name = %s and hr_codemst_id= %s'
            cursor.execute(postgreSQL_select_Query, [strdtlName,mstID,])
            records = cursor.fetchall()
            for row in records:
                rtn = row[0]
                dtlid[str(strmstCode) + strdtlName] = row[0]
    return rtn


def getTableField(tableName,fieldNames,eqRule,fieldValue,returnFields,extRule,rList=[],isActive = False,isMulti=False):
    rtn = None
    if type(returnFields) == list:
        allField = ','.join(returnFields)
    else:
        allField = returnFields
    if type(extRule)== list:
        strRule = ' And '.join(extRule)
    elif (not extRule.startswith('And')) and extRule.strip() !='':
        strRule = ' And ' + extRule
    else:
        strRule = extRule
    strActive = ''
    if isActive:
        strActive = ' And Active = True'
    searchRule =' And '+fieldNames + eqRule + "'"+fieldValue+"'"
    postgreSQL_select_Query= "select "+allField +" from "+tableName+" where True " +strActive  +  strRule + ' '+ searchRule
    cursor = conn.cursor()
    # print(postgreSQL_select_Query)
    cursor.execute(postgreSQL_select_Query)

    # postgreSQL_select_Query= "select %s from %s where %s %s %s where true "+ strActive + strRule
    # cursor = conn.cursor()
    # cursor.execute(postgreSQL_select_Query, [allField,tableName, fieldNames,eqRule ,fieldValue,])
    records = cursor.fetchall()
    rtnValue=[]
    for row in records:
        if isMulti:
            rtnValue.append(row)
            rList.append(row)
        else:
            rtnValue = row[0]
    return rtnValue

if __name__=='__main__':
    print ('Start...')
    initDb(TcIntt14)
    rList = []
    # getIDdtlAll('HRA069')
    #    print (getIDmst('HRA07'))
    #     print (getIDmst('HRA07'))
    # print (getIDdtl('HRA07','特休折現(人事專用)'))
    #   print(getIDdtl('HRA07', '特休折現(人事專用)'))
   # id,ch_name,emp_no,company_id = getTableField('hre_empbas','ch_name','=','陳德順',('id,ch_name,emp_no,company_id').split(','),' ',rList,isActive=True,isMulti=True)
    getIDdtlAll('HRE131')

   # print ( id,ch_name,emp_no,company_id )
    if conn:
        conn.close()

    pprint.pprint(dtlid)
    print ('---end---')

allsn = {}
def validate(date_text):
    try:
        return datetime.strptime(date_text,'%Y/%m/%d')
    except:
        return None

def getseq(hre_empbas_id):
    if hre_empbas_id in allsn:
        allsn[hre_empbas_id] = allsn[hre_empbas_id] + 1
    else:
        allsn[hre_empbas_id] = 1
    return allsn[hre_empbas_id]
