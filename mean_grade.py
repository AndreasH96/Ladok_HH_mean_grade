from selenium import webdriver
import time
import sys
import re
import matplotlib.pyplot as plt
from getpass import getpass
# First, read user input 
plot_result_dict = {"y":True,"n":False}
institution = input("Institution\n")
username = input("Username:\n")
password = getpass("Password:\n")
plot_result = plot_result_dict[input("Plot results? (y/n):\n").lower()]
grade_pattern = "\d|U"

# Then start Chrome
driver = webdriver.Chrome()

# Using try/finally to make certain that the driver is closed on completion or if anything fails
try:
    # ======== Log in to website ==========

    driver.get("https://www.student.ladok.se/student/app/studentwebb/min-utbildning/avklarade")
    driver.find_element_by_class_name("btn-primary").click()
    time.sleep(0.5)
    driver.find_element_by_id("searchinput").send_keys(institution)
    time.sleep(0.5)
    driver.find_element_by_class_name("identityprovider").click()
    time.sleep(0.5)
    username_input, password_input = driver.find_elements_by_class_name("form-control")
    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element_by_class_name("btn").click()
    driver.get("https://www.student.ladok.se/student/app/studentwebb/min-utbildning/avklarade")
    # =====================================

    # ========== Get grade for every course taken ============= #
    time.sleep(0.5)
    
    elements = driver.find_element_by_class_name("ladok-accordian")
    





    course_links = [course.find_element_by_class_name("card-link").get_attribute("href") for course in  elements.find_elements_by_class_name("ladok-list-kort")]
    grades = []
    for link in course_links:
        try:
            driver.get(link)
            time.sleep(0.5)
            grade_element = driver.find_element_by_class_name("ladok-list-kort-header-rubrik")
        except:
            continue
        grade_match = re.findall(grade_pattern,grade_element.text)
        
        if len(grade_match) < 1:
            continue
        grade_number = 0 if grade_match[0] == "U" else int(grade_match[0])

        grades.append(grade_number)
    grade_mean = sum(grades)/len(grades)
    # ====================================================
    if plot_result:
        plt.title("Mean grade: {} ".format(grade_mean),fontsize= 20)
        grade_U = list(filter(lambda x: x == 0, grades))
        grade_3 = list(filter(lambda x: x == 3, grades))
        grade_4 = list(filter(lambda x: x == 4, grades))
        grade_5 = list(filter(lambda x: x == 5, grades))
        plt.bar(x=[2,3,4,5],height=[len(grade_U),len(grade_3),len(grade_4),len(grade_5)])
        plt.xticks(ticks=[2,3,4,5],labels=["U",3,4,5])
        plt.savefig("result.png")
        plt.show()
    else:
        print("Mean grade: {}".format(grade_mean))
finally:
    driver.close()
