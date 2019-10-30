from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message,Friend,Group,Good, Choice
from .forms import GroupCheckForm,GroupSelectForm,SearchForm,FriendsForm,CreateGroupForm,PostForm,GoodAddForm

from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.utils import timezone
import math
import datetime

# Create your views here.

# indexのビュー関数


@login_required(login_url='/admin/login/')
def index(request):
    # publicのuser取得
    (public_user, public_group) = get_public()

    # POST送信時の処理
    if request.method == 'POST':

        # Groupsのチェックを更新したときの処理
        if request.POST['mode'] == '__check_form__':
            # フォームの用意
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user, request.POST)
            # チェックされたGroup名をリストにまとめる
            glist = []
            for item in request.POST.getlist('groups'):
                glist.append(item)
            # Messageの取得
            messages = get_your_group_message(request.user, glist, None)

            # ChoiceのGroupを指定されたものに変更
            gr_name = request.POST['groups']
            gp = Group.objects.filter(title=gr_name).first()
            ch = Choice.objects.filter(user=request.user).first()
            ch.group = gp
            ch.save()

        # Groupsメニューを変更したときの処理
        if request.POST['mode'] == '__search_form__':
            # フォームの用意
            searchform = SearchForm(request.POST)
            checkform = GroupCheckForm(request.user)
            ''''# Groupのリストを取得
            gps = Group.objects.filter(Q(owner=request.user) | Q(members=request.user))
            glist = [public_group]
            for item in gps:
                glist.append(item) '''
            # Groupを選択
            ch = Choice.objects.filter(user=request.user).first()
            glist = []
            glist.append(ch.group)
            # Messageの取得
            if request.POST['search'] == '':
                re = None
            else:
                re = request.POST['search']
            messages = get_your_group_message(request.user, glist, re, int(request.POST['type']))

        #GETアクセス時の処理
    else:
            # フォームの用意
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user)
            ''''# Groupのリストを取得
            gps = Group.objects.filter(Q(owner=request.user) | Q(members=request.user))
            glist = [public_group]
            for item in gps:
                glist.append(item) '''
            # Groupを選択
            ch = Choice.objects.filter(user=request.user).first()
            glist = []
            glist.append(ch.group)
            # Messageの取得
            messages = get_your_group_message(request.user, glist, None)

    # 共通処理

    # 日付に関する処理
    date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    deadline = ch.group.deadline
    d = math.floor((deadline-date).total_seconds())
    hours = math.floor(d/3600)
    minutes = math.floor((d-hours*3600)/60)
    seconds = math.floor(d-hours*3600-minutes*60)
    params = {
        'login_user': request.user,
        'contents': messages,
        'check_form': checkform,
        'search_form': searchform,
        'selected_group': ch.group,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'd': d,
    }
    return render(request, 'app/index.html', params)




# いらない
@login_required(login_url='/admin/login/')
def groups(request):
    # 自分が登録したFriendを取得
    friends = Friend.objects.filter(owner=request.user)

    ch = Choice.objects.filter(user=request.user).first()

    # POST送信時の処理
    if request.method == 'POST':

        # Groupsメニュー選択しの処理
        if request.POST['mode'] == '__groups_form__':
            # 選択したGroup名を表示
            sel_group = request.POST['groups']
            # Groupを取得
            gp = Group.objects.filter(Q(owner=request.user) | Q(members=request.user)).filter(title=sel_group).first()
            # 以下、自分のフレンドのうちグループに含まれる人を取得
            fds = Friend.objects.filter(owner=request.user)
            mem = gp.members.all()
            # FriendのUserをリストにまとめる
            vlist_old = []
            for item in fds:
                for jtem in mem:
                    if item.user.username == jtem.username:
                        vlist_old.append(item.user.username)

            vlist = list(set(vlist_old))

            # フォームの用意
            groupsform = GroupSelectForm(request.user, request.POST)
            friendsform = FriendsForm(request.user, friends=friends, vals=vlist)

        # Friendsのチェック更新時の処理
        if request.POST['mode'] == '__friends_form__':
            # 選択したGroupの取得
            sel_group = request.POST['group']
            group_obj = Group.objects.filter(title=sel_group).first()
            # チェックしたFriendsを取得
            sel_fds = request.POST.getlist('friends')
            # FriendsのUserを取得
            sel_users = User.objects.filter(username__in=sel_fds)
            # Userのリストに含まれるユーザーが登録したFriendを取得
            fds = Friend.objects.filter(owner=request.user).filter(user__in=sel_users)
            # 全てのFriendにGroupを設定し保存する
            vlist = []
            for item in fds:
                vlist.append(item.user.username)

            for mem in sel_users:
                group_obj.members.add(mem)
                group_obj.save()

            # メッセージを設定
            messages.success(request, ' チェックされたFriendを' + sel_group + 'に登録しました。')
            # フォームの用意
            groupsform = GroupSelectForm(request.user, {'groups':sel_group})
            friendsform = FriendsForm(request.user, friends=friends, vals=vlist)

    # GETアクセス時の処理
    else:
        # フォームの用意
        groupsform = GroupSelectForm(request.user)
        friendsform = FriendsForm(request.user, friends=friends, vals=[])
        sel_group = '-'

    # 共通処理
    createform = CreateGroupForm()
    # 日付に関する処理
    date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    deadline = ch.group.deadline
    d = math.floor((deadline - date).total_seconds())
    params = {
        'login_user': request.user,
        'groups_form': groupsform,
        'friends_form': friendsform,
        'create_form': createform,
        'group': sel_group,
        'selected_group': ch.group,
        'd': d,
    }
    return render(request, 'app/groups.html', params)


