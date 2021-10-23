import json
import requests
import hashlib

# =================用户配置=======================
phone="L47"          #账号
password="L47是我的"      #密码
country="中国"                   #国家
province="湖北省"             #省
city="十堰"                  #城市
address="今天也想抱抱L47"       #地址
latitude="32.652811"                  #纬度
longitude="110.743494"                 #经度  
types="END"                     #类型，START和END，START上班，END下班
#===================推送key=============================
serveSendKey="SCT81708Tgz4lewIrwFEqcDaXN8MvpU"
# =================脚本配置(不可擅自更改)=======================
Login_Url='https://api.moguding.net:9000/session/user/v1/login'
planUrl = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
saveUrl = "https://api.moguding.net:9000/attendence/clock/v2/save"
salt="3478cbbc33f84bd00d75d7dfa69e0daa"
headers={
        'Accept-Language':"zh-CN,zh;q=0.8",
        'roleKey': 'student',
        "Content-Type": "application/json; charset=UTF-8",
        "Cache-Control": "no-cache",
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-cn; Redmi K20 Pro Premium Edition Build/RKQ1.200826.002) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1'
        }
body = {
        "country":country,
        "address":address,
        "province":province,
        "city":city,
        "latitude":latitude,
        "description":"",
        "type":types,
        "device":"Android",
        "longitude":longitude}
# ===============================serve酱推送=====================
def sendMsg(title, desp):
    print('正在将打卡结果推送到微信...')
    url = "https://sctapi.ftqq.com/"+serveSendKey+".send"
    body = {
        "title": title,
        "desp": desp
    }
    res = requests.post(url=url, data=body)
    # print(res.text)
# =================生成签名===================
def GenerateSign(x):
    a = x.encode('utf-8')
    a = hashlib.md5(a).hexdigest() 
    # print(a)
    return a
# ================登录====================
def login():
    global token,userId
    data = {
            "password": password,
            "loginType": "android",
            "uuid": "",
            "phone": phone
        }
    req = requests.post(Login_Url,data=json.dumps(data),headers=headers)
    token=json.loads(req.text)['data']['token']
    userId=json.loads(req.text)['data']['userId']
# ===================获取planID=======================
def getPlanId():
    login()
    global planId
    data = {"state": ""}
    headers["Authorization"]=token 
    # sign= userId+"student"+salt
    headers["sign"]=GenerateSign(userId+"student"+salt)
    req = requests.post(planUrl,data=json.dumps(data),headers=headers)
    req.headers.keys
    planId=json.loads(req.text)['data'][0]['planId']
    # print("planId",planId)
# =======================开始打卡=======================
def main():
    getPlanId()
     # sign= device + type + planID + userId + Address + salt    
    body["planId"]=planId
    # headers["sign"]=GenerateSign(body["device"]+body["type"]+planId+userId+body["address"]+salt)
    req = requests.post(saveUrl,data=json.dumps(body),headers=headers)
    req_json=json.loads(req.text)
    if(req_json["code"]==200):
        sendMsg("蘑菇丁打卡状态通知","打卡状态："+req_json["msg"]+"\n\n打卡时间："+req_json["data"]["createTime"])
    else:
        sendMsg("蘑菇丁打卡状态通知","打卡失败"+"\n\n失败原因："+req_json["msg"])
    # print(req.text)
    # print(req.cookies)
    # print(req.headers)


main()