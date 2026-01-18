# import time
# import threading

# print(time.gmtime())

# from datetime import datetime

# now = datetime.now()
# print(now.strftime("%Y-%m-%d %H:%M:%S"))

# def print_number():
#     for i in range(5):
#         print(i)
#         time.sleep(1)

# def print_letter():
#     for letter in 'abcde':
#         print(letter)
#         time.sleep(1)

# thread1 = threading.Thread(target=print_number)
# thread2 = threading.Thread(target=print_letter)

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

# print("Done")

import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
