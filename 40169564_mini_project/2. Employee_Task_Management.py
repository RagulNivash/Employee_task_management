#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pymysql')


# In[2]:


import pymysql
import time


# ## Common Functions

# In[3]:



def create_task(emp_id): #common for all employees
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
      
    cur = conn.cursor()
    
    name = input("Enter task Name ")
    department = input("Enter department ")
    status = "unassigned"
    assigned_by = emp_id
    
    query = "insert into tasks(name,department,status,assigned_by) values('%s','%s','%s','%s')"%(name,department,status,assigned_by)
    cur.execute(query)
    conn.commit()
    query = "insert into notifications(taskId ,type, description, request, raisedBy, assignedTo) values('%s','%s','%s','%s','%s','%s')"%(str(0),"alert","new task created" ,"0",str(emp_id) ,"0")
    cur.execute(query)
    conn.commit()
    conn.close()
    print("task created successfully!")
    time.sleep(3)
    
    
def getValueById(table, column, emp_id):
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
      
    cur = conn.cursor()
    query = "select %s from %s where id ='%s'"%(column,table,emp_id)
    cur.execute(query)
    res = cur.fetchall()
    value =res[0][0]
    conn.close()
    return value

def getCount(emp_id):
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
      
    cur = conn.cursor()
    query = "select * from tasks where assigned_to = %s"%emp_id
    cur.execute(query)
    res = cur.fetchall()
    c = len(res)
    return c


# ## General Manager

# In[15]:


def gmPermissions(emp_id):
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    cur = conn.cursor()
    query = "select * from notifications "
    cur.execute(query)
    res = cur.fetchall()
    print("Notifications")
    print("-------------------------------------------------------------")
    print("id | taskId | type | description | request | raisedBy | assignedTo" )
    for i in res:
        print("%s | %s | %s | %s | %s | %s | %s |"%(i[0], i[6],i[1],i[2],i[3],i[4],i[5]))
    print("-------------------------------------------------------------")
    noti_id  = input("enter id to take action")
    noti_type = getValueById("notifications","type",noti_id)
    
    if noti_type == "permission":
        status = input("Please enter A to accept and R to reject")
        query = "update notifications set request = '%s'"%(status)
        cur.execute(query)
        conn.commit()        
        if status =='A':
            task_id = getValueById("notifications", "taskId",noti_id)
            query = "delete from tasks where id = '%s'"%(task_id)
            cur.execute(query)
            conn.commit()
            
        elif status != R:
            print("Invalid option entered")
    conn.close()
    print("Success!")
    time.sleep(3)
            

def generalManagerTaskAssign(emp_id):
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    cur = conn.cursor()
    query = "select * from employee where role < 3"
    cur.execute(query)
    res = cur.fetchall()
    print("All Employees")
    print("-------------------------------------------------------------")
    print("id | name | role | department |" )
    for i in res:
        print("%s | %s | %s | %s |"%(i[0],i[1],i[2],i[3]))
    print("-------------------------------------------------------------")
    
    departmentReport(emp_id)
    task_id = input("select task id to be assigned")
    id2 = input("enter employee id to assign task")
    if getCount(id2) >2:
        print("Employee cannot have more than 3 tasks!")
        return 0
    query = "update tasks set status = 'assigned', assigned_to = %s where id = %s"%(id2,task_id)
    cur.execute(query)
    conn.commit()
    print ("Success!")
    time.sleep(3)
    
def completeReport(emp_id):
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    
    cur = conn.cursor()
    query = "select * from tasks"
    cur.execute(query)
    res = cur.fetchall()
    print("All Tasks")
    print("-------------------------------------------------------------")
    print("id | assigned by | department | status | assigned to | name" )
    for i in res:
        print("%s | %s | %s | %s | %s | %s"%(i[0],i[1],i[2],i[3],i[4],i[5]))
    print("-------------------------------------------------------------")
    time.sleep(5)
    
def gmTaskCancel(emp_id):   
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    cur = conn.cursor()
    query = "select * from tasks"
    cur.execute(query)
    res = cur.fetchall()
    print("All Tasks")
    print("-------------------------------------------------------------")
    print("id | assigned by | department | status | assigned to | name" )
    for i in res:
        print("%s | %s | %s | %s | %s | %s"%(i[0],i[1],i[2],i[3],i[4],i[5]))
    print("-------------------------------------------------------------")
#     query = "select id from employee where role = 3"
#     cur.execute(query)
#     res = cur.fetchall()
#     gm_id = res[0][0]
    task_id = input("Enter id of task to be cancelled")
    query = "delete from tasks where id = '%s'"%(task_id)
    cur.execute(query)
    conn.commit()
    print("Success!")
    time.sleep(3)
    
def generalManagerMenu(emp_id):
    print("General Manager Options:")
    print("1: view complete report")
    print("2: Create task")
    print("3: assign task to employee")
    print("4: View notifications")
    print("5: cancel task")
    print("6: exit")

    option = int(input())
    if option == 1:
        completeReport(emp_id)
    elif option == 2:
        create_task(emp_id)
    elif option == 3:
        generalManagerTaskAssign(emp_id)
    elif option == 4:
        gmPermissions(emp_id)
    elif option == 5:
        gmTaskCancel(emp_id)
    elif option == 6:
        return False


