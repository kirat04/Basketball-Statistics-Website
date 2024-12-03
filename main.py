from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# def init_db():
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)''')
#     conn.commit()
#     conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['query']
        print("Search request received:" + search_query)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name FROM Players WHERE name LIKE ?", ('%' + search_query + '%',))
        results = c.fetchall()
        results = list(results)
        print(results)
        conn.close()
        return render_template('search.html', items=results)
    return render_template('search.html', results=[])

if __name__ == '__main__':
    # init_db()
    app.run(debug=True)