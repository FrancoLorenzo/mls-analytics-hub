# MLS Analytics Hub

Welcome to the **MLS Analytics Hub**! This web application is designed to create and manage a comprehensive fantasy database for the MLS soccer league.

In this project, you'll find a database system that simulates real-world values through mocked data, allowing users to explore various aspects of the league, including player statistics, team performance, and match outcomes. The application supports essential CRUD (Create, Read, Update, Delete) operations, making it a versatile tool for soccer enthusiasts and data analysts alike.

Join me to delve into the exciting world of MLS and unlock insights that can enhance your fantasy league experience!

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

This application is built using Flask and MySQL. It provides a web interface to manage essential CRUD (Create, Read, Update, Delete) operations.

## Introduction

The **MLS Analytics Hub** is a web application built using Flask and MySQL, designed to manage and analyze mock Major League Soccer (MLS) data for education purposes. It provides a user-friendly interface to perform essential CRUD (Create, Read, Update, Delete) operations, alongside advanced data processing capabilities. 

The application leverages optimized database features such as indexes, views, stored procedures, and triggers to ensure efficient data retrieval, manipulation, and consistency. With functionality for detailed player performance tracking, club statistics, and league standings, this platform serves as a comprehensive tool for managing and analyzing soccer-related data within the MLS.

## Features

This project incorporates a variety of powerful database functionalities aimed at enhancing data retrieval, manipulation, and ensuring data integrity. Key features include:

- **Indexes for Fast Lookups**: 
    - Indexes are created on crucial columns to optimize search performance, such as `Year_ID` in `Club_stats` and `Player_stats`, and `Competition_ID` in `Standings`. These indexes significantly improve query execution times by enabling faster lookups for common queries like year-based and competition-based data searches.
  
- **Views for Efficient Data Retrieval**: 
    - Custom views are designed to aggregate and present data from multiple tables in a simplified manner. For instance, the `standings_club_stats_view` combines club standings with stats, while the `top_scorers_view` and `top_assist_players_view` summarize the best performers across the league. These views allow for quick and insightful data exploration without repetitive complex queries.

- **Temporary Tables for Data Processing**:
    - Temporary tables like `players_to_watch` and `player_performance_comparison` are used for intermediate data analysis, enabling comparisons and filtering for specific players. These tables facilitate efficient handling of smaller datasets for targeted analysis.

- **Triggers for Data Integrity**: 
    - A trigger is implemented to automatically update the `Total_points` in the `Standings` table whenever the corresponding club stats are updated, ensuring data consistency without manual intervention. This mechanism keeps standings accurate and in sync with changes in club performance.

- **Stored Procedures for CRUD Operations**:
    - Custom stored procedures streamline database operations. For example, procedures to add a new year (`add_new_year`), a new player (`add_new_player`), or update club stats (`update_club_stats`) simplify database updates, enforcing consistency and preventing redundant SQL code.

- **Functions for Data Calculation**: 
    - A custom function (`calculate_win_percentage`) is implemented to compute the win percentage for any club based on their performance statistics. This function automates the calculation and provides insights into club performance by returning the percentage of wins relative to total matches played.

These features together create a robust, optimized environment for working with large-scale data sets, ensuring fast, efficient, and reliable data processing within the MLS Analytics Hub project.

## Installation

1. Clone the repository:
   
    ```bash
    git clone https://github.com/FrancoLorenzo/mls-analytics-hub.git
    cd mls-analytics-hub
    ```

2. Create a virtual environment and activate it:
   
    ```bash
    python -m venv venv
    source venv/bin/activate   # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3. Install the dependencies:
   
    ```bash
    pip install -r requirements.txt
    ```

## Usage

- Open your web browser and navigate to `http://127.0.0.1:5000`.
- Use the interface to view and add users.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