# ## Manager

# In[16]:


def departmentReport(emp_id):
    department = getValueById("employee","department",emp_id)
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    
    cur = conn.cursor()
    query = "select * from tasks where department = '%s'"%(department)
    cur.execute(query)
    res = cur.fetchall()
    print("Department Tasks")
    print("-------------------------------------------------------------")
    print("id | assigned by | department | status | assigned to | name" )
    for i in res:
        print("%s | %s | %s | %s | %s | %s"%(i[0],i[1],i[2],i[3],i[4],i[5]))
    print("-------------------------------------------------------------")
#     wait = input("press enter to continue")
    time.sleep(5)
    
    
def managerTaskAssign(emp_id):
    department = getValueById("employee","department",emp_id)
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    cur = conn.cursor()
    query = "select * from employee where department = '%s'"%(department)
    cur.execute(query)
    res = cur.fetchall()
    print("Department Employees")
    print("-------------------------------------------------------------")
    print("id | name | role | department |" )
    for i in res:
        if int(i[2] == 1):
            print("%s | %s | %s | %s |"%(i[0],i[1],i[2],i[3]))
    print("-------------------------------------------------------------")
    
    departmentReport(emp_id)
    task_id = input("select task id to be assigned")
    id2 = input("enter employee id to assign task")
    department_worker = getValueById("employee", "department", id2)
    if department_worker != department:
        print("Employee id entered doesnt belong to your department!!!!")
        return 0
    if getCount(id2) >2:
        print("Employee cannot have more than 3 tasks!")
        time.sleep(3)
        return 0
    query = "update tasks set status = 'assigned', assigned_to = %s where id = %s"%(id2,task_id)
    cur.execute(query)
    conn.commit()
    print ("Success!")
    time.sleep(3)
    
def managerTaskCancel(emp_id):
    department = getValueById("employee","department",emp_id)   
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    cur = conn.cursor()
    query = "select * from tasks where department = '%s'"%(department)
    cur.execute(query)
    res = cur.fetchall()
    print("Department Tasks")
    print("-------------------------------------------------------------")
    print("id | assigned by | department | status | assigned to | name" )
    for i in res:
        print("%s | %s | %s | %s | %s | %s"%(i[0],i[1],i[2],i[3],i[4],i[5]))
    print("-------------------------------------------------------------")
    query = "select id from employee where role = 3"
    cur.execute(query)
    res = cur.fetchall()
    gm_id = res[0][0]
    task_id = input("Enter id of task to be cancelled")
    query = "select * from tasks where department = '%s' and id = '%s'"%(department,task_id)
    cur.execute(query)
    res = cur.fetchall()
    description = input("please enter reason for cancellation")
    query = "insert into notifications(taskId,type, description, request, raisedBy, assignedTo) values('%s','%s','%s','%s','%s','%s')"%(str(res[0][0]),"permission",str(description) ,"0",str(emp_id) , str(res[0][4]))
    cur.execute(query)
    conn.commit()
    conn.close()
    print("Success!")
    time.sleep(3)
    
def managerMenu(emp_id):
    print("Manager Options:")
    print("1: view department report")
    print("2: assign task to department employee")
    print("3:Create task")
    print("4:cancel task")
    print("5: Exit")

    option = int(input())
    if option == 1:
        departmentReport(emp_id)
    elif option == 2:
        managerTaskAssign(emp_id)
    elif option == 3:
        create_task(emp_id)
    elif option == 4:
        managerTaskCancel(emp_id)
    elif option == 5:
        return False


# ## Worker

# In[17]:


def assign_task_worker(emp_id):
    if (getCount(emp_id)>2):
        print("you cannot undertake more than three tasks!")
        time.sleep(3)
        return 0
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "rootpassword@1",
        db='employee',
        )
    
    cur = conn.cursor()
    query = "select * from tasks where status ='unassigned' and assigned_to is NULL"
    cur.execute(query)
    res = cur.fetchall()
    print("-------------------------------------------------------------")
    print("id | assigned by | department | status | assigned to | name" )
    for i in res:
        print(i)
    print("-------------------------------------------------------------")
    task_id = input("Enter task id to undertake")
    if task_id != None:
        query = "update tasks set status = 'assigned', assigned_to = %s where id = '%s'"%(emp_id,task_id)
        cur.execute(query)
        conn.commit()
        print ("Success!")
        time.sleep(3)
    conn.close()

def workerMenu(emp_id):
    print("Worker Options:")
    print("1: assign task to self")
    print("2: Exit")

    option = int(input())
    if option == 1:
        assign_task_worker(emp_id)
    elif option == 2:
        return False


# ## Driver Code

# In[19]:


from IPython.display import clear_output
while(True):
#     clear_output(wait=True)
    emp_id = input("Enter your Employee id ")
    role = getValueById("employee","role",emp_id)
    flag = True
    while(flag == True):
        clear_output(wait=True)
        if role == 3:
            flag = generalManagerMenu(emp_id)
        elif role == 2:
            flag = managerMenu(emp_id)
        elif role == 1:
            flag = workerMenu(emp_id)
        if flag != False:
            flag = True


# In[ ]:


getCount(3)


# In[ ]:


((a))


# In[ ]:




