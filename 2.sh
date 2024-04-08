#!/bin/bash

curl 'http://192.168.1.168/Esafe-Server-Web/rest/login/login' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: websocketIp=192.168.4.200; e_safe_accounts=13012345678; sidebarStatus=1' \
  -H 'Origin: http://192.168.1.168' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://192.168.1.168/esafe/login' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' \
  --data-raw '{"header":{"appName":"LL_ESAFE","dateTime":1712495762259,"user":"admin","language":"ZH_CN","serviceName":"getClientInfo","versionId":"v0.1","token":null},"body":{"username":"13012345678","password":"cqMYG14dss"}}' \
  --insecure
