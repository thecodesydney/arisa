from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Institute, ContactPrincipal, ContactIntStudent, Course, CourseLocation, Base
from datetime import datetime

##################
# Prerequisites / Instructions
# 1. Install Chrome webdriver for Selenium.
# 2. Set up MySQL. Run python models.py to create the tables
# 3. Change the variable state below to state you want to search
# 4. Set page to start searching. Default is 1
# 5. Run this script - python scrape_course.py
##################

##################
# db init
# from https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
##################

engine = create_engine('mysql+pymysql://kevin:Sydn3y30@localhost:3306/cricos')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

##################
# Config
##################

url = 'http://cricos.education.gov.au/Course/CourseSearch.aspx'
# state = 'Australian Capital Territory'
# state = 'New South Wales'
# state = 'Northern Territory'
# state = 'Queensland'
# state = 'South Australia'
# state = 'Tasmania'
# state = 'Victoria'
state = 'Western Australia'
goto_page = 1
now = datetime.now()
log_filename=now.strftime('%Y%m%d_%H%M') + '_log_course.txt'
# string to write to file
log = ''

##################
# Helper functions
##################
# not all fields are in every record so need to catch exception


def getElementById(id):
    try:
        elem = driver.find_element_by_id(id).text
    except NoSuchElementException:
        elem = ''
    return elem


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# print to screen and write to log file
def output(s):
    print(s)
    return (s+'\n')

##################
# Script begin
##################

log += output(state)

# Headless Chrome
opt = Options()
opt.headless = True
driver = webdriver.Chrome(options=opt)
driver.get(url)

# select the state
elem_state = driver.find_element_by_id('ctl00_cphDefaultPage_courseSearchCriteria_ddlCourseLocation')
Select(elem_state).select_by_visible_text(state)

# click submit button
elem_submit = driver.find_element_by_id('ctl00_cphDefaultPage_btnSearch')
elem_submit.click()
time.sleep(2)

# get page numbers
num_pages = 1
pages = []
soup = BeautifulSoup(driver.page_source,'html.parser')
elem_page = soup.find('tr',class_='gridPager')
if elem_page:
    txt = elem_page.select('span[style="cursor:default;"]')
    if txt:
        txt = txt[0].get_text()

    # find index location of substring "of" as in Page 1 of 20
    i = txt.index('of')
    num_pages = int(txt[i+3:i+6].rstrip())
    log += output('Pages: ' + str(num_pages))

    # build page number links
    # remember page link starts from page 2
    for i in range(num_pages-1):
        pages.append('a[href*="Page$' + str(i+2) + '"]')

    # check if goto_page is actually valid, if not then ignore setting
    if (goto_page <= 1) or (goto_page > num_pages):
        goto_page = 1

np = 1
# might need to jump to a certain page
while goto_page != 1:
    # loop until you reach the page
    try:
        elem_np = driver.find_element_by_css_selector('a[href*="Page$'+str(goto_page)+'"]')
        elem_np.click()
        log += output('jump to page '+str(goto_page))
        break
    except NoSuchElementException:
        np+=10
        elem_np = driver.find_element_by_css_selector('a[href*="Page$'+str(np)+'"]')
        elem_np.click()
        log += output('jump to page '+str(np))

# keep looping through all pages
for page_index in range(goto_page,num_pages+1):
    # get list of courses with matched css
    elem_all_course = driver.find_elements_by_css_selector('tr[onclick*="click-"]')
    # store all the ids in a list
    # you need to store id , otherwise if you click back you will get an error stale reference
    all_id = []
    for i in range(len(elem_all_course)):
        all_id.append('click-'+str(i))

    # loop through each course
    for id in all_id:
        # click on course to view details
        elem_course = driver.find_element_by_css_selector('tr[onclick*="'+id+'"]')
        log += output('Loop: ' + id + ' ' + elem_course.text)
        elem_course.click()

        # create course db object
        new_course = Course (course_name = getElementById('ctl00_cphDefaultPage_courseDetail_lblCourseName'), \
                course_sector = getElementById('ctl00_cphDefaultPage_courseDetail_lblCourseSector'), \
                cricos_course_code = getElementById('ctl00_cphDefaultPage_courseDetail_lblCourseCode'), \
                vet_nat_code = getElementById('ctl00_cphDefaultPage_courseDetail_lblVetNationalCode'), \
                dual_qual = getElementById('ctl00_cphDefaultPage_courseDetail_lblDualQualification'), \
                broad_field = getElementById('ctl00_cphDefaultPage_courseDetail_lblFieldOfEducationBroad1'), \
                narrow_field = getElementById('ctl00_cphDefaultPage_courseDetail_lblFieldOfEducationNarrow1'), \
                detailed_field = getElementById('ctl00_cphDefaultPage_courseDetail_lblFieldOfEducationDetailed1'), \
                course_level = getElementById('ctl00_cphDefaultPage_courseDetail_lblCourseLevel'), \
                foundation_studies = getElementById('ctl00_cphDefaultPage_courseDetail_lblFoundationStudies'), \
                work_component = getElementById('ctl00_cphDefaultPage_courseDetail_lblWorkComponent'), \
                course_language = getElementById('ctl00_cphDefaultPage_courseDetail_lblCourseLanguage'), \
                duration = getElementById('ctl00_cphDefaultPage_courseDetail_lblDuration'), \
                tution_fee = getElementById('ctl00_cphDefaultPage_courseDetail_lblTuition'), \
                non_tution_fee = getElementById('ctl00_cphDefaultPage_courseDetail_lblNonTuition'), \
                total_cost = getElementById('ctl00_cphDefaultPage_courseDetail_lblTotalCourseCost'), \
                page = page_index, \
                state = state)

        # click on location
        elem_tab_loc = driver.find_element_by_css_selector('a[href="#location"]')
        elem_tab_loc.click()

        elem_all_loc = []
        try:
            elem_all_loc = driver.find_elements_by_css_selector('span[id^="ctl00_cphDefaultPage_courseLocationList_gridSearchResults"]')
        except NoSuchElementException:
            log += output('No locations found')

        for elem_loc in elem_all_loc:
            # create location db object
            new_loc = CourseLocation(location = elem_loc.text, page = page_index)
            # add entry to course location table and link to course table
            new_course.course_location.append(new_loc)

        # click on institute
        elem_tab_inst = driver.find_element_by_css_selector('a[href="#institution"]')
        elem_tab_inst.click()
        # get Cricos provider code
        elem_prov_code = driver.find_element_by_id('ctl00_cphDefaultPage_institutionDetail_lnkProviderCode')
        # get institute db object
        inst_db = session.query(Institute).filter(Institute.cricos_prov_code == elem_prov_code.text).first()
        # shouldnt be null but if it is dont do anything
        if inst_db:
            inst_db.course.append(new_course)
            session.add(inst_db)
        else:
            #skip it if institution not found
            log += output('cricos provider id not found, course skipped')

        # go back to previous page and get the next institute
        driver.back()
        # click results tab to make sure you are on results tab
        elem_tab_res = driver.find_element_by_css_selector('a[href="#results"]')
        elem_tab_res.click()
        time.sleep(1)

    # commit to database at the end of every page
    session.commit()
    log += output('Database committed')

    # go to next page
    if (page_index < num_pages):
        log += output(pages[page_index-1])
        elem_page = driver.find_element_by_css_selector(pages[page_index-1])
        elem_page.click()
        time.sleep(1)

    # write log to file
    with open(log_filename,'a') as out_file:
        out_file.write(log)
    log = ''


#close browser window
#driver.close()
