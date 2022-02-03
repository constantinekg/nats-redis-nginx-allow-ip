#!/usr/bin/env python3

import redis
import config

def getIpAddressesFromRedis():
    try:
        r = redis.StrictRedis(host=config.redis_host,port=config.redis_port,password=config.redis_auth_key,db=config.redis_database)
        # print(r)
        # r.ping()
        iplist = r.keys()
        iplistwithwhiteaddresses = config.ip_addresses_white_list
        for ip in iplist:
            iplistwithwhiteaddresses.append(ip.decode('utf-8'))
        # print(list(set(iplistwithwhiteaddresses)))
        return list(set(iplistwithwhiteaddresses))
    except Exception as ex:
        print ('Error:', ex)
        exit('Failed to connect, terminating.')
        return False

def setDoneStateForIpAddressInRedis(ipaddr):
    try:
        r = redis.StrictRedis(host=config.redis_host,port=config.redis_port,password=config.redis_auth_key,db=config.redis_database)
        # print(r)
        # r.ping()
        r.setex(ipaddr, config.redis_key_expire_ttl,  "done")
        return True
    except Exception as ex:
        print ('Error:', ex)
        exit('Failed to connect while trying to set done state of ip address, terminating.')
        return False

def setBadStateForIpAddressInRedis(ipaddr):
    try:
        r = redis.StrictRedis(host=config.redis_host,port=config.redis_port,password=config.redis_auth_key,db=config.redis_database)
        # print(r)
        # r.ping()
        r.setex(ipaddr, config.redis_key_expire_ttl, "bad")
        return True
    except Exception as ex:
        print ('Error:', ex)
        exit('Failed to connect while trying to set bad state of ip address, terminating.')
        return False