#!/usr/bin/env python
#!coding=utf-8
import requests
import json
import time
from lxml import etree
import pymysql
from urllib import parse
config={
    "host":"192.168.220.88",
    "user":"root",
    "password":"123456",
    "database":"test",
    "charset":"utf8"
}
position=input("请输入你要查询的岗位： ")
ty=parse.quote(position)
city=input("请输入你要查询的城市：")
url = 'https://www.lagou.com/jobs/positionAjax.json?city='+city+'&needAddtionalResult=false'
HEADERS = {'Referer':'https://www.lagou.com/jobs/list_'+ty+'?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',               'Origin':'https://www.lagou.com',                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Accept':'application/json, text/javascript, */*; q=0.01',
               'Cookie':'_ga=GA1.2.1699039794.1528465721; _gid=GA1.2.1973835728.1528465721; user_trace_token=20180608214839-a63f6313-6b22-11e8-9431-5254005c3644; LGUID=20180608214839-a63f689a-6b22-11e8-9431-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=91; WEBTJ-ID=20180610164548-163e8df755335f-09987c8f28051a-444a022e-1296000-163e8df7554100; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528620349; LGSID=20180610164550-ad79a9e1-6c8a-11e8-9446-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D1%26tn%3D93380420_hao_pg%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rsv_pq%3Dcbd0a1c800015ce8%26rsv_t%3Dc4d8uCxMFx6wzeY1y5TE48Xj6mWCaUQofIkrPi%252BfjYHDqIE4rPXX12WQWIXUjjWqoXdx%252FuV1%26rqlang%3Dcn%26rsv_enter%3D1%26rsv_sug3%3D5%26rsv_sug1%3D1%26rsv_sug7%3D100; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; X_HTTP_TOKEN=da456ffd907c9b82494d80ee5c8d17be; LG_LOGIN_USER_ID=a518f75d3f5bb0ba162b75dd3df45fb79bfa23ccbe2194e1; _putrc=D4E6472823B54423; JSESSIONID=ABAAABAAAIAACBIE032E5886BA57888CB40123289AB6D81; login=true; unick=%E6%9C%B1%E6%B0%B8%E5%AF%8C; gate_login_token=c35c3268e1181c055b568708d5027831109f7e65821f0ffc; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528620423; LGRID=20180610164704-d97315dc-6c8a-11e8-9446-5254005c3644; SEARCH_ID=15d3e61b9e874a358ee4d4e1c888a112; index_location_city=%E5%B9%BF%E5%B7%9E'}
def getPages():
    form_data = {'first': 'true',
                 'pn': 1,
                 'kd': position}
    res = requests.post(url=url, headers=HEADERS, data=form_data)
    result = res.json()
    totalCount=result['content']['positionResult']['totalCount']
    resultSiz=result['content']['positionResult']['resultSize']
    pageCount = int(totalCount) // int(resultSiz) + 1
    return pageCount
def getjobs(pagenum):
    page=1
    for page in range(1,pagenum):
        data = {'first': 'true',
                'pn': str(page),
                'kd': position}
        res = requests.post(url=url, headers=HEADERS, data=data)
        result = res.json()
        jobs = result['content']['positionResult']['result']
        db = pymysql.connect(**config)
        count = 1
        for job in jobs:
            print("---总共%d页---正在爬取第%d页第%d条信息-------"  %(pagenum,page,count))
            count = count + 1
            a=[]
            b={}
            companyShortName= job['companyShortName']
            positionId = job['positionId']  # 主页ID
            companyFullName = job['companyFullName']  # 公司全名
            companySize = job['companySize']  # 公司规模
            industryField = job['industryField']
            createTime = job['createTime']  # 发布时间
            district = job['district']  # 地区
            education = job['education']  # 学历要求
            financeStage = job['financeStage']  # 上市否
            firstType = job['firstType']  # 类型
            companyId = job['companyId']
            score = job['score']
            secondType = job['secondType']  # 类型
            formatCreateTime = job['formatCreateTime']  # 发布时间
            publisherId = job['publisherId']  # 发布人ID
            salary = job['salary']  # 薪资
            workYear = job['workYear']  # 工作年限
            positionName = job['positionName']  #
            jobNature = job['jobNature']  # 全职
            isSchoolJob = job['isSchoolJob']
            subwayline = job['subwayline']
            stationname = job['stationname']
            linestaion = job['linestaion']
            timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            resumeProcessRate = job['resumeProcessRate']
            positionAdvantage = job['positionAdvantage']  # 工作福利
            ##爬取岗位描述
            detail_url = 'https://www.lagou.com/jobs/'+str(positionId)+'.html'
            response = requests.get(url=detail_url, headers=HEADERS)
            response.encoding = 'utf-8'
            tree = etree.HTML(response.text)
            decription = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
            b['decription']=decription
            b['companyLabelList'] = job['companyLabelList']  # 福利待遇
            b['industryLables'] = job['industryLables']
            b['positionLables'] = job['positionLables']
            b['businessZones'] = job['businessZones']

            if b['decription']:
                decription = ",".join(b['decription'])
            else:
                decription = "null"

            if b['businessZones']:
                businessZones = "".join(b['businessZones'])
            else:
                businessZones = "null"

            if b['companyLabelList']:
                companyLabelList = ",".join(b['companyLabelList'])
            else:
                companyLabelList = "null"

            if b['industryLables']:
                industryLables = ",".join(b['industryLables'])
            else:
                industryLables = "null"
            if b['positionLables']:
                positionLables = ",".join(b['positionLables'])
            else:
                positionLables = "null"
            db = pymysql.connect("192.168.220.88", "root", "123456", "test", charset='utf8')
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            sql = "INSERT INTO lagou(companyShortName,positionId\
                                           ,companyFullName,companyLabelList,companySize,industryField,createTime \
                                           ,district,education,financeStage, companyId, score,secondType,formatCreateTime, publisherId \
                                           ,salary, industryLables, workYear, positionName, jobNature \
                                           ,businessZones, subwayline, isSchoolJob, stationname,linestaion, timeNow, resumeProcessRate,positionAdvantage, positionLables,city,decription) \
                                                        VALUES ('%s','%s','%s', '%s','%s', '%s', '%s', \
                                            '%s', '%s','%s', '%s','%s','%s', '%s','%s',\
                                            '%s', '%s','%s', '%s','%s',\
                                            '%s', '%s','%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s')" % \
                  (companyShortName, positionId, companyFullName, companyLabelList, companySize, industryField,createTime, district, education,
                   financeStage, companyId, score,secondType,formatCreateTime, publisherId,
                   salary, industryLables, workYear, positionName, jobNature,
                   businessZones, subwayline, isSchoolJob, stationname,
                   linestaion, timeNow, resumeProcessRate,positionAdvantage, positionLables,city,decription)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            # 关闭数据库连接
            db.close()

    print("爬取完成")
if __name__ == '__main__':
    pagenum=getPages()
    getjobs(pagenum)


