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

        self.username = username
        api = self.api
        api.USER_AGENT = 'Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM lSW; armani; qcom; en_US)'
        api.login()

    def get_userID(self, username):
        """
        :param username: nickname from instagram
        :return: its user ID
        """
        api = self.api

        api.searchUsername(username)
        result = api.LastJson

        return result['user']['pk']

    def get_profile_details(self, usernameID=1, savefile=''):
        """
        :param usernameID: ID, if ID == 1, return information about your profile :param savefile: path for file
        without its name. The name will be /profile_usernameID.csv, sep=\t :return: df with usernameID info such as
        nickname, full_name, profile_pic_url, follower_count, following_count and media_count
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
        :return: list of your followers
        """
        api = self.api

        api.searchUsername(username)
        r = api.LastJson
        return api.getTotalFollowers(r['user']['pk'])

    def get_followings(self, username):
        """
        :param username: nickname from instagram
        :return: list of your followings
        """
        api = self.api

        api.searchUsername(username)
        r = api.LastJson
        return api.getTotalFollowings(r['user']['pk'])

    def filtering(self, list_for_fliter, threshold=2000, by='followers'):
        """
        by = 'followers' or 'following'
        """
        api = self.api

        filtered = []
        if by == 'followers':
            for i in tqdm(list_for_fliter):
                api.searchUsername(i['username'])
                if api.LastJson['user']['follower_count'] < threshold:
                    filtered.append(i)
        elif by == 'following':
            for i in tqdm(list_for_fliter):
                api.searchUsername(i['username'])
                if api.LastJson['user']['following_count'] < threshold // 4:
                    filtered.append(i)
        return filtered

    def auto_sub(self, username, from_='followers', cnt=10, threshold_for_filtering=2000):
        """
        :param username: nickname from instagram
        :param from_: 'followers' or 'following'
        :param cnt: count of users to follow
        :return: list of usersID which you followed
        """
        from_ = from_.lower()
        assert isinstance(username, str), 'incorrect type of username'
        assert from_ in ['followers', 'following'], 'incorrect, choose from followers/ following'

        api = self.api
        my_username = self.username

        if from_ == 'followers':
            to_choose = self.get_followers(username)

        if from_ == 'following':
            to_choose = self.get_folowings(username)

        to_follow = np.random.choice(to_choose, cnt)
        to_follow_filtered = self.filtering(to_follow, by=from_, threshold=threshold_for_filtering)
        to_follow_filtered_id = [i['pk'] for i in to_follow_filtered]

        your_followers = self.get_followers(my_username)
        your_followers_id = [i['pk'] for i in your_followers]

        to_follow_final = list(set(to_follow_filtered_id) - set(your_followers_id))

        for user in tqdm(to_follow_final):
            api.follow(user)
            sleep(np.random.randint(35, 60))

        curr_date = str(datetime.datetime.now().date()).replace('-', '_')
        with open('followed_' + curr_date + '.pickle', 'wb') as f:
            pickle.dump(to_follow, f)

        return to_follow_filtered

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
            sleep(np.random.randint(5, 10))

        return 'Done!'

    def give_like(self, *userIDs, cnt_likes=5):
        """
        :param userIDs: users from instagram (their IDs, not nicknames)
        :param cnt_likes: count posts to like for each user
        :return: 'all likes are given out'
        """
        api = self.api
        for user in userIDs:
            api.getUserFeed(user)
            feed = api.LastJson['items']
            feedIDs = [i['pk'] for i in feed]
            random_feed = np.random.choice(feedIDs, cnt_likes)
            for feedID in tqdm(random_feed):
                api.like(int(feedID))
                sleep(np.random.randint(5, 15))

        return 'all likes are given out'
