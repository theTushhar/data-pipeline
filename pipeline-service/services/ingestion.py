import requests
from sqlalchemy.orm import Session
from models.customer import Customer
from dateutil.parser import parse
import decimal

MOCK_SERVER_URL = "http://mock-server:5000/api/customers"

def ingest_data(db: Session):
    page = 1
    limit = 10
    total_ingested = 0
    
    while True:
        response = requests.get(f"{MOCK_SERVER_URL}?page={page}&limit={limit}")
        if response.status_code != 200:
            break
            
        data = response.json()
        customers = data.get('customers', [])
        
        if not customers:
            break
            
        for cust_data in customers:
            customer = Customer(
                customer_id=cust_data['customer_id'],
                first_name=cust_data['first_name'],
                last_name=cust_data['last_name'],
                email=cust_data['email'],
                phone=cust_data.get('phone'),
                address=cust_data.get('address'),
                date_of_birth=parse(cust_data['date_of_birth']).date() if cust_data.get('date_of_birth') else None,
                account_balance=decimal.Decimal(str(cust_data['account_balance'])) if cust_data.get('account_balance') is not None else None,
                created_at=parse(cust_data['created_at']) if cust_data.get('created_at') else None
            )
            db.merge(customer)
            total_ingested += 1
            
        db.commit()
        
        if len(customers) < limit:
            break
            
        page += 1
        
    return total_ingested
