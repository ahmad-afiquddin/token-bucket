# token-bucket
An example of a python based token bucket rate limiter currently set with refresh-rate of 100 tokens/hour. When a user makes a first request,
the current time stamp is obtained, and any other requests made within an hour after the time stamp is allowed until 100 requests are 
made. If within the same hour, more than 100 requests are made, excess requests are rejected with error 429. 

After an hour has passed from the time stamp, if a request is made, the time stamp is update with current time, and the bucket is refilled 
with 100 tokens.

Files:

- settings.json contains settings for the rate limiter, tokens field specifies how many spaces are available in the bucket, and the time field specifies the time each request is alive for
- tokenbucket.py is the main program that contains the necessary classes
- tests.py is the test program that verifies the functionality of the rate limiter

tokenbucket.py: Contains 3 classes, Error429, User, and Server
- Error429 is for easy string returns. Call str(Error429(time until refresh))
- User contains the api key for the user, token bucket, and time stamp. Also contains a function for making requests, returns success if its successful, or error otherwise
- Server contains an {api key:User} dictionary that stores the User class for each api key, and handles requests from users. Initialize server with server = Server(), and initialize users for the server with server.user_init(api key). Users make request on the server with server.req_made(api key).

tests.py: After initializing 2 users with api keys user001 and user002, 6 test cases are run

1: Making a request on both users. Expecting success for both
2: Making 98 requests on both users. Expceting success for all requests.
3: Making the 100th request in the same hour. Expecting success.
4: Making a request after limit is reached. Expecting Error 429
5: Wait for time limit then make a new request. Expecting success since bucket has been refilled
6: Making another request. Expecting success since the bucket has been refilled with 100 tokens

Tests shows that there are no overlaps between users, and token bucket is successful
