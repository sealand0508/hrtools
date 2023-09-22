# -*- coding: utf-8 -*-

class StringTool:
    def runSerious(self,data,snStart = 0):
        lines =  data.split('\n')
        rtn =''
        for line in lines:
            oneline = line.replace('{ssn}',str(snStart))
            snStart +=1
            rtn = rtn+'\n'+oneline if rtn else oneline
        return rtn
    def splitAndConvert(self,data,split='\n',cstart="'",cafter="'",csep=",",mod5 = False ,isRepeatData=False,clast=""):
        _vlist=[]
        rtn=""
        _vlist=list(data) #''.split(split)
        icnt = 0


        for one in _vlist:
            if isRepeatData:
                repeat = one
            else:
                repeat =""
            if str(one).strip()!='':
                icnt +=1
                if mod5:
                    rtn = cstart + one.strip() + cafter if rtn == '' else rtn+csep+cstart+one.strip()+cafter.strip()  + ( '\n'  if icnt % 5 == 0 else '') + repeat.strip()+clast.strip()
                else:
                    rtn = cstart + one.strip() + cafter if rtn == '' else rtn + csep + cstart + one.strip() + cafter.strip()+ repeat.strip()+clast.strip()
                  # '15953'
        return rtn

    def genCode(self,fields, strsplit=',', strprev='', strafter='', outsplit='\n', strmid='', runi=False, starti=0,
                strmid2=''):
        tmp = fields.split(strsplit)
        rtndata = ''
        for onetmp in tmp:
            thistmp = onetmp
            thistmp = thistmp.strip()
            showi = ''
            if runi:
                showi = str(runi)
                runi = runi + 1
            rtndata = strprev + thistmp + strmid + showi + strmid2 + strafter if rtndata == '' else rtndata + outsplit + strprev + thistmp + strmid + showi + strmid2 + strafter
        print(rtndata)
        return rtndata

    def printlistdetail(self,*detail, wdsplit=',', **var):
        '''
        :param detail: 傳入的list
        :param var: 複製list的文字串,使用逗號分隔
        :return: None,會列印出 帶序號及list的欄位說明及值
        '''
        vax = (var['varname'].split(wdsplit))

        cnt = 0
        for datai in detail[0]:
            print(str(cnt).rjust(2) + "(" + vax[cnt].replace('\n','').strip() + "):", datai,
                  str(type(datai)).replace('<', '').replace('>', '').replace('class', ''),
                  end=('.\t' if cnt % 3 != 0 else '\n'))
            cnt = cnt + 1

    def genParamEqualNone(self, args, split='\n'):
        v = args
        v1=s.splitAndConvert(v,cstart='',cafter='',csep=',')
        v2=s.genPercent(v,pack='None',mod5=False)
        return v1 +" = " + v2

    def genPercent(self,args,split='\n',pack='%s',mod5 = True):
        rtnvalue = ""
        icnt =0
        for one in range(len(args)):
            icnt +=1
            if str(one).strip() != '':
                if mod5:
                    rtnvalue = pack if rtnvalue == '' else rtnvalue + "," + pack + ( '\n'  if icnt % 5 == 0 else '')
                else:
                    rtnvalue = pack if rtnvalue == '' else rtnvalue + "," + pack
        return rtnvalue

def testcase1(s,v):

    print("-A-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)
    print(s.splitAndConvert(v, cstart='', cafter='', csep=','))

    print("-A2-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)
    print(s.splitAndConvert(v, cstart='', cafter='', csep=',', mod5=True))

    print("-B-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)
    print(s.splitAndConvert(v, csep=','))
    print("-C-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)
    print(s.splitAndConvert(v, cstart='', cafter="=''", csep='\n'))


    print("-D-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)
    print(s.splitAndConvert(v, cstart="data= chgtype('S',sheet.cell(r, 1).value) #", csep='\n'))
    print("-D1-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)

    print(s.splitAndConvert(v, cstart='xlsheet1.cells(1, 1).value ="',cafter='"', csep='\n'))
    print("-E-" + '*===' * 5 + 'genPercent()' + '===' * 10)
    print(s.genPercent(v))  # 應該要能使用 List
    # print("-F-" +'===' * 5 + 'printlistdetail()' + '===' * 10)
    # print (s.printlistdetail(v.split(','),wdsplit=',',varname=v))

    # print("-G-" + '===' * 5 + 'printlistdetail()' + '===' * 10)
    # print(s.printlistdetail(v.split(','), wdsplit=',', varname=v))

    print("-H-" + '===' * 5 + 'genParamEqualNone()' + '===' * 10)
    print(s.genParamEqualNone(v, split=','))

    print("-I-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)  # dim xxx as string
    print(s.splitAndConvert(v, cstart=' ', cafter=" as string", csep='\n'))

    print("-J-" + ('===' * 5) + 'splitAndConvert()' + '===' * 10)  # ndoc.id = oneData.id
    print(s.splitAndConvert(v, cstart=' ndoc.', cafter=" = oneData.", csep='\n'))


if __name__=='__main__':
    s = StringTool()
    v="""salary,advance,remark,code_type,code_belong,active,code_desc,code_len,mdm_flag""".split(',')
    v = """ id_no,name,black_type,reason,start_date,end_date,
company_id,hre_empbas_id,
create_uid,create_date,write_ui
d,write_date
    """.split(',')
    v = '''code_name
code_no
hr_codemst_id
remark
active
oth_flag
prc_flag
code_value
write_date
create_uid
create_date
write_uid'''.split('\n')
    # v = """ 人員姓名	執照名稱	管理類別	執照日期	執照生效日	有效期限	狀態	到職日	部門		金額	身份證號	執照號碼	狀態說明

       
    
    # """.split('\t')

   # v="""組套,包班單位名稱,備註,班數,金額,特殊說明,包班班別1,包班班別2,包班班別3,包班班別4,包班班別5,包班班別6,包班班別7,包班班別8,包班班別9,包班班別10,包班班別11,包班班別12,包班班別13,包班班別14,包班班別15,包班班別16,包班班別17,包班班別18,包班班別19,包班班別20,""".split(',')
    v ="""disa_sys
condadisa_type
condadisa_nameconda   
condadisa_level
condadisa_num
condacreate_uid
condawrite_uid
condacreate_date
condawrite_date""".split('\n')
    testcase1(s,v)

