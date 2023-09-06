from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(_name_)

# Create a SQLite database
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Create a recipes table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# Routes
@app.route('/')
def home():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)',
                       (title, ingredients, instructions))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
    
    return render_template('add_recipe.html')

if _name_ == '_main_':
    app.run(debug=True)