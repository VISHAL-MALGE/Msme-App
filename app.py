from flask import Flask, render_template, request
import MySQLdb

app = Flask(__name__)

# MySQL Configuration
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="vishh",
    db="register"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Insert into DB
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, password)
    cursor.execute(query, values)
    db.commit()

    return f"Registered successfully! Welcome, {name}"

@app.route('/login', methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['eamil']
        password = request.form['password']

        # Check if the user exists in the database
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email , password)
        cursor.execute(query, values)

        user = cursor.fetchone()

        if user:
            return f"Welome Back, {user[1]}!"
        else:
            return "Invalid email or password"
        
    # if GET request, show login form
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)




# Close the database connection when the app is stopped
@app.teardown_appcontext
def close_db(error):
    if db:
        db.close()