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
import pdb

VERSION = '20170728_style'
num_methods = 8      #gt, ours, baseline

# Create your views here.
def index(request):

    if( request.method == "POST" ):
        return redirect('main')

    return render(request, 'userstudy/index.html')


index_to_method = {0: 'ref', 1: 'ours', 2: 'photomontage-full'}

def main(request):


    ########## config variables ##########
    num_scenes              = 1
    #num_styles              = 48

    #num_selected_styles     = 1
    #num_selected_contents   = 1
    ######################################

    #total_votes = num_selected_styles * num_selected_contents
    total_votes = 1  # TODO: change this to number of image pairs


    if( request.method != "POST" ):

        #### first visiting, create user
        user = People()
        user.st_time = timezone.now()
        user.save()

        ## create Hash code
        code_generator = Hashids(min_length=10)
        user.code = code_generator.encode(user.id)
        user.save()


        #### create votes
        ## select styles
        # selected_scene_idxs = np.random.permutation(num_scenes)[:num_scenes] #+ 1
        selected_scene_idxs = np.arange(num_scenes)[:num_scenes] #+ 1
        print(selected_scene_idxs)

        vote_list = []

        for s in range(len(selected_scene_idxs)):
            vote            = Vote()
            vote.user       = user
            vote.order      = 0
            vote.sceneId    = selected_scene_idxs[s]
            #vote.content    = selected_content_idxs[c]

            ## random method, we only show the first two method
            method_order    = [1, 2, 
                            #    4, 5
                               ]  # TODO: change this to reflect the subdir index name
            random.shuffle(method_order)
            vote.method1    = method_order[0]
            vote.method2    = method_order[1]
            # vote.method3    = method_order[2]
            # vote.method4    = method_order[3]
            #vote.method5    = method_order[4]
            # pdb.set_trace()
            vote.save()

            vote_list.append(vote.id)


        ## random shuffle vote order
        random.shuffle(vote_list)

        ## bound votes with user
        user.save_vote_list(vote_list)


        #### extract vote
        current_vote_id = 0

        ## extract vote from database
        vote = user.get_vote(current_vote_id)

        ## image paths
        #style_path = 'data/style/%d.png' %vote.style
        #content_path = 'data/content/%d.png' %vote.content

        ref_path = 'data/%d/%d.jpg' %(0,vote.sceneId)
        m1_path = 'data/%d/%d.png' %(vote.method1,vote.sceneId)
        m2_path = 'data/%d/%d.png' %(vote.method2,vote.sceneId)
        # m3_path = 'data/%d/%d.jpg' %(vote.method3,vote.sceneId)
        # m4_path = 'data/%d/%d.jpg' %(vote.method4,vote.sceneId)
        # m5_path = 'data/%d/%d.jpg' %(vote.method5,vote.sceneId)
        # m6_path = 'data/%d/%d.jpg' %(vote.method6,vote.sceneId)
        # m7_path = 'data/%d/%d.jpg' %(vote.method7,vote.sceneId)
        # m8_path = 'data/%d/%d.jpg' %(vote.method8,vote.sceneId)
        #m3_path = 'data/result/%d_%d_m%d.png' %(vote.content, vote.style, vote.method3)
        #m4_path = 'data/result/%d_%d_m%d.png' %(vote.content, vote.style, vote.method4)
        #m5_path = 'data/result/%d_%d_m%d.png' %(vote.content, vote.style, vote.method5)


        # record vote-starting time
        vote.st_time = timezone.now()
        vote.save()

        ## progress
        percentage = int(current_vote_id * 100.0 / total_votes)

        context = {'current_vote_id': current_vote_id, 'total_votes': total_votes, \
                   'percentage': percentage, 'user_id': user.id, \
                   'm1_path': m1_path, 'm2_path': m2_path, 'ref_path': ref_path,
                #    'm3_path': m3_path, 'm4_path': m4_path,
                #    'm5_path': m5_path, 'm6_path': m6_path,
                #    'm7_path': m7_path, 'm8_path': m8_path,
                   }

        return render(request, 'userstudy/main.html', context)

    else:

        if( "comment" in request.POST ):
            # end of comment page, save comment and close survey

            user_id = int(request.POST["user_id"])
            user = People.objects.get(id = user_id)

            user.comment = request.POST["comment"]
            user.save()

            # redirect to home page
            return redirect('index')


        else:
            #### during survey, save current vote and extract next vote

            #### save current vote
            ## extract user
            user_id = int(request.POST["user_id"])
            user = People.objects.get(id = user_id)

            ## extract current vote
            current_vote_id = int(request.POST["current_vote_id"])
            vote = user.get_vote(current_vote_id)

            ## record vote-starting time
            vote.ed_time = timezone.now()

            ## extract vote results
            m1_vote = int(request.POST["m1_vote"])
            m2_vote = int(request.POST["m2_vote"])
            # m3_vote = int(request.POST["m3_vote"])
            # m4_vote = int(request.POST["m4_vote"])
            # m5_vote = int(request.POST["m5_vote"])
            # m6_vote = int(request.POST["m6_vote"])
            # m7_vote = int(request.POST["m7_vote"])
            # m8_vote = int(request.POST["m8_vote"])
            #m5_vote = int(request.POST["m5_vote"])

            ## save vote result
            if( m1_vote == 1 ):
                vote.result = 1
                method = vote.method1
            elif( m2_vote == 1 ):
                vote.result = 2
                method = vote.method2
            # elif( m3_vote == 1 ):
            #     vote.result = 3
            #     method = vote.method3
            # elif( m4_vote == 1 ):
            #     vote.result = 4
            #     method = vote.method4
            # elif( m5_vote == 1 ):
            #     vote.result = 3
            #     method = vote.method5
            # elif( m6_vote == 1 ):
            #     vote.result = 3
            #     method = vote.method6
            # elif( m7_vote == 1 ):
            #     vote.result = 3
            #     method = vote.method7
            # elif( m8_vote == 1 ):
            #     vote.result = 3
            #     method = vote.method8

            print("User select vote %d (method %d)" %(vote.result, method))

            vote.order = current_vote_id + 1
            vote.save()


            #### move to next vote
            current_vote_id += 1

            ## finish voting, redirect to comment page
            if( current_vote_id == total_votes ):

                user.ed_time = timezone.now()
                user.save()
                code = user.code

                context = {'user_id': user.id, 'code': code}
                return render(request, 'userstudy/comment.html', context)


            #### extract next vote
            vote = user.get_vote(current_vote_id)

            ## image paths
            #style_path = 'data/style/%d.png' %vote.style
            #content_path = 'data/content/%d.png' %vote.content

            ref_path = 'data/%d/%d.jpg' %(0,vote.sceneId)
            m1_path = 'data/%d/%d.png' %(vote.method1,vote.sceneId)
            m2_path = 'data/%d/%d.png' %(vote.method2,vote.sceneId)
            # m3_path = 'data/%d/%d.jpg' %(vote.method3,vote.sceneId)
            # m4_path = 'data/%d/%d.jpg' %(vote.method4,vote.sceneId)
            # m5_path = 'data/%d/%d.jpg' %(vote.method5,vote.sceneId)
            # m6_path = 'data/%d/%d.jpg' %(vote.method6,vote.sceneId)
            # m7_path = 'data/%d/%d.jpg' %(vote.method7,vote.sceneId)
            # m8_path = 'data/%d/%d.jpg' %(vote.method8,vote.sceneId)
            # 'data/result/%d_%d_m%d.png' %(vote.content, vote.style, vote.method3)
            #m4_path = 'data/result/%d_%d_m%d.png' %(vote.content, vote.style, vote.method4)
            #m5_path = 'data/result/%d_%d_m%d.png' %(vote.content, vote.style, vote.method5)


            # record vote-starting time
            vote.st_time = timezone.now()
            vote.save()

            ## progress
            percentage = int(current_vote_id * 100.0 / total_votes)

            context = {'current_vote_id': current_vote_id, 'total_votes': total_votes, \
                       'percentage': percentage, 'user_id': user.id, \
                       'm1_path': m1_path, 'm2_path': m2_path, 
                    #    'm3_path': m3_path,
                    #    'm4_path': m4_path,
                       'ref_path': ref_path,
                    #    'm5_path': m5_path, 'm6_path': m6_path,
                    #     'm7_path': m7_path, 'm8_path': m8_path,
                        }

            return render(request, 'userstudy/main.html', context)


