import random
from django.shortcuts import render_to_response
from dataload.models import *

### Utilities ###
def w_choice(lst):
    n = random.uniform(0, 1)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item

def show_all(request):
    students = Demographics.objects.all()
    students_all = []
    graphs = {'mcasxy': [], 'languages': [], 'iep': [], 'frl': []}
    for student in students:
        # setup data structure to return
        student_d = {'data': student,'generated': {}, 'tests': {}}

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

        # Generate some per-student
        student_d['generated']['mepa_r'] = random.randint(10,30)
        student_d['generated']['mepa_w'] = random.randint(10,30)
        student_d['generated']['afterschool'] = \
            set( [
                w_choice([("B&G", 0.5), ("Peabody", 0.05), ("Mystic", 0.15), ("", .30)]),
                w_choice([("B&G", 0.1), ("Peabody", 0.05), ("Mystic", 0.15), ("", .50)])
            ])

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

    ## Values that still need to be randomly generated
    values = {}
    values['tardies'] = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 4, 5, 9]
    values['ward'] = [0, 1, 2, 3, 4, 5, 6, 7]

    return render_to_response('student_list.html', {
        'students': students, 
        'students_all': students_all, 
        'generated_values': values, 
        'graphs': graphs, 
        'frl_options': ['Reduced Lunch', 'Free Lunch', 'Not Eligible']
        })
