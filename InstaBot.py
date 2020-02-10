import pandas as pd
import numpy as np

from time import sleep
from tqdm import tqdm
import datetime
import pickle

from InstagramAPI import InstagramAPI


class InstaBot:
    def __init__(self, username, password):
        self.api = InstagramAPI(username, password)

        api = self.api
        api.USER_AGENT = 'Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM lSW; armani; qcom; en_US)'
        api.login()

    def get_profile_details(self, usernameID=1, savefile=''):
        """
        :param usernameID: ID, if ID == 1, return information about your profile
        :param savefile: path for file without its name. The name will be /profile_usernameID.csv, sep=\t
        :return: df with usernameID info such as nickname, full_name, profile_pic_url, follower_count, following_count and media_count
        """
        api = self.api

        api.login()
        assert isinstance(usernameID, int), 'incorrect type of userID'
        assert isinstance(savefile, str), 'incorrect type of savefile'

        if usernameID == 1:
            api.getSelfUsernameInfo()
        else:
            api.getUsernameInfo(usernameID)

        result = api.LastJson
        username = result['user']['username']
        full_name = result['user']['full_name']
        profile_pic_url = result['user']['profile_pic_url']
        followers = result['user']['follower_count']
        following = result['user']['following_count']
        media_count = result['user']['media_count']
        df_profile = pd.DataFrame(
            {'username': username,
             'full name': full_name,
             'profile picture URL': profile_pic_url,
             'followers': followers,
             'following': following,
             'media count': media_count,
             }, index=[0])
        if savefile == '':
            return df_profile
        else:
            df_profile.to_csv(savefile + '/profile_' + str(usernameID) + '.csv', sep='\t', encoding='utf-8')
            return df_profile

    def get_followers(self, username):
        """
        :param username: nickname from instagram
        :return: list of users who follow you
        """
        api = self.api

        api.login()
        api.searchUsername(username)
        r = api.LastJson
        return api.getTotalFollowers(r['user']['pk'])

    def get_followings(self, username):
        """
        :param username: nickname from instagram
        :return: list of users who you follow
        """
        api = self.api

        api.login()
        api.searchUsername(username)
        r = api.LastJson
        return api.getTotalFollowings(r['user']['pk'])

    def auto_sub(self, your_followers, cnt=10):
        """
        :param your_followers: list of your followers
        :param cnt: count of users to follow
        :return: list of usersID which you followed
        """
        assert len(your_followers) >= 1, 'users not found'

        user = np.random.choice(your_followers, 1)[0]
        his_followers = api.getTotalFollowers(user['pk'])

        to_follow = [i['pk'] for i in np.random.choice(his_followers, cnt)]
        your_followers_id = [i['pk'] for i in your_followers]
        to_follow = list(set(to_follow) - set(your_followers_id))

        for user in tqdm(to_follow):
            api.follow(user)
            sleep(np.random.randint(15, 45))

        curr_date = str(datetime.datetime.now().date()).replace('-', '_')
        with open('followed_' + curr_date + '.pickle', 'wb') as f:
            pickle.dump(to_follow, f)

        return to_follow

    def auto_unsab(self, username, follower_PATH):
        """
        :param username:  nickname from instagram
        :param follower_PATH: PATH to file with subscribers for check
        :return: 'Done!'
        """
        api = self.api

        api.login()
        current_followers = self.get_followers(username)
        current_followers_id = [i['pk'] for i in current_followers]

        with open(follower_PATH, 'rb') as f:
            followers_for_check = pickle.load(f)

        to_unsab = list(set(followers_for_check) - set(current_followers_id))

        for user in tqdm(to_unsab):
            api.unfollow(user)
            sleep(np.random.randint(15, 45))

        return 'Done!'

    def give_like(self, *userIDs, cnt_likes=5):
        """
        :param userIDs: users from instagram (their IDs, not nicknames)
        :param cnt_likes: count posts to like for each user
        :return: 'all likes are given out'
        """
        api = self.api
        for user in tqdm(userIDs):
            api.getUserFeed(user)
            feed = api.LastJson['items']
            feedIDs = [i['pk'] for i in feed]
            random_feed = np.random.choice(feedIDs, cnt_likes)
            for feedID in random_feed:
                api.like(int(feedID))
                sleep(np.random.randint(15, 45))

        return 'all likes are given out'