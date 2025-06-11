from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import time
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# In-memory user database
USERS = {"testuser": "password123"}
PRODUCTS = {
    "1": {"name": "Laptop", "price": 1200},
    "2": {"name": "Mouse", "price": 25},
    "3": {"name": "Keyboard", "price": 75},
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('products'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            session['username'] = username
            session['cart'] = {}
            return redirect(url_for('products'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('cart', None)
    return redirect(url_for('login'))

@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Simulate performance anomaly
    if random.random() < 0.2: # 20% chance of being slow
        print("INFO: Product page is intentionally slow for this request.")
        time.sleep(2.5)
    
    return render_template('products.html', products=PRODUCTS, cart=session.get('cart', {}))

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    product_id = request.json.get('product_id')
    if product_id not in PRODUCTS:
        return jsonify({"success": False, "error": "Product not found"}), 404
        
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    
    return jsonify({"success": True, "cart": cart})

if __name__ == '__main__':
    app.run(debug=True)