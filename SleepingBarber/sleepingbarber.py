# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time, queue, random
from threading import Thread,Lock

class Barber(Thread):								# thread class invokes the run() method in a separate thread of control.	
	def __init__(self, barber, chairs):				# barbers(one-by-one) and number of chairs.
		Thread.__init__(self)						# Because the *args and **kwargs values passed to the Thread constructor are saved in private variables, they are not easily accessed from a subclass. To pass arguments to a custom thread type, we need to redefine the constructor to save the values in an instance attribute that can be seen in the subclass.
		self.barber = barber
		self.chairs = chairs						# queue of people with the max size of how many chairs there are.
		self.asleep = True  						# barber is sleeping.

	def run(self):									# in this section, we will create a subclass of Thread and override run() for customers to go to the barber and get their haircut.
		while True: 								# if customer in waiting room.
			self.asleep = False						# barber wakes up.	
			customer = self.chairs.get()			# dequeueing customer because customer is going for haircut so he is not sitting on a chair anymore.
			print("> Customer {} goes to Barber {}".format(customer, self.barber))
			Customer.chair = True  					# customer is in barber chair.
			time.sleep(random.randrange(3,8))		# random haircutting time.
			print("\nBarber {}: Finished with Customer {}, next!\n".format(self.barber,customer))
			if self.chairs.empty():					# if the queue is empty.
				print("No more customers")
				print("Barber {} is sleeping\U0001F634\U0001F634\U0001F634\n".format(self.barber)) # printing string with unicode for emoji's.

class Customer(Thread):								# thread class invokes the run() method in a separate thread of control.

	def __init__(self, customer, chairs):			# customers(one-by-one) and the number of chairs.
		Thread.__init__(self)						# Because the *args and **kwargs values passed to the Thread constructor are saved in private variables, they are not easily accessed from a subclass. To pass arguments to a custom thread type, we need to redefine the constructor to save the values in an instance attribute that can be seen in the subclass.
		self.customer = customer
		self.chairs = chairs 						# queue of people with the max size of how many chairs there are.
		self.busy = False  							# is barber busy?
		self.lock = Lock()							# used to prevent race condition.

	def wait(self):
		time.sleep(random.randrange(3,6))			# random wait time 3-6secs.

	def run(self):									# in this section, we will create a subclass of Thread and override run() for customers to be enqueued if the queue is not full.
		with self.lock:								# using lock to handle data race(race condition).
			if not self.chairs.full():  			# if waiting room isn't full
				time.sleep(random.randrange(2,7))	# random time for customers to walk in 2-7secs.
				self.chairs.put(self.customer) 		# add customer into waiting room.
				print(">>> Customer {} walks into shop" .format(self.customer))
			else:
				print ("No more chairs, customer {} will come back later".format(self.customer))

def listof(num):									# function to turn a number into a list counting up to a given number.
	a = []											# initializing list.
	for i in range(1, int(num) + 1):				# getting numbers from 1 to the number.
		a.append(i)									# appending the number.
	return a										# return the list.

def main():
	barbers = listof(3)								# 3 barbers.
	customers = listof(30)							# 30 customers will be coming in.
	chairs = queue.Queue(15)						# queue with max size of 15 which are the chairs.
	customer_threads = []							# initializing a list for customer threads.
	barber_threads = []								# initializing a list for barber threads.

#-----------------Creating Threads-----------------#

	for customer in customers:						# for every customer in the list customers,
		t1 = Customer(customer, chairs)				# creating t1 thread for every customer there is (in this case 20).
		customer_threads.append(t1)					# appending the threads to customer_threads list.
		t1.setDaemon = True							# By setting them as daemon threads, we can let them run and forget about them, and when our program quits, any daemon threads are killed automatically.

	for barber in barbers:							# for every barber in the list barbers.
		t2 = Barber(barber, chairs)					# creating t2 thread for every barber there is (in this case 3).
		barber_threads.append(t2)					# appending the threads to barber_threads list.
		t2.setDaemon = True							# By setting them as daemon threads, we can let them run and forget about them, and when our program quits, any daemon threads are killed automatically.

#-----------------Starting Threads-----------------#

	for thread in barber_threads:					# for every thread in barber_threads,
		thread.start()								# start thread.
	for thread in customer_threads:					# for every thread in customer_threads,
		thread.start()								# start thread.

#-----------------Joining Threads-----------------#

	for thread in barber_threads:					# for every thread in barber_thread,
		thread.join()								# join thread.
	for thread in customer_threads:					# for every thread in customer_threads,
		thread.join()								# join thread.

if __name__ == '__main__':
	main()