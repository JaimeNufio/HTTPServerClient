#Name: Jaime Nufio
#UCID: Jen25
#Class Section: 003

#SERVER
import sys, time, datetime, os.path, re
from socket import *
from datetime import timezone
argv = sys.argv
#port hardcoded to 12000,should be 80 for native web 

SERVER = socket(AF_INET, SOCK_STREAM);
SERVER.bind(("127.0.0.1",12000));
SERVER.listen(1);
print("Server Started on port 12000");

while True:
    filename=""
    HTTPREPLY="";
    
    Error=False;
    cont = False;
    Conditional = False;

    CONNECT,address = SERVER.accept();
    #Read Request
    HTTPREQ = CONNECT.recv(2048).decode();
    print("INCOMING REQUEST:\n"+HTTPREQ); 

    #Handle Request
    filename = "";
    date = time.strftime("%a, %d %b %Y %H:%M:%S GMT");
    ParseForFileName = re.search("GET /(.+?) HTTP", HTTPREQ);
    if ParseForFileName:
        filename = ParseForFileName.group(1) 
        if (os.path.isfile(filename)):
            cont = True;
        else:
            Error = True;   
            #print("Couldn't find "+filename);
    else:
        filename = "./filename.html"
        cont = True; 

    timeCheck = "";
    fields = HTTPREQ.split("\r\n");
    for field in fields:
        if "If-Modified-Since:" in field:
            Conditional = True
            fieldParse = re.search(": (.*?)$",field);
            timeCheck = fieldParse.group(1);
            t = time.strptime(timeCheck, "%a, %d %b %Y %H:%M:%S %Z");
            timeCheck = time.mktime(t); 
 
    if (cont and not Error):
       # t = datetime.datetime.now(timezone.utc) 
        lastmodtime =time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime(filename)))
        with open(filename) as f:
            htmlpage = f.read()
        #HTTP Server Response to Client GET Request (assuming file exists)
        HTTPREPLY+="HTTP/1.1. 200 OK\r\n"
        HTTPREPLY+="Date: "+date+"\r\n"
        HTTPREPLY+="Last-Modified: "+lastmodtime+"\r\n"
        HTTPREPLY+="Content-Length: "+str(len(htmlpage))+"\r\n"
        HTTPREPLY+="Content-Type: text/html; charset=UTF-8\r\n"
        HTTPREPLY+="Encoding: gzip, deflate, br\r\n"
        HTTPREPLY+="Language: en-US,en;q=0.9\r\n"
        HTTPREPLY+="\r\n"
        HTTPREPLY+=htmlpage
        print("wrote reply");
        if (not Conditional):
            #Reply to Request
            print("Sending back: \n"+HTTPREPLY);
            CONNECT.send(HTTPREPLY.encode());
            CONNECT.close()
        else:
            #Conditional Response.
            #print("SERVERSIDELASTMODIFIED: "+lastmodtime);
            l = time.strptime(lastmodtime, "%a, %d %b %Y %H:%M:%S %Z");
            l = time.mktime(l);
            #print("EPOCHSECONDSSERVERSIDE: ",l);
            #print("REQUESTEPOCHSECONDS: ",timeCheck);
            if (l>timeCheck):
                CONNECT.send(HTTPREPLY.encode());
                CONNECT.close()
                #print("Modified, lets resend");
            else: 
                HTTPREPLY="HTTP/1.1 304 Not Modified\r\n";
                HTTPREPLY+="Date: "+date+"\r\n\r\n";
                CONNECT.send(HTTPREPLY.encode());
                CONNECT.close()
    elif(Error):
            HTTPREPLY="HTTP/1.1 404 Not Found\r\n";
            HTTPREPLY+="Date: "+date+"\r\n\r\n";
            CONNECT.send(HTTPREPLY.encode());
            CONNECT.close()

SERVER.close()
