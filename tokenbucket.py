#Importing modules
#For reading json formats
import json
#For time tracking
import time

#Reading from settings file
with open ('settings.json', encoding='utf-8') as settings_file:
    settings = json.loads(settings_file.read())

#Global settings
#In case someone tries to delibirately mess up the settings file
try:
    req_tokens = int(settings["tokens"])
    req_time = int(settings["time"])
#Exits program in case settings format is incorrect
except:
    print("Please make sure that only integers are used in the settings file")
    exit()

#Class for Error
class Error429:
    def __init__(self, time_until):
	    self.time_until = time_until

    def __str__(self):
    	#String overloading
	    return ("Error 429! Rate limit exceeded. Try again in {} seconds".format(self.time_until))

class User():
	def __init__(self, api_key):
		#Storing api key, initializing token bucket to full, and setting time stamp to current time
		self.api_key = api_key
		self.tokens = req_tokens
		self.time_stamp = time.time()

	def make_req(self):
		if (self.tokens == req_tokens):
			#If token bucket is full, set time stamp to current time and reduce token by 1
			self.time_stamp = time.time()
			self.tokens -= 1
		elif ((time.time() - self.time_stamp) > req_time):
			#If time limit has passed since latest time stamp, refill token bucket, set new time stamp
			#and reduce token by 1
			self.time_stamp = time.time()
			self.tokens = req_tokens
			self.tokens -= 1
		elif ((time.time() - self.time_stamp) < req_time and self.tokens > 0):
			#If time limit has not passed and there are still tokens
			#reduce tokens by 1
			self.tokens -= 1
		elif ((time.time() - self.time_stamp) < req_time and self.tokens == 0):
			#If time limit hasnt passed and token bucket is empty
			return str(Error429(int(req_time - (time.time() - self.time_stamp))))
		
		#Return success message
		self.time_read = time.asctime(time.localtime())
		return "Successful request on " + self.time_read

#Class for server
class Server:
    #Initialize {api_key:User} dictionary
    def __init__(self):
        self.user_dict = {}

    def user_init(self, api_key):
        if (not self.user_dict.get(api_key)):
            self.user_dict.update({api_key:User(api_key)})
        else:
            return ("User with api key {} already exists".format(api_key))

    def req_made(self, api_key):
        return self.user_dict.get(api_key).make_req()

    def get_user(self, api_key):
        if (self.user_dict.get(api_key)):
            return self.user_dict.get(api_key)
        else:
            return ("User with api key {} does not exist".format(api_key))

