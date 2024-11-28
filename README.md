# MLS Analytics Hub

Welcome to the **MLS Analytics Hub**! This web application is designed to manage and analyze a comprehensive fantasy database for Major League Soccer (MLS). Built with Flask and MySQL, it provides tools for soccer enthusiasts and data analysts to explore player statistics, team performance, and league standings.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## Introduction

The **MLS Analytics Hub** is a web application created for educational purposes. It leverages mocked data to simulate real-world MLS scenarios, allowing users to interact with the data through an intuitive web interface. The application supports CRUD operations and provides advanced features for analyzing soccer data.

---

## Features

This project incorporates several powerful functionalities, including:

- **Indexes for Fast Lookups**: Optimize queries on key columns like `Year_ID` and `Competition_ID`.
- **Views for Simplified Data Access**: Predefined views for insights such as league standings, top scorers, and top assist players.
- **Triggers for Data Integrity**: Automatically update `Total_points` in standings when club stats change.
- **Stored Procedures and Functions**: Streamline database operations like adding players or calculating win percentages.
- **Temporary Tables for Advanced Analysis**: Compare players or highlight specific performances.

---

## Project Structure

Here’s an overview of the project’s organization:

- **app**: Contains the application logic and templates.
  - `db_connection.py`: Database connection setup.
  - `routes.py`: Defines application routes.
  - **templates**: HTML templates organized by feature (e.g., `club`, `player`, `standings`).
  - **static**: Contains static assets (CSS, JavaScript, images).
- **config.py**: Application configuration settings.
- **run.py**: Entry point for running the Flask application.
- **venv**: Virtual environment for dependencies.

---

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

Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the application:

    ```bash
    python run.py
    ```

## Usage

- Open your web browser and navigate to `http://127.0.0.1:5000`.
- Explore the features:
    - View and manage players, teams, and league standings.
    - Analyze player and team statistics through intuitive dashboards.
- Modify and expand the database with CRUD operations.

## Technologies Used
- **Backend:** Flask, MySQL
- **Frontend:** HTML, CSS (via Bootstrap), Jinja2 for templates
- **Database Optimization:** Indexes, views, triggers, stored procedures
- **Development Tools:** Python 3.x, virtualenv, Git

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
