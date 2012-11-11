class start():
    def __init__(self):
        print "Welcome to Mega Irc Client 5000"
    
    def live(self):
        while True:
            i = 0
            print i
            line = None
            line = input()
            if line == "exit":
                pass
            print line
            i += 1

s = start()
s.live()
