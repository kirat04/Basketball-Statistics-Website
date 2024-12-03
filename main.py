from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
teams = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls",
    "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors",
    "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
    "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
    "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
    "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"
]
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
        team_query = int(request.form['team'])
        print("Search request received:" + teams[team_query] + " " + search_query)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #find the all players that have this name if no team specified
        if(team_query == 0):
            c.execute("SELECT name FROM Players WHERE name LIKE ?", ('%' + search_query + '%',))
        else:
            c.execute('''SELECT Players.name
                         FROM Players
                         JOIN Played_In ON Players.player_ID = Played_In.player
                         JOIN Games ON Played_In.game = Games.game_Id
                         JOIN Competed_In ON Games.game_Id = Competed_In.game
                         JOIN Teams ON Competed_In.team = Teams.full_name
                         WHERE Players.name LIKE ? AND Teams.full_name = ?''', ('%' + search_query + '%', teams[team_query]))
        results = c.fetchall()
        results = list(results)
        print(results)
        conn.close()
        return render_template('search.html', items=results)
    return render_template('search.html', results=[])

# @app.route('/player/<int:player_id>')
# def player(player_id):
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM Players WHERE id = ?", (player_id,))
#     player = c.fetchone()
#     conn.close()
#     if player:
#         return render_template('player.html', player=player)
#     else:
#         return "Player not found", 404

if __name__ == '__main__':
    # init_db()
    app.run(debug=True)