# Friendの追加処理 いらぬ
@login_required(login_url='/admin/login/')
def add(request):
    # 追加するUser選択
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()
    # Userが本人だった場合の処理
    if add_user == request.user:
        messages.info(request, "自分自身をFriendに追加することはできません。")
        return redirect(to='/app')
    # publicの取得
    (public_user, public_group) = get_public()
    # add_userのFriendの数を調べる
    frd_num = Friend.objects.filter(owner=request.user).filter(user=add_user).count()
    # ゼロより大きければすでに登録済み
    if frd_num > 0:
        messages.info(request, add_user.username + ' はすでに登録されています。')
        return redirect(to='/app')

    # ここからFriendの登録処理
    frd = Friend()
    frd.owner = request.user
    frd.user = add_user
    #frd.group = public_group
    frd.save()
    # メッセ―ジを設定
    messages.success(request, add_user.username + ' を追加しました！groupページに移動して、追加したFriendをメンバーに設定してください。')
    return redirect(to='/app')


# グループの作成処理　いらぬ
@login_required(login_url='/admin/login/')
def creategroup(request):
    # Groupを作り、Userとtitleを設定して保存する
    gp = Group()
    gp.owner = request.user
    gp.title = request.POST['group_name']
    gp.save()
    gp.members.add(request.user)
    gp.save()
    messages.info(request, '新しいグループを作成しました。')
    return redirect(to='/app/groups')


# メッセージのポスト処理
@login_required(login_url='/admin/login/')
def post(request):
    # 共通処理
    ch = Choice.objects.filter(user=request.user).first()
    # 日付に関する処理
    date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    deadline = ch.group.deadline
    d = math.floor((deadline - date).total_seconds())

    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        # gr_name = request.POST['groups']
        content = request.POST['content']
        type = request.POST['type']

        # Groupの取得
        '''group = Group.objects.filter(Q(owner=request.user) | Q(members=request.user)).filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()'''

        # もしグループが締め切りを過ぎていたら、新規作成できないようにする
        if d < 0:
            messages.info(request, '締め切りを過ぎているため追加できません。')
            return redirect(to='/app')

        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.group = ch.group
        msg.content = content
        msg.type = type
        msg.price = int(0)
        msg.save()
        # メッセージを設定
        messages.success(request, msg.content + 'を新たに追加しました！')
        return redirect(to='/app')

    # GETアクセス時の処理
    else:
        form = PostForm()


    params = {
        'login_user': request.user,
        'form': form,
        'selected_group': ch.group,
        'd': d,
    }
    return render(request, 'app/post.html', params)


def messagedelete(request, message_id):
    try:
        get_message = Message.objects.filter(id=message_id).first()
        get_message.delete()
    except:
        messages.info(request, 'すでに削除されています。')
        return redirect(to='/app')

    return redirect(to='/app')


# goodボタンの処理 この処理はいらない
@login_required(login_url='/admin/login/')
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    # 自分がメッセージにgoodした数を調べる
    is_good = Good.objects.filter(owner=request.user).filter(message=good_msg).count()
    # ゼロより大きければすでにgood済み
    if is_good > 0:
        messages.success(request, ' すでにメッセージにはGoodしています。')
        return redirect(to='/app')

    # Messageのsumを1増やす
    good_msg.sum += 1
    good_msg.save()
    # Goodを作成し、設定して保存
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()
    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect(to='/app')


@login_required(login_url='/admin/login/')
def gooddetail(request, message_id):
    try:
        get_message = Message.objects.filter(id=message_id).first()
    except:
        messages.info(request, 'すでに削除されています。')
        return redirect(to='/app')
    else:
        goods = Good.objects.filter(message=get_message)
        ch = Choice.objects.filter(user=request.user).first()

    # 日付に関する処理
    date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    deadline = ch.group.deadline
    d = math.floor((deadline - date).total_seconds())

    params = {
        'login_user': request.user,
        'goods': goods,
        'message': get_message,
        'selected_group': ch.group,
        'd': d,
    }
    return render(request, 'app/good_detail.html', params)


