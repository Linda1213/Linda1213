#2021_5_7 yxy 30 
#2021_5_6 yxy
#2021_5_5 Yangxinya
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from lxml import etree
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import requests
import re
#******************************************************************************************************************#
#root=Tk()
#root.title('课程计划及完成情况考核系统')
#********************************************************************************************************************#
#获取每门课程及其对应的id
def get_id():
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400','cookie':'JG_fcdf8e635093adde6bef42651_PV=1620039633433|1620039633433; csrftoken=bx28ZlQfUNm18B3KRyQWI91IPJiP6su3; sessionid=1ad949ri5et530p5tkgcoe9jdal06iur'}
    id_list=[]
    session=requests.Session()
    id_response=requests.get('https://changjiang.yuketang.cn/v2/api/web/courses/list?identity=2',headers=headers).json()
    data_list=id_response["data"]['list']
    for p in data_list:
       id_list.append(p['course']['name'])
       id_list.append(p['classroom_id'])
    return id_list
#获取指定课程的目录及每节课的习题数和课件数
def get_class_content():
        headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400','cookie':'JG_fcdf8e635093adde6bef42651_PV=1620039633433|1620039633433; csrftoken=bx28ZlQfUNm18B3KRyQWI91IPJiP6su3; sessionid=1ad949ri5et530p5tkgcoe9jdal06iur'}
        class_id=eval(inputnum1.get())
        session=requests.Session()
        pro_id=[]
        content_list=[]
        ppt_count=[]
        pro_num=[]
        correct_pro=[]
        doubt_ppt=[]
        content_list1=[]
        content_list2=[]
        r=[]
        for page in range(0,5):
           content_url='https://changjiang.yuketang.cn/v2/api/web/logs/learn/{}?actype=-1&page={}&offset=20&sort=-1'.format(class_id,page)
           content_response=requests.get(url=content_url,headers=headers).json()
           for a in content_response['data']['activities']:
               pro_id.append(a['courseware_id'])
               content_list.append(a['title'])
        for u in pro_id:
            try:
             ppt_url='https://changjiang.yuketang.cn/v2/api/web/lessonafter/{}/presentation?classroom_id={}'.format(u,class_id)
             ppt_response=requests.get(url=ppt_url,headers=headers).json()
             ppt_count.append(ppt_response['data'][0]['count'])
             doubt_ppt.append(ppt_response['data'][0]['doubt_count'])
            except:
             ppt_count.append('*')
             doubt_ppt.append('*')
        for u in pro_id:
           try:
            pro_url='https://changjiang.yuketang.cn/v2/api/web/lessonafter/{}/problem_quiz_results?classroom_id={}'.format(u,class_id)
            pro_response=requests.get(url=pro_url,headers=headers).json()
            pro_num.append(pro_response['data']['objective_count'])
            correct_pro.append(pro_response['data']['correct_objective_count']) 
           except:
            pro_num.append('*')
            correct_pro.append('*')
        index=0
        while index<len(pro_num):
            if pro_num[index]=='*':
                del pro_num[index]
                del content_list[index]
                del ppt_count[index]
                del correct_pro[index]
                del doubt_ppt[index]
            else:
                index+=1
        for i in content_list:
          content_list1.append(re.sub("\（.*?\）|\(.*?\)'","",i))
        content_list=content_list1
        for i in content_list:
           content_list2.append(i.replace(" ",""))
        content_list=content_list2   
        content_list.reverse()
        pro_num.reverse()
        ppt_count.reverse()
        correct_pro.reverse()
        doubt_ppt.reverse()
        r.append(content_list)
        r.append(pro_num)
        r.append(ppt_count)
        r.append(correct_pro)
        r.append(doubt_ppt)
        return r

#**********************************************************************************************************************************************************************************#
#构造评价模型:教师的行为数据s[0],学生的行为数据是s[1]
def evaluate():
  r=get_class_content()
  tech_goals=[0]*len(r[1])
  stu_state=[0]*len(r[1])
  sum_pro=0
  sum_ppt=0
  s=[]
  for i in r[1]:
      sum_pro+=i
  aver_pro=sum_pro/len(r[1])
  for i in r[2]:
      sum_ppt+=i
  aver_ppt=sum_ppt/len(r[2])
  index=0
  while index<len(r[1]):
      if r[1][index]<aver_pro and r[2][index]<aver_ppt:
          tech_goals[index]=1
      elif r[1][index]>aver_pro and r[2][index]>aver_ppt:
          tech_goals[index]=3
      elif r[1][index]>aver_pro and r[2][index]<aver_ppt or r[1][index]<aver_pro and r[2][index]>aver_ppt:  
          tech_goals[index]=2
      index+=1
  for i in range(len(r[1])):
      if float(1-r[3][i]/(r[1][i]+1))+float(r[4][i]/(r[2][i]+1))<=0.2:
          stu_state[i]=3
      elif 0.2<float(1-r[3][i]/(r[1][i]+1))+float(r[4][i]/(r[2][i]+1))<=0.6:
          stu_state[i]=2
      elif float(1-r[3][i]/(r[1][i]+1))+float(r[4][i]/(r[2][i]+1))>0.6:
           stu_state[i]=1
  s.append(tech_goals)
  s.append(stu_state)
  return s
