import pronotepy
import os
from datetime import date
from datetime import timedelta 
import json
import logging
#from pronotepy.ent import atrium_sud
from ent import atrium_sud

#Variables a remplacer (ou laisser comme ça pour tester la démo)
studentname="eveline" #nom de votre enfant - ne sert que pour le nom du fichier json
prefix_url = "0061642c" # sert au prefix de l'url https://PREFIX.index-education.net/pronote/
username="eveline.vingerhoeds2" #utlisateur pronote  - a remplacer par le nom d'utilisateur pronote de l'élève
password="sanyo123" # mot de passe pronote - a remplacer par le mot de passe du compte de l'élève
ent=atrium_sud
lessonDays=10
homeworkDays=10

index_note=0
limit_note=11 #nombre max de note à afficher + 1 
longmax_devoir = 125 #nombre de caractère max dans la description des devoirs



class Pronote:
    def __init__(self):
        
        # Initialize instance variables
        
        self.session = None
        self.auth_nonce = None
        self.gradeList = []
        self.averageList = []
        self.periodList = []
        self.evalList = []
        self.lessonList = []
        self.homeworkList = []
        self.whoiam = None
        self.isConnected = False

    def getGradeList(self):
        self.isConnected = False
        index_note=0
        limit_note=11
        client = pronotepy.Client('https://'+prefix_url+'.index-education.net/pronote/eleve.html', username, password, ent)
        if client.logged_in:
           self.isConnected = True
        else:
           logging.error("Error while authenticating when calling")
           return

        jsondata = {}

        #Récupération des notes 
        periods = client.periods
        #Transformation des notes en Json
        jsondata['grades'] = []
        for period in periods:
            for grade in period.grades:
        #data in order: id, date, subject(course),grade,out_of,default_out_of,coefficient,average(class),max,min 
                jsondata['grades'].append({
                    'pid': period.id,
                    'periodName': period.name,
                    'periodStart': period.start.strftime("%Y/%m/%d"),
                    'periodEnd': period.end.strftime("%Y/%m/%d"),
                    'gid': grade.id,
                    'date': grade.date.strftime("%Y/%m/%d"),
                    'subject': grade.subject.name,
                    'grade': grade.grade,            
                    'outOf': grade.out_of,
                    'defaultOutOf': grade.grade+'\u00A0/\u00A0'+grade.out_of,
                    'coefficient': grade.coefficient,
                    'average': grade.average,           
                    'max': grade.max,
                    'min': grade.min,
            })
        gradeList = jsondata
 #       print('Gradejsondata: ', gradeList)
        if gradeList:

           for grade in gradeList["grades"]:
               myGrade = Grade(studentname,grade) 
               self.addGrade(myGrade)
#               print('Gade: ', grade)

        else:
            logging.error("Grade list is empty")

    def addGrade(self,grade):
        self.gradeList.append(grade)

    def getAverageList(self):
        self.isConnected = False
        client = pronotepy.Client('https://'+prefix_url+'.index-education.net/pronote/eleve.html', username, password, ent)
        if client.logged_in:
           self.isConnected = True
        else:
           logging.error("Error while authenticating when calling")
           return

        jsondata = {}

        #Récupération des notes
        periods = client.periods
#        averages = client.current_period.averages
        #Transformation des notes en Json
        jsondata['averages'] = []
        for period in periods:
            for average in period.averages:
        #data in order: id, date, subject(course),grade,out_of,default_out_of,coefficient,average(class),max,min
                jsondata['averages'].append({
                    'pid': period.id,
                    'periodName': period.name,
                    'periodStart': period.start.strftime("%Y/%m/%d"),
                    'periodEnd': period.end.strftime("%Y/%m/%d"),
                    'student': average.student,
                    'classAverage': average.class_average,
                    'max': average.max,
                    'min': average.min,
                    'outOf': average.out_of,
                    'defaultOutOf': average.student+' / '+average.out_of,
                    'subject': average.subject.name,
            })
        averageList = jsondata
#        print('averagejsondata: ', averageList)
        if averageList:

           for average in averageList["averages"]:
               myAverage = Average(studentname,average)
               self.addAverage(myAverage)
