#!/bin/bash

WORKSPACE="$(dirname $0)"
LOGIN_COUNT=0

source "$WORKSPACE/.env"

function doLogin()
{
    LOGIN_COUNT=1
    CURL_LOGIN=$(curl "http://$IP/Esafe-Server-Web/rest/login/login" -H "Accept: application/json, text/plain, */*" -H "Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6" -H "Cache-Control: no-cache" -H "Connection: keep-alive" -H "Content-Type: application/json;charset=UTF-8" -H "Cookie: websocketIp=$IP; e_safe_accounts=$USERNAME; sidebarStatus=1" -H "Origin: http://$IP" -H "Pragma: no-cache" -H "Referer: http://$IP/esafe/login" -H "User-Agent: $USER_AGENT" --data-raw "{\"header\":{\"appName\":\"LL_ESAFE\",\"user\":\"$USERNAME\",\"language\":\"ZH_CN\",\"serviceName\":\"getClientInfo\",\"versionId\":\"v0.1\",\"token\":null},\"body\":{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}}" --insecure  --silent)

    LOGIN_RESULT=$(echo "$CURL_LOGIN" | jq -r ".result.code")
    LOGIN_MESSAGE=$(echo "$CURL_LOGIN" | jq -r ".result.message")
    LOGIN_TOKEN=$(echo "$CURL_LOGIN" | jq -r ".body.token")
    if [[ "$LOGIN_RESULT" == "200" ]]; then
        echo "$LOGIN_TOKEN" | sed -i "s/TOKEN=.*/TOKEN=\""$LOGIN_TOKEN"\"/g" "$WORKSPACE/.env"
        echo "Got token, now try openDoor..."
        openDoor
    else
            echo "Something wrong..."
            echo "$CURL_LOGIN" 1>&2
            exit 1
    fi
}

function openDoor()
{
    CURL_OPENDOOR=$(curl "http://$IP/Esafe-Server-Web/rest/deviceList/openDoor" -H "Accept: application/json, text/plain, */*" -H "Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6" -H "Cache-Control: no-cache" -H "Connection: keep-alive" -H "Content-Type: application/json;charset=UTF-8" -H "Cookie: JSESSIONID=$TOKEN; websocketIp=$IP; e_safe_accounts=$USERNAME; sidebarStatus=1" -H "Origin: http://$IP" -H "Pragma: no-cache" -H "Referer: http://$IP/esafe/deviceManage/deviceList" -H "User-Agent: $USER_AGENT" -H "X-Token: $TOKEN" --data-raw "{\"header\":{\"appName\":\"LL_ESAFE\",\"user\":\"$USERNAME\",\"language\":\"ZH_CN\",\"serviceName\":\"getClientInfo\",\"versionId\":\"v0.1\",\"token\":null},\"body\":{\"sign\":1,\"openType\":1,\"openDoors\":[{\"id\":2,\"floor\":\"FF\",\"direction\":1}]}}" --insecure --silent)

    OPENDOOR_RESULT=$(echo "$CURL_OPENDOOR" | jq -r ".result.code")
    OPENDOOR_MESSAGE=$(echo "$CURL_OPENDOOR" | jq -r ".result.message")
    if [[ "$OPENDOOR_RESULT" == "200" ]]; then
        echo -e "code:\t $OPENDOOR_RESULT"
        echo -e "message: $OPENDOOR_MESSAGE"
        exit 0
    else
        if [[ $LOGIN_COUNT -eq 0 ]]; then
            echo "Session expired, now try doLogin..."
            doLogin
        else
            echo "Something wrong..."
            echo "$CURL_OPENDOOR" 1>&2
            exit 1
        fi
    fi
}

openDoor
