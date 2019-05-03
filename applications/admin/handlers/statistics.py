#!/usr/bin/env python
# -*- coding: utf-8  -*-
import tornado
from applications.core.decorators import required_permissions
import codecs
from .common import CommonHandler
from pyrestful.rest import get
from applications.core.db import mysqldb

class StatisticsHandler(CommonHandler):

    @get('/admin/statistic/conversion')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:conversion')
    def conversion(self):
        """
        渠道转化
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        sql="select channel,device_counts,customer_counts,apply_counts,issue_counts,overdue30_plus_counts,created_at from stats_operation_channel_conversion where 1=1 %s "%condition
        #导出数据
        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (channel,device_counts,customer_counts,apply_counts,issue_counts,overdue30_plus_counts,created_at)=val
                middle={}
                middle['channel']=channel
                middle['device_counts']=device_counts
                middle['customer_counts']=customer_counts
                middle['apply_counts']=apply_counts
                middle['issue_counts']=issue_counts
                middle['overdue30_plus_counts']=overdue30_plus_counts
                middle['created_at']=created_at
                res_data.append(middle)
            title=[u'渠道',u'设备量',u'注册人数',u'申请人数','u放款人数',u'逾期30+人数',u'时间']
            self.export_csv('conversion',title,res_data)

        else:
            total_sql='select count(1) as num from(%s) as f'%sql
            limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)
            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (channel,device_counts,customer_counts,apply_counts,issue_counts,overdue30_plus_counts,created_at)=val
                middle={}
                middle['channel']=channel
                middle['device_counts']=device_counts
                middle['customer_counts']=customer_counts
                middle['apply_counts']=apply_counts
                middle['issue_counts']=issue_counts
                middle['overdue30_plus_counts']=overdue30_plus_counts
                middle['created_at']=created_at
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/register')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:register')
    def register(self):
        """
        VTG-注册口径
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        sql="select `date`,`customer_counts`,`apply_customer_counts`,`issue_customer_counts`,`deposit_customer_counts`,`reapply_one_counts`,`reapply_two_counts` from `stats_operation_customer` where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)
        total=db_conn.execute(total_sql).fetchone()
        #导出数据
        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (dates,customer_counts,apply_customer_counts,issue_customer_counts,deposit_customer_counts,reapply_one_counts,reapply_two_counts )=val
                middle={}
                middle['dates']=dates
                middle['customer_counts']=customer_counts
                middle['apply_customer_counts']=apply_customer_counts
                middle['issue_customer_counts']=issue_customer_counts
                middle['deposit_customer_counts']=deposit_customer_counts
                middle['reapply_one_counts']=reapply_one_counts
                middle['reapply_two_counts']=reapply_two_counts
                res_data.append(middle)
            title=[u'每天的日期时间',u'注册人数',u'申请人数',u'放款人数',u'还款人数',u'复借1次以上',u'复借2次以上',u'时间']
            self.export_csv('register',title,res_data)

        else:

            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (dates,customer_counts,apply_customer_counts,issue_customer_counts,deposit_customer_counts,reapply_one_counts,reapply_two_counts )=val
                middle={}
                middle['dates']=dates
                middle['customer_counts']=customer_counts
                middle['apply_customer_counts']=apply_customer_counts
                middle['issue_customer_counts']=issue_customer_counts
                middle['deposit_customer_counts']=deposit_customer_counts
                middle['reapply_one_counts']=reapply_one_counts
                middle['reapply_two_counts']=reapply_two_counts
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/issue')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:issue')
    def issue(self):
        """
        VTG-放款口径
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        sql="select issue_date,issue_case_counts,issue_principal,issue_amount,once_overdue_case_counts,due_case_counts, first_overdue_rate,due_principal,deposit_amount,paidoff_case_counts,paidoff_principal,paidoff_amount,overdue1_7_case_counts,overdue1_7_principal,overdue8_14_case_counts,overdue8_14_principal,overdue15_30_case_counts,overdue15_30_principal,overdue30_plus_case_counts,overdue30_plus_principal from stats_operation_issue where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)

        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (issue_date,issue_case_counts,issue_principal,issue_amount,once_overdue_case_counts,due_case_counts, first_overdue_rate,due_principal,deposit_amount,paidoff_case_counts,paidoff_principal,paidoff_amount,overdue1_7_case_counts,overdue1_7_principal,overdue8_14_case_counts,overdue8_14_principal,overdue15_30_case_counts,overdue15_30_principal,overdue30_plus_case_counts,overdue30_plus_principal)=val
                middle={}
                middle['issue_date']=issue_date
                middle['issue_case_counts']=issue_case_counts
                middle['issue_principal']=float(issue_principal)
                middle['issue_amount']=float(issue_amount)
                middle['once_overdue_case_counts']=once_overdue_case_counts
                middle['due_case_counts']=due_case_counts
                middle['first_overdue_rate']=float(first_overdue_rate)
                middle['due_principal']=float(due_principal)
                middle['deposit_amount']=float(deposit_amount)
                middle['paidoff_case_counts']=paidoff_case_counts
                middle['paidoff_principal']=float(paidoff_principal)
                middle['paidoff_amount']=float(paidoff_amount)
                middle['overdue1_7_case_counts']=overdue1_7_case_counts
                middle['overdue1_7_principal']=float(overdue1_7_principal)
                middle['overdue8_14_case_counts']=overdue8_14_case_counts
                middle['overdue8_14_principal']=float(overdue8_14_principal)
                middle['overdue15_30_case_counts']=overdue15_30_case_counts
                middle['overdue15_30_principal']=float(overdue15_30_principal)
                middle['overdue30_plus_case_counts']=overdue30_plus_case_counts
                middle['overdue30_plus_principal']=float(overdue30_plus_principal)
                res_data.append(middle)

            title=[u'放款时间',u'放款笔数',u'放款本金',u'实际放款金额',u'曾逾期笔数',u'到期应还笔数',u'首逾率',u'到期应还本金',u'还款金额',u'已还清笔数',u'已还清本金',u'还款结清金额',u'逾期1到7天笔数',u'逾期1到7天本金',u'逾期8到14天笔数',u'逾期8到14天本金',u'逾期15到30天笔数',u'逾期15到30天本金',u'逾期30+笔数',u'逾期30+本金']
            self.export_csv('issue',title,res_data)

        else:

            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (issue_date,issue_case_counts,issue_principal,issue_amount,once_overdue_case_counts,due_case_counts, first_overdue_rate,due_principal,deposit_amount,paidoff_case_counts,paidoff_principal,paidoff_amount,overdue1_7_case_counts,overdue1_7_principal,overdue8_14_case_counts,overdue8_14_principal,overdue15_30_case_counts,overdue15_30_principal,overdue30_plus_case_counts,overdue30_plus_principal)=val
                middle={}
                middle['issue_date']=issue_date
                middle['issue_case_counts']=issue_case_counts
                middle['issue_principal']=float(issue_principal)
                middle['issue_amount']=float(issue_amount)
                middle['once_overdue_case_counts']=once_overdue_case_counts
                middle['due_case_counts']=due_case_counts
                middle['first_overdue_rate']=float(first_overdue_rate)
                middle['due_principal']=float(due_principal)
                middle['deposit_amount']=float(deposit_amount)
                middle['paidoff_case_counts']=paidoff_case_counts
                middle['paidoff_principal']=float(paidoff_principal)
                middle['paidoff_amount']=float(paidoff_amount)
                middle['overdue1_7_case_counts']=overdue1_7_case_counts
                middle['overdue1_7_principal']=float(overdue1_7_principal)
                middle['overdue8_14_case_counts']=overdue8_14_case_counts
                middle['overdue8_14_principal']=float(overdue8_14_principal)
                middle['overdue15_30_case_counts']=overdue15_30_case_counts
                middle['overdue15_30_principal']=float(overdue15_30_principal)
                middle['overdue30_plus_case_counts']=overdue30_plus_case_counts
                middle['overdue30_plus_principal']=float(overdue30_plus_principal)
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/over_period')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:over_period')
    def over_period(self):
        """
        贷款逾期情况
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        sql="select `date`,`overdue_case_counts`,`once_overdue_counts`,`due_case_counts`,`first_overdue_rate`,`today_due_case_counts`,`today_first_overdue_counts`,`today_first_overdue_rate`,`overdue_principal`,`overdue1_7_case_counts`,`overdue1_7_principal`,`overdue8_14_case_counts`,`overdue8_14_principal`,`overdue15_30_case_counts`,`overdue15_30_principal`,`overdue30_plus_case_counts`,`overdue30_plus_principal` from stats_operation_loan_overdue where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)

        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (date,overdue_case_counts,once_overdue_counts,due_case_counts,first_overdue_rate,today_due_case_counts, today_first_overdue_counts,today_first_overdue_rate,overdue_principal,overdue1_7_case_counts,overdue1_7_principal,overdue8_14_case_counts,overdue8_14_principal,overdue15_30_case_counts,overdue15_30_principal,overdue30_plus_case_counts,overdue30_plus_principal)=val
                middle={}
                middle['date']=date
                middle['overdue_case_counts']=overdue_case_counts
                middle['once_overdue_counts']=once_overdue_counts
                middle['due_case_counts']=due_case_counts
                middle['first_overdue_rate']=float(first_overdue_rate)
                middle['today_due_case_counts']=float(today_due_case_counts)
                middle['today_first_overdue_counts']=float(today_first_overdue_counts)
                middle['today_first_overdue_rate']=float(today_first_overdue_rate)
                middle['overdue_principal']=float(overdue_principal)
                middle['overdue1_7_case_counts']=overdue1_7_case_counts
                middle['overdue1_7_principal']=float(overdue1_7_principal)
                middle['overdue8_14_case_counts']=overdue8_14_case_counts
                middle['overdue8_14_principal']=float(overdue8_14_principal)
                middle['overdue15_30_case_counts']=overdue15_30_case_counts
                middle['overdue15_30_principal']=float(overdue15_30_principal)
                middle['overdue30_plus_case_counts']=float(overdue30_plus_case_counts)
                middle['overdue30_plus_principal']=float(overdue30_plus_principal)
                res_data.append(middle)

            title=[u'时间',u'逾期笔数',u'历史逾期笔数',u'到期应还笔数',u'首逾率',u'当日到期应还',u'当日到期未还',u'当日首逾率',u'逾期本金',u'逾期1到7天笔数',u'逾期1到7天本金',u'逾期8到14天笔数',u'逾期8到14天本金',u'逾期15到30天笔数',u'逾期15到30天本金',u'逾期30+笔数',u'逾期30+本金']
            self.export_csv('over_period',title,res_data)

        else:
            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (date,overdue_case_counts,once_overdue_counts,due_case_counts,first_overdue_rate,today_due_case_counts, today_first_overdue_counts,today_first_overdue_rate,overdue_principal,overdue1_7_case_counts,overdue1_7_principal,overdue8_14_case_counts,overdue8_14_principal,overdue15_30_case_counts,overdue15_30_principal,overdue30_plus_case_counts,overdue30_plus_principal)=val
                middle={}
                middle['date']=date
                middle['overdue_case_counts']=overdue_case_counts
                middle['once_overdue_counts']=once_overdue_counts
                middle['due_case_counts']=due_case_counts
                middle['first_overdue_rate']=float(first_overdue_rate)
                middle['today_due_case_counts']=float(today_due_case_counts)
                middle['today_first_overdue_counts']=float(today_first_overdue_counts)
                middle['today_first_overdue_rate']=float(today_first_overdue_rate)
                middle['overdue_principal']=float(overdue_principal)
                middle['overdue1_7_case_counts']=overdue1_7_case_counts
                middle['overdue1_7_principal']=float(overdue1_7_principal)
                middle['overdue8_14_case_counts']=overdue8_14_case_counts
                middle['overdue8_14_principal']=float(overdue8_14_principal)
                middle['overdue15_30_case_counts']=overdue15_30_case_counts
                middle['overdue15_30_principal']=float(overdue15_30_principal)
                middle['overdue30_plus_case_counts']=float(overdue30_plus_case_counts)
                middle['overdue30_plus_principal']=float(overdue30_plus_principal)
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/day_count')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:day_count')
    def day_count(self):
        """
        平台每日统计
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        sql="select `date`,`customer_counts`,`login_customer_counts`,`apply_customer_counts`,`issue_customer_counts`,`issue_case_count`,`issue_amount`,`deposit_amount`,`paidoff_case_counts`,`prepayment_paid_off`,`the_day_paid_off`,`overdue_paid_off`,`paidoff_amount`,`prepayment_paid_off_amount`,`the_day_paid_off_amount`,`overdue_paid_off_amount`,`due_today_count`,`due_today_paidoff_count`,`today_first_overdue_counts`,`today_first_overdue_rate`,`due_today_amount`,`due_today_paidoff_amount`,`today_first_overdue_amount`,`today_first_overdue_amount_rate` from stats_operation_platform where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)

        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (date,customer_counts,login_customer_counts,apply_customer_counts,issue_customer_counts,issue_case_count, issue_amount,deposit_amount,paidoff_case_counts,prepayment_paid_off,the_day_paid_off,overdue_paid_off,paidoff_amount,prepayment_paid_off_amount,the_day_paid_off_amount,overdue_paid_off_amount,due_today_count,due_today_paidoff_count,today_first_overdue_counts,today_first_overdue_rate,due_today_amount,due_today_paidoff_amount,today_first_overdue_amount,today_first_overdue_amount_rate)=val
                middle={}
                middle['date']=date
                middle['customer_counts']=customer_counts
                middle['login_customer_counts']=login_customer_counts
                middle['apply_customer_counts']=apply_customer_counts
                middle['issue_customer_counts']=issue_customer_counts
                middle['issue_case_count']=issue_case_count
                middle['issue_amount']=float(issue_amount)
                middle['deposit_amount']=float(deposit_amount)
                middle['paidoff_case_counts']=paidoff_case_counts
                middle['prepayment_paid_off']=prepayment_paid_off
                middle['the_day_paid_off']=the_day_paid_off
                middle['overdue_paid_off']=overdue_paid_off
                middle['paidoff_amount']=float(paidoff_amount)
                middle['prepayment_paid_off_amount']=float(prepayment_paid_off_amount)
                middle['the_day_paid_off_amount']=float(the_day_paid_off_amount)
                middle['overdue_paid_off_amount']=float(overdue_paid_off_amount)
                middle['due_today_count']=float(due_today_count)
                middle['due_today_paidoff_count']=float(due_today_paidoff_count)
                middle['today_first_overdue_counts']=float(today_first_overdue_counts)
                middle['today_first_overdue_rate']=float(today_first_overdue_rate)
                middle['due_today_amount']=float(due_today_amount)
                middle['due_today_paidoff_amount']=float(due_today_paidoff_amount)
                middle['today_first_overdue_amount']=float(today_first_overdue_amount)
                middle['today_first_overdue_amount_rate']=float(today_first_overdue_amount_rate)
                res_data.append(middle)

            title=[u'时间',u'注册人数',u'登录人数',u'申请笔数',u'放款人数',u'放款笔数',u'实际放款金额',u'还款金额',u'已还清笔数',u'提前还款结清数',u'到期还款结清数',u'逾期还款结清数',u'还款结清金额',u'提前还款结清金额',u'到期还款结清金额',u'逾期还款结清金额',u'当日到期应还',u'当日到期已还',u'当日到期未还',u'当日首逾率',u'当日到期应还金额',u'当日到期已还金额',u'当日到期未还金额',u'当日金额首逾率']
            self.export_csv('day_count',title,res_data)

        else:
            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (date,customer_counts,login_customer_counts,apply_customer_counts,issue_customer_counts,issue_case_count, issue_amount,deposit_amount,paidoff_case_counts,prepayment_paid_off,the_day_paid_off,overdue_paid_off,paidoff_amount,prepayment_paid_off_amount,the_day_paid_off_amount,overdue_paid_off_amount,due_today_count,due_today_paidoff_count,today_first_overdue_counts,today_first_overdue_rate,due_today_amount,due_today_paidoff_amount,today_first_overdue_amount,today_first_overdue_amount_rate)=val
                middle={}
                middle['date']=date
                middle['customer_counts']=customer_counts
                middle['login_customer_counts']=login_customer_counts
                middle['apply_customer_counts']=apply_customer_counts
                middle['issue_customer_counts']=issue_customer_counts
                middle['issue_case_count']=issue_case_count
                middle['issue_amount']=float(issue_amount)
                middle['deposit_amount']=float(deposit_amount)
                middle['paidoff_case_counts']=paidoff_case_counts
                middle['prepayment_paid_off']=prepayment_paid_off
                middle['the_day_paid_off']=the_day_paid_off
                middle['overdue_paid_off']=overdue_paid_off
                middle['paidoff_amount']=float(paidoff_amount)
                middle['prepayment_paid_off_amount']=float(prepayment_paid_off_amount)
                middle['the_day_paid_off_amount']=float(the_day_paid_off_amount)
                middle['overdue_paid_off_amount']=float(overdue_paid_off_amount)
                middle['due_today_count']=float(due_today_count)
                middle['due_today_paidoff_count']=float(due_today_paidoff_count)
                middle['today_first_overdue_counts']=float(today_first_overdue_counts)
                middle['today_first_overdue_rate']=float(today_first_overdue_rate)
                middle['due_today_amount']=float(due_today_amount)
                middle['due_today_paidoff_amount']=float(due_today_paidoff_amount)
                middle['today_first_overdue_amount']=float(today_first_overdue_amount)
                middle['today_first_overdue_amount_rate']=float(today_first_overdue_amount_rate)
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/again_loan')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:again_loan')
    def again_loan(self):
        """
        VTG-复借口径
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        sql="select `re_apply_date`,`re_apply_count`,`re_apply_issue_count`,`re_apply_due_count`,`re_apply_paid_off_count`,`re_apply_overdue_count`,`re_apply_overdue_rate`,`overdue1_7_case_counts`,`overdue8_14_case_counts`,`overdue15_30_case_counts`,`overdue30_plus_case_counts` from stats_operation_reapply where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)
        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (re_apply_date,re_apply_count,re_apply_issue_count,re_apply_due_count,re_apply_paid_off_count,re_apply_overdue_count, re_apply_overdue_rate,overdue1_7_case_counts,overdue8_14_case_counts,overdue15_30_case_counts,overdue30_plus_case_counts)=val
                middle={}
                middle['re_apply_date']=re_apply_date
                middle['re_apply_count']=re_apply_count
                middle['re_apply_issue_count']=re_apply_issue_count
                middle['re_apply_due_count']=re_apply_due_count
                middle['re_apply_paid_off_count']=re_apply_paid_off_count
                middle['re_apply_overdue_count']=re_apply_overdue_count
                middle['re_apply_overdue_rate']=float(re_apply_overdue_rate)
                middle['overdue1_7_case_counts']=overdue1_7_case_counts
                middle['overdue8_14_case_counts']=overdue8_14_case_counts
                middle['overdue15_30_case_counts']=overdue15_30_case_counts
                middle['overdue30_plus_case_counts']=overdue30_plus_case_counts
                res_data.append(middle)
            title=[u'复借申请日期',u'复借申请笔数',u'复借放款笔数',u'复借到期应还笔数',u'复借还款笔数',u'复借逾期笔数',u'复借逾期率',u'逾期1到7天笔数',u'逾期8到14天笔数',u'逾期15到30天笔数',u'逾期30+笔数']
            self.export_csv('again_loan',title,res_data)

        else:
            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (re_apply_date,re_apply_count,re_apply_issue_count,re_apply_due_count,re_apply_paid_off_count,re_apply_overdue_count, re_apply_overdue_rate,overdue1_7_case_counts,overdue8_14_case_counts,overdue15_30_case_counts,overdue30_plus_case_counts)=val
                middle={}
                middle['re_apply_date']=re_apply_date
                middle['re_apply_count']=re_apply_count
                middle['re_apply_issue_count']=re_apply_issue_count
                middle['re_apply_due_count']=re_apply_due_count
                middle['re_apply_paid_off_count']=re_apply_paid_off_count
                middle['re_apply_overdue_count']=re_apply_overdue_count
                middle['re_apply_overdue_rate']=float(re_apply_overdue_rate)
                middle['overdue1_7_case_counts']=overdue1_7_case_counts
                middle['overdue8_14_case_counts']=overdue8_14_case_counts
                middle['overdue15_30_case_counts']=overdue15_30_case_counts
                middle['overdue30_plus_case_counts']=overdue30_plus_case_counts
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/trial')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:trial')
    def trial(self):
        """
        审批统计
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        full_name=self.get_argument('full_name',None)
        mobile=self.get_argument('mobile',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        if full_name:
            condition+=' and full_name="%s"'%full_name
        if mobile:
            condition+=' and mobile=%s'%mobile
        sql="select `statistics_time`,`full_name`,`mobile`,`first_review_counts`,`second_review_counts`,`final_review_counts` from stats_review_efficiency where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)
        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (statistics_time,full_name,mobile,first_review_counts,second_review_counts,final_review_counts)=val
                middle={}
                middle['statistics_time']=statistics_time
                middle['full_name']=full_name
                middle['mobile']=mobile
                middle['first_review_counts']=first_review_counts
                middle['second_review_counts']=second_review_counts
                middle['final_review_counts']=final_review_counts
                res_data.append(middle)
            title=[u'时间',u'审批员',u'手机',u'初审件数',u'复审件数',u'终审件数']
            self.export_csv('trial',title,res_data)

        else:
            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (statistics_time,full_name,mobile,first_review_counts,second_review_counts,final_review_counts)=val
                middle={}
                middle['statistics_time']=statistics_time
                middle['full_name']=full_name
                middle['mobile']=mobile
                middle['first_review_counts']=first_review_counts
                middle['second_review_counts']=second_review_counts
                middle['final_review_counts']=final_review_counts
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/deal_efficiency')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:deal_efficiency')
    def deal_efficiency(self):
        """
        处理效率明细
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end

        sql="select `date`,`full_name`,`first_case_counts`,`first_reject_case_counts`,`first_close_case_counts`,`first_approve_case_counts`,`issue_counts`,`due_case_counts`,`overdue_counts`,`overdue_ratio`,`second_case_counts`,`second_reject_case_counts`,`second_close_case_counts`,`second_approve_case_counts`,`final_case_counts`,`final_reject_case_counts`,`final_close_case_counts`,`final_approve_case_counts` from stats_review_efficiency_detail where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)
        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (date,full_name,first_case_counts,first_reject_case_counts,first_close_case_counts,first_approve_case_counts,issue_counts,due_case_counts,overdue_counts,overdue_ratio,second_case_counts,second_reject_case_counts,second_close_case_counts,second_approve_case_counts,final_case_counts,final_reject_case_counts,final_close_case_counts,final_approve_case_counts)=val
                middle={}
                middle['date']=date
                middle['full_name']=full_name
                middle['first_approve_case_counts']=first_approve_case_counts
                middle['first_case_counts']=first_case_counts
                middle['first_reject_case_counts']=first_reject_case_counts
                middle['first_close_case_counts']=first_close_case_counts
                middle['issue_counts']=issue_counts
                middle['due_case_counts']=due_case_counts
                middle['overdue_counts']=overdue_counts
                middle['overdue_ratio']=overdue_ratio
                middle['second_case_counts']=second_case_counts
                middle['second_reject_case_counts']=second_reject_case_counts
                middle['second_approve_case_counts']=second_approve_case_counts
                middle['second_close_case_counts']=second_close_case_counts
                middle['final_case_counts']=final_case_counts
                middle['final_reject_case_counts']=final_reject_case_counts
                middle['final_close_case_counts']=final_close_case_counts
                middle['final_approve_case_counts']=final_approve_case_counts
                res_data.append(middle)
            title=[u'时间',u'姓名',u'初审案件数',u'初审拒绝数',u'初审关闭数',u'初审通过数',u'放款笔数',u'到期应还笔数',u'历史逾期笔数',u'逾期率',u'复审案件数',u'复审拒绝数',u'复审关闭数',u'复审通过数',u'终审案件数',u'终审拒绝数',u'终审关闭数',u'终审通过数']
            self.export_csv('deal_efficiency',title,res_data)

        else:
            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (date,full_name,first_case_counts,first_reject_case_counts,first_close_case_counts,first_approve_case_counts,issue_counts,due_case_counts,overdue_counts,overdue_ratio,second_case_counts,second_reject_case_counts,second_close_case_counts,second_approve_case_counts,final_case_counts,final_reject_case_counts,final_close_case_counts,final_approve_case_counts)=val
                middle={}
                middle['date']=date
                middle['full_name']=full_name
                middle['first_approve_case_counts']=first_approve_case_counts
                middle['first_case_counts']=first_case_counts
                middle['first_reject_case_counts']=first_reject_case_counts
                middle['first_close_case_counts']=first_close_case_counts
                middle['issue_counts']=issue_counts
                middle['due_case_counts']=due_case_counts
                middle['overdue_counts']=overdue_counts
                middle['overdue_ratio']=overdue_ratio
                middle['second_case_counts']=second_case_counts
                middle['second_reject_case_counts']=second_reject_case_counts
                middle['second_approve_case_counts']=second_approve_case_counts
                middle['second_close_case_counts']=second_close_case_counts
                middle['final_case_counts']=final_case_counts
                middle['final_reject_case_counts']=final_reject_case_counts
                middle['final_close_case_counts']=final_close_case_counts
                middle['final_approve_case_counts']=final_approve_case_counts
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    @get('/admin/statistic/deal')
    @tornado.web.authenticated
    @required_permissions('admin:statistic:deal')
    def deal(self):
        """
        处理效率
        :return:
        """
        res_data=[]
        start=self.get_argument('start',None)
        end=self.get_argument('end',None)
        page=self.get_argument('page',1)
        limit=self.get_argument('limit',10)
        export_tag=self.get_argument('export_tag',0)
        db_conn = mysqldb()
        condition=''
        if start:
            condition+=' and created_at=%s'%start
        if end:
            condition+=' and created_at=%s'%end
        sql="select `date`,`pre_case_counts`,`pre_reject_case_counts`,`pre_approve_case_counts`,`first_case_counts`,`first_reject_case_counts`,`first_close_case_counts`,`first_approve_case_counts`,`second_case_counts`,`second_reject_case_counts`,`second_close_case_counts`,`second_approve_case_counts`,`final_case_counts`,`final_reject_case_counts`,`final_close_case_counts`,`final_approve_case_counts`,`issue_case_counts` from stats_review_efficiency_total where 1=1 %s "%condition
        total_sql='select count(1) as num from(%s) as f'%sql
        limit_sql=sql+' limit %s,%s'%((int(page)-1)*int(limit),limit)
        if int(export_tag)==1:
            data=db_conn.execute(sql).fetchall()
            db_conn.commit()
            for val in data:
                (date,pre_case_counts,pre_reject_case_counts,pre_approve_case_counts,first_case_counts,first_reject_case_counts,first_close_case_counts,first_approve_case_counts,second_case_counts,second_reject_case_counts,second_close_case_counts,second_approve_case_counts,final_case_counts,final_reject_case_counts,final_close_case_counts,final_approve_case_counts,issue_case_counts)=val
                middle={}
                middle['date']=date
                middle['pre_case_counts']=pre_case_counts
                middle['pre_reject_case_counts']=pre_reject_case_counts
                middle['pre_approve_case_counts']=pre_approve_case_counts
                middle['first_case_counts']=first_case_counts
                middle['first_reject_case_counts']=first_reject_case_counts
                middle['first_close_case_counts']=first_close_case_counts
                middle['first_approve_case_counts']=first_approve_case_counts
                middle['second_case_counts']=second_case_counts
                middle['second_reject_case_counts']=second_reject_case_counts
                middle['second_close_case_counts']=second_close_case_counts
                middle['second_approve_case_counts']=second_approve_case_counts
                middle['final_case_counts']=final_case_counts
                middle['final_reject_case_counts']=final_reject_case_counts
                middle['final_close_case_counts']=final_close_case_counts
                middle['final_approve_case_counts']=final_approve_case_counts
                middle['issue_case_counts']=issue_case_counts
                res_data.append(middle)
            title=[u'时间',u'机审案件数',u'机审拒绝数',u'机审通过数',u'初审案件数',u'初审拒绝数',u'初审关闭数',u'初审通过数',u'复审案件数',u'复审拒绝数',u'复审关闭数',u'复审通过数',u'终审案件数',u'终审拒绝数',u'终审关闭数',u'终审通过数',u'放款笔数']
            self.export_csv('deal_efficiency',title,res_data)

        else:
            total=db_conn.execute(total_sql).fetchone()
            data=db_conn.execute(limit_sql).fetchall()
            db_conn.commit()
            num=0
            if total[0]:
                num=total[0]
            for val in data:
                (date,pre_case_counts,pre_reject_case_counts,pre_approve_case_counts,first_case_counts,first_reject_case_counts,first_close_case_counts,first_approve_case_counts,second_case_counts,second_reject_case_counts,second_close_case_counts,second_approve_case_counts,final_case_counts,final_reject_case_counts,final_close_case_counts,final_approve_case_counts,issue_case_counts)=val
                middle={}
                middle['date']=date
                middle['pre_case_counts']=pre_case_counts
                middle['pre_reject_case_counts']=pre_reject_case_counts
                middle['pre_approve_case_counts']=pre_approve_case_counts
                middle['first_case_counts']=first_case_counts
                middle['first_reject_case_counts']=first_reject_case_counts
                middle['first_close_case_counts']=first_close_case_counts
                middle['first_approve_case_counts']=first_approve_case_counts
                middle['second_case_counts']=second_case_counts
                middle['second_reject_case_counts']=second_reject_case_counts
                middle['second_close_case_counts']=second_close_case_counts
                middle['second_approve_case_counts']=second_approve_case_counts
                middle['final_case_counts']=final_case_counts
                middle['final_reject_case_counts']=final_reject_case_counts
                middle['final_close_case_counts']=final_close_case_counts
                middle['final_approve_case_counts']=final_approve_case_counts
                middle['issue_case_counts']=issue_case_counts
                res_data.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':num,
                'items':res_data
            }
            return self.success(data=res)


    def export_csv(self,file_name,title,data):
        if len(title)==0 or not data:
            return False
        self.set_header("Content-Type", "text/csv; charset=UTF-8")
        # self.set_header('Cache-Control', 'public, max-age=4320000000')
        self.set_header('Content-Disposition', ' attachment; filename=%s.csv'%file_name)
        self.write(codecs.BOM_UTF8)
        self.write(','.join(title))
        self.write('\r\n')
        for item in data:
            middle=[]
            _str=''
            for val in item:

                value=item[val]
                middle.append(value)
            _str=','.join(str(e) for e in middle)
            self.write(_str)
            self.write('\r\n')
