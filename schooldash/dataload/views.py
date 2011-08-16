import datetime
from decimal import *

from django.shortcuts import render_to_response
#from dataload.models import *

def load_demographics(request):
    """
    Read locally hosted csv files from Somerville's X2 export and feeds them 
    into the django database.  This enables us to reload on new export or to 
    fix errors from a static platonic ideal.
    """
    # TODO: rename, not just touching upon demographics anymore
    from django.shortcuts import redirect
    import csv
    import decimal

    from display.models import Demographics
    from display.models import DIEBELS
    from display.models import Mcasela
    from display.models import Mcasmath
    from display.models import Maplang
    from display.models import Mapmath

    ## Clean out old tables and reimport from scratch
    Demographics.objects.all().delete()
    DIEBELS.objects.all().delete()

    ## Load the Demographics table
    file = open('./data/HEA_DEMO.txt', 'r')
    reader = csv.reader(file)
    for student in reader:
        d = Demographics()
        d.fname         = student[0]
        d.mname         = student[1]
        d.lname         = student[2]
        d.id1           = int(student[3])
        d.id2           = int(student[4])
        d.grade_level   = student[5]
        d.grad_year     = int(student[6])
        d.homeroom      = student[7]
        d.gender        = student[8]
        d.birth_date    = student[9]
        d.home_lang     = student[10]
        d.lang_level    = student[11]
        d.race          = student[12]
        d.other1        = student[13] # IEP status?
        d.iep           = student[14] # IEP code?
        d.frl           = student[15]   
        if student[16] != '\N':
            d.attendance    = decimal.Decimal(student[16])
        d.other2        = student[17]
        d.enrollment    = student[18]
        d.save()
    file.close()

    ## Load District Entry and Exit info
    file1 = open('./data/HEA_ENTRY.txt', 'r')
    file2 = open('./data/HEA_EXIT.txt', 'r')
    entry_reader = csv.reader(file1)
    exit_reader = csv.reader(file2)
    for record in entry_reader:
        # TODO: make these one update statement
        sid1 = record[1]
        years = 2011 - int(record[5][:4])
        Demographics.objects.filter(id1=sid1).update(entry_date=record[5])
        Demographics.objects.filter(id1=sid1).update(years_at=years)
    for record in exit_reader:
        sid1 = record[1]
        Demographics.objects.filter(id1=sid1).update(exit_date=record[5])
        Demographics.objects.filter(id1=sid1).update(withdrawl=record[3])
    file1.close()
    file2.close()

    ## Load Attendence for Year to Date
    file = open('./data/HEA_ATT_YTD.txt', 'r')
    reader = csv.reader(file)
    for record in reader:
        Demographics.objects.filter(id1=record[0]).update(missed_days=record[1])

    ## DIBELS tests
    grades          = ['KF', '01', '02', '03']
    test_numbers    = ['1', '2', '3']
    for grade in grades:
        for test in test_numbers:
            filename = './data/HEA_DIBELS' + test + '_G' + grade + '.txt'
            file = open(filename, 'r')
            reader = csv.reader(file)
            for test in reader:
                demo = Demographics.objects.filter(id1=test[1]).all()[0]
                dd = DIEBELS()
                dd.f_id1 = demo
                dd.test_name = test[3]
                dd.date = test[4]
                dd.result = test[7]
                dd.save()

    ## MCAS English Language Arts (ELA)
    grades = ['03', '04', '05', '06', '07', '08']
    for grade in grades:
        filename = './data/HEA_ELA_G' + grade + '.txt'
        file = open(filename, 'r')
        reader = csv.reader(file)
        for test in reader:
            demo = Demographics.objects.filter(id1=test[1]).all()[0]
            ela = Mcasela()
            ela.f_id1 = demo
            ela.test_name = test[3]
            ela.date = test[4]
            if test[7] != '\N':
                ela.scaled_score = test[7]
            if test[8] != '\N':
                ela.raw_score = test[8]
            ela.level = test[9]
            ela.save()

    ## MCAS Math
    grades = ['03', '04', '05', '06', '07', '08']
    for grade in grades:
        filename = './data/HEA_MATH_G' + grade + '.txt'
        file = open(filename, 'r')
        reader = csv.reader(file)
        for test in reader:
            demo = Demographics.objects.filter(id1=test[1]).all()[0]
            math = Mcasmath()
            math.f_id1 = demo
            math.test_name = test[3]
            math.date = test[4]
            if test[7] != '\N':
                math.scaled_score = test[7]
            if test[8] != '\N':
                math.raw_score = test[8]
            math.level = test[9]
            math.save()

    ## MAP Lang
    grades = [2, 3, 4, 5, 6, 7, 8]
    test_id = [1, 2, 3]
    for test_num in test_id:
        for grade in grades:
            filename = './data/HEA_MAP' + str(test_num) + 'LANG_G0' + str(grade) + '.txt'
            file = open(filename, 'r')
            reader = csv.reader(file)
            for test in reader:
                demo = Demographics.objects.filter(id1=test[1]).all()[0]
                mlang                   = Maplang()
                mlang.f_id1             = demo
                mlang.test_interval     = test_num
                mlang.test_name         = test[3]
                mlang.date              = test[4]
                mlang.score             = test[7]
                mlang.save()

    ## MAP Math
    grades = [2, 3, 4, 5, 6, 7, 8]
    test_id = [1, 2, 3]
    for test_num in test_id:
        for grade in grades:
            filename = './data/HEA_MAP' + str(test_num) + 'MATH_G0' + str(grade) + '.txt'
            file = open(filename, 'r')
            reader = csv.reader(file)
            for test in reader:
                demo = Demographics.objects.filter(id1=test[1]).all()[0]
                mmath                   = Mapmath()
                mmath.f_id1             = demo
                mmath.test_interval     = test_num
                mmath.test_name         = test[3]
                mmath.date              = test[4]
                mmath.score             = test[7]
                mmath.save()

    return redirect('/real')
