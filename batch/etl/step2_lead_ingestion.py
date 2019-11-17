import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="12er34ty",
  database="arisa"
)

mycursor = mydb.cursor()
mycursor.execute('select * from chatlogs_session_ids')
results = mycursor.fetchall()

i = 0
while i < len(results):
    results_list = list(results[i])
    session_id = results_list[1]

    mycursor2 = mydb.cursor()
    mycursor2.execute('select * from chatlogs where session_id = %s', [session_id])
    results2 = mycursor2.fetchall()

    intent_ctr = 0
    j = 0

    session_id = ''
    email = ''
    country_of_origin = ''
    nationality = ''
    date_of_birth = ''
    education = ''
    target_city = ''
    course = ''
    course_keyword = ''
    school = ''
    arrival_date = ''
    stay_permanently_flag = ''
    report_extracted_flag = 'N'
    report_sent_flag = 'N'
    download_count = 0
    report_name = ''


    while j < len(results2):
        results_list2 = list(results2[j])
        session_id = results_list2[1]
        resolved_query = results_list2[3]
        intent_name = results_list2[4]
        if intent_name == 'StayPermanently':
            if '@' in resolved_query:
                email = resolved_query
                intent_ctr += 1
            else:
                stay_permanently_flag = resolved_query
                intent_ctr += 1
        if intent_name == 'CountryOfOrigin':
            country_of_origin = resolved_query
            intent_ctr += 1
        if intent_name == 'CountryOfOriginFallback1':
            country_of_origin = resolved_query
            intent_ctr += 1
        if intent_name == 'CountryOfOriginTry2':
            country_of_origin = resolved_query
            intent_ctr += 1
        if intent_name == 'Nationality':
            nationality = resolved_query
            intent_ctr += 1
        if intent_name == 'NationalityFallback1':
            nationality = resolved_query
            intent_ctr += 1
        if intent_name == 'NationalityTry2':
            nationality = resolved_query
            intent_ctr += 1
        if intent_name == 'Birthday':
            date_of_birth = resolved_query
            intent_ctr += 1
        if intent_name == 'BirthdayFallback1':
            date_of_birth = resolved_query
            intent_ctr += 1
        if intent_name == 'BirthdayTry2':
            date_of_birth = resolved_query
            intent_ctr += 1
        if intent_name == 'Education':
            education = resolved_query
            intent_ctr += 1
        if intent_name == 'EducationFallback1':
            education = resolved_query
            intent_ctr += 1
        if intent_name == 'EducationTry2':
            education = resolved_query
            intent_ctr += 1
        if intent_name == 'City':
            target_city = resolved_query
            intent_ctr += 1
        if intent_name == 'CityFallback1':
            target_city = resolved_query
            intent_ctr += 1
        if intent_name == 'CityTry2':
            target_city = resolved_query
            intent_ctr += 1
        if intent_name == 'Course':
            course = resolved_query
            intent_ctr += 1
        if intent_name == 'CourseFallback1':
            course = resolved_query
            intent_ctr += 1
        if intent_name == 'CourseTry2':
            course = resolved_query
            intent_ctr += 1
        if intent_name == 'CourseKeyword':
            course_keyword = resolved_query
            intent_ctr += 1
        if intent_name == 'CourseKeywordFallback1':
            course_keyword = resolved_query
            intent_ctr += 1
        if intent_name == 'CourseKeywordTry2':
            course_keyword = resolved_query
            intent_ctr += 1
        if intent_name == 'School':
            school = resolved_query
            intent_ctr += 1
        if intent_name == 'SchoolFallback1':
            school = resolved_query
            intent_ctr += 1
        if intent_name == 'SchoolTry2':
            school = resolved_query
            intent_ctr += 1
        if intent_name == 'ArrivalDate':
            arrival_date = resolved_query
            intent_ctr += 1
        if intent_name == 'ArrivalDateFallback1':
            arrival_date = resolved_query
            intent_ctr += 1
        if intent_name == 'ArrivalDateTry2':
            arrival_date = resolved_query
            intent_ctr += 1
        j += 1

    if '@' in email:
        print ('email:' + email)
        try:
            mycursor3 = mydb.cursor()
            mycursor3.execute('INSERT INTO leads \
                (session_id, email, country_of_origin, \
                nationality, date_of_birth, education, target_city, course, course_keyword,  \
                school, arrival_date, stay_permanently_flag, \
                report_extracted_flag, report_sent_flag, download_count, report_name) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', \
                        (session_id, email, country_of_origin, \
                         nationality, date_of_birth, education, target_city, course, course_keyword, \
                         school, arrival_date, stay_permanently_flag, \
                         report_extracted_flag, report_sent_flag, download_count, report_name))
            mydb.commit()
            print ('Session ID : ' + session_id + ' Inserted to leads database')
        except mysql.connector.Error as err:
            print("Insert to leads failed : {}".format(err))
    else:
        print ('Session ID : '+session_id+' No email found')
    intent_ctr = 0
    i += 1