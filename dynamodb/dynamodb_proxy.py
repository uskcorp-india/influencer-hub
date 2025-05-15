import dao.customer_dao as customer_dao

def create_customer(customer: dict):
    return customer_dao.create(customer)

def update_customer(customer: dict):
    return customer_dao.update(customer)

def delete_customer(customer_id:str):
    return customer_dao.delete(customer_id)

def find_customer(customer_id:str):
    return customer_dao.find(customer_id)