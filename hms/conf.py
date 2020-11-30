from datetime import datetime
import time 


def role_set(s):
    global role
    role = s



login = False
user_id = ''
username = ''
name = ''
email = ''
role = ''
today = str(time.strftime("%Y-%m-%d"))
adate = ''
ddate = ''
#roles can be customer, staff, manager, director, (admin?)

def getuser():
    return {'user_id' : user_id, 'username' : username, 'name' : name, 'email' : email, 'role' : role}