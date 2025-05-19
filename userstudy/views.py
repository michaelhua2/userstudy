from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from userstudy.models import People, Vote
from datetime import datetime
import numpy as np
import random
from hashids import Hashids
from userstudy.utils import CommaString_to_IntArray, IntArray_to_CommaString, choose_imgs, save_csv, load_csv
from django import template
import pdb, json

VERSION = '20170728_style'
num_methods = 2      #ours, sd, dalton, jiabin

# Create your views here.
def index(request):

    if( request.method == "POST" ):
        return redirect('info')

    return render(request, 'userstudy/index.html')


index_to_method = {1: 'ours', 2: 'unguided', 3: 'dalton', 4: 'jiabin'}

def main(request):

    ########## config ##########
    num_scenes = 50
    base_method = 1
    compare_methods = [2, 3, 4]
    total_votes = num_scenes * len(compare_methods)
    prompts = json.load(open('userstudy/static/prompts.json', 'r'))

    is_colorblind = request.session.get('is_colorblind', False)

    # First-time visitor: create user and generate votes
    if request.method != "POST" or "user_id" not in request.POST:
        user = People()
        user.st_time = timezone.now()
        user.is_colorblind = is_colorblind
        user.save()

        from hashids import Hashids
        code_generator = Hashids(min_length=10)
        user.code = code_generator.encode(user.id)
        user.save()

        vote_list = []
        for scene_id in range(num_scenes):
            for m2 in compare_methods:
                vote = Vote()
                vote.user = user
                vote.sceneId = scene_id
                vote.method1 = base_method
                vote.method2 = m2
                vote.order = 0
                vote.swap_display = random.choice([True, False])
                vote.save()
                vote_list.append(vote.id)

        random.shuffle(vote_list)
        user.save_vote_list(vote_list)

        current_vote_id = 0
        vote = user.get_vote(current_vote_id)
        subdir = 'rgb' if is_colorblind else 'cvd'

        if vote.swap_display:
            left_method, right_method = vote.method2, vote.method1
            left_is_method1 = False
        else:
            left_method, right_method = vote.method1, vote.method2
            left_is_method1 = True

        context = {
            'current_vote_id': current_vote_id,
            'total_votes': total_votes,
            'percentage': 0,
            'user_id': user.id,
            'm1_path': f'data/{left_method}/{subdir}/{vote.sceneId}_0_.png',
            'm2_path': f'data/{right_method}/{subdir}/{vote.sceneId}_0_.png',
            'left_is_method1': left_is_method1,
            'prompt': prompts[vote.sceneId],
        }

        vote.st_time = timezone.now()
        vote.save()
        return render(request, 'userstudy/main.html', context)

    # POST with comment at end of survey
    elif "comment" in request.POST:
        user_id = int(request.POST["user_id"])
        user = People.objects.get(id=user_id)
        user.comment = request.POST["comment"]
        user.save()
        return redirect('index')

    # Voting step
    else:
        user_id = int(request.POST["user_id"])
        user = People.objects.get(id=user_id)
        current_vote_id = int(request.POST["current_vote_id"])
        vote = user.get_vote(current_vote_id)

        vote.ed_time = timezone.now()

        m1_vote = int(request.POST.get("m1_vote", 0))
        m2_vote = int(request.POST.get("m2_vote", 0))

        left_is_method1 = request.POST.get("left_is_method1") == "1"
        m1_vote = int(request.POST.get("m1_vote", 0))
        m2_vote = int(request.POST.get("m2_vote", 0))

        if m1_vote == 1 and left_is_method1:
            vote.result = 1
        elif m2_vote == 1 and not left_is_method1:
            vote.result = 1
        elif m1_vote == 1 and not left_is_method1:
            vote.result = 2
        elif m2_vote == 1 and left_is_method1:
            vote.result = 2
        else:
            return HttpResponse("No vote selected", status=400)

        vote.order = current_vote_id + 1
        vote.save()

        current_vote_id += 1
        if current_vote_id == total_votes:
            user.ed_time = timezone.now()
            user.save()
            return render(request, 'userstudy/comment.html', {
                'user_id': user.id,
                'code': user.code
            })

        vote = user.get_vote(current_vote_id)
        subdir = 'rgb' if is_colorblind else 'cvd'

        if vote.swap_display:
            left_method, right_method = vote.method2, vote.method1
            left_is_method1 = False
        else:
            left_method, right_method = vote.method1, vote.method2
            left_is_method1 = True

        context = {
            'current_vote_id': current_vote_id,
            'total_votes': total_votes,
            'percentage': 0,
            'user_id': user.id,
            'm1_path': f'data/{left_method}/{subdir}/{vote.sceneId}_0_.png',
            'm2_path': f'data/{right_method}/{subdir}/{vote.sceneId}_0_.png',
            'left_is_method1': left_is_method1,
            'prompt': prompts[vote.sceneId],
        }

        vote.st_time = timezone.now()
        vote.save()
        return render(request, 'userstudy/main.html', context)

def finish(request):
    return render(request, 'userstudy/finish.html')

def info(request):
    if request.method == 'POST':
        colorblind = request.POST.get('colorblind')
        request.session['is_colorblind'] = (colorblind == '1')
        request
        return redirect('main')
    return render(request, 'userstudy/info.html')

def dump(request):
    user_all = People.objects.all().exclude(ed_time=None)

    user_header = ["User ID", "Time", "Code", "Finished Votes"]
    user_data = []

    vote_header = ["User ID", "SceneId", "Method 1", "Method 2", "Result", "Time"]
    vote_data = []

    num_methods = 4
    count = [0 for _ in range(num_methods)]  # per-method win counts
    binary_count = [[[0, 0] for _ in range(num_methods)] for _ in range(num_methods)]  # [win_count, total]

    for user in user_all:
        user.duration = (user.ed_time - user.st_time) if user.ed_time else "Not Finish"
        votes = Vote.objects.filter(user=user).exclude(result=0)
        user.finish_votes = len(votes)
        user_data.append([user.id, user.duration, user.code, user.finish_votes])

        for vote in Vote.objects.filter(user=user):
            vote_duration = (vote.ed_time - vote.st_time).seconds if vote.ed_time else 0
            vote_data.append([user.id, vote.sceneId, vote.method1, vote.method2, vote.result, vote_duration])

            m1 = vote.method1
            m2 = vote.method2

            if vote.result == 1:
                winner, loser = m1, m2
            elif vote.result == 2:
                winner, loser = m2, m1
            else:
                continue  # skip invalid vote

            # win count
            count[winner - 1] += 1

            # total comparisons
            binary_count[m1 - 1][m2 - 1][1] += 1
            binary_count[m2 - 1][m1 - 1][1] += 1

            # winner wins over loser
            binary_count[winner - 1][loser - 1][0] += 1

    # CSV output
    save_csv('user.csv', user_header, user_data)
    save_csv('vote.csv', vote_header, vote_data)
    num_valid_vote = len(vote_data)

    context = {
        "user_all": user_all,
        "num_valid_vote": num_valid_vote,
        "version": VERSION,
    }

    for k, v in index_to_method.items():
        context[f'Method_{k}'] = v

    # Per-method win totals
    for i in range(num_methods):
        context[f'method{i + 1}'] = count[i]

    # Pairwise wins
    for i in range(num_methods):
        for j in range(i + 1, num_methods):
            win_ij = binary_count[i][j][0]
            win_ji = binary_count[j][i][0]
            context[f'method{i + 1}v{j + 1}'] = f"{win_ij} {win_ji}"

    return render(request, 'userstudy/dump.html', context)
