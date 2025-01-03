--------------------------------------------------------------------------
-- MLS Analytics Hub Database
--------------------------------------------------------------------------

-- Create the MLS Analytics Hub database
CREATE DATABASE mls_analytics_hub_db;
use mls_analytics_hub_db;

-- Create the Conference table
CREATE TABLE Conference (
    Conference_ID INT PRIMARY KEY AUTO_INCREMENT,
    Conference_Name VARCHAR(100)
);

-- Create the Club table
CREATE TABLE Club (
    Club_ID INT PRIMARY KEY AUTO_INCREMENT,
    Conference_ID INT NULL,
    Club_Name VARCHAR(100),
    Club_Name_Abbreviation VARCHAR(10) NULL,
    Club_Established_date DATE NULL,
    Club_badge VARCHAR(255) NULL,
    FOREIGN KEY (Conference_ID) REFERENCES Conference(Conference_ID)
);

-- Create the Year table
CREATE TABLE Year (
    Year_ID INT PRIMARY KEY AUTO_INCREMENT,
    Year INT
);

-- Create the Club_stats table
CREATE TABLE Club_stats (
    Club_stats_ID INT PRIMARY KEY AUTO_INCREMENT,
    Club_ID INT,
    Year_ID INT,
    Competition_ID INT,
    Total_Wins INT,
    Total_Losses INT,
    Total_Draws INT,
    FOREIGN KEY (Club_ID) REFERENCES Club(Club_ID),
    FOREIGN KEY (Year_ID) REFERENCES Year(Year_ID),
    FOREIGN KEY (Club_stats_ID) REFERENCES Club_stats(Club_stats_ID)
);

-- Create the Competition table
CREATE TABLE Competition (
    Competition_ID INT PRIMARY KEY AUTO_INCREMENT,
    Competition_Name VARCHAR(100)
);

-- Create the Player table
CREATE TABLE Player (
    Player_ID INT PRIMARY KEY AUTO_INCREMENT,
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
    Player_stats_ID INT PRIMARY KEY AUTO_INCREMENT,
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
    Standing_ID INT PRIMARY KEY AUTO_INCREMENT,
    Club_stats_ID INT,
    Year_ID INT,
    Total_points INT,
    FOREIGN KEY (Competition_ID) REFERENCES Competition(Competition_ID),
    FOREIGN KEY (Year_ID) REFERENCES Year(Year_ID)
);

---------------------------------------
-- Indexes for fast lookups
---------------------------------------

-- Index for Year lookups in Club_stats
CREATE INDEX idx_club_in_club_stats ON Club_stats(Year_ID);

--Call the indexes for fast lookups
--SHOW INDEX FROM Club_stats;

-- Index for Year lookups in Player_stats
CREATE INDEX idx_year_in_player_stats ON Player_stats(Year_ID);

--Call the indexes for fast lookups
--SHOW INDEX FROM Player_stats;

-- Index for fast searches on standings by competition
CREATE INDEX idx_competition_in_standings ON Standings(Competition_ID);

--Call the indexes for fast lookups
--SHOW INDEX FROM Standings;

---------------------------------------
-- Views for data retrieval
---------------------------------------

-- View that combines Club, Club_stats, and Standings data for a summary of club standings
CREATE OR REPLACE VIEW standings_club_stats_view AS
SELECT 
    y.Year,
    c.Club_Name,
    cs.Total_Wins,
    cs.Total_Draws,
    cs.Total_Losses,
    s.Total_points
FROM 
    Standings s
JOIN 
    Club_stats cs ON s.Club_stats_ID = cs.Club_stats_ID
JOIN 
    Club c ON cs.Club_ID = c.Club_ID
JOIN 
    Year y ON cs.Year_ID = y.Year_ID
WHERE 
    cs.Year_ID = s.Year_ID;

--Call the view for club standings
--SELECT * FROM standings_club_stats_view;

-- View to summarize Top scorer players per year
CREATE OR REPLACE VIEW top_scorers_view AS
SELECT p.Player_First_Name, p.Player_Last_Name, ps.Goals, ps.Assists, c.Club_Name
FROM
    Player p
    JOIN Player_stats ps ON p.Player_ID = ps.Player_ID
    JOIN Club c ON p.Club_ID = c.Club_ID
WHERE
    ps.Year_ID = 15 -- Filter for year 2024
ORDER BY ps.Goals DESC
LIMIT 10;

--Call the views for top scorers and top assist players
--SELECT * FROM top_scorers_view;

-- View to summarize Top assists players per year
CREATE OR REPLACE VIEW top_assist_players_view AS
SELECT p.Player_First_Name, p.Player_Last_Name, ps.Assists, c.Club_Name
FROM
    Player p
    JOIN Player_stats ps ON p.Player_ID = ps.Player_ID
    JOIN Club c ON p.Club_ID = c.Club_ID
WHERE
    ps.Year_ID = 15 -- Filter for year 2024
ORDER BY ps.Assists DESC
LIMIT 10;

--Call the views for top scorers and top assist players
--SELECT * FROM top_scorers_view;

