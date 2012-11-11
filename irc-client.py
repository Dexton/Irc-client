from sys import exit

class start():
    def __init__(self):
        print "Welcome to Mega Irc Client 5000"
        host = raw_input("\nType host name: ")
    
    def live(self):
        while True:
            line = raw_input()
            if line == "exit":
                break 
            print line

    def die(self):
        exit()

s = start()
s.live()
