from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Load data
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    data = load_data()
    
    # Pagination
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    
    start = (page - 1) * limit
    end = start + limit
    
    paginated_data = data[start:end]
    
    return jsonify({
        "total": len(data),
        "page": page,
        "limit": limit,
        "customers": paginated_data
    })

@app.route('/api/customers/<id>', methods=['GET'])
def get_customer(id):
    data = load_data()
    customer = next((item for item in data if item["customer_id"] == id), None)
    
    if customer:
        return jsonify(customer)
    else:
        return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
