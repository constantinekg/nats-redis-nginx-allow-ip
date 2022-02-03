#!/usr/bin/env python3

natsconnection = 'nats://127.0.0.1:4222'
redis_host = '127.0.0.1'
redis_port = 6379
redis_database = 1
redis_auth_key = 'HBkscfsdjdnosewtsdgvs'
redis_key_expire_ttl = 43200 # seconds
ip_addresses_white_list = ['192.168.0.0/24', '10.4.4.0/24']
allowlistoutfile = '/etc/nginx/ipset/allowlist.conf'