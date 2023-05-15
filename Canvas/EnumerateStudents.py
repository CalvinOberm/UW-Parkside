import requests
import json

# Canvas domain goes here
domain = ""
# Canvas access token goes here
access_token = ""

headers = {"Authorization": "Bearer " + access_token}

# Gets all courses
courses_url = f"{domain}/api/v1/courses"
response = requests.get(courses_url, headers=headers)

courses = []
failed_courses = []

if response.status_code == 200:
    courses = json.loads(response.content)
else:
    print("Error: " + str(response.status_code))
    exit()

# Get enrolled users for each course
for course in courses:
    try:
        enrollments_url = f"{domain}/api/v1/courses/{course['id']}/enrollments"
        response = requests.get(enrollments_url, headers=headers)
        if response.status_code == 200:
            enrollments = json.loads(response.content)
            for enrollment in enrollments:
                print(f"{enrollment['user']['name']} is enrolled in {course['name']}")
        else:
            failed_courses.append(course['id'])
    except KeyError as e:
        failed_courses.append(course['id'])
        print(f"Error: {e}. Failed to enumerate enrollments for course {course['id']}")

if len(failed_courses) > 0:
    print("Failed to enumerate enrollments for the following courses:")
    print(failed_courses)
