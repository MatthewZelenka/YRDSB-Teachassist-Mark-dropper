import webInterface
import requests
import getpass
import copy

def _sumOfweights(courseObject):
    sumOfweights = {catagory:sum([float(assignment[catagory]["weight"]) for assignment in courseObject["assignment"].values() if catagory in assignment.keys() and assignment[catagory]["weight"] != None]) for catagory in list(courseObject["weighting"].keys())}
    return sumOfweights

def getCategoryMarks(courseObject):
    sumOfweights = _sumOfweights(courseObject)
    categoryMarks = {catagory:sum([((float(assignment[catagory]["weight"])*float(assignment[catagory]["mark"]))/sumOfweights[catagory]) for assignment in courseObject["assignment"].values() if catagory in assignment.keys() and assignment[catagory]["weight"] != None]) for catagory in list(courseObject["weighting"].keys())} # .values()[catagory]
    print(categoryMarks)

def getWeightOutOfOne(courseObject):
    weightChangedCourseObject = copy.deepcopy(courseObject)
    sumOfweights = _sumOfweights(courseObject)
    for assignment in weightChangedCourseObject["assignment"]:
        for catagory in weightChangedCourseObject["assignment"][assignment]:
            weightChangedCourseObject["assignment"][assignment][catagory]["weight"] = ((float(weightChangedCourseObject["assignment"][assignment][catagory]["weight"])/sumOfweights[catagory])*(float(weightChangedCourseObject["weighting"][catagory])/100)) if weightChangedCourseObject["assignment"][assignment][catagory]["weight"] != None else None
    weightMultiple = sum(_sumOfweights(weightChangedCourseObject).values())
    for assignment in weightChangedCourseObject["assignment"]:
        for catagory in weightChangedCourseObject["assignment"][assignment]:
            weightChangedCourseObject["assignment"][assignment][catagory]["weight"] = (float(weightChangedCourseObject["assignment"][assignment][catagory]["weight"])/weightMultiple) if weightChangedCourseObject["assignment"][assignment][catagory]["weight"] != None else None
    return weightChangedCourseObject

def getCourseMark(courseObject):
    weightChangedCourseObject = getWeightOutOfOne(courseObject)
    return sum([sum([((float(assignment[catagory]["weight"])*float(assignment[catagory]["mark"]))) for assignment in weightChangedCourseObject["assignment"].values() if catagory in assignment.keys() and assignment[catagory]["weight"] != None]) for catagory in list(weightChangedCourseObject["weighting"].keys())])



if __name__ == '__main__':
    with requests.Session() as s:
        responseData = webInterface.login(session=s, username=input('username: '), password=getpass.getpass(prompt='password: '))
        print(responseData.url)
        coursesData = webInterface.getCourses(session=s, userPageUrl=responseData.url)
        print(coursesData)
        courseData = webInterface.getCourseData(session=s, coursePageUrl=coursesData[1]["url"])
        print(courseData)
        _sumOfweights(courseData)
        getCategoryMarks(courseObject=courseData)
        getCourseMark(courseObject=courseData)