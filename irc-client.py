from sys import exit
import socket, threading, datetime, select, sys
import os

class start():
    #Members
    sock = None
    host = "irc.freenode.net"
    port = 6667
    nick = "Banzaii"
    identity = "Brans"
    realname = "Grettir"
    channel = None

    #Initiate a connection
    def __init__(self):
        print "Welcome to Mega Irc Client 5000"
        self.connect()
        self.ident()
        print "**** Press ENTER to write commands ****"
        self.live()

    #Keep the connection alive
    def live(self):
        i = 0
        while True:
            #Check for input in the pipes
            r,w,e = select.select([sys.stdin, self.sock],[],[],1)
            for c in r:
                if isinstance(c, socket.socket):
                    #Deal with in coming data in socket
                    msg = self.sock.recv(4096)
                    self.log("server", msg)
                    if "PING :" in msg:
                        self.pong()
                    elif " PRIVMSG " in msg:
                        #Chop up and format private messages
                        pieces = msg.splitlines()
                        for p in pieces:
                            #ChopChop
                            tub = p.partition(':')
                            rest = tub[2]
                            tub = rest.partition('!')
                            sender = tub[0]
                            rest = tub[2]
                            tub = rest.partition(' ')
                            rest = tub[2]
                            tub = rest.partition(' ')
                            rest = tub[2]
                            tub = rest.partition(' :')
                            recvr = tub[0]
                            text = tub[2]
                            #Slap it back together
                            print '{' + sender + '}' + '@' + recvr + ': ' + text
                    else:
                        #Print messages from server to the user
                        print msg


                else:
                    #Handle data from stdin
                    print "Enter command with / or say something in channel"
                    raw_input()
                    command = raw_input()
                    if command.startswith('/'):
                        #Handle as if a command from user
                        if "/exit" in command:
                            print command
                            self.die()
                        elif "/join" in command:
                            print command
                            self.joinChannel(command[6:])
                        elif "/part" in command:
                            print command
                            self.leaveChannel()
                        else:
                            print "No such command available"
                    elif self.channel:
                        #Handle as message to channel
                        self.say(command)
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
        #Identify self to server
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
        #Establis a connection to server
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

    def changeNick(self, newnick):
        self.nick = newnick
        command = "NICK %s\r\n" % self.nick 
        self.sock.send(command)
        print command 
        self.log("client", command)

    def pong(self):
        msg = "PONG : Pong\r\n"
        self.sock.send(msg)
        print msg
        self.log("client", msg)

    def joinChannel(self, channelName):
        command = "JOIN " + channelName + "\r\n"
        self.sock.send(command)
        print command
        self.log("client", command)
        self.channel = channelName

    def leaveChannel(self):
        command = "PART %s\r\n" % self.channel
        self.sock.send(command)
        print command
        self.log("client", command)
        self.channel = None

    def say(self, message, receiver=None):
        if not receiver:
            receiver = self.channel
        command = "PRIVMSG " + receiver + " : " + message + "\r\n"
        self.sock.send(command)
        print "@" + receiver + "[" + self.nick + "]" + " : " + message 
        self.log("client", command)


    #Logging
    def log(self,source,msg):
        #Handle the logging needed
        f = open("irc.log", "a+")
        s = str(datetime.datetime.now()) + " : " + source + " : " + msg
        f.write(s)
        f.close()

if "posix" in os.name:
    s = start()
else:
    print "This client only works on linux"
    exit()
