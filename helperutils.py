#!/usr/bin/env python3
import ipaddress
import config
import subprocess

# ip address validation
def checkForCorrectIpAddress(ipaddr):
    try:
        ip = ipaddress.ip_address(ipaddr)
        # print('%s is a correct IP%s address.' % (ip, ip.version))
        return True
    except ValueError:
        # print('address/netmask is invalid: %s' % ipaddr)
        return False
    except:
        # print('Usage : %s  ip' % ipaddr)
        return False


def generateAllowListFile(iplist):
    try:
        with open(config.allowlistoutfile, "w") as outfile:
            for ip in iplist:
                outfile.write('allow ' + ip + ";\n")
        return True
    except IOError:
        print ('oops! can\'t write allow list file')
        return False


def reloadNginxService():
    p =  subprocess.Popen(["systemctl", "reload",  "nginx"], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    if p.returncode == 0:
        return True
    else:
        return False


