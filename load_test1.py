__author__ = 'wehappyfew'
import time
from locust import HttpLocust, TaskSet, task

#  comment2
class UserBehavior(TaskSet):

	def on_start(self):
		#
		self.the_scenario()

	def the_scenario(self):
		# request 1
		self.client.get("/explore")
		time.sleep(5)

		# request 2
		self.client.get("/features")
		time.sleep(5)

		# etc
		self.client.get("/pricing")
		time.sleep(5)

		# etc
		self.client.get("/login")
		time.sleep(5)

		#
		self.client.get("help")

	# it is needed for the locustfile to work like this (only one time)
	@task(1)
	def index(self):
		return True

class WebsiteUser(HttpLocust):
	host     = 'https://github.com/'
	task_set = UserBehavior
	min_wait = 1000
	max_wait = 5000
