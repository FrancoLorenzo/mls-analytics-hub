from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_connection import get_db_connection  # Ensure this is the correct DB connection function

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

@main.route('/clubs')
def clubs():
    # Connect to the database and fetch conference and club information
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch all conferences for the dropdown
    cursor.execute("SELECT conference_id, conference_name FROM Conference")  # Adjust columns as needed
    conferences = cursor.fetchall()
    
    # Fetch all clubs by default (no filter)
    cursor.execute("SELECT Club_Name, Club_Name_Abbreviation, Club_badge FROM Club WHERE Club_Name != 'Free Agent'")
    clubs = cursor.fetchall()
    
    connection.close()
    
    return render_template('clubs.html', conferences=conferences, clubs=clubs)


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

