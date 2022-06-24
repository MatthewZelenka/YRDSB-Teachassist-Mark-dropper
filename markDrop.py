import webInterface
import markCalc
import requests
import getpass
import copy
import math

def getLowestMarks(courseObject):
    correctWeightCourseObject = markCalc.getWeightOutOfOne(courseObject)
    markList = []
    for assignment in correctWeightCourseObject["assignment"]:
        for catagory in correctWeightCourseObject["assignment"][assignment]:
            if correctWeightCourseObject["assignment"][assignment][catagory]["mark"] != None and correctWeightCourseObject["assignment"][assignment][catagory]["weight"] != None:
                markRating = [math.sqrt(((1-float(correctWeightCourseObject["assignment"][assignment][catagory]["mark"]))**2)+((1-float(correctWeightCourseObject["assignment"][assignment][catagory]["weight"]))**2))-math.sqrt(((float(correctWeightCourseObject["assignment"][assignment][catagory]["mark"]))**2)+((1-float(correctWeightCourseObject["assignment"][assignment][catagory]["weight"]))**2)),["assignment",assignment,catagory]]
                # print(markRating)
                markList.append(markRating)
    sortedMarkList = sorted(markList, key=lambda x: x[0])
    return sortedMarkList

def removeLowestMark(courseObject):
    updatedCourseObject = copy.deepcopy(courseObject)
    markList = getLowestMarks(courseObject)
    updatedCourseObject[markList[-1][1][0]][markList[-1][1][1]][markList[-1][1][2]]["mark"] = None
    updatedCourseObject[markList[-1][1][0]][markList[-1][1][1]][markList[-1][1][2]]["weight"] = None
    return updatedCourseObject
if __name__ == '__main__':
    with requests.Session() as s:
        responseData = webInterface.login(session=s, username=input('username: '), password=getpass.getpass(prompt='password: '))
        # print(responseData.url)
        coursesData = webInterface.getCourses(session=s, userPageUrl=responseData.url)
        # print(coursesData)
        coursesDataWithUrls = [course for course in coursesData if coursesData[coursesData.index(course)]["url"] != None]
        for course in coursesData:
            print((str(coursesDataWithUrls.index(course))+") " if course in coursesDataWithUrls else "")+course["courseCode"])
        courseData = webInterface.getCourseData(session=s, coursePageUrl=coursesDataWithUrls[int(input("select class number: "))]["url"])
        # print(courseData)
        newMarks = copy.deepcopy(courseData)
        for markDrop in range(int(input("Amount of marks dropped: "))):
            buffer = newMarks
            newMarks = removeLowestMark(buffer)
            print(getLowestMarks(buffer)[-1][1])
            print(markCalc.getCourseMark(courseObject=newMarks))