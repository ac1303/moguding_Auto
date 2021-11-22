
import time
import requests
# 此处是抄F-19-F的作业，原主仓库地址https://github.com/F-19-F/SWU-CpDaily/blob/master/index.py
# 注：没有使用这段代码，因为我自己的服务器IP没有被屏蔽，所以不需要，如果用户有需要，请自行修改
def checkip(ip: str):
    res = requests.get(
        'http://ip.taobao.com/outGetIpInfo?ip={}&accessKey=alibaba-inc'.format(ip.split(':')[0])).json()
    # 国内ip
    if res['data']['country'] == '中国':
        # 检测代理可用性
        try:
            requests.get(url='http://baidu.com',
                         proxies={'http': 'http://{}'.format(ip)}, timeout=2)
        except:
            return False
        return True
    return False

def getproxy():
    r = True
    while r:
        res = requests.get("http://demo.spiderpy.cn/get/").json()
        # print(res)
        if not res['https']:
            print("{}不可用，切换代理中".format(res['proxy']))
            continue
        r = not checkip(res['proxy'])
        if r:
            time.sleep(0.2)
    res = {
        'http': 'http://{}'.format(res['proxy']),
        'https': 'http://{}'.format(res['proxy'])
    }

    return res