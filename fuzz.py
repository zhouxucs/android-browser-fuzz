import time
import subprocess
import os

host = '192.168.43.182'
port = 8888
def start_fuzzing():
    clear_logcat()
    tmpuri = 'fuzzyou?id=%d' % time.time()
    print "fuzz %s" % tmpuri

    ouput = subprocess.Popen(['adb', 'shell', 'am', 'start',
                            '-a', 'android.intent.action.VIEW',
                            '-d', 'http://%s:%d/%s' % (host, port, tmpuri),
                            '-e', 'com.android.browser.application_id', "wooo",
                            'com.android.browser'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

    print "wait for 30 seconds"
    time.sleep(30)

    print "check log"
    check_logcat(tmpuri)

def clear_logcat():
    subprocess.Popen(['adb', 'logcat', '-c']).wait()

def check_logcat(tmpuri):
    log = subprocess.Popen(['adb', 'logcat', '-d'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).communicate()[0]
    if log.find('SIGSEGV') != -1:
        crashfn = os.path.join('crashes', tmpuri)
        print " Crash!! save page/log to %s" % crashfn
        #with open(crashfn, "wb") as f:
        #    f.write(self.server.page)
        with open(crashfn + '.log', "wb") as f:
            f.write(log)
    else:
        crashfn = os.path.join('non-crashes', tmpuri)
        with open(crashfn + '.log', "wb") as f:
            f.write(log)

class Fuzzer():
    def __init__(self):
        self.keep_going = True

    def run(self):
        while self.keep_going:
            start_fuzzing()

if __name__ == "__main__":
    fuzzer = Fuzzer()
    fuzzer.run()
