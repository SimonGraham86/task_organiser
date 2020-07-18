from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta, datetime
import pandas as pd
import pandas_bokeh
from bokeh.embed import components
from bokeh.resources import CDN
from tasksite import db

#-------------------------------------------------------------------------------------------------------------------------
# Database table
#-------------------------------------------------------------------------------------------------------------------------
class Task(db.Model):
	__tablename__ = "task_data"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	due_date = db.Column(db.DATE)
	est_time = db.Column(db.Float)
	details = db.Column(db.String(300))
	created_by = db.Column(db.String(20))
	created_date = db.Column(db.DATE)
	completed_date = db.Column(db.DATE)

	def __init__(self, title, due_date, est_time, details, created_by):
		self.title = title
		self.due_date = due_date
		self.est_time = est_time
		self.details = details
		self.created_by = created_by
		self.created_date = date.today()
		self.completed_date = None

#-------------------------------------------------------------------------------------------------------------------------
# Functions to query database or perform actions
#-------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------
def get_dashboard_info():

	#Timeframes needed for queries
	today = date.today()
	start_of_week = today - timedelta(days=today.weekday()) 
	end_of_week = start_of_week + timedelta(days=6) 
	start_of_last_week = start_of_week - timedelta(days=7) 
	end_of_last_week = start_of_last_week + timedelta(days=6) 
	
	#Query for first DataFrame
	completed_tasks = (db.session.query(
                    Task.due_date, db.func.count(Task.id).label('tasks_completed'))
                   .filter(Task.completed_date != None)
                   .group_by(Task.due_date).subquery()
                  )
	overdue_tasks = (db.session.query(
	                    Task.due_date, db.func.count(Task.id).label('tasks_overdue'))
	                   .filter(Task.completed_date == None, date.today() > Task.due_date)
	                   .group_by(Task.due_date).subquery()
	                  )
	task_query = (db.session.query(
	                Task.due_date.label('date'),
	                db.func.count(Task.id).label('tasks_due'),
	                completed_tasks.c.tasks_completed.label('tasks_completed'),
	                overdue_tasks.c.tasks_overdue.label('tasks_overdue'))
	            .outerjoin(completed_tasks, Task.due_date == completed_tasks.c.due_date)
	            .outerjoin(overdue_tasks, Task.due_date == overdue_tasks.c.due_date)
	            .filter(Task.due_date >= start_of_week, Task.due_date <= end_of_week)
	            .group_by(Task.due_date, completed_tasks.c.tasks_completed, overdue_tasks.c.tasks_overdue)
	            .order_by(Task.due_date)
	             )

	#Query for second DataFrame
	comp_early = db.session.query(db.func.count(Task.id)
             .filter(Task.completed_date < Task.due_date,
                    Task.due_date >= start_of_last_week,
                    Task.due_date <= end_of_last_week)).scalar()
	comp_on_time = db.session.query(db.func.count(Task.id)
	             .filter(Task.completed_date == Task.due_date,
	                    Task.due_date >= start_of_last_week,
	                    Task.due_date <= end_of_last_week)).scalar()
	comp_late = db.session.query(db.func.count(Task.id)
	             .filter(Task.completed_date > Task.due_date,
	                    Task.due_date >= start_of_last_week,
	                    Task.due_date <= end_of_last_week)).scalar()
	incomplete = db.session.query(db.func.count(Task.id)
	             .filter(Task.completed_date == None,
	                    Task.due_date >= start_of_last_week,
	                    Task.due_date <= end_of_last_week)).scalar()

	#First df
	df = pd.DataFrame(task_query)
	df = df.fillna(0)
	df["date"] = df["date"].apply(pd.to_datetime)
	df["day"] =df["date"].dt.day_name()
	df.set_index("day")

	#Second df
	df2 = pd.DataFrame({"status" : ["Completed_early", "Completed_on_time", "Completed_late", "Incomplete"],
                   		"count" : [comp_early, comp_on_time, comp_late, incomplete]})

	#First bar chart
	p_bar = df.plot_bokeh.bar(
                    x = "day",
                    ylabel = "No. of Tasks",
                    title = "Tasks this week",
                    toolbar_location = None,
                    colormap = ["#8FBC8F", "#663399", "#DB7093"],
                    show_figure = False,
                    figsize=(900, 500), 
                    sizing_mode="scale_width")

	#Second bar chart
	p_bar2 = df2.plot_bokeh.bar(
                    x = "status",
                    legend = False,
                    toolbar_location = None,
                    title = "Task completion times (last week)",
                    ylabel = "No. of Tasks",
                    xlabel = "Status",
                    ylim = (0, df2["count"].max()+1),
                    color = "#8FBC8F",
                    show_figure = False,
                    figsize=(900, 500), 
                    sizing_mode="scale_width")

	#Dashboard layout
	layout = pandas_bokeh.column(p_bar, p_bar2)
	layout_html = pandas_bokeh.embedded_html(layout)

	script1, div1 = components(layout)
	cdn_js = CDN.js_files[0]

	return (script1, div1, cdn_js)


#-------------------------------------------------------------------------------------------------------------------------
def get_task_list_info():
	
	#Query to get list of Uncompleted Tasks
	uncomp_task_list = db.session.query(Task).filter(Task.completed_date == None)
	#Query to get list of Overdue Tasks
	overdue_task_list = db.session.query(Task).filter(date.today() > Task.due_date, Task.completed_date == None)
	#Query to get list of Completed Tasks
	comp_task_list = db.session.query(Task).filter(Task.completed_date != None)

	return (uncomp_task_list, overdue_task_list, comp_task_list)


#-------------------------------------------------------------------------------------------------------------------------
def add_new_task(title, due_date, est_time, details, created_by):
	#Create instance of Task class
	new_task_data = Task(title, due_date, est_time, details, created_by)
	#Add new_task_data to the DB table
	db.session.add(new_task_data)
	db.session.commit()


#-------------------------------------------------------------------------------------------------------------------------
def get_task_details(task_id):
	task_data = db.session.query(Task).get(task_id)

	return task_data


#-------------------------------------------------------------------------------------------------------------------------
def mark_complete(task_id):
	task_data = db.session.query(Task).get(task_id)
	#Update the completed_date to today
	task_data.completed_date = date.today()
	db.session.commit()
	

#-------------------------------------------------------------------------------------------------------------------------
def update_task_details(task_id, title, due_date, est_time, details):
	#Get task record using task_id
	task_data = db.session.query(Task).get(task_id)
	#Update the record with the new details
	task_data.title = title
	task_data.due_date = due_date
	task_data.est_time = est_time
	task_data.details = details
	db.session.commit()
	