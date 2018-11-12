#Name: Jaime Nufio
#UCID: Jen25
#Class Section: 003
#Program Language and Version: Python 3.5
#Testing Environment:
#   OS: Fedora Workstation 28
#   IDE: Vim, TCPClient.py
#   Command lines: TCPClient.py takes one argument, an address of format "localhost:12000/filename.html"

#Reffrences:
#   These were the mains ones for TCP implementation, but I also did a fair bit of reading on HTTP
#   https://docs.python.org/3/library/socket.html
#   https://docs.python.org/3/howto/sockets.html

#Comments:
#  For the Web Browser Version, I set it that by default, "localhost:12000" was enough to get to filename.html; filename.html was the default landing page. Earlier, this was a simple "Bad Request" printout

#   If its a problem that the Wireshark trace don't match the screenshots (I had it on wlsp when I took the screenshots), I apologise, but it works. The headers on that wiretrace match what webrowsers (For example, the 'Connection: keep-alive\r\n' which does not show in my client implementation) would ask. Instead of fixing them I went off of the assumption you just wanted proof it works. 

# I also used urllib.parse. It's not an HTTP, but I feel it might be potentially problematic that I did. In my defense, its work done is minimal. HTTP is parsed with .split, and I assumed you care more that we did that the long way.
