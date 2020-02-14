<img src="https://camo.githubusercontent.com/9ac4a1f7f5ea0f573451b5ddc06e29c8aa113a85/68747470733a2f2f692e696d6775722e636f6d2f6948326a6468562e706e67" align="right">

# InstagramBot

A couple of functions which automize your work on instagram. You can follow/unfollow people, like or post etc. Collect information and statistic for your data analysis.


### Class InstaBot

functions

 - get_userID: return user id instead of you nickname
 - get_profile_details: return basic information about user with usernameID in pandas DataFrame. If usernameID == 1 it returns your profile.
 - get followers: return all who follow 'username'
 - get_followings: returns everyone 'username' follow
 - auto_sub: auto subscriber
 - auto_unsub: auto unsubscriber
 - give_like: likes random posts from the feed

 Delay in a loop functions has a random number from 15 to 45 seconds on each iteration

 # TODO
 - [ ] Think about extra functions
 - [x] Test current functionality
 - [ ] Make telegram bot and run it on the server
 - [x] Put this class into .py module
 - [ ] add stop list for each function to avoid some users
 - [ ] add check for username if there are several accounts, when you search with nickname
 - [ ] add filter for list of foloowers to avoid business  and spam accounts
 - [x] change delay to avoid blocks from Instagram api (set from 30 to 50)