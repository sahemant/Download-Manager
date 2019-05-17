import urllib2
import urllib
import os
import threading
import time
totalBytes=0
globalStartTime=None
lock=threading.Lock()
def addBytes(byte):
    #print 'adding'
    global lock
    global totalBytes
    lock.acquire()
    totalBytes+=byte
    #print totalBytes
    lock.release()

class HTTPRangeHandler(urllib2.BaseHandler):
    def http_error_206(self, req, fp, code, msg, hdrs):
        # Range header supported
        r = urllib.addinfourl(fp, hdrs, req.get_full_url())
        r.code = code
        r.msg = msg
        return r

    def http_error_416(self, req, fp, code, msg, hdrs):
        # Range header not supported
        raise urllib2.URLError('Requested Range Not Satisfiable')



class download(threading.Thread):
    def __init__(self,filename,url,x,y):
        threading.Thread.__init__(self)
        self.filename=filename
        self.url=url
        self.x=x
        self.y=y
    def run(self):
        startDownload(self.filename,self.url,self.x,self.y)

def startDownload(filename,url,x,y):
    CHUNK=None
    res=None
    try:
        #print 'thread started'
        req = urllib2.Request(url)
        rangee='bytes='+str(x)+'-'+str(y)
        req.add_header('Range', rangee)
        res = urllib2.urlopen(req)
        CHUNK = 16*1024
    except:
        print 'here is exception'
        print Exception.message
        return
    with open(filename, 'wb') as f:
        if True:
            startTime = time.time()
            bytesRead = 0
            global globalStartTime
            global lock
            lock.acquire()
            if globalStartTime == None:
                globalStartTime = time.time()
            lock.release()
            while True:
                chunk = res.read(CHUNK)
                #print type(chunk)
                #print chunk
                #print len(chunk)
                bytesRead += len(chunk)
                if not chunk:
                    break
                try:
                    f.write(chunk)
                except:
                    print 'here is error'
                    return
                nowTime = time.time()
                diff = nowTime - startTime
                if diff > 1:
                    addBytes(bytesRead)
                    startTime = time.time()
                    bytesRead = 0
    #print 'thread ended'

def isAnyLive(threads):
    for t in threads:
        if t.isAlive():
            return True
    return False

def main(url):
    count = 0
    opener = urllib2.build_opener(HTTPRangeHandler)
    urllib2.install_opener(opener)
    maxlength = urllib2.urlopen(url).info().dict['content-length']
    print maxlength
    segmentLength = int(maxlength)/100
    startLength = 0
    threads=[]
    for i in range(100):
        filename = 'filepart'+str(i)
        endLength = startLength+segmentLength
        if endLength > maxlength:
            endLength = maxlength
        try:
            t=download(filename,url,startLength,endLength)
            t.start()
            threads.append(t)   #thread.start_new_thread(startDownload, (filename, url, startLength, endLength))
            count+=1
        except:
            pass
        if endLength==maxlength:
            break
        startLength = endLength + 1
    #print 'all threads started'
    #print 'COUNT IS:::: '+str(count)
    while isAnyLive(threads):
        time.sleep(2)
        global totalBytes
        #print totalBytes
        if totalBytes == None or globalStartTime == None:
            continue
        avgBytesPerSecond = totalBytes/(time.time() - globalStartTime)
            
        print 'Avg Download Speed: '+str(avgBytesPerSecond/1024)+' KB/s'
    print 'Total Time Elapsed: '+str((time.time() - globalStartTime)/60.0) +' Mins'

def combineFiles(filename):
    finalFile = open("C:\\Downloads\\"+filename,"ab")
    for i in range(100):
        try:
            filename='filepart'+str(i)
            f=open(filename,'rb')
            finalFile.write(f.read())
            f.close()
            os.remove(filename)
        except:
            pass
    finalFile.close()


import sys
if len(sys.argv)==1:
    print 'No download url passed'
else:
    url = sys.argv[1]
    filename=url.split('/')[-1]
    main(url)
    combineFiles(filename)


