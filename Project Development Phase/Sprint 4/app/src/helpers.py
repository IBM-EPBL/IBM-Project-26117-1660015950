from dbactions import Customer,Complaint,Agent
from flask_mail import Mail,Message

class AgentHelper:
    @staticmethod
    def get_agent_select_field_list(agents):
        agents_options = []
        for agent in agents:
            agents_options.append([agent.id,f"{agent.first_name} {agent.last_name} | {agent.category} "])
        return agents_options

class AppHelper:
    @staticmethod
    def send_complaint_opened_mail_to_customer(conn,mail:Mail,complaint:Complaint):
        customer:Customer = Customer.find_customer_by_id(conn,complaint.customer_id)
        subject = f"New Ticket Opened # {complaint.title}"
        body = f"Hi {customer.first_name} {customer.last_name}, you have opened a new ticket.\n\nStatus : {complaint.status}\n\nCategory : {complaint.category}\n\nTitle : {complaint.title}\n\nDescription :\n\t{complaint.description}\n\n"
        print("SENDING MAIL TO : "+customer.email)
        message = Message(subject=subject,body=body,recipients=[customer.email])
        mail.send(message)
    
    @staticmethod
    def send_complaint_assigned_mail_to_customer(conn,mail:Mail,complaint:Complaint,agent_id):
        customer:Customer = Customer.find_customer_by_id(conn,complaint.customer_id)
        agent:Agent = Agent.find_agent_by_id(conn,agent_id)
        subject = f"Agent Assigned :  # {complaint.title}"
        body = f"Hi {customer.first_name} {customer.last_name}, we have assigned an agent to your ticket.\n\nStatus : {complaint.status}\n\nCategory : {complaint.category}\n\nTitle : {complaint.title}\n\nDescription :\n\t{complaint.description}\n\nAgent Name : {agent.first_name} {agent.last_name}."
        print("SENDING MAIL TO : "+customer.email)
        message = Message(subject=subject,body=body,recipients=[customer.email])
        mail.send(message)

    @staticmethod
    def send_complaint_assigned_mail_to_agent(conn,mail:Mail,complaint:Complaint,agent_id):
        customer:Customer = Customer.find_customer_by_id(conn,complaint.customer_id)
        agent:Agent = Agent.find_agent_by_id(conn,agent_id)
        subject = f"Complaint Assigned :  # {complaint.title}"
        body = f"Hi {agent.first_name} {agent.last_name}, we have assigned an ticket to you.\n\nCustomer ID : {customer.id}\n\nCustomer Name : {customer.first_name} {customer.last_name}\n\nStatus : {complaint.status}\n\nCategory : {complaint.category}\n\nTitle : {complaint.title}\n\nDescription :\n\t{complaint.description}\n\nAgent Name : {agent.first_name} {agent.last_name}.\n\nPlease resolve the issue."
        print("SENDING MAIL TO : "+agent.email)
        message = Message(subject=subject,body=body,recipients=[agent.email])
        mail.send(message)
        

    @staticmethod
    def send_complaint_resolved_mail_to_customer(conn,mail:Mail,complaint:Complaint,agent_id,agent_message):
        customer:Customer = Customer.find_customer_by_id(conn,complaint.customer_id)
        agent:Agent = Agent.find_agent_by_id(conn,agent_id)
        subject = f"Complaint Resolved :  # {complaint.title}"
        body = f"Hi {customer.first_name} {customer.last_name}, your ticket#{complaint.id} has be resolved.\n\nStatus : {complaint.status}\n\nCategory : {complaint.category}\n\nTitle : {complaint.title}\n\nDescription :\n\t{complaint.description}\n\nAgent Name : {agent.first_name} {agent.last_name}\n\nAgnet Reply :\n\t{agent_message}."
        print("SENDING MAIL TO : "+customer.email)
        message = Message(subject=subject,body=body,recipients=[customer.email])
        mail.send(message)