def finish(request):

    context = {}
    return render(request, 'userstudy/finish.html')



def dump(request):

    user_all = People.objects.all().exclude(ed_time = None)

    user_header = ["User ID", "Time", "Code", "Finished Votes"]
    user_data = []

    vote_header = ["User ID", "SceneId", "Method 1", "Method 2", "Method 3", "Method 4", "Result", "Time"]
    vote_data = []

    ## aggregate vote for each method
    count = [0 for _ in range(num_methods)]
    binary_count = [[[0, 0] for _ in range(num_methods)] for _ in range(num_methods)]

    for user in user_all:
        if( user.ed_time != None ):
            user.duration = user.ed_time - user.st_time
        else:
            user.duration = "Not Finish"


        # check numbers of finished votes
        votes = Vote.objects.filter(user = user).exclude(result = 0)
        user.finish_votes = len(votes)

        user_data.append([user.id, user.duration, user.code, user.finish_votes])


        # extract valid votes
        votes = Vote.objects.filter(user = user)
        for vote in votes:
            vote.duration = 0
            if( vote.ed_time != None ):
                diff = vote.ed_time - vote.st_time
                vote.duration = diff.seconds
                vote_data.append([user.id, vote.sceneId, 
                                #   vote.method1, vote.method2, 
                                #   vote.method3, vote.method4, 
                                  vote.result, vote.duration])

                order = [vote.method1, vote.method2, 
                        #  vote.method3, vote.method4
                         ]
                selected_method = order[ vote.result - 1 ] - 1
                print(order, selected_method, vote.result)
                count[ selected_method ] = count[ selected_method ] + 1

                binary_count[ order[0]-1 ][ order[1]-1 ][1] += 1 # total
                binary_count[ order[1]-1 ][ order[0]-1 ][1] += 1 # total
                # winner + 1
                if( vote.result == 1 ): 
                    binary_count[ order[0]-1 ][ order[1]-1 ][0] += 1
                    # binary_count[ order[1]-1 ][ order[0]-1 ][0] += 1
                else:
                    binary_count[ order[1]-1 ][ order[0]-1 ][0] += 1


    print(binary_count)

    output_filename = 'user.csv'
    save_csv(output_filename, user_header, user_data)

    output_filename = 'vote.csv'
    save_csv(output_filename, vote_header, vote_data)

    num_valid_vote = len(vote_data)

    context = {"user_all": user_all, 'num_valid_vote': num_valid_vote, 'version': VERSION, }
            #    'method1': count[0], 'method2': count[1], 'method3': count[2]}
    for i in range(num_methods):
        context['method%d' % (i+1)] = count[i]
    
    for i in range(num_methods):
        for j in range(i+1,num_methods):
                print((binary_count[i][j], binary_count[j][i]))
                context['method%dv%d' % (i+1, j+1)] = '%d %d' % (binary_count[i][j][0], binary_count[j][i][0])
                print(context)
    return render(request, 'userstudy/dump.html', context)
