import dao.customer_dao as customer_dao

# user_id is used a dummy parameter to handle for audit log
def create_customer(customer: dict):
    return customer_dao.create(customer)
