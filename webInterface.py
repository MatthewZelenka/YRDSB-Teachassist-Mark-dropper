import requests
from bs4 import BeautifulSoup, ResultSet
import getpass
import htmlmin

url = "https://ta.yrdsb.ca/live/"

def login(session:requests.Session, username:str, password:str):
    webResponse = session.get(url)
    soup = BeautifulSoup(webResponse.content, "html.parser")
    loginData = {
        "subject_id": soup.find('input', attrs={"name": "subject_id"})["value"],
        "username": username,
        "password": password,
        "submit": soup.find('input', attrs={"name": "submit"})["value"]
    }
    return session.post(url=url, data=loginData)

def _courseTableIndex(tables: ResultSet, header:list):
        for table in tables:
            if [col.getText() for col in table.findAll('tr')[0]] == header:
                return tables.index(table)

def getCourses(session:requests.Session, userPageUrl:str):
    webResponse = session.get(userPageUrl)
    # print(webResponse.content)
    soup = BeautifulSoup(htmlmin.minify(webResponse.text, remove_empty_space=True), "html.parser")
    tables = soup.findAll('table')
    
    def _getUrl(bs4Object:BeautifulSoup):
        try:
            return bs4Object.find("a")["href"] #BeautifulSoup(html, "html.parser")
        except Exception:
            return None
        
    courses = [
            {
                "courseCode":list(row)[0].getText().split("  ")[0].split(":")[0].lstrip().rstrip(),
                "courseName":list(row)[0].getText().split("  ")[0].split(":")[1].lstrip().rstrip(),
                "timeSlot":list(row)[0].getText().split("  ")[1].split("-")[0].lstrip().rstrip(),
                "roomNumber":list(row)[0].getText().split("  ")[1].split("-")[1].lstrip().rstrip(),
                "date":list(row)[1].getText(),
                "mark": float(list(row)[3].getText().split("current mark =")[-1].lstrip().rstrip().removesuffix('%')) if list(row)[3].getText().split("current mark =")[-1].lstrip().rstrip().removesuffix('%') != "Please see teacher for current status regarding achievement in the course" else None,
                "url":url+"students/"+_getUrl(list(row)[3]) if list(row)[3].getText().split("current mark =")[-1].lstrip().rstrip().removesuffix('%') != "Please see teacher for current status regarding achievement in the course" else None,
            } for row in tables[_courseTableIndex(tables=tables, header=['Course Name', 'Date', 'Mark'])].findAll('tr')[1:]
        ] #
    # for row in tables[_courseTableIndex(tables=tables, header=['Course Name', 'Date', 'Mark'])].findAll('tr')[1:]: # code to see table
    #     print([[col.getText(), _getUrl(col)] for col in row])
    return courses

def getCourseData(session:requests.Session, coursePageUrl:str):
    webResponse = session.get(coursePageUrl)
    # print(webResponse.content)
    soup = BeautifulSoup(htmlmin.minify(webResponse.text, remove_empty_space=True), "html.parser")
    tables = soup.findAll('table')
    # for row in tables[_courseTableIndex(tables=tables, header=['Assignment', 'Knowledge / Understanding', 'Thinking', 'Communication', 'Application'])].findAll('tr')[1:]: # code to see table
    #     print([col.getText() for col in row])
    course = {
        "weighting":{list(row)[0].getText().replace(" ", ""): list(row)[-2].getText().removesuffix('%') for row in tables[_courseTableIndex(tables=tables, header=['Category', 'Weighting', 'Course Weighting', 'Student Achievement'])].findAll('tr')[1:]},
        "assignment":{list(row)[0].getText():{'Knowledge/Understanding':{"mark":eval(list(row)[1].getText().split("=")[0]) if list(row)[1].getText() != "" and "no mark" not in list(row)[1].getText() and "no weight" not in list(row)[1].getText() else None,"weight":list(row)[1].getText().split("=")[-1] if list(row)[1].getText() != "" and "no mark" not in list(row)[1].getText() and "no weight" not in list(row)[1].getText() else None}, 'Thinking':{"mark":eval(list(row)[2].getText().split("=")[0]) if list(row)[2].getText() != "" and "no mark" not in list(row)[2].getText() and "no weight" not in list(row)[2].getText() else None,"weight":list(row)[2].getText().split("=")[-1] if list(row)[2].getText() != "" and "no mark" not in list(row)[2].getText() and "no weight" not in list(row)[2].getText() else None}, 'Communication':{"mark":eval(list(row)[3].getText().split("=")[0]) if list(row)[3].getText() != "" and "no mark" not in list(row)[3].getText() and "no weight" not in list(row)[3].getText() else None,"weight":list(row)[3].getText().split("=")[-1] if list(row)[3].getText() != "" and "no mark" not in list(row)[3].getText() and "no weight" not in list(row)[3].getText() else None}, 'Application':{"mark":eval(list(row)[4].getText().split("=")[0]) if list(row)[4].getText() != "" and "no mark" not in list(row)[4].getText() and "no weight" not in list(row)[4].getText() else None,"weight":list(row)[4].getText().split("=")[-1] if list(row)[4].getText() != "" and "no mark" not in list(row)[4].getText() and "no weight" not in list(row)[4].getText() else None}} for row in tables[_courseTableIndex(tables=tables, header=['Assignment', 'Knowledge / Understanding', 'Thinking', 'Communication', 'Application'])].findAll('tr')[1:] if len(row) > 1
        }
    }
    # print(course)
    return course

if __name__ == '__main__':
    with requests.Session() as s:
        responseData = login(session=s, username=input('username: '), password=getpass.getpass(prompt='password: '))
        print(responseData.url)
        coursesData = getCourses(session=s, userPageUrl=responseData.url)
        print(coursesData)
        getCourseData(session=s, coursePageUrl=coursesData[1]["url"])