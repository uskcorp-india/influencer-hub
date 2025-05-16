import dao.customer_dao as customer_dao
import dao.influencer_dao as influencer_dao

def create_customer(customer: dict):
    return customer_dao.create(customer)

def update_customer(customer: dict):
    return customer_dao.update(customer)

def delete_customer(customer_id:str):
    return customer_dao.delete(customer_id)

def find_customer(customer_id:str):
    return customer_dao.find(customer_id)

def find_all_customers():
    return customer_dao.find_all()

def create_influencer(influencer:dict):
    return influencer_dao.create(influencer)

def update_influencer(influencer:dict):
    return influencer_dao.update(influencer)

def delete_influencer(influencer_id:str):
    return influencer_dao.delete(influencer_id)

def find_influencer(influencer_id:str):
    return influencer_dao.find(influencer_id)

def find_all_influencer():
    return influencer_dao.find_all()