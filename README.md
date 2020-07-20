# 'Task Manager' Flask Web App

This app was created to help manage individual tasks that I had to complete on a daily basis.

It allows me to enter new and manage existing tasks; view separate lists of tasks due to completed, task that were overdue, and tasks that were recently completed; and view a dashboard of analytical graphs, making it easier to manage my tasks.

This app was built in a **Flask** framework, and is connected to a simple **postgres** database using **SALAlchemy**. The tables and graphs are created using **pandas** and **bokeh**. **html** and **CSS** were used to create the front end of the application.

## Installation
### Libraries
The following third party libraries will need to be installed for the app to work:

1. flask
2. flask_sqlalchemy
3. pandas
4. bokeh
5. psycopg2

### PGAdmin4
This is used to create and manage the database. If you do not have this software already, then follow the steps below:

1. First, download the [pgAdmin4 software](https://www.pgadmin.org/download/) from the web.
2. Install the software once downloaded. 
3. Create an account. 

### Creating the database
From **pgAdmin4** window, do the following:

![alt text](https://github.com/SimonGraham86/task_organiser/blob/master/readme_files/my_gif1.gif)

Ensure that the databae name is *Task_manager*.

### Creating the data tables
From your command prompt and once you're in the correct directory, do the following:

![alt text](https://github.com/SimonGraham86/task_organiser/blob/master/readme_files/my_gif2.gif)

1. Open up a **python** shell.
2. Type `from db_queries import db`.
3. Type `db.create_all()`.
4. Exit the **python** shell by typing `exit()`.

## How to use

From your command prompt, once you're in the correct directory, enter `python tasksite.py`

![alt text](https://github.com/SimonGraham86/task_organiser/blob/master/readme_files/my_gif3.gif)

## Contributions
If anyone would like to contribute on ways to improve the code, that would be greatly appreciated.

## Support
If there are any issue or any questiosn about the code, please let me know through the issue tracker.



