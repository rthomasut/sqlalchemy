#Climate Analysis and Flask API Project
This project involves conducting a climate analysis using Python and SQLAlchemy, and designing a Flask API for data retrieval based on the analysis results.

Project Overview
Step 1: Set Up Repository
Create a new repository named "sqlalchemy-challenge".
Clone the repository to your local machine.
Create a directory named "SurfsUp" inside the repository.
Place Jupyter notebook, app.py scripts, and the Resources folder containing data files in the "SurfsUp" directory.
Push changes to the GitHub repository.
Step 2: Analyze and Explore Climate Data
Utilize Python and SQLAlchemy for basic climate analysis and data exploration of the climate database.
Connect to the SQLite database using SQLAlchemy's create_engine() function.
Reflect tables ("station" and "measurement") into classes using automap_base().
Create a SQLAlchemy session to interact with the database.
Perform precipitation analysis and station analysis using SQL queries.
Step 3: Design Flask API
Create a Flask API to provide routes for data retrieval.
Design routes as follows:
/: Landing page listing available routes.
/api/v1.0/precipitation: Return JSON data of precipitation analysis for the last 12 months.
/api/v1.0/stations: Return JSON list of stations.
/api/v1.0/tobs: Return JSON list of temperature observations for the most-active station in the previous year.
/api/v1.0/<start> and /api/v1.0/<start>/<end>: Return JSON list of temperature statistics for specified date range.
