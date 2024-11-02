from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_connection import get_db_connection, delete_club  # Ensure this is the correct DB connection function


main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Fetch clubs for the index page if needed
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT club_id, club_name FROM Club")  # Adjust to your actual column names
    clubs = cursor.fetchall()
    connection.close()
    
    return render_template('index.html', clubs=clubs)


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



@main.route('/add_club', methods=['GET'])
def add_club_page():
    # Connect to the database and fetch conference information
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT conference_id, conference_name FROM Conference")  # Adjust column names if needed
    conferences = cursor.fetchall()
    connection.close()
    
    return render_template('club/add_club.html', conferences=conferences)


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
    
    flash('Club added successfully!')
    return redirect(url_for('main.clubs'))



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
    
    flash('Club updated successfully!')
    return redirect(url_for('main.clubs'))




@main.route('/delete_club/<int:club_id>', methods=['POST'])
def delete_club(club_id):
    try:
        print(f"Attempting to delete club with ID: {club_id}")
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Club WHERE club_id = ?", (club_id,))
                print(f"Delete executed for club ID {club_id}")  # Confirm deletion statement execution
                connection.commit()
                print(f"Club with ID {club_id} deleted successfully.")
            connection.close()
        flash("Club deleted successfully", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        print(f"Error during deletion: {e}")
    return redirect(url_for('main.clubs'))


