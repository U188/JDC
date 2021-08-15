import os, re,requests,sys,json
from urllib.parse import unquote
# scriptname=os.environ["scriptname"]
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
class getJDCookie:
    def getck(self):
        with open('/ql/config/env.sh', 'r') as f:
            cookie = f.read()
            com=re.compile(r'(?<=JD_COOKIE=\").+?(?=\")',re.S)
            cookies=re.findall(com,cookie)[0].replace('\\n','').split('\\n')
        return cookies

    def getUserInfo(self, ck):
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback='
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'close',
            'Referer': 'https://home.m.jd.com/myJd/home.action',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'me-api.jd.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'zh-cn'
        }
        try:
            if sys.platform == 'ios':
                resp = requests.get(url=url, verify=False, headers=headers, timeout=60).json()
            else:
                resp = requests.get(url=url, headers=headers, timeout=60).json()
            if resp['retcode'] == "0":
                nickname = resp['data']['userInfo']['baseInfo']['nickname']
                return ck, nickname
            else:
                return ck, False
        except Exception:
            context = f"{ck}已失效！请重新获取。"
            print(context)
            return ck, False
class spiltlog:
    def __init__(self):
        self.path = '/ql/log/yuannian1112_jd_scripts_'
    # 获取最近的日志
    def newloggg(self,p):
        path=self.path+p+'/'
        #print(path)
        list = os.listdir(path)
        list.sort(key=lambda fn: os.path.getmtime(path + fn) if not os.path.isdir(path + fn) else 0)
        #print(f"{path}{list[-1]}")
        with open(f"{path}{list[-1]}",'r') as f:
            txt=f.read()
        return txt
    # 农场关键词
    def ncparagraph(self,txt,pin,active):
        try:
            if active:
                com = re.compile(f'(?<=】{pin}).+', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            else:
                com = re.compile(f'(?<=】{pin}).+?(?=开始【京东)', re.S)
                para = re.findall(com, txt)[0] # 截取PIN段落
            if '提醒⏰】' in para:
                s = '你是不是忘了中水果\n'
            elif len(para)>=1:
                com2 = re.compile(r'(?<=进度】).+(?=，)', re.M)
                jindu = re.findall(com2, para)[0]
                com3 = re.compile(r'(?<=预测】).+(?=水果)', re.M)
                yuce = re.findall(com3, para)[0]
                com4 = re.compile(r'(?<=名称】).+', re.M)
                name = re.findall(com4, para)[0]
                s = f'{name}已完成{jindu},预计{yuce}\n'
        except:
            s='请进入活动页面检查,如果正常可能是未找到日志，稍后再看\n'
        return s

    # 工厂关键词
    def gcparagraph(self, txt,pin,active):
        try:
            if active:
                com = re.compile(f'(?<={pin}\*\*\*\*\*\*\*\*\*).+', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            else:
                com = re.compile(f'(?<={pin}\*\*\*\*\*\*\*\*\*).+?(?=\*\*\*\*\*\*开始)', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            if '【提示】' in para:
                s='你忘记选择商品，如果显示火爆可尝试寻找客服\n'
            elif '商品兑换已超时' in para:
                s='你的兑换超时了请重新选择商品，如果显示火爆可尝试寻找客服\n'
            elif len(para) >= 1:
                com2 = re.compile(r'(?<=生产进度】).+', re.M)
                jindu = re.findall(com2, para)[0]
                com3 = re.compile(r'(?<=预计最快).+', re.M)
                yuce = re.findall(com3, para)[0]
                com4 = re.compile(r'(?<=商品】).+', re.M)
                name = re.findall(com4, para)[0]
                s = f'{name}已完成{jindu},预计{yuce}\n'
        except Exception as e:
            s='请进入活动页面检查,如果正常可能是未找到日志，稍后再看\n'
        return s
    # 牧场关键词
    def mcparagraph(self,txt,pin,active):
        try:
            if active:
                com = re.compile(f'(?<={pin}).+', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            else:
                com = re.compile(f'(?<={pin}).+?(?=\*\*\*\*\*开始)', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            if '温馨提示' in para:
                s = '请先手动完成【新手指导任务】再运行脚本\n'
            elif len(para) >= 1:
                com2=re.compile(r'(?<=投喂).+', re.M)
                jdpara=re.findall(com2, para)[-1]
                if '吃太多' in jdpara:
                    s='要撑死了，小鸡吃的太多了\n'
                else:
                    s=f'投喂{jdpara}\n'

        except:
            s = '请进入活动页面检查,如果正常可能是未找到日志，稍后再看\n'
        return s

    # 京豆
    def jdparagraph(self, txt,pin,active):
        try:
            if active:
                com = re.compile(f'(?<={pin}).+', re.S)
                para = re.findall(com, txt)[1]  # 截取PIN段落
            else:
                com=re.compile(f'(?<={pin}).+?(?=\*)',re.S)
                para=re.findall(com,txt)[1]#截取PIN段落
            if len(para) >= 1:
                com2=re.compile(r'(?<=当前京豆：).+(?=\(今日将)',re.M)
                jdpara=re.findall(com2,para)[0]
                com3 = re.compile(r'(?<=今日收入：).+(?=京豆)', re.M)
                tdjdpara = re.findall(com3, para)[0]
                com4 = re.compile(r'(?<=昨日收入：).+(?=京豆)', re.M)
                zrjdpara = re.findall(com4, para)[0]
                com5= re.compile(r'(?<=当前总红包：).+(?=今日)', re.M)
                hbjdpara = re.findall(com5, para)[0]
                com6 = re.compile(r'(?<=总过期).+(?=\)元)', re.M)
                gqjdpara = re.findall(com6, para)[0]

                s = f'{jdpara}京豆({tdjdpara},{zrjdpara})\n💰当前红包：{hbjdpara}{gqjdpara})\n'
        except Exception as e:
            s='请进入活动页面检查,如果正常可能是未找到日志，稍后再看\n'
        return s


    # 萌宠
    def mmcparagraph(self, txt,pin,active):
        try:
            if active:
                com = re.compile(f'(?<=】{pin}).+', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            else:
                com = re.compile(f'(?<=】{pin}).+?(?=开始【京东)', re.S)
                para = re.findall(com, txt)[0]# 截取PIN段落
            if '萌宠活动未开启' in para:
                s = '萌宠活动未开启,请到APP开启活动\n'
            elif len(para) >= 1:
                com2 = re.compile(r'(?<=完成进度】).+(?=，)', re.M)
                jindu = re.findall(com2, para)[0]
                s = f'已完成{jindu}\n'
        except:
            s='请进入活动页面检查,如果正常可能是未找到日志，稍后再看\n'
        return s
    # 大老板
    def dlbparagraph(self,txt,pin,active):
        try:
            if active:
                com = re.compile(f'(?<=】{pin}).+', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            else:
                com = re.compile(f'(?<=】{pin}).+?(?=开始)', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            if '忘了种植新的水果' in para:
                s = '你的活动未开启，请到极速版开启活动\n'
            elif len(para) >= 1:
                com2 = re.compile(r'(?<=还需要浇水：)\d+(?=次)', re.M)
                jindu = re.findall(com2, para)[0]
                s = f'还需要浇水{jindu}次\n'
        except:
            s='请进入活动页面检查,如果正常可能是未找到日志，稍后再看\n'
        return s
    # 极速金币
    def jsparagraph(self,txt,pin,active):
        try:
            if active:
                com = re.compile(f'(?<=】{pin}).+', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            else:
                com = re.compile(f'(?<=】{pin}).+?(?=开始)', re.S)
                para = re.findall(com, txt)[0]  # 截取PIN段落
            if len(para) >= 1:
                com2 = re.compile(r'(?<=金币，共计).+', re.M)
                jindu = re.findall(com2, para)[0]
                com3 = re.compile(r'(?<=可兑换).+', re.M)
                jinbi = re.findall(com3, para)[0]
                s = f'{jindu},可兑换{jinbi}\n'
        except:
            s = '未找到账户信息，可能任务还没做完一会再看\n'
        return s
def wecom_app(title, content):
    QYWX_AM="ww56da8866f5367917,iogo3TmkpT5rsZLT6H_Nl2HU8RZe7oix0H03ehDBcps,@all,1000002,2NPDqg9xB9bWKej642zKsedDhVH15_eMCi_7hDVcSkLMBjyvok0G35nSPHzaF7p6c"
    try:
        QYWX_AM_AY = re.split(',', QYWX_AM)
        if 4 < len(QYWX_AM_AY) > 5:
            print("QYWX_AM 设置错误！！\n取消推送")
            return
        corpid = QYWX_AM_AY[0]
        corpsecret = QYWX_AM_AY[1]
        touser = QYWX_AM_AY[2]
        agentid = QYWX_AM_AY[3]
        try:
            media_id = QYWX_AM_AY[4]
        except:
            media_id = ''
        wx = WeCom(corpid, corpsecret, agentid)
        # 如果没有配置 media_id 默认就以 text 方式发送
        if not media_id:
            message = title + '\n\n' + content
            response = wx.send_text(message, touser)
        else:
            response = wx.send_mpnews(title, content, media_id, touser)
        if response == 'ok':
            print('推送成功！')
        else:
            print('推送失败！错误信息如下：\n', response)
    except Exception as e:
        print(e)

class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace('\n', '<br/>'),
                        "digest": message
                    }
                ]
            }
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

if __name__== '__main__':
    logh = ['jd_fruit', 'jd_dreamFactory', 'jd_jxmc', 'jd_bean_change', 'jd_pet', 'jd_wsdlb', 'jd_speed_sign']
    getJDCookie=getJDCookie()
    spiltlog = spiltlog()
    cookies = list(filter(None, getJDCookie.getck()[0].split('\n')))
    msg=''
    for n in range(0,len(cookies)):
        msg1 = ''
        m = cookies[n].replace('\\n', '')
        ck, pin = getJDCookie.getUserInfo(m)
        if n+1 == len(cookies):
            active=True
        else:
            active=False
        for p in logh:
            txt=spiltlog.newloggg(p)
            if 'bean_change' in p:
                bean_chage=spiltlog.jdparagraph(txt,pin,active)
            if 'speed_sign' in p:
                speed_sign = spiltlog.jsparagraph(txt,pin,active)
            if 'jd_fruit' in p:
                nc = spiltlog.ncparagraph(txt,pin,active)
            if 'jd_wsdlb' in p:
                dlb = spiltlog.dlbparagraph(txt,pin,active)
            if 'jd_pet' in p:
                mmc = spiltlog.mmcparagraph(txt,pin,active)
            if 'jd_jxmc' in p:
                mc=spiltlog.mcparagraph(txt,pin,active)
            if 'jd_dreamFactory' in p:
                gc=spiltlog.gcparagraph(txt,pin,active)

        msg1=f'\n🙆账户：{pin} 💨\n🐶当前京豆：{bean_chage}🏃极速金币：{speed_sign}🍒京东农场：{nc}🍅极速农场：{dlb}🐾京东萌宠：{mmc}🐤京喜牧场：{mc}🏢京东工厂：{gc}'
        msg+=msg1
    wecom_app('账户通知',msg)

