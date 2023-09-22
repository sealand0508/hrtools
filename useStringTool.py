# -*- coding: utf-8 -*-
from StringTool import *
s = StringTool()
if __name__=='__main__':


    v = """uid
trans
canBack
key
id
io_flag
write_uid
edu_epfdate
work_company_id
branch_id
un_id
leave_src
company_id
hre_postset_id
emp_type
hre_orgbas_id
disp_postset_id
fahow
stayid_no
married
pos_rank
e_mail
create_date
sex
leave_date
spaid_no
come_src
elesign
emp_flag
c_addres
trn_mission_kind
branch_code
query_flag
emp_id
work_place
a_tel2
mission_type
hre_jobset_id
emp_photo
job_code
dayoff_date
remark
confirm_flag
personal_mail
come_date
passport_id
fellowship_type
hre_posmst_id
visible
lev_apply_flag
h_tel
c_tel
create_uid
ch_name
pleave_date
last_flag
trn_mission_type
pos_kind
a_tel
regular_reason
emp_age
dept_no2
trn_date
job_lev
seq_no
disp_orgbas_id
disp_job_lev
country
transfer_date
formal_date
id_no
disp_jobset_id
pre_formal_date
hre_orgbas_wf_id
edu_epf05
charter_flag
branch
doc_flag
fami_num
en_l
en_m
h_address
regular_flag
emp_status
blood
write_date
en_anme
emp_no
train_yr
adtdoc_flag
birth_date
""".split('\n')
    data1 = s.splitAndConvert(v, cstart='F7.',cafter='+cm+', csep=' ')
    data2 = s.runSerious(data1)
    print(data2)
    data1 = s.splitAndConvert(v, cstart='"', cafter='"+cm+', csep=' ')
    data2 = s.runSerious(data1)
    print (data2)
