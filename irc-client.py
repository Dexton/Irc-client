from sys import exit
import socket, threading, datetime

class start():
    #Members
    sock = None
    host = "irc.freenode.net"
    port = 6667
    nick = "Banzaii"
    identity = "Brans"
    realname = "Grettir"
    #Initiate a connection
    def __init__(self):
        print "Welcome to Mega Irc Client 5000"
        self.connect()
        self.ident()
        self.live()

    #Keep the connection alive
    def live(self):
        while True:
            msg = ""
            while True:
                part = self.sock.recv(4096)
                msg += part
                if part.endswith("\r\n"):
                    break
            print msg
            self.log("server", msg)
            command = raw_input()
            if command == "exit":
                self.die()
    #Quit
    def die(self):
        self.sock.send("QUIT \r\n")
        command = "Closing connection to %s" % self.host
        print command
        self.log("client", command)
        msg = self.sock.recv(1024)
        print msg
        self.log("server", msg)
        exit()

    #Messages
    def ident(self):
        msg = self.sock.recv(1024)
        print msg
        self.log("server", msg)
        command = "NICK %s\r\n" % self.nick 
        self.sock.send(command)
        print command
        self.log("client", command)
        msg = self.sock.recv(1024)
        print msg
        self.log("server", msg)
        command = "USER %s %s bla :%s\r\n" % (self.identity,self.host, self.realname)
        self.sock.send(command)
        print command
        self.log("server", command)

    def connect(self):
        self.host = raw_input("\nType host name: ")
        self.sock = socket.socket()
        command = "Connecting to %s" % self.host
        print command
        self.log("client", command)
        try:
            self.sock.connect((self.host,self.port))
        except:
            command = "Failed to connect to %s" % self.host
            print command
            self.log("client", command)
            exit()
    #Logging
    def log(self,source,msg):
        f = open("irc.log", "a+")
        s = str(datetime.datetime.now()) + " : " + source + " : " + msg
        f.write(s)
        f.close()

s = start()
