#!/usr/bin/python

"""

HTTP Proxy (v1)
Purpose: For deployment in Mininet as part of PhD SDN research

Author: Dennis Ong
                                
"""

import sys,thread,socket
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = True            # set to True to see the debug msgs

#********** Global Class ********
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


#**************************************
#********* MAIN PROGRAM ***************
#**************************************
def main():

    # check the length of command running
    if (len(sys.argv)<2):
        print "usage: proxy <port>"  
        return sys.stdout    

    # host and port info.
    host = ''               # blank for localhost
    port = int(sys.argv[1]) # port from argument
    
    try:
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # associate the socket to host and port
        s.bind((host, port))

        # listenning
        s.listen(BACKLOG)

    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message
        sys.exit(1)

    # get the connection from client
    while 1:
        print "Proxy running..."
        conn, client_addr = s.accept()

        # create a thread to handle request
        thread.start_new_thread(proxy_thread, (conn, client_addr))

    s.close()
#************** END MAIN PROGRAM ***************


#*******************************************
#********* PROXY_THREAD FUNC ***************
# A thread to handle request from browser
#*******************************************
def proxy_thread(conn, client_addr):
    print "received something..."

    # get the request from browser
    request_text = conn.recv(MAX_DATA_RECV)
    print request_text

    request = HTTPRequest(request_text)

    if not request:
        sys.exit(1)
    
    if request.error_code:
        sys.exit(1)


    host = request.headers['host']

    port_pos = host.find(":")           # find the port pos (if any)
    if (port_pos==-1):      # default port
        port = 80
        webserver = host
    else:       # specific port
        webserver = host.split(":")[0]
        port = host.split(":")[1]

    print "Connect to: %s:%i" % (webserver, port)

    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.connect((webserver, port))
        s.send(request_text)         # send request to webserver

        while 1:
            # receive data from web server
            data = s.recv(MAX_DATA_RECV)
            
            if (len(data) > 0):
                # send to browser
                conn.send(data)
            else:
                break
        s.close()
        conn.close()
    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        print "Runtime Error:", message
        sys.exit(1)
#********** END PROXY_THREAD ***********

# Initial code from http://luugiathuy.com/2011/03/simple-web-proxy-python/

# def proxy_thread(conn, client_addr):

#     # get the request from browser
#     request = conn.recv(MAX_DATA_RECV)

#     # parse the first line
#     first_line = request.split('\n')[0]

#     # get url
#     url = first_line.split(' ')[1]

#     if (DEBUG):
#         print first_line
#         print
#         print "URL:",url
#         print
    
#     # find the webserver and port
#     http_pos = url.find("://")          # find pos of ://
#     if (http_pos==-1):
#         temp = url
#     else:
#         temp = url[(http_pos+3):]       # get the rest of url
    
#     port_pos = temp.find(":")           # find the port pos (if any)

#     # find end of web server
#     webserver_pos = temp.find("/")
#     if webserver_pos == -1:
#         webserver_pos = len(temp)

#     webserver = ""
#     port = -1
#     if (port_pos==-1 or webserver_pos < port_pos):      # default port
#         port = 80
#         webserver = temp[:webserver_pos]
#     else:       # specific port
#         port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
#         webserver = temp[:port_pos]

#     print "Connect to:", webserver, port

#     try:
#         # create a socket to connect to the web server
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
#         s.connect((webserver, port))
#         s.send(request)         # send request to webserver

#         while 1:
#             # receive data from web server
#             data = s.recv(MAX_DATA_RECV)
            
#             if (len(data) > 0):
#                 # send to browser
#                 conn.send(data)
#             else:
#                 break
#         s.close()
#         conn.close()
#     except socket.error, (value, message):
#         if s:
#             s.close()
#         if conn:
#             conn.close()
#         print "Runtime Error:", message
#         sys.exit(1)

    
if __name__ == '__main__':
    main()
