from django.contrib import admin
from .models import Message,Friend,Group,Good,Choice


# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'group', 'content', 'sum', 'type', 'pub_date', 'price')  # 一覧に出したい項目
    list_display_links = ('owner', 'group', 'content', 'sum', 'type', 'price')  # 修正リンクでクリックできる項目


'''class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'page',)  # 一覧に出したい項目
    list_display_links = ('id', 'name',)  # 修正リンクでクリックできる項目'''


class GroupAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'deadline',)  # 一覧に出したい項目
    list_display_links = ('owner', 'title', 'deadline')  # 修正リンクでクリックできる項目


class GoodAdmin(admin.ModelAdmin):
    list_display = ('owner', 'message', 'whose', 'count', 'comment')  # 一覧に出したい項目
    list_display_links = ('owner', 'message', 'whose', 'count', 'comment')  # 修正リンクでクリックできる項目


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')  # 一覧に出したい項目
    list_display_links = ('user', 'group',)  # 修正リンクでクリックできる項目



admin.site.register(Message, MessageAdmin)
#admin.site.register(Friend)
admin.site.register(Group, GroupAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(Choice, ChoiceAdmin)