#               print('Avg: ',average)

        else:
            logging.error("Average list is empty")

    def addAverage(self,average):
        self.averageList.append(average)

    def getPeriodList(self):
        self.isConnected = False
        client = pronotepy.Client('https://'+prefix_url+'.index-education.net/pronote/eleve.html', username, password, ent)
        if client.logged_in:
           self.isConnected = True
        else:
           logging.error("Error while authenticating when calling")
           return

        jsondata = {}

        #Récupération des notes
        periods = client.periods
        #Transformation des notes en Json
        jsondata['periods'] = []
        for period in periods:
        #data in order: id, date, subject(course),grade,out_of,default_out_of,coefficient,average(class),max,min
            jsondata['periods'].append({
                'pid': period.id,
                'periodName': period.name,
                'periodStart': period.start.strftime("%Y/%m/%d"),
                'periodEnd': period.end.strftime("%Y/%m/%d"),
        })
        periodList = jsondata
#        print('periodjsondata: ', periodList)
        if periodList:

           for period in periodList["periods"]:
               myPeriod = Period(period)
               self.addPeriod(myPeriod)
#               print('Per: ',period)

        else:
            logging.error("Period list is empty")

    def addPeriod(self,period):
        self.periodList.append(period)

    def getEvalList(self):
        self.isConnected = False
        client = pronotepy.Client('https://'+prefix_url+'.index-education.net/pronote/eleve.html', username, password, ent)
        if client.logged_in:
           self.isConnected = True
        else:
           logging.error("Error while authenticating when calling")
           return

        jsondata = {}

        #Récupération des notes
        periods = client.periods
#        averages = client.current_period.averages
        #Transformation des notes en Json
        jsondata['evaluations'] = []
        for period in periods:
            for eval in period.evaluations:
        #data in order: id, date, subject(course),grade,out_of,default_out_of,coefficient,average(class),max,min
                jsondata['evaluations'].append({
                    'pid': period.id,
                    'periodName': period.name,
                    'periodStart': period.start.strftime("%Y/%m/%d"),
                    'periodEnd': period.end.strftime("%Y/%m/%d"),
                    'eid': eval.id,
                    'evalName': eval.name,
                    'evalDomain': eval.domain,
                    'evalTeacher': eval.teacher,
                    'evalCoefficient': eval.coefficient,
                    'evalDescription': eval.description,
                    'evalSubject': eval.subject.name,
                    'evalDate': eval.date.strftime("%Y/%m/%d"),
            })
        evalList = jsondata
#        print('averagejsondata: ', averageList)
        if evalList:

           for eval in evalList["evaluations"]:
               myEval = Evaluation(studentname,eval)
               self.addEval(myEval)
#               print('Avg: ',average)

        else:
            logging.error("Average list is empty")

    def addEval(self,eval):
        self.evalList.append(eval)

    def getLessonList(self):
        self.isConnected = False
        client = pronotepy.Client('https://'+prefix_url+'.index-education.net/pronote/eleve.html', username, password, ent)
        if client.logged_in:
           self.isConnected = True
        else:
           logging.error("Error while authenticating when calling")
           return

        jsondata = {}

        jsondata['lessons'] = []
        index = 0
        dateLesson = date.today() + timedelta(days = 10)
        #Get lessons over X period
        while index <= lessonDays:
            print('index:', index)
            print('dateLesson', dateLesson)
            lessons = client.lessons(dateLesson)
            for lesson in lessons:
                jsondata['lessons'].append({
                    'lid': lesson.id,
                    'lessonDateTime': lesson.start.strftime("%Y/%m/%d, %H:%M"),
                    'lessonStart': lesson.start.strftime("%H:%M"),
                    'lessonEnd': lesson.end.strftime("%H:%M"),
                    'lessonSubject': lesson.subject.name,
                    'lessonRoom': lesson.classroom,
                    'lessonCanceled': lesson.canceled,
                    'lessonStatus': lesson.status,
            })
            index += 1
            dateLesson = dateLesson + timedelta(days = 1)
        lessonList = jsondata
        print('LESSONlist: ', lessonList)
        if lessonList:

           for lesson in lessonList["lessons"]:
               myLesson = Lesson(studentname,lesson)
               self.addLesson(myLesson)
