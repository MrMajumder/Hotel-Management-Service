def role_set(s):
    global role
    role = s



login = False
user_id = ''
username = ''
name = ''
email = ''
role = ''
#roles can be customer, staff, manager, director, (admin?)

def getuser():
    return {'user_id' : user_id, 'username' : username, 'name' : name, 'email' : email, 'role' : role}