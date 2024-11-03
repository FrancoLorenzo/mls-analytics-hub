from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_connection import get_db_connection, delete_club  




main = Blueprint('main', __name__)

@main.route('/')
def index():

    return render_template('index.html', clubs=clubs)


# --------------------------------------------------------------------------------------------------------------------
# Club route details
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
        cursor.execute("SELECT Club_ID, Club_Name, Club_Name_Abbreviation, Club_badge, Club_Established_Date FROM Club WHERE Conference_ID = ? AND Club_Name != 'Free Agent'", (conference_id,))
    else:
        cursor.execute("SELECT Club_ID, Club_Name, Club_Name_Abbreviation, Club_badge, Club_Established_Date FROM Club WHERE Club_Name != 'Free Agent'")
    
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


# --------------------------------------------------------------------------------------------------------------------
# Year route details
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
        flash(" deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.years'))



# --------------------------------------------------------------------------------------------------------------------
# Conference route details
# Conference route
@main.route('/conferences', methods=['GET'])
def conferences():
    # Connect to the database and fetch year information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Conference_ID, Conference_Name FROM Conference")  
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
        flash(" deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.conferences'))




# --------------------------------------------------------------------------------------------------------------------
# Player route details
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
        flash(" deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.players'))