#               print('Avg: ',average)

        else:
            logging.error("Average list is empty")

    def addLesson(self,lesson):
        self.lessonList.append(lesson)

    def getHomeworkList(self):
        self.isConnected = False
        client = pronotepy.Client('https://'+prefix_url+'.index-education.net/pronote/eleve.html', username, password, ent)
        if client.logged_in:
           self.isConnected = True
        else:
           logging.error("Error while authenticating when calling")
           return

        jsondata = {}

        jsondata['homework'] = []
        index = 0
        dateHomework = date.today() + timedelta(days = 10)
        #Get lessons over X period
        while index <= homeworkDays:
            print('index:', index)
            print('dateHW', dateHomework)
            homework = client.homework(dateHomework)
            for hw in homework:
                jsondata['homework'].append({
                    'hid': hw.id,
                    'homeworkSubject': hw.subject.name,
                    'homeworkDescription': hw.description,
                    'homeworkDone': hw.done,
                    'homeworkDate': hw.date.strftime("%Y/%m/%d"),
            })
            index += 1
            dateHomework = dateHomework + timedelta(days = 1)
        homeworkList = jsondata
        print('Homeworklist: ', homeworkList)
        if homeworkList:

           for homework in homeworkList["homework"]:
               myHomework = Homework(studentname,homework)
               self.addHomework(myHomework)

        else:
            logging.error("Homework list is empty")

    def addHomework(self,homework):
        self.homeworkList.append(homework)


class Grade:
    
    # Constructor
    def __init__(self, student, grade):
        
        # Init attributes
        self.pid = None
        self.periodName = None
        self.periodStart = None
        self.periodEnd = None
        self.gid = None
        self.student = None
        self.date = None
        self.subject = None
        self.grade = None
        self.outOf = None
        self.defaultOutOf = None
        self.coefficient = None
        self.average = None
        self.max = None
        self.min = None

        self.pid = grade["pid"]
        self.periodName = grade["periodName"]
        self.periodStart = grade["periodStart"]
        self.periodEnd = grade["periodEnd"]
        self.gid = grade["gid"]
        self.student = studentname
        self.date = grade["date"]
        self.subject = grade["subject"]
        self.grade = grade["grade"]
        self.outOf = grade["outOf"]
        self.defaultOutOf = grade["defaultOutOf"]
        self.coefficient = grade["coefficient"]
        self.average = grade["average"]
        self.max = grade["max"]
        self.min =  grade["min"]


    # Store measure to database
    def store(self,db):

        dbTable = "grades"

        if dbTable:
            logging.debug("Store grades %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",self.pid,self.periodName,self.periodStart,self.periodEnd, \
                          self.gid,self.student,str(self.date),self.subject,self.grade,self.outOf,self.defaultOutOf,self.coefficient,self.average,self.max,self.min)
            grade_query = f"INSERT OR REPLACE INTO grades VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            db.cur.execute(grade_query, [self.pid,self.periodName,self.periodStart,self.periodEnd,self.gid,self.student,self.date,self.subject,self.grade,self.outOf,self.defaultOutOf,self.coefficient,self.average,self.max,self.min])

class Average:

    # Constructor
    def __init__(self, studentname, average):

        # Init attributes
        self.pid = None
        self.periodName = None
        self.periodStart = None
        self.periodEnd = None
        self.studentname = None
        self.student = None
        self.classAverage = None
        self.max = None
        self.min = None
        self.outOf = None
        self.defaultOutOf = None
        self.subject = None

        self.pid = average["pid"]
        self.periodName = average["periodName"]
        self.periodStart = average["periodStart"]
        self.periodEnd = average["periodEnd"]
        self.studentname = studentname
        self.student = average["student"]
        self.classAverage = average["classAverage"]
        self.max = average["max"]
        self.min = average["min"]
        self.outOf = average["outOf"]
        self.defaultOutOf = average["defaultOutOf"]
        self.subject = average["subject"]

    # Store measure to database
    def store(self,db):

        dbTable = "averages"

        if dbTable:
            logging.debug("Store averages %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",self.pid,self.periodName,self.periodStart,self.periodEnd,self.studentname,self.student,self.classAverage,self.max,self.min, \
                         self.outOf,self.defaultOutOf,self.subject)
            average_query = f"INSERT OR REPLACE INTO averages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            db.cur.execute(average_query, [self.pid,self.periodName,self.periodStart,self.periodEnd,self.studentname,self.student,self.classAverage,self.max,self.min,self.outOf,self.defaultOutOf,self.subject])

