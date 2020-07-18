from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import db_queries as dbq

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres+psycopg2://postgres:postgres123@localhost/Task_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the Home page from the top menu.
@app.route("/")
def home():
	script1, div1, cdn_js = dbq.get_dashboard_info()
	return render_template("home.html", 
							script1=script1, 
							div1=div1, 
							cdn_js=cdn_js)


#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the New task page from the top menu.
@app.route("/task_new")
def task_new():
	return render_template("task_new.html")


#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the Task list page from the top menu.
@app.route("/task_list")
def task_list():
	uncomp_task_list, overdue_task_list, comp_task_list = dbq.get_task_list_info()
	return render_template("task_list.html", 
							output_data=uncomp_task_list, 
							output_data2=overdue_task_list, 
							output_data3=comp_task_list)


#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the Success page when you have entered a new task.
@app.route("/success", methods=["POST"])
def success():
	if request.method == "POST":
		#Gather information from the form on new_tasks page
		title = request.form["task_title"]
		due_date = request.form["due_date"]
		est_time = request.form["time_complete"]
		details = request.form["details"]
		created_by = "Simon Graham"
		#Add task to the database
		dbq.add_new_task(title, due_date, est_time, details, created_by)
		return render_template("success.html")


#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the Task details page from the tables in Task list page.
@app.route("/task_details", methods=["POST"])
def task_details():
	if request.method == "POST":
		task_id = int(request.form["task_id"])
		task_data = dbq.get_task_details(task_id)
		return render_template("task_details.html", 
								task=task_data)


#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the Edit task page from the Task details page.
@app.route("/task_edit", methods=["POST"])
def task_edit():
	if request.method == "POST":
		task_id = int(request.form["task_id"])
		task_data = dbq.get_task_details(task_id)
		return render_template("task_edit.html", 
								task=task_data)


#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the Success2 page from the Task details page.
@app.route("/task_complete", methods=["POST"])
def task_complete():
	if request.method == "POST":
		task_id = int(request.form["task_id"])
		dbq.mark_complete(task_id)
		return render_template("success2.html")


#----------------------------------------------------------------------------------------------------------------------------------------
# Route to the Success2 page from the Task edit page.
@app.route("/success2", methods=["POST"])
def success2():
	if request.method == "POST":
		#Get task data from the form on Task edit page
		task_id = int(request.form["task_id"])
		title = request.form["task_title"]
		due_date = request.form["due_date"]
		est_time = request.form["time_complete"]
		details = request.form["details"]
		#Update the record with the new details
		dbq.update_task_details(task_id, title, due_date, est_time, details)
		return render_template("success2.html")


	
if __name__ == "__main__":
	app.run(debug=True)



