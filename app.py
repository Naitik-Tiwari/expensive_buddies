from flask import Flask, render_template, request, redirect, url_for, session, flash
from tracker import Expense

app = Flask(__name__)
app.secret_key = 'super_secret_trackify_key' # Needed for user sessions
tracker = Expense()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        if action == 'register':
            if tracker.createNew(username, password):
                flash('User created successfully! Please log in.', 'success')
            else:
                flash('User already exists.', 'danger')
                
        elif action == 'login':
            user = tracker.find_user(username, password)
            if user:
                session['username'] = username
                session['password'] = password
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. User Not Found.', 'danger')
                
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Protect route - ensure user is logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    
    username = session['username']
    password = session['password']
    
    # Fetch data using your class methods
    expenses = tracker.showExpense(username, password)
    total = tracker.totalSpend(username, password)
    
    return render_template('dashboard.html', username=username, expenses=expenses, total=total)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'username' in session:
        date = request.form.get('date')
        category = request.form.get('category')
        description = request.form.get('description')
        amount = request.form.get('amount')
        
        tracker.newExpense(session['username'], session['password'], date, category, description, amount)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear() # Clears the logged-in state
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)