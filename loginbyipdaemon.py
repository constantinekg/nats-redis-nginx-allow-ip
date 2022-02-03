#!/usr/bin/env python3
import asyncio
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
import config
import helperutils
import redisutils
import sys
sys.dont_write_bytecode = True


async def main():
    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.
    nc = await nats.connect(config.natsconnection)

    # You can also use the following for TLS against the demo server.
    #
    # nc = await nats.connect("tls://demo.nats.io:4443")

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        if helperutils.checkForCorrectIpAddress(data) == True:
            print("ip addres has been found, making allow list file...")
            iplist = redisutils.getIpAddressesFromRedis()
            if iplist != False:
                allowlistcreated = helperutils.generateAllowListFile(iplist)
                if allowlistcreated == True:
                    print("allow list has been created")
                    reloadnginx = helperutils.reloadNginxService()
                    if reloadnginx == True:
                        print("nginx daemon successfully reloaded")
                        redisutils.setDoneStateForIpAddressInRedis(data)
                    else:
                        redisutils.setBadStateForIpAddressInRedis(data)
                        print("can\'t reload nginx service. probably it\'s not running?")
                else:
                    redisutils.setBadStateForIpAddressInRedis(data)
                    print("fail to create allow list")
            else:
                redisutils.setBadStateForIpAddressInRedis(data)
                print("fail to get ip adreesess from redis server")
        else:
            redisutils.setBadStateForIpAddressInRedis(data)
            print("bad value from nats - this is not an ip address")

    # Simple publisher and async subscriber via coroutine.
    sub = await nc.subscribe("new_allowed_ip", cb=message_handler)



if __name__ == '__main__':
    print('Daemon started...')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    try:
        loop.run_forever()
    finally:
        loop.close()