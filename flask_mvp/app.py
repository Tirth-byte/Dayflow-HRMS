from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import datetime
import os
import random
from functools import wraps

app = Flask(__name__)
app.secret_key = 'hackathon-secret-key'
DB_NAME = 'dayflow.db'

# --- Database Helper ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # ALWAYS RESET DB FOR HACKATHON DEMO
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        
    conn = get_db()
    c = conn.cursor()
    
    # schemas
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        department TEXT,
        salary REAL DEFAULT 0,
        leave_balance INTEGER DEFAULT 20
    )''')
    
    c.execute('''CREATE TABLE attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        check_in TIME,
        check_out TIME,
        status TEXT
    )''')
    
    c.execute('''CREATE TABLE leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'pending'
    )''')
    
    c.execute('''CREATE TABLE payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        salary REAL,
        bonus REAL DEFAULT 0,
        deductions REAL DEFAULT 0,
        net_wage REAL
    )''')
    
    # --- DEMO DATA GENERATION ---
    employees = [
        ('admin@dayflow.com', 'admin', 'Admin HR', 'hr', 'Management', 95000),
        ('john@dayflow.com', 'user', 'John Doe', 'employee', 'IT Support', 50000),
        ('jane@dayflow.com', 'user', 'Jane Smith', 'employee', 'Marketing', 60000),
        ('mike@dayflow.com', 'user', 'Mike Ross', 'employee', 'Legal', 75000),
        ('rachel@dayflow.com', 'user', 'Rachel Zane', 'employee', 'Paralegal', 45000),
        ('harvey@dayflow.com', 'user', 'Harvey Specter', 'employee', 'Senior Partner', 250000),
        ('donna@dayflow.com', 'user', 'Donna Paulsen', 'hr', 'Administration', 85000),
        ('louis@dayflow.com', 'user', 'Louis Litt', 'employee', 'Finance', 90000)
    ]

    print("Generating Employees...")
    for emp in employees:
        c.execute("INSERT INTO users (email, password, name, role, department, salary) VALUES (?,?,?,?,?,?)", emp)
        user_id = c.lastrowid
        
        # Payroll
        bonus = random.choice([0, 1000, 2500, 5000])
        deductions = random.choice([0, 200, 500])
        net = emp[5] + bonus - deductions
        c.execute("INSERT INTO payroll (user_id, salary, bonus, deductions, net_wage) VALUES (?,?,?,?,?)",
                  (user_id, emp[5], bonus, deductions, net))
        
        # Attendance (Past 5 days)
        today = datetime.date.today()
        for i in range(5):
            date = today - datetime.timedelta(days=i)
            # Skip weekends logic simplified for demo: just randomness
            status_dice = random.random()
            
            if status_dice > 0.2: # 80% Present
                in_hour = random.randint(8, 10)
                in_min = random.randint(0, 59)
                out_hour = random.randint(17, 19)
                out_min = random.randint(0, 59)
                
                check_in = f"{in_hour:02d}:{in_min:02d}"
                check_out = f"{out_hour:02d}:{out_min:02d}"
                
                # If today, maybe not checked out yet
                if i == 0 and random.random() > 0.5:
                    check_out = None
                
                c.execute("INSERT INTO attendance (user_id, date, check_in, check_out, status) VALUES (?,?,?,?,?)",
                          (user_id, date, check_in, check_out, 'present'))
            elif status_dice > 0.1: # 10% Half Day
                c.execute("INSERT INTO attendance (user_id, date, check_in, check_out, status) VALUES (?,?,?,?,?)",
                          (user_id, date, "09:00", "13:00", 'half_day'))
            else: # 10% Absent
                c.execute("INSERT INTO attendance (user_id, date, status) VALUES (?,?,?)",
                          (user_id, date, 'absent'))

        # Leaves
        if emp[3] == 'employee':
            # Create a random leave
            start = today + datetime.timedelta(days=random.randint(1, 10))
            end = start + datetime.timedelta(days=random.randint(1, 3))
            l_type = random.choice(['sick', 'paid', 'unpaid'])
            status = random.choice(['pending', 'approved', 'rejected'])
            reason = random.choice(['Vacation', 'Not feeling well', 'Personal matter', 'Family event'])
            
            c.execute("INSERT INTO leaves (user_id, type, start_date, end_date, reason, status) VALUES (?,?,?,?,?,?)",
                      (user_id, l_type, start, end, reason, status))

    conn.commit()
    conn.close()
    print("Database initialized with realistic demo data.")

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def hr_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'hr':
            flash('Access Denied: HR Only', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
@login_required
def dashboard():
    conn = get_db()
    today = datetime.date.today()
    
    stats = {}
    stats['employees'] = conn.execute("SELECT COUNT(*) FROM users WHERE role='employee'").fetchone()[0]
    stats['present'] = conn.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='present'", (today,)).fetchone()[0]
    
    if session['role'] == 'hr':
        stats['leaves'] = conn.execute("SELECT COUNT(*) FROM leaves WHERE status='pending'").fetchone()[0]
        # Recent Activity (Last 5 check-ins)
        recent_activity = conn.execute("""
            SELECT a.*, u.name as user_name 
            FROM attendance a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.date = ? 
            ORDER BY a.check_in DESC LIMIT 5
        """, (today,)).fetchall()
    else:
        stats['leaves'] = conn.execute("SELECT COUNT(*) FROM leaves WHERE user_id=? AND status='pending'", (session['user_id'],)).fetchone()[0]
        recent_activity = conn.execute("""
            SELECT * FROM attendance WHERE user_id=? ORDER BY date DESC LIMIT 5
        """, (session['user_id'],)).fetchall()
        
    conn.close()
    return render_template('dashboard.html', stats=stats, activity=recent_activity)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Employee Management (HR Only) ---
@app.route('/employees')
@login_required
@hr_required
def employees():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('employees.html', employees=users)

@app.route('/employees/new', methods=['GET', 'POST'])
@app.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@hr_required
def manage_employee(id=None):
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dept = request.form['department']
        role = request.form['role']
        salary = float(request.form['salary'])
        
        if id:
             conn.execute("UPDATE users SET name=?, email=?, department=?, role=?, salary=? WHERE id=?", 
                          (name, email, dept, role, salary, id))
             conn.execute("UPDATE payroll SET salary=? WHERE user_id=?", (salary, id))
        else:
            pwd = request.form['password']
            cur = conn.execute("INSERT INTO users (name, email, password, department, role, salary) VALUES (?,?,?,?,?,?)",
                         (name, email, pwd, dept, role, salary))
            conn.execute("INSERT INTO payroll (user_id, salary, net_wage) VALUES (?, ?, ?)", (cur.lastrowid, salary, salary))
            
        conn.commit()
        conn.close()
        return redirect(url_for('employees'))
        
    employee = None
    if id:
        employee = conn.execute("SELECT * FROM users WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('employee_form.html', employee=employee)

# --- Attendance ---
@app.route('/attendance')
@login_required
def attendance():
    conn = get_db()
    today = datetime.date.today()
    today_record = conn.execute("SELECT * FROM attendance WHERE user_id=? AND date=?", 
                                (session['user_id'], today)).fetchone()
                                
    if session['role'] == 'hr':
        history = conn.execute("SELECT a.*, u.name as user_name FROM attendance a JOIN users u ON a.user_id = u.id ORDER BY date DESC, check_in DESC LIMIT 50").fetchall()
    else:
        history = conn.execute("SELECT * FROM attendance WHERE user_id=? ORDER BY date DESC LIMIT 30", (session['user_id'],)).fetchall()
        
    conn.close()
    return render_template('attendance.html', today=today, today_record=today_record, history=history)

@app.route('/attendance/check_in', methods=['POST'])
@login_required
def check_in():
    conn = get_db()
    today = datetime.date.today()
    now_time = datetime.datetime.now().strftime("%H:%M")
    
    exist = conn.execute("SELECT id FROM attendance WHERE user_id=? AND date=?", (session['user_id'], today)).fetchone()
    if not exist:
        conn.execute("INSERT INTO attendance (user_id, date, check_in, status) VALUES (?,?,?,?)",
                     (session['user_id'], today, now_time, 'present'))
        conn.commit()
        flash('Checked In Successfully', 'success')
    
    conn.close()
    return redirect(url_for('attendance'))

@app.route('/attendance/check_out', methods=['POST'])
@login_required
def check_out():
    conn = get_db()
    today = datetime.date.today()
    now_time = datetime.datetime.now().strftime("%H:%M")
    
    conn.execute("UPDATE attendance SET check_out=? WHERE user_id=? AND date=?", 
                 (now_time, session['user_id'], today))
    conn.commit()
    flash('Checked Out Successfully', 'success')
    conn.close()
    return redirect(url_for('attendance'))

# --- Leaves ---
@app.route('/leaves')
@login_required
def leaves():
    conn = get_db()
    if session['role'] == 'hr':
        # SQLite sort: Pending first (1), Approved second (2), Rejected third (3)
        leaves = conn.execute("""
            SELECT l.*, u.name as user_name 
            FROM leaves l 
            JOIN users u ON l.user_id = u.id 
            ORDER BY 
                CASE l.status 
                    WHEN 'pending' THEN 1 
                    WHEN 'approved' THEN 2 
                    WHEN 'rejected' THEN 3 
                    ELSE 4 
                END, 
                l.start_date DESC
        """).fetchall()
    else:
        leaves = conn.execute("""
            SELECT * FROM leaves 
            WHERE user_id=? 
            ORDER BY 
                CASE status 
                    WHEN 'pending' THEN 1 
                    WHEN 'approved' THEN 2 
                    WHEN 'rejected' THEN 3 
                    ELSE 4 
                END, 
                start_date DESC
        """, (session['user_id'],)).fetchall()
    conn.close()
    return render_template('leaves.html', leaves=leaves)

@app.route('/leaves/new', methods=['GET', 'POST'])
@login_required
def new_leave():
    if request.method == 'POST':
        l_type = request.form['type']
        start_str = request.form['start_date']
        end_str = request.form['end_date']
        reason = request.form['reason']
        
        try:
            start_date = datetime.datetime.strptime(start_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'error')
            return redirect(url_for('new_leave'))
            
        if start_date > end_date:
            flash('Start date cannot be after end date', 'error')
            return redirect(url_for('new_leave'))
            
        if start_date < datetime.date.today():
            flash('Cannot apply for leave in the past', 'error')
            return redirect(url_for('new_leave'))

        conn = get_db()
        
        # Overlap Check
        # Overlap if: (RequestStart <= ExistingEnd) and (RequestEnd >= ExistingStart)
        # SQLite dates are strings, but consistent YYYY-MM-DD works for comparison
        overlap = conn.execute("""
            SELECT id FROM leaves 
            WHERE user_id=? AND status != 'rejected'
            AND date(start_date) <= date(?) AND date(end_date) >= date(?)
        """, (session['user_id'], end_str, start_str)).fetchone()
        
        if overlap:
            conn.close()
            flash('Leave request overlaps with an existing leave!', 'error')
            return redirect(url_for('new_leave'))
            
        conn.execute("INSERT INTO leaves (user_id, type, start_date, end_date, reason) VALUES (?,?,?,?,?)",
                     (session['user_id'], l_type, start_str, end_str, reason))
        conn.commit()
        conn.close()
        flash('Leave Request Submitted', 'success')
        return redirect(url_for('leaves'))
        
    return render_template('leave_form.html')

@app.route('/leaves/approve/<int:id>')
@login_required
@hr_required
def approve_leave(id):
    conn = get_db()
    # verify it exists
    leave = conn.execute("SELECT * FROM leaves WHERE id=?", (id,)).fetchone()
    if leave:
        conn.execute("UPDATE leaves SET status='approved' WHERE id=?", (id,))
        conn.commit()
        flash('Leave Approved', 'success')
    else:
        flash('Leave request not found', 'error')
    conn.close()
    return redirect(url_for('leaves'))

@app.route('/leaves/reject/<int:id>')
@login_required
@hr_required
def reject_leave(id):
    conn = get_db()
    # verify it exists
    leave = conn.execute("SELECT * FROM leaves WHERE id=?", (id,)).fetchone()
    if leave:
        conn.execute("UPDATE leaves SET status='rejected' WHERE id=?", (id,))
        conn.commit()
        flash('Leave Rejected', 'warning')
    else:
        flash('Leave request not found', 'error')
    conn.close()
    return redirect(url_for('leaves'))

# --- Payroll ---
@app.route('/payroll', methods=['GET'])
@login_required
def payroll():
    conn = get_db()
    payrolls = []
    my_payroll = None
    if session['role'] == 'hr':
        payrolls = conn.execute("SELECT p.*, u.name as user_name FROM payroll p JOIN users u ON p.user_id = u.id").fetchall()
    else:
        my_payroll = conn.execute("SELECT * FROM payroll WHERE user_id=?", (session['user_id'],)).fetchone()
    conn.close()
    return render_template('payroll.html', payrolls=payrolls, my_payroll=my_payroll)

@app.route('/payroll/update/<int:id>', methods=['POST'])
@login_required
@hr_required
def update_payroll(id):
    bonus = float(request.form['bonus'])
    deductions = float(request.form['deductions'])
    conn = get_db()
    record = conn.execute("SELECT salary FROM payroll WHERE id=?", (id,)).fetchone()
    salary = record['salary']
    net = salary + bonus - deductions
    conn.execute("UPDATE payroll SET bonus=?, deductions=?, net_wage=? WHERE id=?", 
                 (bonus, deductions, net, id))
    conn.commit()
    conn.close()
    flash('Payroll Updated', 'success')
    return redirect(url_for('payroll'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000) # Changed to 8000 to avoid conflicts
