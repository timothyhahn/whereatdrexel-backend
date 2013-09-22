import json
import urllib2

from models import BuildingLocation, CourseLocation
from whereatdrexel import db
from bs4 import BeautifulSoup


def load_buildings():
    json_data = open('building-locations.json').read()
    data = json.loads(json_data)
    locations_list = data['locations']
    for location in locations_list:
        bl = BuildingLocation(name=location['name'],description=location['description'],latitude=location['latitude'],longitude=location['longitude'],short_name=location['short_name'])
        db.session.add(bl)
    db.session.commit()


def load_courses():
    courses_json_data=open('courses.json').read()
    buildings_json_data=open('building-locations.json').read()
    
    courses = json.loads(courses_json_data)
    buildings = json.loads(buildings_json_data)
    
    for course in courses['courses']:
        course_building = course['building']
        latitude = 0.000
        longitude = 0.000
        if course_building == 'URBN' and 'ANNEX' in course['room']:
            course_building = 'URBN ANNEX'
    
        for building in buildings['locations']:
            if course_building == building['short_name']:
                latitude = building['latitude']
                longitude = building['longitude']
    
        
        short_name = course['subject'] + ' ' + course['course_number']
        name = short_name + ': ' + course['title']
    
        description = course['subject'] + ' ' + course['course_number'] + ': '  + course['title'] 
        description += '<hr />'
        description += 'Location: ' + course['building'] + ' ' + course['room'] + '<br />'
        description += 'Time: ' + course['time'] + '<br />'
        description += 'Instructor: ' + course['instructor']
    
        cl = CourseLocation(name=name, short_name=short_name, description=description, latitude=latitude, longitude=longitude)
        db.session.add(cl)
    
    db.session.commit()


def download_courses():
    courses_list = list()
    
    root_response = urllib2.urlopen("https://duapp2.drexel.edu/webtms_du/app?component=collSubj&page=CollegesSubjects&service=direct&sp=ZH4sIAAAAAAAAADWLTQ6CMBBGR4w%2Fa%2BNeLmChoiuXGldsjFxgpBNS0yK0g7LyRF7NO1hD%2FJbve%2B%2F9gYl3sCLVCeWoJyO0Y%2FGkK1svFDKKgpyFYaMIxjnMsORCW2JY5jd8YOJbk%2FyAZ7TNPoc5h%2BRwV8FYDIbBukou7HRd%2Ff8j%2BbKFF0R90zBMN6nM5C4EJzQmPnfoghTLbC23Xw08naqkAAAA&sp=0")
    root_html = root_response.read()
    
    root_soup = BeautifulSoup(root_html)
    
    for college_link in root_soup.find(id="sideLeft").find_all("a"):
        print college_link.get("href")
        college_response = urllib2.urlopen("https://duapp2.drexel.edu" + college_link.get("href"))
        college_html = college_response.read()
    
        college_soup = BeautifulSoup(college_html)
        
        for subject_link in college_soup.find("table", {"class": "collegePanel"}).find_all("a"):
            print subject_link.get("href")
            subject_response = urllib2.urlopen("https://duapp2.drexel.edu" + subject_link.get("href"))
            subject_html = subject_response.read()
            
            subject_soup = BeautifulSoup(subject_html)
    
            for course_link in subject_soup.find("table", {"bgcolor": "#cccccc"}).find_all("a"):
                print course_link.get("href")
                course_response = urllib2.urlopen("https://duapp2.drexel.edu" + course_link.get("href"))
                course_html = course_response.read()
                course_soup = BeautifulSoup(course_html)
                table = course_soup.find("table", {"bgcolor": "#cccccc"})
                course_dict = dict()
                course_dict["crn"] = table.find_all("tr")[0].find_all("td")[1].get_text()
                course_dict["subject"] = table.find_all("tr")[1].find_all("td")[1].get_text()
                course_dict["course_number"] = table.find_all("tr")[2].find_all("td")[1].get_text()
                course_dict["title"] = table.find_all("tr")[5].find_all("td")[1].get_text()
                course_dict["instructor"] = table.find_all("tr")[7].find_all("td")[1].get_text()
                date_table = course_soup.find("table", {"bgcolor": "cccccc"})
                
                course_dict["building"] = date_table.find_all("tr")[1].find_all("td")[4].get_text() 
                course_dict["room"] = date_table.find_all("tr")[1].find_all("td")[5].get_text() 
                print date_table.find_all("tr")[1].find_all("td")[4].get_text() + date_table.find_all("tr")[1].find_all("td")[5].get_text()
                courses_list.append(course_dict)
    
    courses_dict = dict()
    
    courses_dict['courses'] = courses_list
    with open("courses.json", "w") as jsonfile:
        json.dump(courses_dict, jsonfile)
