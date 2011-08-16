from django.db import models

class Demographics(models.Model):
    ## Demographics dataset
    fname       = models.TextField()
    mname       = models.TextField(null=True)
    lname       = models.TextField()
    id1         = models.IntegerField(unique=True)
    id2         = models.IntegerField(unique=True)
    grade_level = models.TextField()            # KF,1..8
    grad_year   = models.IntegerField()         # expected
    homeroom    = models.TextField()
    gender      = models.TextField()            # dare I make a binary?
    birth_date  = models.TextField()
    home_lang   = models.TextField()
    lang_level  = models.TextField()            # eg Fluent
    race        = models.TextField()            # eg White
    other1      = models.TextField(null=True)
    iep         = models.TextField(null=True)   # eg: Partial Inclusion
    frl         = models.TextField()            # Free & reduced Lunch, [0, 1, 2]
    attendance  = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    other2      = models.TextField(null=True)
    enrollment  = models.TextField(default="Active")

    ## Entry/exit dataset
    # These have to have null=True so I can update them later
    entry_date = models.TextField(null=True)
    exit_date = models.TextField(null=True) # if withdrawn
    years_at = models.IntegerField(null=True)
    withdrawl = models.TextField(null=True) # Withdrawl code
    ## HEA_ATT_YTD
    missed_days = models.IntegerField(null=True) # Missed to date this year

    def __unicode__(self):
        return str(self.id1) + " " + self.lname + ", "  + self.fname + " " + str(self.id)

class DIEBELS(models.Model):
    """
    DIEBELS test table representation
    [0] name
    [1] id1
    [2] id2
    [3] Test Name
    [4] Date taken
    [5] school
    [6] grade lvl
    [7] Benchmark | Strategic | Intensive
    """
    f_id1 = models.ForeignKey(Demographics) #[1]
    test_id = models.TextField(default='diebels')
    test_name = models.TextField()  #[3]
    date = models.TextField()       #[4]
    result = models.TextField()     #[7]

    class Meta:
        unique_together = ("f_id1", "test_name", "result")

    def __unicode__(self):
        return str(self.f_id1) + " " + self.date + " " + self.result


class Mcasela(models.Model):
    """
    MCAS English Language Arts (ELA)
    [0] name
    [1] id1
    [2] id2
    [3] Test name
    [4] Date taken
    [5] School
    [6] Grade level
    [7] Scaled score
    [8] Raw score
    [9] NI (needs improvement) | W (warning) | P (proficient)
    """
    f_id1 = models.ForeignKey(Demographics)                             #[1]
    test_id = models.TextField(default='ela')
    test_name = models.TextField()                                      #[3]
    date = models.TextField()                                           #[4]
    scaled_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)  #[7]
    raw_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)     #[8]
    level = models.TextField()                                          #[9]

    def __unicode__(self):
        return str(self.f_id1) + " " + self.date + " " + str(self.scaled_score)

class Mcasmath(models.Model):
    """
    MCAS Math
    [0] name
    [1] id1
    [2] id2
    [3] Test name
    [4] Date taken
    [5] School
    [6] Grade level
    [7] Scaled score
    [8] Raw score
    [9] NI (needs improvement) | W (warning) | P (proficient) | A (?)
    """
    f_id1 = models.ForeignKey(Demographics)                             #[1]
    test_id = models.TextField(default='math')
    test_name = models.TextField()                                      #[3]
    date = models.TextField()                                           #[4]
    scaled_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)  #[7]
    raw_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)     #[8]
    level = models.TextField()                                          #[9]

    def __unicode__(self):
        return str(self.f_id1) + " " + self.date + " " + str(self.scaled_score)

class Maplang(models.Model):
    """
    MAP Language
    [0] name
    [1] id1
    [2] id2
    [3] Test name
    [4] Date taken
    [5] School
    [6] Grade level
    [7] Score
    """
    f_id1 = models.ForeignKey(Demographics)                             #[1]
    test_id = models.TextField(default='maplang')
    test_interval = models.IntegerField()
    test_name = models.TextField()                                      #[3]
    date = models.TextField()                                           #[4]
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)  #[7]

    def __unicode__(self):
        return str(self.f_id1) + " " + self.date + " " + str(self.score)

class Mapmath(models.Model):
    """
    MAP Math
    [0] name
    [1] id1
    [2] id2
    [3] Test name
    [4] Date taken
    [5] School
    [6] Grade level
    [7] Score
    """
    f_id1 = models.ForeignKey(Demographics)                             #[1]
    test_id = models.TextField(default='maplang')
    test_interval = models.IntegerField()
    test_name = models.TextField()                                      #[3]
    date = models.TextField()                                           #[4]
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)  #[7]

    def __unicode__(self):
        return str(self.f_id1) + " " + self.date + " " + str(self.score)
