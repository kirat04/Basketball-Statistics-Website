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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['query']
        team_query = int(request.form['team'])-1
        year = int(request.form['year'])
        points = int(request.form['points'])
        print("Search request received:" + teams[team_query] + " " + search_query)
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #find the all players that have this name if no team specified else use the team in the query
        if(team_query == -1):
            c.execute("SELECT name,player_ID FROM Players WHERE name LIKE ?", ('%' + search_query + '%',))
        else:
            c.execute('''SELECT DISTINCT Players.name, Players.player_ID
                         FROM Players
                         JOIN Played_In ON Players.player_ID = Played_In.player
                         JOIN Games ON Played_In.game = Games.game_Id
                         JOIN Competed_In ON Games.game_Id = Competed_In.game
                         JOIN Teams ON Competed_In.team = Teams.full_name
                         WHERE Players.name LIKE ? AND Teams.full_name = ?''', ('%' + search_query + '%', teams[team_query]))
        results = c.fetchall()
        results = list(results)
        print(results)
        #for each player, get the games they played in
        game_results = []
        #if there i a team query, use the team query to get the games
        if team_query != -1 :
            #if year is 0, get all games, else get games for that year
            if year == 0:
                for result in results:
                    c.execute('''SELECT Players.name, Games.game_Id, Games.Date, Games.season_played, Played_In.points, Played_In.rebounds, Played_In.assists, Played_In.steals, Played_In.blocks
                        FROM Played_In
                        JOIN Players ON Played_In.player = Players.player_ID
                        JOIN Games ON Played_In.game = Games.game_Id
                        JOIN Competed_In ON Games.game_Id = Competed_In.game
                        JOIN Teams ON Competed_In.team = Teams.full_name
                        WHERE Players.name = ? 
                        AND Played_In.points > ?
                        AND Teams.full_name = ?''', (result[0], points, teams[team_query]))
                    game_results.append((result, c.fetchall()))
            else:
                for result in results:
                    c.execute('''SELECT Players.name, Games.game_Id, Games.Date, Games.season_played, Played_In.points, Played_In.rebounds, Played_In.assists, Played_In.steals, Played_In.blocks
                                FROM Played_In
                                JOIN Players ON Played_In.player = Players.player_ID
                                JOIN Games ON Played_In.game = Games.game_Id
                                JOIN Competed_In ON Games.game_Id = Competed_In.game
                                JOIN Teams ON Competed_In.team = Teams.full_name
                                WHERE Players.name = ? 
                                AND Games.season_played = ? 
                                AND Played_In.points > ?
                                AND Teams.full_name = ?''', (result[0], year, points, teams[team_query]))
                    game_results.append((result, c.fetchall()))
       #if there is no team query, get all games
        elif year == 0:
            for result in results:
                c.execute('''SELECT Players.name, Games.game_Id, Games.Date, Games.season_played, Played_In.points, Played_In.rebounds, Played_In.assists, Played_In.steals, Played_In.blocks
                             FROM Played_In
                             JOIN Players ON Played_In.player = Players.player_ID
                             JOIN Games ON Played_In.game = Games.game_Id
                             WHERE Players.name = ? 
                               AND Played_In.points > ?''', (result[0], points))
                game_results.append((result,c.fetchall()))
        #if there is a year, but no team, get games for that year
        else:
            for result in results:
                c.execute('''SELECT Players.name, Games.game_Id, Games.Date, Games.season_played, Played_In.points, Played_In.rebounds, Played_In.assists, Played_In.steals, Played_In.blocks
                            FROM Played_In
                            JOIN Players ON Played_In.player = Players.player_ID
                            JOIN Games ON Played_In.game = Games.game_Id
                            WHERE Players.name = ? 
                            AND Games.season_played = ? 
                            AND Played_In.points > ?''', (result[0], year, points))
                game_results.append((result,c.fetchall()))
        print(game_results)
        conn.close()
        return render_template('search.html', items=game_results, games = game_results)
    return render_template('search.html', results=[])

@app.route('/player/<int:player_id>')
def player(player_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT Players.name, Games.game_Id, Games.Date, Games.season_played, Played_In.points, Played_In.rebounds, Played_In.assists, Played_In.steals, Played_In.blocks
                FROM Played_In
                JOIN Players ON Played_In.player = Players.player_ID
                JOIN Games ON Played_In.game = Games.game_Id
                WHERE Players.player_ID = ?''', (player_id,))
    player = c.fetchall()
    conn.close()
    if player:
        return render_template('player.html', player=player)
    else:
        return "Player not found", 404

if __name__ == '__main__':
    app.run(debug=True)