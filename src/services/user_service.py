import random
import string
from datetime import datetime

from fastapi import UploadFile
from dtos.auth.aurh_user_response import AuthUserResponse
from dtos.register.generated_pin_response import GeneratedPinResponse
from dtos.user.edit_user import EditUser
from dtos.user.user_profile import UserProfile
from dtos.user.user_profile_preview import UserProfilePreview
from dtos.user.user_builder import UserBuilder
from exceptions.conflict_exception import ConflictException
from models.user import User
from models.interest import Interest
from repositories.user_repository import user_repository
from exceptions.resource_not_found_exception import ResourceNotFoundException
from config.settings import logger, redis_conn, REGISTER_PIN_TTL, REGISTER_PIN_LENGHT
from external.firebase_service import firebase_service
from external.twitsnap_service import twitsnap_service

from dtos.user.user_stats import UserStats

from dtos.user.admin_get_all_users import GetUsers


class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.firebase_service = firebase_service
        self.twitsnap_service = twitsnap_service

    async def create_user(self, register_request: dict):
        logger.debug(f"Attempting to create user with data: {register_request}")
        user = User(**register_request).save()
        await self.update_user_interests(
            user.uid, register_request.get("interests", [])
        )
        logger.debug(f"User created with id: {user.uid}")
        res = (
            UserBuilder(user)
            .with_public_info()
            .with_private_info()
            .with_interests()
            .with_is_banned()
            .build()
        )
        return UserProfile(**res)

    async def get_user_by_email(self, email):
        logger.debug(f"Attempting to get user id by email: {email}")
        user = self.user_repository.find_user_by_email(email)
        if user is None:
            logger.debug(f"User not found with email: {email}")
            raise ResourceNotFoundException(
                detail=f"User not found with email: {email}"
            )
        logger.debug(f"Found user with email: {email} and id: {user.uid}")
        logger.debug(f"user is_banned status: {user.is_banned}")
        return AuthUserResponse(uid=user.uid, is_banned=user.is_banned)

    async def get_user_by_id(self, id, my_uid):
        user = await self._get_user_by_id(id)
        if user.is_banned:
            logger.debug(f"User with id: {id} is banned")
            raise ResourceNotFoundException(detail=f"User with id: {id} not found")

        my_user = await self._get_user_by_id(my_uid)

        user = (
            UserBuilder(user)
            .with_public_info()
            .with_is_followed_by_me(user.followers.is_connected(my_user))
            .build()
        )
        return UserProfile(**user)

    async def get_my_user(self, user_id):
        user = await self._get_user_by_id(user_id)

        res = (
            UserBuilder(user)
            .with_public_info()
            .with_private_info()
            .with_interests()
            .with_device_token()
            .build()
        )
        logger.debug(f"Found user with id: {user_id} - {res}")
        return UserProfile(**res)

    async def _get_user_by_id(self, id) -> User:
        user = self.user_repository.find_user_by_id(id)
        if user is None:
            logger.debug(f"User not found with id: {id}")
            raise ResourceNotFoundException(detail=f"User not found with id: {id}")
        return user

    async def exists_user_by_email(self, email):
        return self.user_repository.find_user_by_email(email) is not None

    async def edit_user_by_id(self, user_data: EditUser, photo: UploadFile, id: str):
        logger.debug(
            f"Attempting to change user data with id: {id}. New values: {user_data}"
        )
        user = await self._get_user_by_id(id)

        for attr, value in user_data.model_dump().items():
            if value is not None:
                if attr == "interests" or attr == "device_token":
                    continue
                setattr(user, attr, value)
        if user_data.interests:
            await self.update_user_interests(user.uid, user_data.interests)
        if user_data.device_token not in user.device_token:
            user.device_token.append(user_data.device_token)
            user.save()

        if photo:
            url = await self.firebase_service.upload_photo(photo, id)
            user.photo = url
        eddited_user = self.user_repository.save(user)
        user = (
            UserBuilder(eddited_user)
            .with_public_info()
            .with_private_info()
            .with_interests()
            .build()
        )
        return UserProfile(**user)

    async def get_users_by_username(self, username: str, offset: int = 0, limit: int = 1):
        users = self.user_repository.get_users_by_username(username, offset, limit)
        res = [
            UserProfilePreview(uid=user.uid, username=user.username, photo=user.photo)
            for user in users
        ]
        logger.debug(f"Found {len(users)} users with username {username}, list: {res}")
        return res

    async def confirm_user(self, user_id, pin):
        user = await self._get_user_by_id(user_id)

        if user.verified:
            logger.debug(f"User with id: {user_id} is already verified")
            raise ConflictException(
                detail=f"User with id: {user_id} is already verified"
            )

        pin_from_uid = redis_conn.get(user_id)

        if pin_from_uid is None:
            logger.debug(f"Pin {pin} is invalid or expired")
            raise ResourceNotFoundException(detail=f"Pin {pin} is invalid or expired")

        if pin_from_uid.decode() != pin:
            logger.debug(f"Pin {pin} is invalid for user with id: {user_id}")
            raise ResourceNotFoundException(detail=f"Pin {pin} is invalid")

        user.verified = True

        redis_conn.delete(user_id)

        self.user_repository.save(user)

        return user

    async def ban_or_unban_user(self, user_id):
        user = await self._get_user_by_id(user_id)
        if user.is_banned:
            user.is_banned = False
        else:
            user.is_banned = True
        self.user_repository.save(user)
        return

    async def get_user_by_id_admin(self, user_id):
        user: User = await self._get_user_by_id(user_id)
        return (
            UserBuilder(user)
            .with_public_info()
            .with_private_info()
            .with_is_banned()
            .with_interests()
            .with_device_token()
            .build()
        )

    async def get_all_users(self, offset: int, limit: int, is_banned: bool = None):
        users, total_users = self.user_repository.get_all_users(offset, limit, is_banned)
        logger.debug(f"total users: {total_users}")
        users = [
            UserProfile(
                **UserBuilder(user)
                .with_public_info()
                .with_private_info()
                .with_interests()
                .with_is_banned()
                .with_device_token()
                .build()
            )
            for user in users
        ]
        return GetUsers(total_users=total_users, users=users)

    async def generate_register_pin(self, user_id):
        user = await self._get_user_by_id(user_id)

        if user.verified:
            logger.debug(f"User with id: {user_id} is already verified")
            raise ConflictException(
                detail=f"User with id: {user_id} is already verified"
            )

        pin = self._generate_pin()
        redis_conn.setex(f"{user.uid}", REGISTER_PIN_TTL, pin)
        await self.twitsnap_service.send_register_pin_to_notification(
            user.email, user.username, pin
        )
        logger.debug(f"Pin generated for user with id: {user_id} - {pin}")
        return GeneratedPinResponse(pin_ttl=REGISTER_PIN_TTL)

    async def follow_user(self, my_uid, user_id):
        logger.debug(f"Attempting to follow user with id: {user_id}")
        if my_uid == user_id:
            logger.debug(f"User with id: {my_uid} can't follow itself")
            raise ConflictException(
                detail=f"User with id: {my_uid} can't follow itself"
            )

        user = await self._get_user_by_id(user_id)
        my_user = await self._get_user_by_id(my_uid)

        if my_user.following.is_connected(user):
            logger.debug(
                f"User with id: {my_uid} is already following user with id: {user_id}"
            )
            return

        my_user.following.connect(user)
        destination = user.device_token
        await self.twitsnap_service.send_new_follower_notification()
        logger.debug(
            f"User with id: {my_uid}- name:{my_user.username} is following user with id: {user_id}, name: {user.username}"
        )
        return

    async def unfollow_user(self, my_uid, user_id):
        if my_uid == user_id:
            logger.debug(f"User with id: {my_uid} can't follow itself")
            raise ConflictException(
                detail=f"User with id: {my_uid} can't follow itself"
            )

        user = await self._get_user_by_id(user_id)
        my_user = await self._get_user_by_id(my_uid)

        if not my_user.following.is_connected(user):
            logger.debug(
                f"User with id: {my_uid} is not following user with id: {user_id}"
            )
            return

        my_user.following.disconnect(user)
        return

    async def get_followers(self, my_uid, user_id, offset, limit):
        user = await self._get_user_by_id(user_id)
        my_user = await self._get_user_by_id(my_uid)

        await self._is_following_each_other(my_user, user)

        followers = self.user_repository.get_followers(user_id, offset, limit)
        logger.debug(f"Found {len(followers)} followers for user with id: {user_id}")
        res = UserBuilder(my_user).with_followers(followers).build()
        return UserProfile(**res)

    async def get_following(self, my_uid, user_id, offset, limit):
        user = await self._get_user_by_id(user_id)
        my_user = await self._get_user_by_id(my_uid)

        await self._is_following_each_other(my_user, user)

        following = self.user_repository.get_following(user_id, offset, limit)
        logger.debug(f"Found {len(following)} following for user with id: {user_id}")
        res = UserBuilder(my_user).with_following(following).build()
        return UserProfile(**res)

    async def get_my_followers(self, my_uid, offset, limit):
        my_user = await self._get_user_by_id(my_uid)
        followers = self.user_repository.get_followers(my_uid, offset, limit)
        logger.debug(f"Found {len(followers)} followers for user with id: {my_uid}")
        res = UserBuilder(my_user).with_followers(followers).build()
        return UserProfile(**res)

    async def get_my_following(self, my_uid, offset, limit):
        my_user = await self._get_user_by_id(my_uid)
        following = self.user_repository.get_following(my_uid, offset, limit)
        logger.debug(f"Found {len(following)} following for user with id: {my_uid}")
        res = UserBuilder(my_user).with_following(following).build()
        return UserProfile(**res)

    async def _is_following_each_other(self, my_user, user):
        # CA - users cannot see other users followers and following if they are
        # not following each other
        if not my_user.following.is_connected(user):
            logger.debug(
                f"my User with id: {my_user.uid} is not following user with id: {user.uid}"
            )
            raise ConflictException(
                detail=f"User with id: {my_user.uid} is not following user with id: {user.uid}"
            )
        logger.debug(
            f"User with id: {my_user.uid} is following user with id: {user.uid}"
        )
        if not my_user.followers.is_connected(user):
            logger.debug(
                f"my User with id: {my_user.uid} is not followed by user with id: {user.uid}"
            )
            raise ConflictException(
                detail=f"User with id: {my_user.uid} is not followed by user with id: {user.uid}"
            )
        logger.debug(
            f"User with id: {my_user.uid} is followed by user with id: {user.uid}"
        )

    async def update_user_interests(self, uid: str, interests: list[str]):
        logger.debug(f"Attempting to update user interests: {interests}")
        if interests is None:
            return
        user = await self._get_user_by_id(uid)

        for i in user.interests.all():
            user.interests.disconnect(i)

        for i in interests:
            interest = Interest.nodes.get_or_none(name=i.lower())
            if interest:
                user.interests.connect(interest)
            else:
                logger.warning(f"Interest '{i}' not found and could not be connected.")

    def delete_user_by_id(self, uid):
        self.user_repository.delete_user_by_id(uid)

    async def get_user_stats(self, uid: str, from_date: datetime):

        followers_gained, following_gained = await self.user_repository.get_user_stats(
            uid, from_date
        )
        return UserStats(
            followers_gained=followers_gained, following_gained=following_gained
        )

    async def get_metrics(self, metric_type: str):

        if not metric_type:
            return await self.get_all_metrics()

        if metric_type == "registration":
            return await self.get_register_metrics()

        if metric_type == "banned":
            return await self.get_banned_metrics()

        if metric_type == "country_distribution":
            return await self.get_country_metrics()

    async def get_register_metrics(self):
        email, google = await self.user_repository.get_register_metrics()
        return {
            "registration": {
                "total": email + google,
                "distribution": {
                    "email": email,
                    "fedetatedIdentity": {"google": google},
                },
            }
        }

    async def get_banned_metrics(self):
        banned_users = await self.user_repository.get_banned_metrics()
        return {"bannedUsers": {"total": banned_users}}

    async def get_country_metrics(self):
        country_distribution = await self.user_repository.get_country_metrics()
        return {"countryDistribution": country_distribution}

    async def get_all_metrics(self):
        return {
            **await self.get_register_metrics(),
            **await self.get_banned_metrics(),
            **await self.get_country_metrics(),
        }

    def _generate_pin(self):
        return "".join(random.choices(string.digits, k=REGISTER_PIN_LENGHT))


user_service = UserService(user_repository)
