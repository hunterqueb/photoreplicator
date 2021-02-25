import threading 
import time

no_input = True
threads=[]

def add_up_time():
    print("adding up time...")
    timeTaken=float(0)
    while no_input:
        # print("here")
        time.sleep(0.01)
        timeTaken=timeTaken+0.01
    print(timeTaken)


# designed to be called as a thread
def signal_user_input():
    global no_input
    print("hit enter to stop things")
    i = input()   # I have python 2.7, not 3.x
    no_input = False
    # thread exits here


# we're just going to wait for user input while adding up time once...
t = threading.Thread(target=signal_user_input)
t.start()

print("adding up time...")
timeTaken = float(0)
while no_input:
    time.sleep(0.01)
    timeTaken = timeTaken+0.01
print(timeTaken)

# add_up_time()

print("done.... we could set no_input back to True and loop back to the previous comment...")
