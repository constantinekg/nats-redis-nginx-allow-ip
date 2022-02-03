#!/usr/bin/env python3

import config
import redisutils
import helperutils
import sys
sys.dont_write_bytecode = True

def mainFunction():
    iplist = redisutils.getIpAddressesFromRedis()
    if iplist != False:
        print ('ip list has been received')
        allowfilecreated = helperutils.generateAllowListFile(iplist)
        if allowfilecreated == True:
            print ('allow file has been created')
            reloadnginx = helperutils.reloadNginxService()
            if reloadnginx == True:
                print ('nginx daemon reload has been successfully')
            else:
                print ('can\'t reload nginx daemon')
                sys.exit(1)
        else:
            print ('can\'t write allow file')
            sys.exit(1)
    else:
        print ("can\'t get ip list from redis and config")
        sys.exit(1)

if __name__ == "__main__":
    mainFunction()