---------------------------------------
-- Temporary Tables for Data Processing
---------------------------------------

-- Players to watch temporary table
CREATE TEMPORARY TABLE players_to_watch AS
SELECT p.Player_ID, p.Player_First_Name, p.Player_Last_Name, ps.Goals, ps.Assists, ps.Yellow_cards, ps.Red_cards
FROM Player p
    JOIN Player_stats ps ON p.Player_ID = ps.Player_ID
WHERE
    ps.Year_ID = 15
    AND (
        ps.Goals >= 10
        OR ps.Assists >= 5
    )
ORDER BY ps.Goals DESC, ps.Assists DESC
LIMIT 10;

--Call the temporary table for players to watch
--SELECT * FROM players_to_watch;

-- Player Performance Comparison temporary table
CREATE TEMPORARY TABLE player_performance_comparison AS
SELECT p.Player_ID, p.Player_First_Name, p.Player_Last_Name, ps.Goals, ps.Assists, ps.Passes_complete, ps.Yellow_cards, ps.Red_cards
FROM Player p
    JOIN Player_stats ps ON p.Player_ID = ps.Player_ID
WHERE
    ps.Year_ID = 15
    AND p.Player_ID IN (1, 2); -- Replace with specific Player_IDs you want to compare

--Call the temporary table for player performance comparison
--SELECT * FROM player_performance_comparison;

----------------------------------------
-- Triggers for data integrity
----------------------------------------

-- Trigger to update standings total points after club stats are updated
CREATE TRIGGER update_total_points
AFTER UPDATE ON club_stats
FOR EACH ROW
BEGIN
    -- Update the Total_points in the standings table after any update in club_stats
    UPDATE standings s
    JOIN club_stats cs ON s.Club_stats_ID = cs.Club_stats_ID
    SET s.Total_points = (cs.Total_Wins * 3) + (cs.Total_Draws)
    WHERE s.Club_stats_ID = NEW.Club_stats_ID;
END //

--Call the trigger to update total points
--UPDATE club_stats SET Total_Wins = 2, Total_Draws = 1, Total_Losses = 0 WHERE Club_stats_ID = 1; -- Replace 1 with the actual Club_stats_ID

----------------------------------------
-- Stored Procedures for CRUD operations
----------------------------------------

-- Conference Stored Procedures

-- Procedure to create a new conference
DELIMITER //

CREATE PROCEDURE create_conference(
    IN conference_name VARCHAR(100)
)
BEGIN
    INSERT INTO Conference (Conference_Name)
    VALUES (conference_name);
END //

DELIMITER ;

-- Procedure to read conference data
DELIMITER //

CREATE PROCEDURE read_conference(
    IN conference_id INT
)
BEGIN
    IF conference_id IS NOT NULL THEN
        SELECT * FROM Conference WHERE Conference_ID = conference_id;
    ELSE
        SELECT * FROM Conference;
    END IF;
END //

DELIMITER ;

-- Procedure to update conference data
DELIMITER //

CREATE PROCEDURE update_conference(
    IN p_conference_id INT,
    IN p_new_conference_name VARCHAR(100)
)
BEGIN
    DECLARE v_conference_id INT;
    
    -- Assign the parameter to a local variable to ensure correct scoping
    SET v_conference_id = p_conference_id;
    
    -- Only update the specific conference with the matching ID
    UPDATE Conference
    SET Conference_Name = p_new_conference_name
    WHERE Conference_ID = v_conference_id;
END //

DELIMITER ;



-- Procedure to delete conference data
DELIMITER //

CREATE PROCEDURE delete_conference(
    IN p_conference_id INT
)
BEGIN
    DECLARE club_count INT;

    -- Check for related clubs
    SELECT COUNT(*) INTO club_count
    FROM Club
    WHERE Conference_ID = p_conference_id;

    -- Only delete if no related clubs exist
    IF club_count = 0 THEN
        DELETE FROM Conference
        WHERE Conference_ID = p_conference_id;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete this conference; related clubs exist.';
    END IF;
END //

DELIMITER ;


--Call the stored procedures for conference operations
CALL create_conference('Test Conference');
CALL read_conference(NULL);
CALL update_conference(12, '1456415665');

CALL delete_conference(12);

-- End of Conference Stored Procedures


----------------------------------------
-- Functions for data processing
----------------------------------------

-- Function to calculate the win percentage for a club
DELIMITER //

CREATE FUNCTION calculate_win_percentage(p_club_stats_id INT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE win_percentage DECIMAL(5,2);

    -- Calculate win percentage using a CASE statement to avoid division by zero
    SELECT 
        CASE 
            WHEN (Total_Wins + Total_Draws + Total_Losses) = 0 THEN 0
            ELSE (Total_Wins / (Total_Wins + Total_Draws + Total_Losses)) * 100
        END
    INTO win_percentage
    FROM club_stats
    WHERE Club_stats_ID = p_club_stats_id;

    RETURN win_percentage;
END //

DELIMITER ;


--Call the function to calculate win percentage
--SELECT calculate_win_percentage(1);  -- Replace 1 with the actual Club_stats_ID

