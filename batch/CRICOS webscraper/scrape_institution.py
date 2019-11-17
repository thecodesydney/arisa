from selenium import webdriver
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
# 4. Run this script - python scrape_course.py
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

url = 'http://cricos.education.gov.au/Institution/InstitutionSearch.aspx'
#state = 'Australian Capital Territory'
state = 'New South Wales'
#state = 'Northern Territory'
#state = 'Queensland'
#state = 'South Australia'
#state = 'Tasmania'
#state = 'Victoria'
#state = 'Western Australia'
now = datetime.now()
log_filename=now.strftime('%Y%m%d_%H%M') + '_log_inst.txt'
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
elem_state = driver.find_element_by_id('ctl00_cphDefaultPage_institutionSearchCriteria_ddlCourseLocation')
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
    num_pages = int(txt[i+3:i+5].rstrip())
    log += output('Pages: ' + str(num_pages))

    # build page number links
    # remember page link starts from page 2
    for i in range(num_pages-1):
        pages.append('a[href*="Page$' + str(i+2) + '"]')

# keep looping through all pages
for page_index in range(num_pages):
    # get list of institutes (id) on page and store in list
    elem_all_inst = driver.find_elements_by_css_selector('span[id^="ctl00_cphDefaultPage_institutionList_gridSearchResults_"]')
    # store all the ids in a list
    # you need to store id , otherwise if you click back you will get an error stale reference
    all_id = []
    for i in elem_all_inst:
        all_id.append(i.get_attribute('id'))

    # loop through each institute on current page
    for id in all_id:
        # click on institution to view details
        elem_inst = driver.find_element_by_id(id)
        log += output('Loop: ' + id + ' ' + getElementById('ctl00_cphDefaultPage_institutionDetail_lblInstitutionName'))
        elem_inst.click()

        # create institute db object
        new_inst = Institute(cricos_prov_code = getElementById('ctl00_cphDefaultPage_institutionDetail_lblProviderCode'), \
                trading_name = getElementById('ctl00_cphDefaultPage_institutionDetail_lblInstitutionTradingName'), \
                inst_name = getElementById('ctl00_cphDefaultPage_institutionDetail_lblInstitutionName'), \
                inst_type = getElementById('ctl00_cphDefaultPage_institutionDetail_lblInstitutionType'), \
                conditions = getElementById('ctl00_cphDefaultPage_institutionDetail_lblCRICOSConditions'), \
                total_capacity = getElementById('ctl00_cphDefaultPage_institutionDetail_lblLocationCapacity'), \
                website = getElementById('ctl00_cphDefaultPage_institutionDetail_hplInstitutionWebAddress'), \
                inst_post_address = getElementById('ctl00_cphDefaultPage_institutionDetail_lblInstitutionPostalAddress'), \
                page = page_index+1,
                state = state)

        # click on contact
        elem_tab_con = driver.find_element_by_css_selector('a[href="#contact"]')
        elem_tab_con.click()

        # create contacts principal exec db object
        # do only if there is principal contact name
        if getElementById('ctl00_cphDefaultPage_contactDetail_litPrincipalExecutiveOfficerName'):
            new_contact_pe = ContactPrincipal(name = getElementById('ctl00_cphDefaultPage_contactDetail_litPrincipalExecutiveOfficerName'), \
                    title = getElementById('ctl00_cphDefaultPage_contactDetail_litPrincipalExcutiveOfficerTitle'), \
                    phone = getElementById('ctl00_cphDefaultPage_contactDetail_litPrincipalExcutiveOfficerPhoneNumber'), \
                    fax = getElementById('ctl00_cphDefaultPage_contactDetail_litPrincipalExcutiveOfficerFaxNumber'), \
                    page = page_index+1)
            # add entry to contact principal table and link to institute table
            new_inst.contact_principal.append(new_contact_pe)

        # create contacts international student db object
        # do only if there is int student contact name
        if getElementById('ctl00_cphDefaultPage_contactDetail_litInternationalStudentContactName'):
            new_contact_is = ContactIntStudent(name = getElementById('ctl00_cphDefaultPage_contactDetail_litInternationalStudentContactName'), \
                    title = getElementById('ctl00_cphDefaultPage_contactDetail_litInternationalStudentContactTitle'), \
                    phone = getElementById('ctl00_cphDefaultPage_contactDetail_litInternationalStudentContactPhoneNumber'), \
                    fax = getElementById('ctl00_cphDefaultPage_contactDetail_litInternationalStudentContactFaxNumber'), \
                    email = getElementById('ctl00_cphDefaultPage_contactDetail_lnkEmailAddress'), \
                    page = page_index+1)
            # add entry to contact int student table and link to institute table
            new_inst.contact_int_student.append(new_contact_is)

        session.add(new_inst)

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
    if (page_index+1 < num_pages):
        print(pages[page_index])
        elem_page = driver.find_element_by_css_selector(pages[page_index])
        elem_page.click()
        time.sleep(1)

    # write log to file
    with open(log_filename,'a') as out_file:
        out_file.write(log)
    log = ''

#close browser window
#driver.close()
