# Database Bestbuy Final Project

## Introduction

Welcome to the Bestbuy Store database project! The aim of this project is to create a simple database using MySQL for Bestbuy Store. This folder includes an E-R diagram design, SQL DDL, SQL delete DDL, dummy data (`BestBuy_dummy_data.txt`) for testing, `queries.py` for testing queries, `insert_dummy_data.py` for inserting dummy data into the database, and a data-preview folder that contains a simple web application built with Flask for previewing and visualizing the dataset.

## Technical Details

In the `data-preview` folder, you'll find a Flask application that allows you to preview and visualize the dataset. To run the application on your local machine, make sure you have all the necessary dependencies installed by running `pip install -r requirements.txt` in your terminal while in the data-preview directory.

Before running the application, you'll need to update the `local.env` file with your database configuration, including the host, port, and password.

Once everything is set up, you can run the application by entering flask run in your terminal.

Please note that the queries included in this project are tailored specifically for the Bestbuy store database. If you plan to use them for your own database project, make sure to modify the queries accordingly to fit your database schema and requirements.

### The database

The data you'll be visualizing will be in a MySQL database. Credentials to access this database will be provided in the following environment variables:

- `MYSQL_HOST` provides the host
- `MYSQL_PORT` provides the port
- `MYSQL_USER` provides the user
- `MYSQL_PASSWORD` provides the password
- `MYSQL_DB` provides the database

An example can be found in `local.env`.
