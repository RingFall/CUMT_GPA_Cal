#-*- coding: UTF-8 -*- 
import requests
import json

url='http://202.119.206.62/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
cookie={
    'JSESSIONID' : 'your_jsessionid_cookie'    #填入用cookieedit插件获取的cookie值,有时限，每次会变化
}
rr=requests.post(url,cookies=cookie) #第一次请求，看总数
al=json.loads(rr.content)
total=al['totalResult']
po={
    'queryModel.showCount':total
}
#'xnm=&xqm=&_search=false&nd=1535349814932&queryModel.showCount=10&queryModel.currentPage=1&queryModel.sortName=&queryModel.sortOrder=asc&time=10'
r=requests.post(url,cookies=cookie,data=po)
res=r.content
all=json.loads(res)
i=0
avgcj=0
jqcj=0
avggpa=0
jqgpa=0
totalxf=0
for item in all['items']:
    i+=1
    flag=1
    mc=item['kcmc']
    if 'kcgsmc' in item:   #公选课不算在内，打印课程名称
        i-=1
        flag=0
        print(mc)
    if(item['cj'].isdigit()):
        cj=int(item['cj'])
    elif(item['cj']==u"优秀"):
        cj=90
    elif(item['cj']==u"良好"):    #有些课需要转换
        cj=80
    else:
        print(item['cj'])      #没成绩的课，如缓考QAQ
        flag=0
        i-=1
    jd=float(item['jd'])
    xf=float(item['xf'])
    if(flag==1):
        avgcj+=cj
        jqcj+=(xf*cj)
        avggpa+=jd
        jqgpa+=(jd*xf)
        totalxf+=xf
avgcj=avgcj/i
jqcj=jqcj/totalxf
avggpa=avggpa/i
jqgpa=jqgpa/totalxf
print "平均成绩：%.2f / 加权成绩：%.2f ".decode('UTF-8').encode('GBK') % (avgcj,jqcj)
print "平均gpa：%.2f / 加权gpa：%.2f ".decode('UTF-8').encode('GBK') % (avggpa,jqgpa)
print "四分制：平均gpa：%.2f / 加权gpa：%.2f ".decode('UTF-8').encode('GBK') % (4*avggpa/5,4*jqgpa/5)
print "已计算 %d 门 / 已完成 %d 门".decode('UTF-8').encode('GBK') % (i,all['showCount'])