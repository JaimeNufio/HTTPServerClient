#Name: Jaime Nufio
#UCID: Jen25
#Class Section: 003

#SERVER
#I used urllib.parse, hope thats ok?
import sys, re, os.path, time
from urllib.parse import urlparse
from socket import *

arg1 = sys.argv[1]

#Protocol is HTTP
parse= urlparse("http://"+arg1)
ip = gethostbyname("localhost")
filename = parse.path;
port = parse.port;
#print(parse.netloc);
#print(parse.port);
#print(parse.path);

CLIENT = socket(AF_INET,SOCK_STREAM);
CLIENT.connect((ip,parse.port));

#Start to Build Request
REQUEST=""

#States
Cached = False;
Cont = False;
RequestType = 0;

#Is the File Cached?
#Conditional Fetch of File; Already Cachem
if (os.path.isfile(filename[1:])):
    Cached = True;
    REQUEST+="GET "+filename+" HTTP/1.1\r\n";
    REQUEST+="HOST: "+ip+":"+str(port)+"\r\n";
    REQUEST+="If-Modified-Since: "+time.strftime(time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", time.gmtime(os.path.getmtime(filename[1:]))))+"\r\n\r\n";

#Fetch File; Not Cached
else:
    Cached = False;
    #HTTP Client GET Request Message
    REQUEST+="GET "+filename+" HTTP/1.1\r\n";
    REQUEST+="HOST: "+ip+":"+str(port)+"\r\n\r\n";

#print("Cached? "+str(Cached));

CLIENT.send(REQUEST.encode());

#Get Request, Print, Break Into Fields
DATA=CLIENT.recv(1024*4);
DATA=DATA.decode()
print("-----------------------------------------------");
print(repr(DATA));
print("-----------------------------------------------");
fields = DATA.split("\r\n")

    
if "404" in fields[0]:
    CLIENT.close();
    cont = False;
#    print("Not found");
if "200" in fields[0]:
    f = open(filename[1:],"w+")
    f.write(fields[-1]);
    f.close()
 #   print("Cached File "+filename+".");
if Cached and "304" in fields[0]:
 #   print("Have most up to date version already.");
    pass;
CLIENT.close()


