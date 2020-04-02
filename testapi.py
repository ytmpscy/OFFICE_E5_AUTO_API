# -*- coding: UTF-8 -*-
import requests as req
import json,sys,time,random
#先注册azure应用,确保应用有以下权限:
#files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
#user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
#mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
#注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用
#以下空行不要删除，以便运行时插入机密





config_list = {'每次轮数':6,
	       '是否启动随机时间':'Y','延时范围起始':600,'结束':1800,
	       '是否开启随机api顺序':'Y',
	       '是否开启各api延时':'Y','分延时范围开始':2,'分结束':8}
    
num1 = [0]*len(id_list)
randomapi = ['']*10
ran = 0
path2=sys.path[0]+r'/randomapi.txt'
rapi = {'1':r'https://graph.microsoft.com/v1.0/me/drive/root',
	'2':r'https://graph.microsoft.com/v1.0/me/drive',
	'3':r'https://graph.microsoft.com/v1.0/drive/root',
	'4':r'https://graph.microsoft.com/v1.0/users ',
	'5':r'https://graph.microsoft.com/v1.0/me/messages',
	'6':r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
	'7':r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
	'8':r'https://graph.microsoft.com/v1.0/me/drive/root/children',
	'9':r'https://graph.microsoft.com/v1.0/me/mailFolders',
	'10':r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'}
fc = open(path2, "r+")
randapi = fc.read()
fc.close()
randomapi = randapi.split(',')
def gettoken(refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'
            }
    data={'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id':id_list[a],
          'client_secret':secret_list[a],
          'redirect_uri':'http://localhost:53682/'
         }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    return access_token
def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    localtime = time.asctime( time.localtime(time.time()) )
    access_token=gettoken(refresh_token)
    headers={
    'Authorization':access_token,
    'Content-Type':'application/json'
    }
    print('账号 '+str(a)+' 此次运行开始时间为 :', localtime)
    if config_list['是否开启随机api顺序'] == 'Y':
        for ra in range(10):
            rana = str(randomapi[ra])
            try:
                if req.get(rapi[rana],headers=headers).status_code == 200:
                    num1[a]+=1
                    print("账号"+str(a)+"的"+rana+"号api调用成功,所有api总成功"+str(num1[a])+'次')
                    if config_list['是否开启各api延时'] != 'N':
                        gg = random.randint(config_list['分延时范围开始'],config_list['分结束'])
                        time.sleep(gg)
            except:
                print("pass")
                pass
    else:
        for ra in range(1,11):
            rana = str(ra)
            try:
                if req.get(rapi[rana],headers=headers).status_code == 200:
                    num1[a]+=1
                    print("账号"+str(a)+"的"+rana+"号api调用成功,所有api总成功"+str(num1[a])+'次')
                    if config_list['是否开启各api延时'] != 'N':
                        gg = random.randint(config_list['分延时范围开始'],config_list['分结束'])
                        time.sleep(gg)
            except:
                print("pass")
                pass    
if config_list['是否启动随机时间'] == 'Y':        
    for _ in range(config_list['每次轮数']): 
        b=random.randint(config_list['延时范围起始'],config_list['结束'])
        time.sleep(b)
        for a in range(0, len(id_list)):
            c=random.randint(5,10)
            path=sys.path[0]+r'/token/'+str(a)+'.txt'
            time.sleep(c)
            main()
else:
    for _ in range(config_list['每次轮数']): 
        for a in range(0, len(id_list)):
            c=random.randint(5,10)
            path=sys.path[0]+r'/token/'+str(a)+'.txt'
            time.sleep(c)
            main()
		    
