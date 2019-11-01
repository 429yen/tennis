from django import forms
from .models import Message,Group,Friend,Good
from django.contrib.auth.models import User
from django.db.models import Q

# 検索フォーム
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    TYPE_CHOICES = (
        (0, '----'),
        (1, '飲み物'),
        (2, '食べ物'),
        (3, 'その他'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES)

# Groupのチェックボックスフォーム
class GroupCheckForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[(item.title, item.title) for item in Group.objects.filter(members=user)],
            #widget=forms.CheckboxSelectMultiple(),
        )


# Groupの選択メニューフォーム
class GroupSelectForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) for item in Group.objects.filter(members=user)],
        )

# Friendのチェックボックスフォーム
class FriendsForm(forms.Form):
    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        super(FriendsForm, self).__init__(*args, **kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user, item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )

# Group作成フォーム
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=50)

# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=10)
    TYPE_CHOICES = (
        (1, '飲み物'),
        (2, '食べ物'),
        (3, 'その他'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES)

    '''def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) for item in Group.objects.filter(Q(owner=public) | Q(members=user))],
        ) '''


class GoodAddForm(forms.Form):
    count = forms.IntegerField(max_value=10, min_value=1)
    comment = forms.CharField(max_length=20, required=False)

    def __init__(self, user, members=[], *args, **kwargs):
        super(GoodAddForm, self).__init__(*args, **kwargs)
        self.fields['whose'] = forms.ChoiceField(
            choices=[(user.username, user.username)] + [(item.username, item.username) for item in members],
        )


class KaikeiForm(forms.Form):
    def __init__(self, members=[], *args, **kwargs):
        super(KaikeiForm, self).__init__(*args, **kwargs)
        self.fields['whose'] = forms.ChoiceField(
            choices=[(item.username, item.username) for item in members],
        )