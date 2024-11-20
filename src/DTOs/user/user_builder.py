from models.user import User


class UserBuilder:
    def __init__(self, user: User):
        self.user = user
        self.data = {}

    def with_public_info(self):
        self.data["uid"] = self.user.uid
        self.data["username"] = self.user.username
        self.data["photo"] = self.user.photo
        self.data["description"] = self.user.description
        self.data["country"] = self.user.country
        self.data["amount_of_followers"] = len(self.user.followers)
        self.data["amount_of_following"] = len(self.user.following)
        return self

    def with_private_info(self):
        self.data["uid"] = self.user.uid
        self.data["phone"] = self.user.phone
        self.data["email"] = self.user.email
        self.data["verified"] = self.user.verified

        return self

    def with_uid(self):
        self.data["uid"] = self.user.uid
        return self

    def with_is_banned(self):
        self.data["is_banned"] = self.user.is_banned
        return self

    def with_is_followed_by_me(self, is_followed_by_me: bool):
        self.data["is_followed_by_me"] = is_followed_by_me
        return self

    def profile_preview(self):
        self.data["uid"] = self.user.uid
        self.data["username"] = self.user.username
        self.data["photo"] = self.user.photo
        return self

    def with_created_at(self):
        self.data["created_at"] = self.user.created_at
        return self

    def with_followers(self, followers):
        self.data["followers"] = []

        for follower in followers:
            if follower.uid == self.user.uid:
                user = (
                    UserBuilder(follower).profile_preview().with_description().build()
                )
            else:
                user = (
                    UserBuilder(follower)
                    .profile_preview()
                    .with_description()
                    .with_is_followed_by_me(follower.followers.is_connected(self.user))
                    .build()
                )
            self.data["followers"].append(user)

        return self

    def with_following(self, following):
        self.data["following"] = []

        for follow in following:
            if follow.uid == self.user.uid:
                user = UserBuilder(follow).profile_preview().with_description().build()
            else:
                user = (
                    UserBuilder(follow)
                    .profile_preview()
                    .with_description()
                    .with_is_followed_by_me(follow.followers.is_connected(self.user))
                    .build()
                )
            self.data["following"].append(user)

        return self

    def with_description(self):
        self.data["description"] = self.user.description
        return self

    def with_interests(self):
        self.data["interests"] = []
        if self.user.interests is not None:
            for interest in self.user.interests:
                self.data["interests"].append(interest)
        return self

    def build(self):
        return self.data
