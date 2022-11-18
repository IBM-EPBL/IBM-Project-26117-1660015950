from __future__ import annotations

import json
import ibm_db

from forms import CustomerSignupForm,AgentSignupForm,ComplaintCreateForm,ComplaintEditForm


class AppModel:
    pass


class Customer(AppModel):
    def __init__(self,id,email:str,password:str,first_name:str,last_name:str,mobile:str,gender:str,address:str,created_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.gender = gender
        self.address = address
        self.created_at = created_at
        
    
    def create_customer(self,conn):
        sql = "INSERT INTO CUSTOMERS (EMAIL,PASSWORD,FIRST_NAME,LAST_NAME,MOBILE,GENDER,ADDRESS) VALUES(?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, self.email)
        ibm_db.bind_param(prep_stmt, 2, self.password)
        ibm_db.bind_param(prep_stmt, 3, self.first_name)
        ibm_db.bind_param(prep_stmt, 4, self.last_name)
        ibm_db.bind_param(prep_stmt, 5, self.mobile)
        ibm_db.bind_param(prep_stmt, 6, self.gender)
        ibm_db.bind_param(prep_stmt, 7, self.address)
        result = ibm_db.execute(prep_stmt)
    

    def to_dict(self,remove_password=True):
        return {'id':self.id,'email':self.email,'password': '' if remove_password else self.password,'first_name':self.first_name,'last_name':self.last_name,'mobile':self.mobile,'gender':self.gender,'address':self.address}
    
    def json(self):
        return json.dumps(self.to_dict())
    
    @staticmethod
    def find_user_by_email(conn,email:str):
        sql = "SELECT * FROM CUSTOMERS WHERE EMAIL = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Customer.construct_customer_from_assoc(assoc)
    
    @staticmethod
    def find_customer_by_id(conn,customer_id):
        sql = "SELECT * FROM CUSTOMERS WHERE ID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,customer_id)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Customer.construct_customer_from_assoc(assoc)
    
    @staticmethod
    def construct_customer_from_assoc(assoc):
        if assoc:
            return Customer(assoc['ID'],assoc['EMAIL'],assoc['PASSWORD'],assoc['FIRST_NAME'],assoc['LAST_NAME'],assoc['MOBILE'],assoc['GENDER'],assoc['ADDRESS'],assoc['CREATED_AT'])
        return False

    @staticmethod
    def construct_customer_from_form(form: CustomerSignupForm):
        return Customer(-1,form.email.data,form.password.data,form.first_name.data,form.last_name.data,form.mobile.data,form.gender.data,form.address.data)


class Agent():

    def __init__(self,id,email:str,password:str,first_name:str,last_name:str,category:str,created_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.category = category
        self.created_at = created_at   


    def create_agent(self,conn):
        sql = "INSERT INTO AGENTS (EMAIL,PASSWORD,FIRST_NAME,LAST_NAME,CATEGORY) VALUES(?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, self.email)
        ibm_db.bind_param(prep_stmt, 2, self.password)
        ibm_db.bind_param(prep_stmt, 3, self.first_name)
        ibm_db.bind_param(prep_stmt, 4, self.last_name)
        ibm_db.bind_param(prep_stmt, 5, self.category)
        result = ibm_db.execute(prep_stmt)
    

    def to_dict(self,remove_password=True):
        return {'id':self.id,'email':self.email,'password': '' if remove_password else self.password,'first_name':self.first_name,'last_name':self.last_name,'category':self.category,'created_at':self.created_at}
    
    def json(self):
        return json.dumps(self.to_dict())
    
    @staticmethod
    def find_agent_by_email(conn,email:str):
        sql = "SELECT * FROM AGENTS WHERE EMAIL = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Agent.construct_agent_from_assoc(assoc)
    
    @staticmethod
    def find_agent_by_id(conn,agent_id):
        sql = "SELECT * FROM AGENTS WHERE ID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,agent_id)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Agent.construct_agent_from_assoc(assoc)
    
    
    @staticmethod
    def find_all_agents(conn):
        sql = "SELECT * FROM AGENTS ORDER BY CREATED_AT DESC"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        agents = []
        while assoc:
            agents.append( Agent.construct_agent_from_assoc(assoc))
            assoc = ibm_db.fetch_assoc(stmt)
        return agents    
    
    @staticmethod
    def construct_agent_from_assoc(assoc):
        if assoc:
            return Agent(assoc['ID'],assoc['EMAIL'],assoc['PASSWORD'],assoc['FIRST_NAME'],assoc['LAST_NAME'],assoc['CATEGORY'],assoc['CREATED_AT'])
        return False

    @staticmethod
    def construct_agent_from_form(form: AgentSignupForm):
        return Agent(-1,form.email.data,form.password.data,form.first_name.data,form.last_name.data,form.category.data)
    


class Complaint():
    def __init__(self,id,customer_id,title,category,status,description,created_at=None):
        self.id = id
        self.customer_id = customer_id
        self.title = title
        self.category = category
        self.status = status
        self.description = description
        self.created_at = created_at   


    def create_complaint(self,conn):
        sql = "INSERT INTO COMPLAINTS (CUSTOMER_ID,TITLE,CATEGORY,STATUS,DESCRIPTION) VALUES(?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, self.customer_id)
        ibm_db.bind_param(prep_stmt, 2, self.title)
        ibm_db.bind_param(prep_stmt, 3, self.category)
        ibm_db.bind_param(prep_stmt, 4, self.status)
        ibm_db.bind_param(prep_stmt, 5, self.description)

        
        result = ibm_db.execute(prep_stmt)
    
    @staticmethod
    def update_complaint(conn,complaint:Complaint):
        sql = "UPDATE COMPLAINTS SET TITLE = ?,CATEGORY = ?, STATUS = ?, DESCRIPTION = ? WHERE ID = ?;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,complaint.title)
        ibm_db.bind_param(stmt,2,complaint.category)
        ibm_db.bind_param(stmt,3,complaint.status)
        ibm_db.bind_param(stmt,4,complaint.description)
        ibm_db.bind_param(stmt,5,complaint.id)
        return ibm_db.execute(stmt)
    
    @staticmethod
    def find_complaint_by_id(conn,id:int|str)->Complaint:
        sql = "SELECT * FROM COMPLAINTS WHERE ID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,id)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Complaint.construct_complaint_from_assoc(assoc)

    @staticmethod
    def find_all_complaint_by_customer_id(conn,customer_id):
        sql = "SELECT * FROM COMPLAINTS WHERE CUSTOMER_ID = ? ORDER BY CREATED_AT DESC"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,customer_id)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        complaints = []
        while assoc:
            complaints.append(Complaint.construct_complaint_from_assoc(assoc))
            assoc = ibm_db.fetch_assoc(stmt)
        return complaints    

    @staticmethod
    def find_all_unassinged_complaints(conn):
        sql = "SELECT * FROM COMPLAINTS WHERE ID NOT IN ( SELECT COMPLAINT_ID FROM COMPLAINT_ASSIGN_STATUS ) AND STATUS='OPENED' ORDER BY CREATED_AT DESC ;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        complaints = []
        while assoc:
            complaints.append(Complaint.construct_complaint_from_assoc(assoc))
            assoc = ibm_db.fetch_assoc(stmt)
        return complaints    
    
    
    @staticmethod
    def find_all_assigned_complaints(conn):
        sql = "SELECT * FROM COMPLAINTS WHERE ID IN ( SELECT COMPLAINT_ID FROM COMPLAINT_ASSIGN_STATUS ) AND STATUS='ASSIGNED' ORDER BY CREATED_AT DESC ;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        complaints = []
        while assoc:
            complaints.append(Complaint.construct_complaint_from_assoc(assoc))
            assoc = ibm_db.fetch_assoc(stmt)
        return complaints    

    @staticmethod
    def find_all_resolved_complaints(conn):
        sql = "SELECT * FROM COMPLAINTS WHERE ID IN ( SELECT COMPLAINT_ID FROM COMPLAINT_ASSIGN_STATUS ) AND STATUS='RESOLVED' ORDER BY CREATED_AT DESC ;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        complaints = []
        while assoc:
            complaints.append(Complaint.construct_complaint_from_assoc(assoc))
            assoc = ibm_db.fetch_assoc(stmt)
        return complaints 


    @staticmethod
    def find_all_complaints_assigned_to_agent(conn,agent_id):
        sql = "SELECT * FROM COMPLAINTS WHERE ID IN ( SELECT COMPLAINT_ID FROM COMPLAINT_ASSIGN_STATUS WHERE AGENT_ID = ? ) AND STATUS='ASSIGNED' ORDER BY CREATED_AT DESC,STATUS ASC;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,agent_id);
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        complaints = []
        while assoc:
            complaints.append(Complaint.construct_complaint_from_assoc(assoc))
            assoc = ibm_db.fetch_assoc(stmt)
        return complaints   


    
    @staticmethod
    def construct_complaint_from_assoc(assoc):
        if assoc:
            return Complaint(assoc['ID'],assoc['CUSTOMER_ID'],assoc['TITLE'],assoc['CATEGORY'],assoc['STATUS'],assoc['DESCRIPTION'],assoc['CREATED_AT'])
        return False

    @staticmethod
    def construct_complaint_from_create_form(form: ComplaintCreateForm)->Complaint:
        return Complaint(-1,-1,form.title.data,form.category.data,'OPENED',form.description.data)
    
    def to_dict(self):
        return {'id':self.id,'customer_id':self.customer_id,'title':self.title,'category':self.category,'status':self.status,'description':self.description,'created_at':self.created_at}
    
    def json(self):
        return json.dumps(self.to_dict())


class Admin():
    def __init__(self,id,email:str,password:str,first_name:str,last_name:str,created_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at   


    def create_admin(self,conn):
        sql = "INSERT INTO ADMINS (EMAIL,PASSWORD,FIRST_NAME,LAST_NAME) VALUES(?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, self.email)
        ibm_db.bind_param(prep_stmt, 2, self.password)
        ibm_db.bind_param(prep_stmt, 3, self.first_name)
        ibm_db.bind_param(prep_stmt, 4, self.last_name)
        result = ibm_db.execute(prep_stmt)
    

    def to_dict(self,remove_password=True):
        return {'id':self.id,'email':self.email,'password': '' if remove_password else self.password,'first_name':self.first_name,'last_name':self.last_name,'created_at':self.created_at}
    
    def json(self):
        return json.dumps(self.to_dict())
    
    @staticmethod
    def find_admin_by_email(conn,email:str):
        sql = "SELECT * FROM ADMINS WHERE EMAIL = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return Admin.construct_admin_from_assoc(assoc)
    
    @staticmethod
    def construct_admin_from_assoc(assoc):
        if assoc:
            return Admin(assoc['ID'],assoc['EMAIL'],assoc['PASSWORD'],assoc['FIRST_NAME'],assoc['LAST_NAME'],assoc['CREATED_AT'])
        return False

    @staticmethod
    def construct_admin_from_form(form: AgentSignupForm):
        return Admin(-1,form.email.data,form.password.data,form.first_name.data,form.last_name.data)


class AgentAssign():
    def __init__(self,id,complaint_id,status,agent_id) -> None:
        self.id = id
        self.complaint_id = complaint_id
        self.status = status
        self.agent_id = agent_id
    
    @staticmethod
    def assign_agent_to_opened_complaint(conn,complaint_id,agent_id):
        sql = "INSERT INTO COMPLAINT_ASSIGN_STATUS (COMPLAINT_ID,STATUS,AGENT_ID) VALUES(?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, complaint_id)
        ibm_db.bind_param(prep_stmt, 2, "ASSIGNED")
        ibm_db.bind_param(prep_stmt, 3, agent_id)
        ibm_db.execute(prep_stmt)
        
        sql = "UPDATE COMPLAINTS SET STATUS = ? WHERE ID = ? AND STATUS = 'OPENED'"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, "ASSIGNED")
        ibm_db.bind_param(prep_stmt, 2, complaint_id)
        ibm_db.execute(prep_stmt)
    
    @staticmethod
    def assign_agent_to_assigned_complaint(conn,complaint_id,agent_id):
        sql = "UPDATE COMPLAINT_ASSIGN_STATUS SET AGENT_ID = ? WHERE COMPLAINT_ID = ? AND STATUS = ? "
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, agent_id)
        ibm_db.bind_param(prep_stmt, 2, complaint_id)
        ibm_db.bind_param(prep_stmt, 3, "ASSIGNED")
        ibm_db.execute(prep_stmt)
        
        
    @staticmethod
    def change_status_to_resolved_complaint(conn,complaint_id,agent_id):
        sql = "UPDATE COMPLAINT_ASSIGN_STATUS SET STATUS = ? WHERE COMPLAINT_ID = ? AND AGENT_ID = ?"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, "RESOLVED")
        ibm_db.bind_param(prep_stmt, 2, complaint_id)
        ibm_db.bind_param(prep_stmt, 3, agent_id)
        ibm_db.execute(prep_stmt)
        
        sql = "UPDATE COMPLAINTS SET STATUS = ? WHERE ID = ?"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt, 1, "RESOLVED")
        ibm_db.bind_param(prep_stmt, 2, complaint_id)
        ibm_db.execute(prep_stmt)
        

    @staticmethod
    def find_agent_assign_by_complaint_id(conn,complaint_id):
        sql = "SELECT * FROM COMPLAINT_ASSIGN_STATUS WHERE COMPLAINT_ID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,complaint_id)
        ibm_db.execute(stmt)
        assoc = ibm_db.fetch_assoc(stmt)
        return AgentAssign.construct_agent_assign_from_assoc(assoc)
    

    @staticmethod
    def construct_agent_assign_from_assoc(assoc):
        if assoc:
            return AgentAssign(assoc['ID'],assoc['COMPLAINT_ID'],assoc['STATUS'],assoc['AGENT_ID'])
        return False   
    