#**************************************************************************************************************************************************************************************#
#图形显示
#图形初始化
def autolabel(rects):
    for rect in rects:
      height = rect.get_height()
      plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % int(height))
def init_display():
    #global pro_num
    r=get_class_content()
    s=evaluate()
    name=list(range(len(r[1])))
    l1=s[0]
    l2=s[1]
    total_width=0.8
    n=2
    width=total_width/n
    x=list(range(len(r[1])))
    plt.rc('font',family='SimHei',size=12)
    a=plt.bar(x,l1,width=width,label='Target',fc='y')
    for i in range(len(x)):
        x[i]=x[i]+width
    b=plt.bar(x,l2,width=width,label='Completed',tick_label=name,fc='b')
    autolabel(a)
    autolabel(b)
    plt.xlabel("目录")
    plt.ylabel("教学计划")
    plt.title("教学计划及完成情况")
    plt.legend()
    plt.show()
#根据用户输入值显示图形
def result_display():
    r=get_class_content()
    s=evaluate()
    #target_input=list(input("请输入教学目标,数据长度为{}".format(len(r[1]))))
    target_input=list(map(int,list(inputnum2.get())))
    name=list(range(len(r[1])))
    l1=target_input
    l2=s[1]
    total_width=0.8
    n=2
    width=total_width/n
    x=list(range(len(r[1])))
    plt.rc('font',family='SimHei',size=12)
    a=plt.bar(x,l1,width=width,label='Target',fc='y')
    for i in range(len(x)):
        x[i]=x[i]+width
    b=plt.bar(x,l2,width=width,label='Completed',tick_label=name,fc='b')
    autolabel(a)
    autolabel(b)
    plt.xlabel("目录")
    plt.ylabel("教学计划")
    plt.title("教学计划及完成情况")
    plt.legend()
    plt.show()
#********************************************************************************************************************************************************************************************************#
#将相关信息写入文本文件
def set_length(src,length,str1):
    n=length-len(src)
    newstr = src + str1 * n
    return  newstr[0:length]
def get_course_txt1():
    r=get_class_content()
    content=r[0]
    content1=[]
    s=evaluate()
    number=list(range(len(content)))
    number.insert(0,'序号')
    content.insert(0,'目录')
    s[1].insert(0,'实际情况')
    s[0].insert(0,'教学目标')
    res=max(content,key=len,default="")
    l=len(res)
    for i in content:
        content1.append(set_length(i,l,chr(12288)))
    with open('课程考核计划.txt','w') as file:
       for i in range(len(content)-1):
            file.write("{:}\t{:^20}\t{:^10}\t{:^10}\n".format(number[i],content1[i],s[0][i],s[1][i]))
    file.close()
def get_course_txt2():
    r=get_class_content()
    content=r[0]
    content1=[]
    s=evaluate()
    #target=list(input("请输入教学目标,数据长度为{}".format(len(r[1]))))
    target=list(inputnum2.get())
    number=list(range(len(content)))
    number.insert(0,'序号')
    content.insert(0,'目录')
    s[1].insert(0,'实际情况')
    target.insert(0,'教学目标')
    res=max(content,key=len,default="")
    l=len(res)
    for i in content:
        content1.append(set_length(i,l,chr(12288)))
    with open('课程考核计划.txt','w') as file:
       for i in range(len(content)):
            file.write("{:}\t{:^20}\t{:^10}\t{:^10}\n".format(number[i],content1[i],target[i],s[1][i]))
    file.close()
#打开文件函数
def openfile():
    filename=filedialog.askopenfilename()
    f=open(filename,'r')
    f2=f.read()
    f.close()
    text.insert(INSERT,f2)

#************************************************************************************************************************************************************************************************#
#设置窗口程序
root=Tk()
root.title('课程计划及完成情况考核系统')
inform=Message(root,text=get_id(),aspect=800,justify=LEFT)
inform.pack()
Label(root,text='请输入课程序号:').pack(side=LEFT,anchor=NW)
inputnum1=StringVar()
entrynum1=Entry(root,width=8,textvariable=inputnum1).pack(side=LEFT,anchor=NW)
result=Button(root,text='初始化',command=get_course_txt1).pack(side=LEFT,anchor=NW)
btn_open = Button(root, text='打开', command=openfile).pack(side=LEFT,anchor=N)
btn_init_display=Button(root,text='初始化图形显示',command=init_display).pack(side=LEFT,anchor=N)
btn_result_display=Button(root,text='实际进度图形显示',command=result_display).pack(side=RIGHT,anchor=N)
btn_edit=Button(root,text='输入完成',command=get_course_txt2).pack(side=RIGHT,anchor=N)
inputnum2=StringVar()
entrynum2=Entry(root,width=8,textvariable=inputnum2).pack(side=RIGHT,anchor=N)
Label(root,text='输入教学目标').pack(side=RIGHT,anchor=N)
text = Text(root)
text.pack(side=BOTTOM,expand=YES,fill=BOTH) 
mainloop()  # 进入消息循环






