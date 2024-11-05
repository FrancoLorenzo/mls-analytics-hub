from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_connection import get_db_connection  


main = Blueprint('main', __name__)

@main.route('/')
def index():

    return render_template('index.html')


#region Club routes
# Club route
@main.route('/clubs', methods=['GET', 'POST'])
def clubs():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch all available conferences for the dropdown
    cursor.execute("SELECT Conference_ID, Conference_Name FROM Conference")
    conferences = cursor.fetchall()

    # Default: Show all clubs if no filter is applied
    conference_id = request.args.get('conference_id')
    
    # If conference_id is provided, filter clubs by the selected conference
    if conference_id and conference_id.isdigit():  # Make sure the ID is a valid number
        cursor.execute("SELECT Club_ID, Club_Name, Club_Name_Abbreviation, Club_badge, Club_Established_Date FROM Club WHERE Conference_ID = ? AND Club_Name != 'Free Agent' ORDER BY Club_Name", (conference_id,))
    else:
        cursor.execute("SELECT Club_ID, Club_Name, Club_Name_Abbreviation, Club_badge, Club_Established_Date FROM Club WHERE Club_Name != 'Free Agent' ORDER BY Club_Name")
    
    clubs = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('clubs.html', clubs=clubs, conferences=conferences, selected_conference=conference_id)


# Add club route
@main.route('/add_club', methods=['GET'])
def add_club_page():
    # Connect to the database and fetch conference information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT conference_id, conference_name FROM Conference")  
    conferences = cursor.fetchall()
    connection.close()
    
    return render_template('club/add_club.html', conferences=conferences)


# Create club route
@main.route('/create_club', methods=['POST'])
def create_club():
    # Get form data
    conference_id = request.form['conference_id']
    club_name = request.form['club_name']
    club_abbr = request.form['club_abbr']
    established_date = request.form['established_date']
    club_badge = request.form['club_badge']

    # Connect to the database and insert the new club
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Club (Conference_ID, Club_Name, Club_Name_Abbreviation, Club_Established_date, Club_badge) "
        "VALUES (?, ?, ?, ?, ?)", 
        (conference_id, club_name, club_abbr, established_date, club_badge)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Club created successfully!", "success")

    return redirect(url_for('main.clubs'))


