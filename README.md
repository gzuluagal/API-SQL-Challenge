# API-SQL-Challenge

This repository provides a set of API endpoints to interact with an SQL database. It uses FastAPI for building RESTful services and SQLAlchemy for database interaction. The API supports multiple operations on entities like employees, departments, and jobs, as well as functionality for handling CSV files and database backups.

## Installation

To get started with this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/API-SQL-Challenge.git
    ```

2. Navigate to the project directory:
    ```bash
    cd API-SQL-Challenge
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Create and configure your `.env` file with the required environment variables (e.g., database URL).

## Usage

To start the application, use Uvicorn to run the FastAPI server:

```bash
uvicorn src.main:app --reload