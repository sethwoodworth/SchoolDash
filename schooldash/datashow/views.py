import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dataload.models import *
from userinfo.models import UserProfile

### Utilities ###
def w_choice(lst):
    n = random.uniform(0, 1)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item

@login_required
def show_all(request, demo=False):
    """
    Return the students a user has permisison to view, format the data, and
    render it. Optionally you can turn on "demo" which enables sample columns
    with randomly generated data.
    """

    up = UserProfile.objects.filter(user=request.user).all()[0]
    if up.homeroom == 'admin':
        students = Demographics.objects.all()
    else:
        students = Demographics.objects.filter(homeroom=up.homeroom).all()

    students_all = []
    graphs = {'mcasxy': [], 'languages': [], 'iep': [], 'frl': []}
    for student in students:
        # setup data structure to return
        student_d = {'data': student, 'generated': {}, 'tests': {}}

        # Return diebel test info
        diebels = student.diebels_set.order_by('date').reverse()
        student_d['tests']['diebels'] = diebels
        # Return mcas_ela test info
        mcas_ela = student.mcasela_set.order_by('date').reverse()
        student_d['tests']['ela'] = mcas_ela
        # Return mcas_math test info
        mcas_math = student.mcasmath_set.order_by('date').reverse()
        student_d['tests']['math'] = mcas_math

        # Return MAP test data
        map_lang = student.maplang_set.order_by('date').reverse()
        student_d['tests']['map_lang'] = map_lang
        map_math = student.mapmath_set.order_by('date').reverse()
        student_d['tests']['map_math'] = map_math

        if demo:
            # Generate values if this is a full-demo
            student_d['generated']['mepa_r'] = random.randint(10,30)
            student_d['generated']['mepa_w'] = random.randint(10,30)
            student_d['generated']['afterschool'] = \
                set( [
                    w_choice([("B&G", 0.5), ("Peabody", 0.05), ("Mystic", 0.15), ("", .30)]),
                    w_choice([("B&G", 0.1), ("Peabody", 0.05), ("Mystic", 0.15), ("", .50)])
                ])

            # Values that still need to be randomly generated
            student_d['generated']['tardies'] = w_choice([(0, 0.3), (1, 0.3), (2, 0.2), (3, 0.2), (4, 0.2), (5, 0.2), (6, 0.1), (7, 0.1), (8, 0.1), (9, 0.1)])
            student_d['generated']['ward'] = w_choice([(0, 0.1), (1, 0.1), (2, 0.1), (3, 0.1), (4, 0.1), (5, 0.1), (6, 0.1), (7, 0.1)])

        ## Generate graph data
        # MCAS ela vs math scores
        if student_d['tests']['ela'] != 'None' and student_d['tests']['ela']:
            try:
                data = [
                    round(student_d['tests']['ela'][0].scaled_score),
                    round(student_d['tests']['math'][0].scaled_score) ]
                graphs['mcasxy'].append(data)
            except:
                pass

        # Language frequency counts
        graphs['languages'].append(student_d['data'].home_lang)
        graphs['iep'].append(student_d['data'].other1)
        graphs['frl'].append(student_d['data'].frl)

        students_all.append(student_d)

    # languages graph
    lang_list = {}
    for language in graphs['languages']:
        if lang_list.has_key(language):
            lang_list[language] += 1
        else:
            lang_list[language] = 1
    graphs['languages'] = lang_list

    # iep graph
    iep_list = {}
    for status in graphs['iep']:
        if iep_list.has_key(status):
            iep_list[status] += 1
        else:
            iep_list[status] = 1
    graphs['iep'] = iep_list

    # frl graph
    frl_list = {}
    for status in graphs['frl']:
        if frl_list.has_key(status):
            frl_list[status] += 1
        else:
            frl_list[status] = 1
    graphs['frl'] = frl_list


    all_values = {
        'students': students,
        'students_all': students_all,
        'graphs': graphs,
        'frl_options': ['Reduced Lunch', 'Free Lunch', 'Not Eligible'],
        'demo': demo,
        }
    return render(request, 'student_list.html', all_values)
