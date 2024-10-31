from flask import Blueprint, render_template
from .db_connection import get_db_connection  # Make sure this is your database connection function

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Fetch clubs for the index page if needed
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT club_id, club_name FROM Club")  # Replace with your actual column names
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

@main.route('/clubs/conference/<int:conference_id>')
def clubs_by_conference(conference_id):
    # Connect to the database and fetch conference and filtered club information
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch all conferences for the dropdown
    cursor.execute("SELECT Conference_id, Conference_Name FROM Conference")
    conferences = cursor.fetchall()
    
    # Fetch clubs for the selected conference
    cursor.execute("SELECT club_id, club_name, city, stadium FROM Club WHERE conference_id = %s", (conference_id,))
    clubs = cursor.fetchall()
    
    connection.close()
    
    return render_template('clubs.html', conferences=conferences, clubs=clubs, selected_conference=conference_id)