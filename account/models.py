from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    Gender = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    username = models.CharField(
        null=True, blank=True, max_length=50, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=6, choices=Gender, null=True, blank=True, default=None)
    position = models.CharField(max_length=40, null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField("media/user_image", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'username', 'gender', 'position', 'bio']

    def __str__(self):
        return f'{self.username}'


# class Follower(models.Model):
#     name = models.ManyToManyField()

class FollowQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability."""

    def get_followers(self, user):
        followers = self.filter(following=user).order_by('-date_follow').all()
        total_followers_no = self.filter(following=user).all().count()
        follow = [{'total_followers_no': total_followers_no}]
        for follower in followers:
            follow.append(

                {'id': follower.pk,
                 'follower_id': follower.follower.id,
                 'follower_username': follower.follower.username,
                 'follow_date': follower.date_follow,
                 'follower_user_bio': follower.follower.bio,
                 'follower_user_fullname': follower.follower.first_name + ' ' + follower.follower.last_name,
                 #  "follower_user_firstname": follower.follower.first_name,
                 #  "follower_user_lastname": follower.follower.last_name

                 #  'follower_user_image': follower.follower.image
                 }
            )
        return follow

    def get_followings(self, user):
        followings = self.filter(follower=user).order_by('-date_follow').all()
        total_followers_no = self.filter(follower=user).all().count()
        follow = [{'total_followed_no': total_followers_no}]
        for following in followings:
            follow.append(
                {'id': following.pk,
                 'following_id': following.following.id,
                 'following_username': following.following.username,
                 'following_date': following.date_follow,
                 'following_user_bio': following.following.bio,
                 'following_user_fullname': following.following.first_name + " " + following.following.last_name
                 #  "following_user_firstname": following.following.first_name,
                 #  "following_user_lastname": following.following.last_name
                 #  'following_user_image': following.following.image
                 }
            )
        return follow

    def get_followers_list(self, user):
        followers = self.filter(following=user).order_by('-date_follow').all()
        return [follower.follower.pk for follower in followers]

    def get_followings_list(self, user):
        followings = self.filter(follower=user).order_by('-date_follow').all()
        return [following.following.pk for following in followings]


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_following')
    date_follow = models.DateTimeField(auto_now_add=True)
    objects = FollowQuerySet.as_manager()

    def __str__(self):
        return u'%s follows %s' % (self.follower, self.following)


class Likes(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_likes')
    poll = models.ForeignKey(
        "polls.Poll", on_delete=models.CASCADE, related_name='poll_likes')
    like_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-like_date',)
        unique_together = ('poll', 'user')


class Share(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # poll = models.CharField(max_length=255)
    poll = models.ForeignKey("polls.Poll", on_delete=models.CASCADE)
    share_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.poll.question

    class Meta:
        ordering = ('-share_date',)


class BookMark(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_bookmarks')
    poll = models.ForeignKey(
        "polls.Poll", on_delete=models.CASCADE, related_name='poll_bookmarks')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.poll.question

    class Meta:
        ordering = ('-created',)
        unique_together = ('poll', 'user')
