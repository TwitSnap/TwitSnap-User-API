from models.user import User


class UserBuilder:
    def __init__(self, user : User):
        self.user = user
        self.data = {}

    def with_public_info(self):
        self.data['uid'] = self.user.uid
        self.data['username'] = self.user.username
        self.data['photo'] = self.user.photo
        self.data['description'] = self.user.description
        self.data['country'] = self.user.country
        self.data['amount_of_followers'] = len(self.user.followers)
        self.data['amount_of_following'] = len(self.user.following)
        return self
    
    def with_private_info(self):
        self.data['uid'] = self.user.uid
        self.data['phone'] = self.user.phone
        self.data['email'] = self.user.email
        self.data['verified'] = self.user.verified
        
        return self
    def with_is_banned(self):
        self.data['is_banned'] = self.user.is_banned
        return self
    
    def with_is_followed_by_me(self, is_followed_by_me: bool):
        self.data['is_followed_by_me'] = is_followed_by_me
        return self
    
    def profile_preview(self):
        self.data['uid'] = self.user.uid
        self.data['username'] = self.user.username
        self.data['photo'] = self.user.photo
        return self

    def with_folowers_and_following(self, followers, following):
        self.datap['uid']= self.user.uid    
        self.data['followers'] = []
        self.data['following'] = []
        self.data['amount_of_followers'] = len(followers)
        self.data['amount_of_following'] = len(following)
        for follower in followers:
            self.data['followers'].append(UserBuilder(follower).profile_preview()
                                          .is_followed_by_me(follower.followers.is_connected(self.user))
                                          .build())

        for follow in following:
            self.data['following'].append(UserBuilder(follow).profile_preview()
                                          .is_followed_by_me(follow.followers.is_connected(self.user))
                                          .build())
        return self
    
    def build(self):
        return self.data