class Evaluation:

    # Constructor
    def __init__(self, studentname, eval):

        # Init attributes
        self.pid = None
        self.periodName = None
        self.periodStart = None
        self.periodEnd = None
        self.studentname = None
        self.eid = None
        self.evalName = None
        self.evalDomain = None
        self.evalTeacher = None
        self.evalCoefficient = None
        self.evalDescription = None
        self.evalSubject = None
        self.evalDate = None

        self.pid = eval["pid"]
        self.periodName = eval["periodName"]
        self.periodStart = eval["periodStart"]
        self.periodEnd = eval["periodEnd"]
        self.studentname= studentname
        self.eid = eval["eid"]
        self.evalName = eval["evalName"]
        self.evalDomain = eval["evalDomain"]
        self.evalTeacher = eval["evalTeacher"]
        self.evalCoefficient = eval["evalCoefficient"]
        self.evalDescription = eval["evalDescription"]
        self.evalSubject = eval["evalSubject"]
        self.evalDate = eval["evalDate"]

    # Store measure to database
    def store(self,db):

        dbTable = "evaluations"

        if dbTable:
            logging.debug("Store evaluations %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",self.pid,self.periodName,self.periodStart,self.periodEnd,self.studentname,self.eid,self.evalName,self.evalDomain,self.evalTeacher,self.evalCoefficient,self.evalDescription,self.evalSubject,self.evalDate)
            eval_query = f"INSERT OR REPLACE INTO evaluations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            db.cur.execute(eval_query, [self.pid,self.periodName,self.periodStart,self.periodEnd,self.studentname,self.eid,self.evalName,self.evalDomain,self.evalTeacher,\
                          self.evalCoefficient,self.evalDescription,self.evalSubject,self.evalDate])

class Lesson:

    # Constructor
    def __init__(self, studentname, lesson):

        # Init attributes
        self.lid = None
        self.studentname = None
        self.lessonDateTime = None
        self.lessonStart = None
        self.lessonEnd = None
        self.lessonSubject = None
        self.lessonRoom = None
        self.lessonCanceled = None
        self.lessonStatus = None

        self.lid = lesson["lid"]
        self.studentname= studentname
        self.lessonDateTime = lesson["lessonDateTime"]
        self.lessonStart = lesson["lessonStart"]
        self.lessonEnd = lesson["lessonEnd"]
        self.lessonSubject = lesson["lessonSubject"]
        self.lessonRoom = lesson["lessonRoom"]
        self.lessonCanceled = lesson["lessonCanceled"]
        self.lessonStatus = lesson["lessonStatus"]

    # Store measure to database
    def store(self,db):

        dbTable = "lessons"

        if dbTable:
            logging.debug("Store lessons %s, %s, %s, %s, %s, %s, %s, %s, %s",self.lid,self.studentname,self.lessonDateTime,self.lessonStart,self.lessonEnd,self.lessonSubject,self.lessonRoom,self.lessonCanceled,self.lessonStatus)
            lesson_query = f"INSERT OR REPLACE INTO lessons VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            db.cur.execute(lesson_query, [self.lid,self.studentname,self.lessonDateTime,self.lessonStart,self.lessonEnd,self.lessonSubject,self.lessonRoom,self.lessonCanceled,self.lessonStatus])



class Period:

    # Constructor
    def __init__(self, period):

        # Init attributes
        self.pid = None
        self.periodName = None
        self.periodStart = None
        self.periodEnd = None

        self.pid = period["pid"]
        self.periodName = period["periodName"]
        self.periodStart = period["periodStart"]
        self.periodEnd = period["periodEnd"]

    # Store measure to database
    def store(self,db):

        dbTable = "periods"

        if dbTable:
            logging.debug("Store periods %s, %s, %s, %s",self.pid,self.periodName,self.periodStart,self.periodEnd)
            period_query = f"INSERT OR REPLACE INTO periods VALUES (?, ?, ?, ?)"
            db.cur.execute(period_query, [self.pid,self.periodName,self.periodStart,self.periodEnd])

class Homework:

    # Constructor
    def __init__(self,studentname,homework):

        # Init attributes
        self.hid = None
        self.studentname = None
        self.homeworkSubject = None
        self.homeworkDescription = None
        self.homeworkDone = None
        self.homeworkDate = None

        self.hid = homework["hid"]
        self.studentname = studentname
        self.homeworkSubject = homework["homeworkSubject"]
        self.homeworkDescription = homework["homeworkDescription"]
        self.homeworkDone = homework["homeworkDone"]
        self.homeworkDate = homework["homeworkDate"]

    # Store measure to database
    def store(self,db):

        dbTable = "homework"

        if dbTable:
            logging.debug("Store homework %s, %s, %s, %s, %s, %s",self.hid,self.studentname,self.homeworkSubject,self.homeworkDescription,self.homeworkDone,self.homeworkDate)
            period_query = f"INSERT OR REPLACE INTO homework VALUES (?, ?, ?, ?, ?, ?)"
            db.cur.execute(period_query, [self.hid,self.studentname,self.homeworkSubject,self.homeworkDescription,self.homeworkDone,self.homeworkDate])
