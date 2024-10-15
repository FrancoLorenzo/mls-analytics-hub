--------------------------------------------------------------------------
-- MLS Analytics Hub Database
--------------------------------------------------------------------------

-- Create the MLS Analytics Hub database
CREATE DATABASE mls_analytics_hub_db;
use mls_analytics_hub_db;

-- Create the Conference table
CREATE TABLE Conference (
    Conference_ID INT PRIMARY KEY,
    Conference_Name VARCHAR(100)
);

-- Create the Club table
CREATE TABLE Club (
    Club_ID INT PRIMARY KEY,
    Conference_ID INT,
    Club_Name VARCHAR(100),
    Club_Name_Abbreviation VARCHAR(10),
    Club_Established_date DATE,
    Club_badge VARCHAR(255),
    FOREIGN KEY (Conference_ID) REFERENCES Conference(Conference_ID)
);

-- Create the Year table
CREATE TABLE Year (
    Year_ID INT PRIMARY KEY,
    Year INT
);

-- Create the Club_stats table
CREATE TABLE Club_stats (
    Club_stats_ID INT PRIMARY KEY,
    Club_ID INT,
    Year_ID INT,
    Total_Wins INT,
    Total_Losses INT,
    Total_Draws INT,
    FOREIGN KEY (Club_ID) REFERENCES Club(Club_ID),
    FOREIGN KEY (Year_ID) REFERENCES Year(Year_ID)
);

-- Create the Competition table
CREATE TABLE Competition (
    Competition_ID INT PRIMARY KEY,
    Competition_Name VARCHAR(100)
);

-- Create the Player table
CREATE TABLE Player (
    Player_ID INT PRIMARY KEY,
    Club_ID INT,
    Player_First_Name VARCHAR(50),
    Player_Last_Name VARCHAR(50),
    Birth_Date DATE,
    Birthplace VARCHAR(100),
    Height DECIMAL(4,2),  -- Height is in meters
    Weight DECIMAL(5,2),  -- Weight is in kilograms
    Position VARCHAR(50),
    FOREIGN KEY (Club_ID) REFERENCES Club(Club_ID)
);

-- Create the Player_stats table
CREATE TABLE Player_stats (
    Player_stats_ID INT PRIMARY KEY,
    Player_ID INT,
    Year_ID INT,
    Goals INT,
    Passes INT,
    Passes_complete INT,
    Assists INT,
    Free_kicks INT,
    Corner_kicks INT,
    Fouls INT,
    Fouls_suffered INT,
    Offside INT,
    Yellow_cards INT,
    Red_cards INT,
    FOREIGN KEY (Player_ID) REFERENCES Player(Player_ID),
    FOREIGN KEY (Year_ID) REFERENCES Year(Year_ID)
);

-- Create the Standings table
CREATE TABLE Standings (
    Standing_ID INT PRIMARY KEY,
    Competition_ID INT,
    Club_stats_ID INT,
    Year_ID INT,
    Total_points INT,
    FOREIGN KEY (Competition_ID) REFERENCES Competition(Competition_ID),
    FOREIGN KEY (Club_stats_ID) REFERENCES Club_stats(Club_stats_ID),
    FOREIGN KEY (Year_ID) REFERENCES Year(Year_ID)
);

---------------------------------------
-- Indexes for fast lookups
---------------------------------------

-- Index for Year lookups in Club_stats
CREATE INDEX idx_club_in_club_stats ON Club_stats(Year_ID);

-- Index for Year lookups in Player_stats
CREATE INDEX idx_year_in_player_stats ON Player_stats(Year_ID);

-- Index for fast searches on standings by competition
CREATE INDEX idx_competition_in_standings ON Standings(Competition_ID);

---------------------------------------
-- Views for data retrieval
---------------------------------------

-- View to get club performance stats
CREATE VIEW club_performance_view AS
SELECT c.Club_Name, cs.Total_Wins, cs.Total_Losses, cs.Total_Draws, y.Year
FROM Club c
JOIN Club_stats cs ON c.Club_ID = cs.Club_ID
JOIN Year y ON cs.Year_ID = y.Year_ID;

-- View to summarize player stats
CREATE VIEW player_summary_view AS
SELECT p.Player_First_Name, p.Player_Last_Name, ps.Goals, ps.Assists, ps.Passes, ps.Yellow_cards, ps.Red_cards, y.Year
FROM Player p
JOIN Player_stats ps ON p.Player_ID = ps.Player_ID
JOIN Year y ON ps.Year_ID = y.Year_ID;

---------------------------------------
-- Temporary Tables for Data Processing
---------------------------------------

-- Create a temporary table to hold top players by goals in the current year
CREATE TEMPORARY TABLE top_goal_scorers_temp AS
SELECT p.Player_ID, p.Player_First_Name, p.Player_Last_Name, ps.Goals
FROM Player_stats ps
JOIN Player p ON p.Player_ID = ps.Player_ID
WHERE ps.Year_ID = (SELECT Year_ID FROM Year WHERE Year = 2024)
ORDER BY ps.Goals DESC;


----------------------------------------
-- Triggers for data integrity
----------------------------------------

-- Trigger to update standings total points after club stats are updated
CREATE TRIGGER update_standings_after_club_stats
AFTER UPDATE ON Club_stats
FOR EACH ROW
BEGIN
    DECLARE total_wins INT;
    DECLARE total_draws INT;
    DECLARE total_losses INT;
    DECLARE total_points INT;

    -- Retrieve the updated total wins, losses, and draws
    SET total_wins = NEW.Total_Wins;
    SET total_draws = NEW.Total_Draws;
    SET total_losses = NEW.Total_Losses;

    -- Calculate total points: 3 points per win, 1 point per draw, 0 points per loss
    SET total_points = (total_wins * 3) + (total_draws * 1);

    -- Update the standings table with the calculated total points
    UPDATE Standings
    SET Total_points = total_points
    WHERE Club_stats_ID = NEW.Club_stats_ID;
END;


----------------------------------------
-- Stored Procedures for CRUD operations
----------------------------------------

-- Procedure to add a new player
DELIMITER //
CREATE PROCEDURE add_new_player(
    IN p_first_name VARCHAR(50), 
    IN p_last_name VARCHAR(50),
    IN p_birth_date DATE, 
    IN p_birthplace VARCHAR(100), 
    IN p_height DECIMAL(4,2), 
    IN p_weight DECIMAL(5,2), 
    IN p_position VARCHAR(50), 
    IN p_club_id INT
)
BEGIN
    INSERT INTO Player(Player_First_Name, Player_Last_Name, Birth_Date, Birthplace, Height, Weight, Position, Club_ID)
    VALUES (p_first_name, p_last_name, p_birth_date, p_birthplace, p_height, p_weight, p_position, p_club_id);
END //
DELIMITER ;


----------------------------------------
-- Functions for data processing
----------------------------------------

-- Function to calculate the win ratio for a club
DELIMITER //
CREATE FUNCTION get_win_ratio(club_id INT, year_id INT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE wins INT;
    DECLARE games_played INT;
    DECLARE win_ratio DECIMAL(5,2);

    -- Get total wins and games played for the given club and year
    SELECT Total_Wins, (Total_Wins + Total_Losses + Total_Draws)
    INTO wins, games_played
    FROM Club_stats
    WHERE Club_ID = club_id AND Year_ID = year_id;

    IF games_played > 0 THEN
        SET win_ratio = (wins / games_played) * 100;
    ELSE
        SET win_ratio = 0;
    END IF;

    RETURN win_ratio;
END //
DELIMITER ;