@login_required(login_url='/admin/login/')
def goodadd(request, message_id, good_id=None ):
    good_message = Message.objects.filter(id=message_id).first()
    if good_id:
        gd = Good.objects.filter(id=good_id).first()
        # Messageのsumを減らしておく
        good_message.sum -= int(gd.count)
    else:
        gd = Good()

    ch = Choice.objects.filter(user=request.user).first()
    # 日付に関する処理
    date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    deadline = ch.group.deadline
    d = math.floor((deadline - date).total_seconds())


    if request.method == 'POST':
        # 送信内容の取得
        whose = request.POST['whose']
        count = request.POST['count']
        comment = request.POST['comment']

        # もし締め切りを過ぎている場合の処理
        if d < 0:
            messages.info(request, '締め切りを過ぎているため追加できません。')
            return redirect(to='/app')

        # goodを作成して保存
        gd.message = good_message
        gd.owner = request.user
        whose = User.objects.filter(username=whose).first()
        gd.whose = whose
        gd.count = count
        gd.comment =comment
        try:
            gd.save()
        except:
            messages.info(request, 'すでに削除されています。')
            return redirect(to='/app')

        # Messageのsumを増やす
        good_message.sum += int(count)
        good_message.save()

        # メッセージを設定
        messages.success(request, gd.message.content + 'を追加しました！')
        return redirect(to='/app')

    else:
        form = GoodAddForm(request.user)

    # 共通処理

    params = {
        'login_user': request.user,
        'form': form,
        'message_id': message_id,
        'good_id': good_id,
        'selected_group': ch.group,
        'd': d,
    }

    return render(request, 'app/good_add.html', params)


@login_required(login_url='/admin/login/')
def gooddelete(request, message_id, good_id):
    ch = Choice.objects.filter(user=request.user).first()

    # 日付に関する処理
    date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    deadline = ch.group.deadline
    d = math.floor((deadline - date).total_seconds())

    # もし締め切りを過ぎている場合の処理
    if d < 0:
        messages.info(request, '締め切りを過ぎているため削除できません。')
        return redirect(to='/app')

    get_message = Message.objects.filter(id=message_id).first()
    gd = Good.objects.filter(id=good_id).first()
    get_message.sum -= int(gd.count)
    try:
        get_message.save()
        gd.delete()
    except:
        messages.info(request, 'すでに削除されています。')
        return redirect(to='/app')

    goods = Good.objects.filter(message=get_message)


    params = {
        'login_user': request.user,
        'goods': goods,
        'message': get_message,
        'selected_group': ch.group,
        'd': d,
    }

    return render(request, 'app/good_detail.html', params)


@login_required(login_url='/admin/login/')
def myproducts(request):
    ch = Choice.objects.filter(user=request.user).first()
    gr = ch.group
    mes = Message.objects.filter(group=gr)
    # メッセージのうち、goodがrequest.userであるものを取り出す
    goods = Good.objects.filter(message__in=mes).filter(whose=request.user)

    sum = 0
    for item in goods:
        sum += int(item.message.price*item.count)


    # 日付に関する処理
    date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    deadline = ch.group.deadline
    d = math.floor((deadline - date).total_seconds())
    params = {
        'login_user': request.user,
        'goods': goods,
        'sum': sum,
        'selected_group': ch.group,
        'd': d,
    }

    return render(request, 'app/myproducts.html', params)




# これ以降はビュー関数ではなく普通の関数　==============================================


# 指定されたグループおよび検索文字によるMessageの取得
def get_your_group_message(owner, glist, find, type=0):
    # publicの取得
    (public_user, public_group) = get_public()
    # チェックされたGroupの取得
    groups = Group.objects.filter(Q(owner=owner) | Q(owner=public_user) | Q(members=owner)).filter(title__in=glist)
    # groupのうち、memberに自分が含まれるものを取り出す
    # me_groups = Group.objects.filter(members=owner)

    # groupがgroupsに含まれるか、me_groupsに含まれるMessageの取得
    if find == None:
        if type == 0:
            messages = Message.objects.filter(group__in=groups)[:100]
        else:
            messages = Message.objects.filter(group__in=groups).filter(type=type)[:100]
    elif type == 0:
        messages = Message.objects.filter(group__in=groups).filter(content__contains=find)[:100]
    else:
        messages = Message.objects.filter(group__in=groups).filter(content__contains=find).filter(type=type)[:100]
    return messages


# publicなUserとGroupを取得する
def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter(owner=public_user).first()
    return (public_user, public_group)