# Edit club route
@main.route('/club/<int:club_id>/edit', methods=['GET'])
def edit_club(club_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch club details
    cursor.execute("SELECT * FROM Club WHERE Club_ID = ?", (club_id,))
    club = cursor.fetchone()

    # Fetch all available conferences for dropdown
    cursor.execute("SELECT Conference_ID, Conference_Name FROM Conference")
    conferences = cursor.fetchall()  # Each entry contains Conference_ID and Conference_Name

    cursor.close()
    connection.close()

    return render_template('club/update_club.html', club=club, conferences=conferences)


# Update club route
@main.route('/club/<int:club_id>/update', methods=['POST'])
def update_club(club_id):
    # Get form data
    conference_id = request.form['conference_id']
    club_name = request.form['club_name']
    club_abbr = request.form['club_abbr']
    established_date = request.form['established_date']
    club_badge = request.form['club_badge']

    # Connect to the database and update the club
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Club SET Conference_ID = ?, Club_Name = ?, Club_Name_Abbreviation = ?, "
        "Club_Established_date = ?, Club_badge = ? WHERE Club_ID = ?",
        (conference_id, club_name, club_abbr, established_date, club_badge, club_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    # Flash success message
    flash("Club updated successfully!", "success")
    
    return redirect(url_for('main.clubs'))


# Delete club route
@main.route('/delete_club/<int:club_id>', methods=['POST'])
def delete_club(club_id):
    try:
        print(f"Attempting to delete club with ID: {club_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Club WHERE club_id = ?", (club_id,))
                print(f"Delete executed for club ID {club_id}")  
                connection.commit()
                print(f"Club with ID {club_id} deleted successfully.")
            connection.close()
        flash("Club deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.clubs'))

#endregion

#region Year routes
# Year route
@main.route('/years', methods=['GET'])
def years():
    # Connect to the database and fetch year information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Year_ID, Year FROM Year")  
    years = cursor.fetchall()
    connection.close()
    
    return render_template('years.html', years=years)


# Add year route
@main.route('/add_year', methods=['GET'])
def add_year_page():
    # Connect to the database and fetch year information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Year_ID, Year FROM Year") 
    conferences = cursor.fetchall()
    connection.close()
    
    return render_template('year/add_year.html')


# Create year route
@main.route('/create_year', methods=['POST'])
def create_year():
    # Get form data for 'year' only
    year = request.form['year']
    
    # Connect to the database and insert the new year
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Year (Year) "
        "VALUES (?)", 
        (year,)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Year created successfully!", "success")

    return redirect(url_for('main.years'))


# Edit year route
@main.route('/year/<int:year_id>/edit', methods=['GET'])
def edit_year(year_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch year details
    cursor.execute("SELECT * FROM Year WHERE Year_ID = ?", (year_id,))
    year = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('year/update_year.html', year=year)


# Update year route
@main.route('/year/<int:year_id>/update', methods=['POST'])
def update_year(year_id):
    # Get form data
    year = request.form['year']

    # Connect to the database and update the year
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Year SET Year = ? WHERE Year_ID = ?",
        (year, year_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Year updated successfully!", "success")

    return redirect(url_for('main.years'))


# Delete year route
@main.route('/delete_year/<int:year_id>', methods=['POST'])
def delete_year(year_id):
    try:
        print(f"Attempting to delete club with ID: {year_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Year WHERE year_id = ?", (year_id,))
                print(f"Delete executed for Year ID {year_id}")
                connection.commit()
                print(f"Club with ID {year_id} deleted successfully.")
            connection.close()
        flash("Year deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.years'))

#endregion

#region Conference routes
# Conference route
@main.route('/conferences', methods=['GET'])
def conferences():
    # Connect to the database and fetch year information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Conference_ID, Conference_Name FROM Conference ORDER BY Conference_Name")  
    conferences = cursor.fetchall()
    connection.close()
    
    return render_template('conferences.html', conferences=conferences)


# Add conference route
@main.route('/add_conference', methods=['GET'])
def add_conference_page():
    # Connect to the database and fetch conference information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Conference_ID, Conference_Name FROM Conference") 
    conferences = cursor.fetchall()
    connection.close()
    
    return render_template('conference/add_conference.html', conferences=conferences)


# Create conference route
@main.route('/create_conference', methods=['POST'])
def create_conference():
    # Get form data for 'conference' only
    conference = request.form['conference']
    
    # Connect to the database and insert the new conference
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Conference (Conference_Name) "  # Updated to match the correct column name
        "VALUES (?)", 
        (conference,)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Conference created successfully!", "success")

    return redirect(url_for('main.conferences'))


# Edit conference route
@main.route('/conference/<int:conference_id>/edit', methods=['GET'])
def edit_conference(conference_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch year details
    cursor.execute("SELECT * FROM Conference WHERE Conference_ID = ?", (conference_id,))
    conference = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('conference/update_conference.html', conference=conference)


# Update conference route
@main.route('/conference/<int:conference_id>/update', methods=['POST'])
def update_conference(conference_id):
    # Get form data
    conference = request.form['conference']

    # Connect to the database and update the conference
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Conference SET Conference_Name = ? WHERE Conference_ID = ?",
        (conference, conference_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Conference updated successfully!", "success")

    return redirect(url_for('main.conferences'))


# Delete conference route
@main.route('/delete_conference/<int:conference_id>', methods=['POST'])
def delete_conference(conference_id):
    try:
        print(f"Attempting to delete conference with ID: {conference_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Conference WHERE conference_id = ?", (conference_id,))
                print(f"Delete executed for Conference ID {conference_id}")
                connection.commit()
                print(f"Conference with ID {conference_id} deleted successfully.")
            connection.close()
        flash("Conference deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.conferences'))

#endregion

#region Player routes
# Player route
@main.route('/players', methods=['GET'])
def players():
    # Connect to the database and fetch player information
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all available clubs for the dropdown
    cursor.execute("SELECT Club_ID, Club_Name FROM Club")
    clubs = cursor.fetchall()

    # Default: Show all players if no filter is applied
    club_id = request.args.get('club_id')

    # If club_id is provided, filter players by the selected club
    if club_id and club_id.isdigit():  # Make sure the ID is a valid number
        cursor.execute("SELECT * FROM Player WHERE Club_ID = ?", (club_id,))
    else:
        cursor.execute("SELECT * FROM Player")
 
    players = cursor.fetchall()

    connection.close()
    return render_template('players.html', players=players, clubs=clubs, selected_club=club_id)


# Add player route
@main.route('/add_player', methods=['GET'])
def add_player_page():
    # Connect to the database and fetch player information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Club_ID, Club_Name FROM Club") 
    clubs = cursor.fetchall()
    connection.close()
    
    return render_template('player/add_player.html', clubs=clubs)


# Create player route
@main.route('/create_player', methods=['POST'])
def create_player():
    # Get form data
    club_id = request.form['club_id']
    
    # Connect to the database and insert the new player
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Player (Club_ID, Player_First_Name, Player_Last_Name, Birth_Date, Birthplace, Height, Weight, Position) " 
        "VALUES (?, ? , ? , ? , ? , ? , ? , ?)", 
        (club_id, request.form['player_first_name'], request.form['player_last_name'], request.form['birth_date'], request.form['birthplace'], request.form['height'], request.form['weight'], request.form['position'])
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Player created successfully!", "success")

    return redirect(url_for('main.players'))


# Edit Player route
@main.route('/player/<int:player_id>/edit', methods=['GET'])
def edit_player(player_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch player details
    cursor.execute("SELECT * FROM Player WHERE Player_ID = ?", (player_id,))
    player = cursor.fetchone()

    # Fetch all available clubs for dropdown
    cursor.execute("SELECT Club_ID, Club_Name FROM Club")
    clubs = cursor.fetchall() 

    cursor.close()
    connection.close()

    return render_template('player/update_player.html', player=player, clubs=clubs)


# Update player route
@main.route('/player/<int:player_id>/update', methods=['POST'])
def update_player(player_id):
    # Get form data
    club_id = request.form['club_id']
    player_first_name = request.form['player_first_name']
    player_last_name = request.form['player_last_name']
    birth_date = request.form['birth_date']
    birthplace = request.form['birthplace']
    height = request.form['height']
    weight = request.form['weight']
    position = request.form['position']

    # Connect to the database and update the club
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Player SET Club_ID = ?, Player_First_Name = ?, Player_Last_Name = ?, Birth_date = ?, Birthplace = ?, Height = ?, Weight = ?, Position = ? WHERE Player_ID = ?",
        (club_id, player_first_name, player_last_name, birth_date, birthplace, height, weight, position, player_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Player updated successfully!", "success")

    return redirect(url_for('main.players'))


# Delete player route
@main.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    try:
        print(f"Attempting to delete player with ID: {player_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Player WHERE Player_id = ?", (player_id,))
                print(f"Delete executed for Player ID {player_id}")
                connection.commit()
                print(f"Player with ID {player_id} deleted successfully.")
            connection.close()
        flash("Player deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.players'))

#endregion

#region Player Stats routes
# Player stats route
@main.route('/players_stats', methods=['GET'])
def players_stats():
    # Get the year filter parameter from the query string
    year_id = request.args.get('year_id')
    
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Build SQL query with an optional year filter
    query = """
        SELECT 
            ps.Player_stats_ID, 
            ps.Player_ID, 
            CONCAT(p.Player_First_Name, ' ', p.Player_Last_Name) AS Player_Name, 
            y.Year, 
            ps.Goals, 
            ps.Passes, 
            ps.Passes_complete, 
            ps.Assists, 
            ps.Free_kicks, 
            ps.Corner_kicks, 
            ps.Fouls, 
            ps.Fouls_suffered, 
            ps.Offside, 
            ps.Yellow_cards, 
            ps.Red_cards
        FROM 
            Player_Stats ps
        JOIN 
            Player p ON ps.Player_ID = p.Player_ID
        JOIN 
            Year y ON ps.Year_ID = y.Year_ID
    """

    # Add filter condition if a year is selected
    filters = []
    if year_id:
        query += " WHERE ps.Year_ID = ?"
        filters.append(year_id)
    
    cursor.execute(query, filters)
    players_stats = cursor.fetchall()
    
    # Fetch available years for the filter dropdown
    cursor.execute("SELECT Year_ID, Year FROM Year")
    years = cursor.fetchall()

    connection.close()
    
    return render_template(
        'players_stats.html', 
        players_stats=players_stats, 
        years=years,
        selected_year=year_id
    )



# Add player stats route
@main.route('/add_player_stat', methods=['GET'])
def add_player_stats():
    # Connect to the database and fetch necessary information for dropdowns (e.g., player names and years)
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch player IDs and first names for dropdown
    cursor.execute("SELECT Player_ID, CONCAT(Player_First_Name, ' ', Player_Last_Name) AS Player_Name FROM Player")
    players = cursor.fetchall()
    
    # Fetch year IDs and actual year values for dropdown
    cursor.execute("SELECT Year_ID, Year FROM Year")
    years = cursor.fetchall()
    
    connection.close()
    
    return render_template('player/add_player_stats.html', players=players, years=years)


# Create player stat route
@main.route('/create_player_stat', methods=['POST'])
def create_player_stat():
    # Get form data for player stats
    player_id = request.form['player_id']
    year_id = request.form['year_id']
    goals = request.form['goals']
    passes = request.form['passes']
    passes_complete = request.form['passes_complete']
    assists = request.form['assists']
    free_kicks = request.form['free_kicks']
    corner_kicks = request.form['corner_kicks']
    fouls = request.form['fouls']
    fouls_suffered = request.form['fouls_suffered']
    offside = request.form['offside']
    yellow_cards = request.form['yellow_cards']
    red_cards = request.form['red_cards']

    # Connect to the database and insert the new player stat
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO player_stats (
            Player_ID, Year_ID, Goals, Passes, Passes_complete, Assists, 
            Free_kicks, Corner_kicks, Fouls, Fouls_suffered, Offside, 
            Yellow_cards, Red_cards
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?) 
    """, (player_id, year_id, goals, passes, passes_complete, assists, free_kicks, corner_kicks, fouls, fouls_suffered, offside, yellow_cards, red_cards))
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Player stats created successfully!", "success")

    return redirect(url_for('main.players_stats'))


# Edit player stat route
@main.route('/player_stat/<int:player_stat_id>/edit', methods=['GET'])
def edit_player_stat(player_stat_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch player stat details including Year_ID and Year for dropdown selection
    cursor.execute("""
        SELECT 
            ps.Player_stats_ID, ps.Player_ID, p.Player_First_Name, p.Player_Last_Name, 
            ps.Year_ID, y.Year, ps.Goals, ps.Passes, ps.Passes_complete, ps.Assists, 
            ps.Free_kicks, ps.Corner_kicks, ps.Fouls, ps.Fouls_suffered, ps.Offside, 
            ps.Yellow_cards, ps.Red_cards 
        FROM Player_Stats ps
        JOIN Player p ON ps.Player_ID = p.Player_ID
        JOIN Year y ON ps.Year_ID = y.Year_ID
        WHERE ps.Player_stats_ID = ?
    """, (player_stat_id,))
    player_stat = cursor.fetchone()

    # Fetch available players and years for dropdowns
    cursor.execute("SELECT Player_ID, CONCAT(Player_First_Name, ' ', Player_Last_Name) AS Player_Name FROM Player")
    players = cursor.fetchall()
    
    cursor.execute("SELECT Year_ID, Year FROM Year")
    years = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('player/update_player_stats.html', player_stat=player_stat, players=players, years=years)


# Update player stat route
@main.route('/player_stat/<int:player_stat_id>/update', methods=['POST'])
def update_player_stat(player_stat_id):
    # Get form data
    player_id = request.form['player_id']
    year_id = request.form['year_id']
    goals = request.form['goals']
    passes = request.form['passes']
    passes_complete = request.form['passes_complete']
    assists = request.form['assists']
    free_kicks = request.form['free_kicks']
    corner_kicks = request.form['corner_kicks']
    fouls = request.form['fouls']
    fouls_suffered = request.form['fouls_suffered']
    offside = request.form['offside']
    yellow_cards = request.form['yellow_cards']
    red_cards = request.form['red_cards']

    # Connect to the database and update the player stat
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Player_Stats 
        SET Player_ID = ?, Year_ID = ?, Goals = ?, Passes = ?, Passes_complete = ?, 
            Assists = ?, Free_kicks = ?, Corner_kicks = ?, Fouls = ?, Fouls_suffered = ?, 
            Offside = ?, Yellow_cards = ?, Red_cards = ?
        WHERE Player_stats_ID = ?
    """, (player_id, year_id, goals, passes, passes_complete, assists, 
          free_kicks, corner_kicks, fouls, fouls_suffered, offside, yellow_cards, 
          red_cards, player_stat_id))
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Player stats updated successfully!", "success")

    return redirect(url_for('main.players_stats'))


# Delete player stat route
@main.route('/player_stat/<int:player_stat_id>/delete', methods=['POST'])
def delete_player_stat(player_stat_id):
    # Connect to the database and delete the player stat
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Player_Stats WHERE Player_stats_ID = ?", (player_stat_id,))
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Player stats deleted successfully!", "success")

    return redirect(url_for('main.players_stats'))

#endregion

#region Club Stats routes
# Clubs_stats route
@main.route('/clubs_stats', methods=['GET'])
def clubs_stats():
    # Connect to the database and fetch club stats information with club names and year numbers
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            cs.Club_Stats_ID, 
            c.Club_Name, 
            co.Competition_Name,
            y.Year, 
            cs.Total_Wins, 
            cs.Total_Losses, 
            cs.Total_Draws 
        FROM Club_stats cs
        JOIN Club c ON cs.Club_ID = c.Club_ID
        JOIN Year y ON cs.Year_ID = y.Year_ID
        JOIN Competition co ON cs.Competition_ID = co.Competition_ID
    """)
    clubs_stats = cursor.fetchall()
    connection.close()
    
    return render_template('clubs_stats.html', clubs_stats=clubs_stats)


# Add club stats route
@main.route('/add_club_stats', methods=['GET'])
def add_club_stats_page():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Club_ID, Club_Name FROM Club")  # Fetch available clubs
    clubs = cursor.fetchall()
    
    cursor.execute("SELECT Year_ID, Year FROM Year")  # Fetch available years
    years = cursor.fetchall()

    cursor.execute("SELECT Competition_ID, Competition_Name FROM Competition")  # Fetch available competitions
    competitions = cursor.fetchall()
    
    connection.close()
    
    return render_template('club/add_club_stats.html', clubs=clubs, years=years, competitions=competitions)



# Create club stats route
@main.route('/create_club_stats', methods=['POST'])
def create_club_stats():
    # Get form data for club stats
    club_id = request.form['club_id']
    year_id = request.form['year_id']
    competition_id = request.form['competition_id']
    total_wins = request.form['total_wins']
    total_losses = request.form['total_losses']
    total_draws = request.form['total_draws']
    
    # Connect to the database and insert the new club stats
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Club_stats (Club_ID, Year_ID, Competition_ID, Total_Wins, Total_Losses, Total_Draws) "
        "VALUES (?, ?, ?, ?, ?, ?)", 
        (club_id, year_id, competition_id, total_wins, total_losses, total_draws)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Club stats created successfully!", "success")

    return redirect(url_for('main.clubs_stats'))


# Edit club stats route
@main.route('/club_stats/<int:club_stats_id>/edit', methods=['GET'])
def edit_club_stats(club_stats_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch club stats details including Competition_ID
    cursor.execute("""
        SELECT 
            cs.Club_Stats_ID, 
            cs.Club_ID, 
            cs.Year_ID,
            cs.Competition_ID,
            cs.Total_Wins, 
            cs.Total_Losses, 
            cs.Total_Draws 
        FROM Club_stats cs
        WHERE cs.Club_Stats_ID = ?
    """, (club_stats_id,))
    club_stats = cursor.fetchone()

    # Fetch available clubs, years, and competitions for dropdowns
    cursor.execute("SELECT Club_ID, Club_Name FROM Club")
    clubs = cursor.fetchall()
    
    cursor.execute("SELECT Year_ID, Year FROM Year")
    years = cursor.fetchall()

    cursor.execute("SELECT Competition_ID, Competition_Name FROM Competition")
    competitions = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('club/update_club_stats.html', club_stats=club_stats, clubs=clubs, years=years, competitions=competitions)



# Update club stats route
@main.route('/club_stats/<int:club_stats_id>/update', methods=['POST'])
def update_club_stats(club_stats_id):
    # Get form data
    club_id = request.form['club_id']
    year_id = request.form['year_id']
    competition_id = request.form['competition_id']
    total_wins = request.form['total_wins']
    total_losses = request.form['total_losses']
    total_draws = request.form['total_draws']

    # Connect to the database and update the club stats
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE Club_stats 
        SET Club_ID = ?, Year_ID = ?, Competition_ID = ?, Total_Wins = ?, Total_Losses = ?, Total_Draws = ?
        WHERE Club_Stats_ID = ?
        """, 
        (club_id, year_id, competition_id, total_wins, total_losses, total_draws, club_stats_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    flash("Club stats updated successfully!", "success")

    return redirect(url_for('main.clubs_stats'))



# Delete club stats route
@main.route('/delete_club_stats/<int:club_stats_id>', methods=['POST'])
def delete_club_stats(club_stats_id):
    try:
        print(f"Attempting to delete club stats with ID: {club_stats_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Club_stats WHERE Club_Stats_ID = ?", (club_stats_id,))
                print(f"Delete executed for Club Stats ID {club_stats_id}")
                connection.commit()
                print(f"Club stats with ID {club_stats_id} deleted successfully.")
            connection.close()
        flash("Club stats deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.clubs_stats'))

#endregion

#region Competition routes
# Competition route
@main.route('/competitions', methods=['GET'])
def competitions():
    # Connect to the database and fetch competition information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Competition_ID, Competition_Name FROM Competition ORDER BY Competition_Name")
    competitions = cursor.fetchall()
    connection.close()
    
    return render_template('competitions.html', competitions=competitions)


# Add competition route
@main.route('/add_competition', methods=['GET'])
def add_competition_page():
    # Render the form for adding a competition with Competition_ID and Competition_Name fields
    return render_template('competitions/add_competition.html')


# Create competition route
@main.route('/create_competition', methods=['POST'])
def create_competition():
    # Get form data for competition ID and name
    competition_name = request.form['competition_name']
    
    # Connect to the database and insert the new competition
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Competition (Competition_Name) VALUES (?)",
        (competition_name)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Competition created successfully!", "success")

    return redirect(url_for('main.competitions'))


# Edit competition route
@main.route('/competition/<int:competition_id>/edit', methods=['GET'])
def edit_competition(competition_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch competition details
    cursor.execute("SELECT * FROM Competition WHERE Competition_ID = ?", (competition_id,))
    competition = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('competitions/update_competition.html', competition=competition)


# Update competition route
@main.route('/competition/<int:competition_id>/update', methods=['POST'])
def update_competition(competition_id):
    # Get form data
    competition_name = request.form['competition_name']

    # Connect to the database and update the competition
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Competition SET Competition_Name = ? WHERE Competition_ID = ?",
        (competition_name, competition_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # Flash success message
    flash("Competition updated successfully!", "success")

    return redirect(url_for('main.competitions'))


# Delete competition route
@main.route('/delete_competition/<int:competition_id>', methods=['POST'])
def delete_competition(competition_id):
    try:
        print(f"Attempting to delete competition with ID: {competition_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Competition WHERE Competition_ID = ?", (competition_id,))
                print(f"Delete executed for Competition ID {competition_id}")
                connection.commit()
                print(f"Competition with ID {competition_id} deleted successfully.")
            connection.close()
        flash("Competition deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.competitions'))

#endregion

#region Standings routes
# Standings route
@main.route('/standings', methods=['GET'])
def standings():
    # Get filter parameters from query string
    competition_id = request.args.get('competition_id')
    year_id = request.args.get('year_id')
    
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Build SQL query with optional filters and order by Total_points in descending order
    query = """
        SELECT 
            s.Standing_ID, 
            cl.Club_Name, 
            y.Year,
            co.Competition_Name, 
            s.Total_points, 
            cs.Total_Wins, 
            cs.Total_Losses, 
            cs.Total_Draws
        FROM Standings s
        JOIN Club_stats cs ON s.Club_stats_ID = cs.Club_Stats_ID
        JOIN Club cl ON cs.Club_ID = cl.Club_ID
        JOIN Year y ON s.Year_ID = y.Year_ID
        JOIN Competition co ON cs.Competition_ID = co.Competition_ID
    """
    
    filters = []
    if competition_id:
        query += " WHERE cs.Competition_ID = ?"
        filters.append(competition_id)
    if year_id:
        if filters:
            query += " AND s.Year_ID = ?"
        else:
            query += " WHERE s.Year_ID = ?"
        filters.append(year_id)
    
    # Add the ORDER BY clause to sort by Total_points descending
    query += " ORDER BY s.Total_points DESC"
    
    cursor.execute(query, filters)
    standings = cursor.fetchall()
    
    # Fetch options for filters
    cursor.execute("SELECT Competition_ID, Competition_Name FROM Competition")
    competitions = cursor.fetchall()

    cursor.execute("SELECT Year_ID, Year FROM Year")
    years = cursor.fetchall()

    connection.close()

    return render_template(
        'standings.html', 
        standings=standings,
        competitions=competitions,
        years=years,
        selected_competition=competition_id,
        selected_year=year_id
    )



# Add standing route with combined dropdown for Club, Competition, and Year
@main.route('/add_standing', methods=['GET'])
def add_standing_page():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch combined data for Club, Competition, and Year
    cursor.execute("""
        SELECT 
            Club_stats.Club_Stats_ID, 
            Club.Club_Name, 
            Competition.Competition_Name, 
            Year.Year
        FROM Club_stats
        JOIN Club ON Club_stats.Club_ID = Club.Club_ID
        JOIN Competition ON Club_stats.Competition_ID = Competition.Competition_ID
        JOIN Year ON Club_stats.Year_ID = Year.Year_ID
    """)
    club_competition_year = cursor.fetchall()

    connection.close()
    
    return render_template('standings/add_standing.html', club_competition_year=club_competition_year)





# Create standing route
@main.route('/create_standing', methods=['POST'])
def create_standing():
    try:
        # Get form data for the new standing entry
        club_stats_id = request.form['club_stats_id']
        
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Retrieve Year_ID and stats (wins, losses, draws) from Club_stats for the selected Club_stats_ID
        cursor.execute("""
            SELECT Year_ID, Total_Wins, Total_Losses, Total_Draws 
            FROM Club_stats 
            WHERE Club_Stats_ID = ?
        """, (club_stats_id,))
        result = cursor.fetchone()
        
        if result is None:
            flash("Error: Club stats not found for the selected Club Stats ID.", "danger")
            return redirect(url_for('main.add_standing_page'))
        
        year_id, total_wins, total_losses, total_draws = result
        
        # Calculate Total_points based on wins, losses, and draws
        total_points = (total_wins * 3) + (total_draws * 1) + (total_losses * 0)
        
        # Insert the new standing with Club_stats_ID, Year_ID, and calculated Total_points
        cursor.execute(
            """
            INSERT INTO Standings (Club_stats_ID, Year_ID, Total_points) 
            VALUES (?, ?, ?)
            """,
            (club_stats_id, year_id, total_points)
        )
        
        # Commit transaction
        connection.commit()
        flash("Standing created successfully with calculated total points!", "success")
    except Exception as e:
        # Log and flash any errors
        flash(f"An error occurred: {e}", "danger")
        print(f"Error during standing creation: {e}")
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('main.standings'))







# Edit standing route
@main.route('/standing/<int:standing_id>/edit', methods=['GET'])
def edit_standing(standing_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch standing details without Competition_ID (retrieve via Club_stats if needed)
    cursor.execute("""
        SELECT 
            s.Standing_ID, 
            s.Club_stats_ID, 
            s.Year_ID, 
            s.Total_points 
        FROM Standings s
        WHERE s.Standing_ID = ?
    """, (standing_id,))
    standing = cursor.fetchone()

    # Fetch available club stats for dropdowns, including competition and year details
    cursor.execute("""
        SELECT 
            cs.Club_Stats_ID, 
            cl.Club_Name, 
            co.Competition_Name, 
            y.Year
        FROM Club_stats cs
        JOIN Club cl ON cs.Club_ID = cl.Club_ID
        JOIN Competition co ON cs.Competition_ID = co.Competition_ID
        JOIN Year y ON cs.Year_ID = y.Year_ID
    """)
    club_stats = cursor.fetchall()
    
    # Fetch available years for the dropdown (optional, depending on requirements)
    cursor.execute("SELECT Year_ID, Year FROM Year")
    years = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        'standings/update_standing.html', 
        standing=standing, 
        club_stats=club_stats, 
        years=years
    )



# Update standing route
@main.route('/standing/<int:standing_id>/update', methods=['POST'])
def update_standing(standing_id):
    # Get form data
    club_stats_id = request.form['club_stats_id']
    total_points = request.form.get('total_points', 0)  # Assuming there's an input for total points

    # Connect to the database and fetch Year_ID based on Club_stats_ID
    connection = get_db_connection()
    cursor = connection.cursor()

    # Retrieve the Year_ID associated with the selected Club_stats_ID
    cursor.execute("SELECT Year_ID FROM Club_stats WHERE Club_Stats_ID = ?", (club_stats_id,))
    year_id = cursor.fetchone()[0]
    
    if year_id is None:
        flash("Error: Year_ID not found for the selected Club Stats.", "danger")
        return redirect(url_for('main.edit_standing', standing_id=standing_id))

    # Update the standing with the retrieved Year_ID
    cursor.execute(
        """
        UPDATE Standings 
        SET Club_stats_ID = ?, Year_ID = ?, Total_points = ?
        WHERE Standing_ID = ?
        """,
        (club_stats_id, year_id, total_points, standing_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    # Flash success message
    flash("Standing updated successfully!", "success")    

    return redirect(url_for('main.standings'))




# Delete standing route
@main.route('/delete_standing/<int:standing_id>', methods=['POST'])
def delete_standing(standing_id):
    try:
        print(f"Attempting to delete standing with ID: {standing_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Standings WHERE Standing_ID = ?", (standing_id,))
                print(f"Delete executed for Standing ID {standing_id}")
                connection.commit()
                print(f"Standing with ID {standing_id} deleted successfully.")
            connection.close()
        flash("Standing deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.standings'))

#endregion