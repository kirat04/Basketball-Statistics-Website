# Basketball Statistics Website

## Author
Prabhkirat Dhaliwal

## Overview
This is a basketball statistics website that allows users to view and search for player statistics. The project is built using HTML for the front end and Python (Flask) for the back end. The data is stored in an SQLite database.

## Project Structure

The repository contains the following files and folders:

1. `templates/` - Folder containing the HTML documents.
    - `index.html` - The main landing page of the website.
    - `player.html` - Page for displaying individual player statistics.
    - `search.html` - Page for searching player statistics.

2. `database.db` - The SQLite database that is used in the project.

3. `main.py` - Source code for the backend implementation.

4. `README.txt` - This file.

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- SQLite

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/basketball-statistics-website.git
    ```

2. Navigate to the project directory:
    ```bash
    cd basketball-statistics-website
    ```

3. Install the Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. Initialize the database:
    ```bash
    python init_db.py
    ```

2. Start the Flask development server:
    ```bash
    flask run
    ```

3. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- Visit the main landing page to see a list of players and their statistics.
- Use the search functionality to find specific players.
- Click on a player's name to view detailed statistics.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
