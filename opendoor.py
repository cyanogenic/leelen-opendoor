import configparser
import json
import os
import subprocess

workspace = os.path.abspath(os.path.dirname(__file__))
login_count = 0
config = configparser.ConfigParser()
config.read(workspace + "/config.ini")

def doLogin():
    login_header = [
        "'Accept: application/json, text/plain, */*'",
        "'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6'",
        "'Cache-Control: no-cache'",
        "'Connection: keep-alive'",
        "'Content-Type: application/json;charset=UTF-8'",
        "'Cookie: websocketIp=" + config['server']['ip'] + "; e_safe_accounts=" + config['server']['username'] + "; sidebarStatus=1'",
        "'Origin: http://" + config['server']['ip'] + "'",
        "'Pragma: no-cache'",
        "'Referer: http://" + config['server']['ip'] + "/esafe/login'",
        "'User-Agent: " + config['server']['user_agent'] + "'",
    ]
    login_body = '{"header":{"appName":"LL_ESAFE","user":"' + config['server']['username'] + '","language":"ZH_CN","serviceName":"getClientInfo","versionId":"v0.1","token":null},"body":{"username":"' + config['server']['username'] + '","password":"' + config['server']['password'] + '"}}'
    login_command = "curl 'http://" + config['server']['ip'] + "/Esafe-Server-Web/rest/login/login' "
    for h in login_header:
        login_command = login_command + "-H " + h + " "

    login_command = login_command + "--data-raw '" + login_body + "' --insecure --silent"
    login_result = subprocess.run(login_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if login_result.returncode == 0:
        data = json.loads(login_result.stdout)
        if data['result']['code'] == 200:
            print(data['body']['token'])  # 输出解析后的数据
            with open(workspace + "/config.ini", 'w') as configfile:
                config['server']['token'] = data['body']['token']
                config.write(configfile)
            doUnlock()
            return 0

    print("命令执行出错:", login_result.stderr.strip())
    return 1

def doUnlock():
    unlock_header = [
        "'Accept: application/json, text/plain, */*'",
        "'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6'",
        "'Cache-Control: no-cache'",
        "'Connection: keep-alive'",
        "'Content-Type: application/json;charset=UTF-8'",
        "'Cookie: JSESSIONID=" + config['server']['token'] + "; websocketIp=" + config['server']['ip'] + "; e_safe_accounts=" + config['server']['username'] + "; sidebarStatus=1'",
        "'Origin: http://" + config['server']['ip'] + "'",
        "'Pragma: no-cache'",
        "'Referer: http://" + config['server']['ip'] + "/esafe/login'",
        "'User-Agent: " + config['server']['user_agent'] + "'",
        "'X-Token: " + config['server']['token'] + "'",
    ]
    unlock_body = '{"header":{"appName":"LL_ESAFE","user":"' + config['server']['username'] + '","language":"ZH_CN","serviceName":"getClientInfo","versionId":"v0.1","token":null},"body":{"sign":1,"openType":1,"openDoors":[{"id":2,"floor":"FF","direction":1}]}}'
    unlock_command = "curl 'http://" + config['server']['ip'] + "/Esafe-Server-Web/rest/deviceList/openDoor' "
    for h in unlock_header:
        unlock_command = unlock_command + "-H " + h + " "

    unlock_command = unlock_command + "--data-raw '" + unlock_body + "' --insecure --silent"
    unlock_result = subprocess.run(unlock_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if unlock_result.returncode == 0:
        try:
            data = json.loads(unlock_result.stdout)
        except json.JSONDecodeError:
            print("命令执行出错:", unlock_result.stderr.strip())
            if login_count == 0:
                print("尝试重新获取Token...")
                doLogin()
            return 1
        try:
            return_code = data['result']['code']
        except KeyError:
            print("返回code异常", data)
            return 1
        if return_code == 200:
            try:
                return_message = data['result']['message']
            except TypeError:
                print("返回message异常", data)
                return 1
            print(return_message)
            return 0
        else:
            print("执行命令失败", data)

    print("命令执行出错:", unlock_result.stderr.strip())
    return 1

doUnlock()
