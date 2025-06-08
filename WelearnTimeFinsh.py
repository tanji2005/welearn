import sys

import requests
import json
import time
import random
import threading
import base64

def generate_cipher_text(password):
    """生成加密后的密码和时间戳"""
    t0 = int(time.time() * 1000)  # 当前时间戳(毫秒)
    p_bytes = password.encode('utf-8')
    v = (t0 >> 16) & 0xFF
    
    for b in p_bytes:
        v ^= b
        
    remainder = v % 100
    t1 = (t0 // 100) * 100 + remainder
    
    # 将密码转换为16进制字符串
    p1 = ''.join([f'{b:02x}' for b in p_bytes])
    s = f'{t1}*{p1}'
    
    # Base64编码
    encrypted = base64.b64encode(s.encode('utf-8')).decode('utf-8')
    return encrypted, t1

session = requests.Session()
def printline():
    print('-'*51)

# 获取账户密码
try:  # 直接从命令行中获取
    username, password = sys.argv[1], sys.argv[2]
except:
    print('=================WELearn挂机时长脚本===============')
    print('============有问题请联系wx:djxxpt2020==============')
    printline()
    print('开源地址: https://gitee.com/xxxhhy/welearn-time-finsh')
    printline()
    print('==================请选择登录方式==================')
    loginmode=input('请选择登录方式: \n  1.账号密码登录\n  2.Cookie登录\n\n请输入数字1或2: ')
    printline()
    if loginmode=='1':
        username = input('请输入账号: ')
        password = input('请输入密码: ')
        
        # 第1步：SSO登录
        encrypted_pwd, timestamp = generate_cipher_text(password)
        
        login_data = {
            'rturl': '/connect/authorize/callback?client_id=welearn_web&redirect_uri=https%3A%2F%2Fwelearn.sflep.com%2Fsignin-sflep&response_type=code&scope=openid%20profile%20email%20phone%20address&code_challenge=p18_2UckWpdGfknVKQp6Ang64zAYH6__0Z8eQu2uuZE&code_challenge_method=S256&state=OpenIdConnect.AuthenticationProperties%3DBhc1Qn6lYFZrxO_KhC7UzXZTYACtsAnIVT0PgzDlhtuxIXeSFLwXaNbthEeuwSCbzvhrw2wECCxFTq8tbd7k2OFPfH0_TCnMkuh8oBFmlhEsZ3ZXUYecidfT2h2YpAyAoaBaXfpuQj2SGCIEW3KVRYpnljmx-mso97xCbjz72URywiBJRMqDS9TqY-0vaviUIH1X72u_phfuiBdbR1s-WOyUj21KAPdNPJXi1nQtUd-hRoeI53WBTrv2EC0U4SNFvhivPgE6YseB2fdYbPv4u0NiFeHPD3EBQyqE_iUVI1QrGPG3VvhD5xs8odx21WncybewKIuTQpH3MAfJkTmDeQ',
            'account': username,
            'pwd': encrypted_pwd,
            'ts': str(timestamp)
        }
        
        login_headers = {
            'host': 'sso.sflep.com',
            'sec-ch-ua-platform': '"Windows"',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://sso.sflep.com',
            'referer': 'https://sso.sflep.com/idsvr/login.html'
        }
        
        res = session.post(
            "https://sso.sflep.com/idsvr/account/login", 
            data=login_data,
            headers=login_headers
        )
        
        if res.ok and 'code' in res.json() and res.json()['code'] == 0:
            print("登录成功!!")
            
            # 第2步：处理SSO回调
            callback_url = "https://sso.sflep.com/idsvr/connect/authorize/callback"
            callback_params = {
                'client_id': 'welearn_web',
                'redirect_uri': 'https://welearn.sflep.com/signin-sflep',
                'response_type': 'code',
                'scope': 'openid profile email phone address',
                'code_challenge': 'p18_2UckWpdGfknVKQp6Ang64zAYH6__0Z8eQu2uuZE',
                'code_challenge_method': 'S256',
                'state': 'OpenIdConnect.AuthenticationProperties=Bhc1Qn6lYFZrxO_KhC7UzXZTYACtsAnIVT0PgzDlhtuxIXeSFLwXaNbthEeuwSCbzvhrw2wECCxFTq8tbd7k2OFPfH0_TCnMkuh8oBFmlhEsZ3ZXUYecidfT2h2YpAyAoaBaXfpuQj2SGCIEW3KVRYpnljmx-mso97xCbjz72URywiBJRMqDS9TqY-0vaviUIH1X72u_phfuiBdbR1s-WOyUj21KAPdNPJXi1nQtUd-hRoeI53WBTrv2EC0U4SNFvhivPgE6YseB2fdYbPv4u0NiFeHPD3EBQyqE_iUVI1QrGPG3VvhD5xs8odx21WncybewKIuTQpH3MAfJkTmDeQ'
            }
            
            # 跟随重定向处理SSO回调
            response = session.get(callback_url, params=callback_params, allow_redirects=True)
            
            # 获取并保存最终的cookies
            cookies_list = []
            for cookie in session.cookies:
                cookies_list.append(f"{cookie.name}={cookie.value}")
            session.cookies_str = "; ".join(cookies_list)
        
        else:
            print("登录失败:", res.text)
            input("按任意键退出")
            exit(0)
    elif loginmode=='2':
        try:
            cookie = dict(map(lambda x:x.split('=',1),input('请粘贴Cookie: ').split(";")))
        except:
            input('Cookie输入错误!!!')
            exit(0)
        for k,v in cookie.items():
              session.cookies[k]=v
    else:
        input('输入错误!!')
        exit(0)
printline()
class NewThread(threading.Thread):
    def __init__(self,learntime,x):
        threading.Thread.__init__(self)
        self.deamon = True
        self.learntime = learntime
        self.x = x
    def run(self):
        startstudy(self.learntime,self.x)
def startstudy(learntime,x):
#    print('\n位置: '+x['location']+'\n已学习: '+x['learntime']+'
#    即将学习'+str(learntime)+'秒～',end='')
    scoid = x['id']
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(url,data={'action':'getscoinfo_v7','uid':uid,'cid':cid,'scoid':scoid},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
    if('学习数据不正确' in req1.text):
        req1 = session.post(url,data={'action':'startsco160928','uid':uid,'cid':cid,'scoid':scoid},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
        req1 = session.post(url,data={'action':'getscoinfo_v7','uid':uid,'cid':cid,'scoid':scoid},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
        if('学习数据不正确' in req1.text):
            print('\n错误:',x['location'])
            wrong.append(x['location'])
            return 0
    back = json.loads(req1.text)['comment']
    if('cmi' in back):
        back = json.loads(back)['cmi']
        cstatus = back['completion_status']
        progress = back['progress_measure']
        session_time = back['session_time']
        total_time = back['total_time']
        crate = back['score']['scaled']
    else:
        cstatus = 'not_attempted'
        progress = session_time = total_time = '0'
        crate = ''
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(url,data={'action':'keepsco_with_getticket_with_updatecmitime','uid':uid,'cid':cid,'scoid':scoid,'session_time':session_time,'total_time':total_time},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
    for nowtime in range(1,learntime + 1):
#        print(str(nowtime)+'～',end='')
        time.sleep(1)
        if(nowtime % 60 == 0):
#            print('发送心跳包～',end='')
            url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
            req1 = session.post(url,data={'action':'keepsco_with_getticket_with_updatecmitime','uid':uid,'cid':cid,'scoid':scoid,'session_time':session_time,'total_time':total_time},headers={'Referer':'https://welearn.sflep.com/student/StudyCourse.aspx' })
#    print('增加学习时间～')
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(url,data={'action':'savescoinfo160928','cid':cid,'scoid':scoid,'uid':uid,'progress':progress,'crate':crate,'status':'unknown','cstatus':cstatus,'trycount':'0'},headers={'Referer':'https://welearn.sflep.com/Student/StudyCourse.aspx'})

while True:
    url = 'https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc'
    req = session.get(url,headers={'Referer':'https://welearn.sflep.com/student/index.aspx'})
    back = json.loads(req.text)['clist']
    i = 1
    for x in back:
        print('[id:{:>2d}]  完成度 {:>2d}%  {}'.format(i,x['per'],x['name']))
        i+=1
    i = int(input('\n请输入需要刷时长的课程id（id为上方[]内的序号）: '))

    cid = str(back[i - 1]['cid'])
    url = 'https://welearn.sflep.com/student/course_info.aspx?cid=' + cid
    req = session.get(url,headers={'Referer':'https://welearn.sflep.com/student/index.aspx'})
    uid = req.text[req.text.find('"uid":') + 6:req.text.find('"',req.text.find('"uid":') + 7) - 2]
    classid = req.text[req.text.find('classid=') + 8:req.text.find('&',req.text.find('classid=') + 9)]


    url = 'https://welearn.sflep.com/ajax/StudyStat.aspx'
    req = session.get(url,params={'action':'courseunits','cid':cid,'uid':uid},headers={'Referer':'https://welearn.sflep.com/student/course_info.aspx'})
    back = json.loads(req.text)['info']

    print('\n\n[id: 0]  按顺序刷全部单元学习时长')
    i = 0
    unitsnum = len(back)
    for x in back:
        i+=1
        print('[id:{:>2d}]  {}  {}'.format(i,x['unitname'],x['name']))
    unitidx = int(input('\n\n请选择要刷时长的单元id（id为上方[]内的序号，输入0为刷全部单元）： '))


    inputdata = input('\n\n\n模式1:每个练习增加指定学习时长，请直接输入时间\n如:希望每个练习增加30秒，则输入 30\n\n模式2:每个练习增加随机时长，请输入时间上下限并用英文逗号隔开\n如:希望每个练习增加10～30秒，则输入 10,30\n\n\n请严格按照以上格式输入: ')
    if(',' in inputdata):
        inputtime = eval(inputdata)
        mode = 2
    else:
        inputtime = int(inputdata)
        mode = 1


    threads = 100 #最大线程数设置
    running = []
    runningnumber = maxtime = 0
    wrong = []

    if(unitidx == 0):
        i = 0
    else:
        i = unitidx - 1
        unitsnum = unitidx

#    while '异常' not in req.text and '出错了' not in req.text:
    for unit in range(i,unitsnum):
        url = 'https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid=' + cid + '&uid=' + uid + '&unitidx=' + str(unit) + '&classid=' + classid
        req = session.get(url,headers={'Referer':'https://welearn.sflep.com/student/course_info.aspx?cid=' + cid})
        back = json.loads(req.text)['info']
        for x in back:
            if(mode == 1):
                learntime = inputtime
            else:
                learntime = random.randint(inputtime[0],inputtime[1])
            if(runningnumber == threads):
                for nowtime in range(1,maxtime + 1):
                    print('\r已启动线程:',runningnumber,'当前秒数:',nowtime,'秒，总时间:',maxtime,'秒',end='')
                    time.sleep(1)
                print('  等待线程退出…')
                for t in running:
                    t.join()
                runningnumber = maxtime = 0
                running = []
            running.append(NewThread(learntime,x))
            running[runningnumber].start()
            runningnumber+=1
            if(learntime > maxtime):
                maxtime = learntime
            print('线程:',runningnumber,'位置:',x['location'],'\n已学: ',x['learntime'],'将学:',learntime,'秒')

        if(runningnumber > 0):
            for nowtime in range(1,maxtime + 1):
                print('\r已启动线程:',runningnumber,'当前秒数:',nowtime,'秒，总时间:',maxtime,'秒',end='')
                time.sleep(1)
            print('  等待线程退出…')
            for t in range(runningnumber):
                running[t].join()
            runningnumber = maxtime = 0
            running = []

    if (unitidx == 0):
        break
    else:
        print('\n\n本单元结束！错误:',len(wrong),'个')
        for i in range(len(wrong)):
            print('第',i + 1,'个错误:',wrong[i])
        print('回到选课处！！\n\n\n\n')

print('运行结束!!\n错误:',len(wrong),'个')
for i in range(len(wrong)):
    print('第',i + 1,'个错误:',wrong[i])
print("\n\n\n**********  如果有问题请联系邮箱hhy5562877@163.com  **********\n\n\n")
input("按任意键退出")

def generate_cipher_text(password):
    """生成加密后的密码和时间戳"""
    t0 = int(time.time() * 1000)  # 当前时间戳(毫秒)
    p_bytes = password.encode('utf-8')
    v = (t0 >> 16) & 0xFF
    
    for b in p_bytes:
        v ^= b
        
    remainder = v % 100
    t1 = (t0 // 100) * 100 + remainder
    
    # 将密码转换为16进制字符串
    p1 = ''.join([f'{b:02x}' for b in p_bytes])
    s = f'{t1}*{p1}'
    
    # Base64编码
    encrypted = base64.b64encode(s.encode('utf-8')).decode('utf-8')
    return encrypted, t1
