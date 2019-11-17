import mysql.connector
from fuzzysearch import find_near_matches
import locale
import re
locale.setlocale(locale.LC_ALL, 'en_US')


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="12er34ty",
  database="arisa"
)

report_extracted_flag = 'N'
mycursor = mydb.cursor()
mycursor.execute('select * from leads where report_extracted_flag = %s', [report_extracted_flag])
results = mycursor.fetchall()
'''
0|id
1|session_id
2|email
3|country_of_origin
4|nationality
5|date_of_birth
6|education
7|target_city
8|course
9|course_keyword
10|school
11|arrival_date
12|stay_permanently_flag
13|report_sent_flag
14|download_count
15|report_name
'''
i = 0
while i < len(results):
    results_list = list(results[i])
    session_id = results_list[1]
    email = results_list[2]
    country_of_origin = results_list[3]
    nationality = results_list[4]
    date_of_birth = results_list[5]
    education = results_list[6]
    target_city = results_list[7]
    course = results_list[8]
    course_keyword = results_list[9]
    school = results_list[10]
    arrival_date = results_list[11]
    stay_permanently_flag = results_list[12]
    report_sent_flag = results_list[13]
    download_count = results_list[14]
    report_name = results_list[15]
    print ('Session ID : ' + session_id)
    print ('#############################################################################')
    print ('#####                       ARISA MATCH REPORT                          #####')
    print ('#############################################################################')
    print ('Email               : ' + email)
    print ('Country of Origin   : ' + country_of_origin)
    print ('Nationality         : ' + nationality)
    print ('Date of Birth       : ' + date_of_birth)
    print ('Education           : ' + education)
    print ('Target City         : ' + target_city)
    print ('Course              : ' + course)
    print ('Course Keyword      : ' + course_keyword)
    print ('School              : ' + school)
    print ('Arrival Date        : ' + arrival_date)
    print ('Stay Permanently    : ' + stay_permanently_flag)

    mycursor_course = mydb.cursor()
    mycursor_course.execute('select * from course')
    results_course = mycursor_course.fetchall()
    '''
    Course Table Columns
    0 | id
    1 | course_name
    2 | course_sector
    3 | cricos_course_code
    4 | vet_nat_code
    5 | dual_qual
    6 | broad_field
    7 | narrow_field
    8 | detailed_field
    9 | course_level
    10 | foundation_studies
    11 | work_component
    12 | course_language
    13 | duration
    14 | tuition_fee
    15 | non_tuition_fee
    16 | total_cost
    17 | inst_id
    18 | page
    19 | state
    20 | update_date
    '''
    print ('-----------------------------------------------------------------------------')
    print('Potential Courses and Institutions Matches   ')
    print ('-----------------------------------------------------------------------------')
    inst_count = 0
    j = 0
    while j < len(results_course):
        results_course_list = list(results_course[j])
        course_name = results_course_list[1]
        course_sector = results_course_list[2]
        cricos_course_code = results_course_list[3]
        vet_nat_code = results_course_list[4]
        dual_qual = results_course_list[5]
        broad_field = results_course_list[6]
        narrow_field = results_course_list[7]
        detailed_field = results_course_list[8]
        course_level = results_course_list[9]
        foundation_studies = results_course_list[10]
        work_component = results_course_list[11]
        course_language = results_course_list[12]
        duration = results_course_list[13]
        tuition_fee = results_course_list[14]
        non_tution_fee = results_course_list[15]
        total_cost = results_course_list[16]
        inst_id = results_course_list[17]
        page = results_course_list[18]
        state = results_course_list[19]
        update_date = results_course_list[20]

        # Check broad_field and narrow_field
        if course != '':
            #Fuzzysearch on Course
            broad_field_match_flag = find_near_matches(course,broad_field, max_deletions=3, max_insertions=3, max_substitutions=3)
            if course_keyword is '':
                course_keyword = ' '
            course_name_match_flag = find_near_matches(course_keyword,course_name, max_deletions=3, max_insertions=3, max_substitutions=3)
            if ('Match' in str(broad_field_match_flag)) and ('Match' in str(course_name_match_flag)):
            #if ('Match' in str(broad_field_match_flag)):
                mycursor_institute = mydb.cursor()
                mycursor_institute.execute('select * from institute where id = %s', [inst_id])
                results_institute = mycursor_institute.fetchall()
                '''
                0 | id
                1 | cricos_prov_code
                2 | trading_name
                3 | inst_name
                4 | inst_type
                5 | conditions
                6 | total_capacity
                7 | website
                8 | inst_post_address
                9 | page
                10 | update_date
                11 | state
                '''
                k = 0
                while k < len(results_institute):
                    results_institute_list = list(results_institute[k])
                    cricos_prov_code = results_institute_list[1]
                    trading_name = results_institute_list[2]
                    inst_name = results_institute_list[3]
                    inst_type = results_institute_list[4]
                    conditions = results_institute_list[5]
                    total_capacity = results_institute_list[6]
                    website = results_institute_list[7]
                    inst_post_address = results_institute_list[8]
                    page = results_institute_list[9]
                    update_date = results_institute_list[10]
                    state = results_institute_list[11]

                    mycursor_institute_address = mydb.cursor()
                    mycursor_institute_address.execute('select * from institute_address where id = %s', [inst_id])
                    results_institute_address = mycursor_institute_address.fetchall()
                    '''
                    0 | id
                    1 | inst_post_address
                    2 | suburb
                    3 | state
                    4 | postcode
                    5 | geocode
                    6 | gecode_level
                    7 | geocode_reliability
                    8 | gnafpidposition
                    '''
                    l = 0
                    while l < len(results_institute_address):
                        results_institute_address_list = list(results_institute_address[l])
                        inst_post_address = results_institute_address_list[1]
                        suburb = results_institute_address_list[2]
                        state = results_institute_address_list[3]
                        postcode = results_institute_address_list[4]
                        geocode = results_institute_address_list[5]
                        geocode_level = results_institute_address_list[6]
                        geocode_reliability = results_institute_address_list[7]
                        gnafpidposition = results_institute_address_list[8]

                        # Fuzzysearch on address
                        if target_city is '':
                            target_city = ' '
                        address_match_flag = find_near_matches(target_city, suburb, max_deletions=3, max_insertions=3, max_substitutions=3)
                        if 'Match' in str(address_match_flag):
                            print ('Course                : ' + course_name.strip())
                            print ('Institution           : ' + inst_name.strip())
                            print ('Tuition Fee           : $' + tuition_fee.strip())
                            print ('Total Capacity        : ' + str(locale.format_string("%d", total_capacity, grouping=True)))
                            print ('Website               : ' + website.strip())
                            print ('Suburb/State/Postcode : ' + suburb.strip()+" "+state.strip()+" "+postcode.strip())
                            print ('Last Update Date      : ' + str(update_date))
                            print ('-----------------------------------------------------------------------------')
                            inst_count += 1
                        l += 1
                    k += 1
        j += 1
    i += 1

    report_name = re.sub('[^a-zA-Z0-9 \n\.]', '', session_id).strip()+".txt"

    mycursor_update = mydb.cursor()
    mycursor_update.execute('update leads set report_extracted_flag = %s, report_name = %s where session_id = %s', ['Y', report_name, session_id])
    mydb.commit()
    if inst_count == 0:
       print ('No matching results found')
