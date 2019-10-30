from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
# Messageクラス
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_owner')
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    sum = models.IntegerField(default=0)
    TYPE_CHOICES = (
        (0, '----'),
        (1, '飲み物'),
        (2, '食べ物'),
        (3, 'その他'),
    )
    type = models.IntegerField(verbose_name='種類', choices=TYPE_CHOICES, default=1)
    pub_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(verbose_name='値段', default=0)

    def __str__(self):
        return str(self.content) + ' (' + str(self.owner) + ')'

    class Meta:
        ordering = ('-pub_date',)


# Groupクラス
class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_owner')
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True, default=1)
    deadline = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# Friendクラス
class Friend(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_owner')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' (group:"' + str(self.group) + '")'


# Goodクラス
class Good(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_owner')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    whose = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_whose')
    count = models.IntegerField(default=1)
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return 'good for "' + str(self.message) + '" (by' + str(self.owner) + ')'


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='choice_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='choice_group', blank=True)

    def __str__(self):
        return str(self.group)

