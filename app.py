from flask import Flask, render_template, redirect, url_for, request, flash, session 
import os, signal
from flask_sqlalchemy  import SQLAlchemy 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Project, ProjectUpdate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
from flask import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_should_be_a_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# Add Register, Login, Logout Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
			name = request.form['name']
			email = request.form['email']
			banner_image = request.form['banner_image']  
			password = request.form['password']

			user = User.query.filter_by(email=email).first()
			if user:
				flash('Email already exists.')
				return redirect(url_for('register'))
		
			new_user = User(
				name=name,
				email=email,
				password=generate_password_hash(password, method='pbkdf2:sha256'),
				banner_image=banner_image
			)
			db.session.add(new_user)
			db.session.commit()
			flash('Registration Successful! Please login.')
			return redirect(url_for('login'))
	
	return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']

		user = User.query.filter_by(email=email).first()
		if not user or not check_password_hash(user.password, password):
			flash('Incorrect email or password.')
			return redirect(url_for('login'))
		
		login_user(user)
		return redirect(url_for('dashboard'))
	
	return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

welcome_phrases = [
    "Howdy, {}!",
    "Welcome back, {}!",
    "Good to see you, {}!",
    "Hi there, {}!",
    "Let's get to work, {}!",
    "Back in action, {}!",
    "You’ve got this, {}!"
]

# Dashboard (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    greeting = random.choice(welcome_phrases).format(user.name)

    page = request.args.get('page', 1, type=int)
    query = Project.query.filter_by(user_id=user.id)

    all_projects = Project.query.filter_by(user_id=user.id).all()
    unique_project_names = sorted(set(p.name for p in all_projects))
    unique_clients = sorted(set(p.client for p in all_projects))
    statuses = sorted(set(p.status for p in all_projects))

    # Filters
    if name := request.args.get('project_name'):
        query = query.filter(Project.name == name)
    if client := request.args.get('client'):
        query = query.filter(Project.client == client)
    status = request.args.get('status')
    if status:
        query = query.filter(Project.status == status)
    if deadline_from := request.args.get('deadline_from'):
        query = query.filter(Project.deadline >= deadline_from)
    if deadline_to := request.args.get('deadline_to'):
        query = query.filter(Project.deadline <= deadline_to)

    projects = query.order_by(Project.deadline.asc()).paginate(page=page, per_page=10)

    return render_template(
        'dashboard.html',
        name=user.name,
        greeting=greeting,
        projects=projects,
        unique_project_names=unique_project_names,
        unique_clients=unique_clients,
        statuses=statuses,
        selected_status=status if status else ""
    )


# Project Creation
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
	if request.method == 'POST':
		name = request.form['name']
		client = request.form['client']
		status = request.form['status']
		deadline_str = request.form['deadline']
		description = request.form['description']
		poc_name = request.form['poc_name']
		poc_email = request.form['poc_email']
		github_link = request.form['github_link']
		deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None

		new_project = Project(
		name=name,
		client=client,
		status=status,
		deadline=deadline,
		description=description,
		poc_name=poc_name,
		poc_email=poc_email,
		github_link=github_link,
		user_id=current_user.id,
        
        unique_project_names=unique_project_names,
        unique_clients=unique_clients,
        statuses=statuses,
	)

		db.session.add(new_project)
		db.session.commit()
		flash('Project added successfully!')
		return redirect(url_for('dashboard'))
	
	return render_template('add_project.html')

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    # Make sure the user owns this project
    if project.user_id != current_user.id:
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        project.name = request.form['name']
        project.client = request.form['client']
        project.status = request.form['status']
        project.description = request.form['description']
        deadline_str = request.form['deadline']
        project.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None
        project.poc_name = request.form['poc_name']
        project.poc_email = request.form['poc_email']
        project.github_link = request.form['github_link']

        db.session.commit()
        flash('Project updated!')
        return redirect(url_for('dashboard'))

    return render_template('edit_project.html', project=project)

@app.route('/delete_project/<int:project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    # Check if the logged-in user owns this project
    if project.user_id != current_user.id:
        flash('Unauthorized access.')
        return redirect(url_for('dashboard'))

    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.')
    return redirect(url_for('dashboard'))

@app.route('/project/<int:project_id>/updates', methods=['GET', 'POST'])
@login_required
def project_updates(project_id):
    project = Project.query.get_or_404(project_id)

    # Handle adding an update
    if request.method == 'POST':
        update_text = request.form['update_text']
        author = request.form.get('author', 'System')
        if update_text.strip():
            update = ProjectUpdate(project_id=project.id, update_text=update_text, author=author)
            db.session.add(update)
            db.session.commit()
            flash('Update added!', 'success')
            return redirect(url_for('project_updates', project_id=project_id))
        else:
            flash('Update cannot be empty.', 'danger')

    # Date filter parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    updates_query = ProjectUpdate.query.filter_by(project_id=project.id)

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        updates_query = updates_query.filter(ProjectUpdate.created_at >= start_date)
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        updates_query = updates_query.filter(ProjectUpdate.created_at <= end_date)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 5
    paginated_updates = updates_query.order_by(ProjectUpdate.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('project_updates.html', project=project, updates=paginated_updates, start_date=start_date_str, end_date=end_date_str)

from flask import request, abort

@app.route('/shutdown', methods=['POST'])
@login_required
def shutdown():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    print("Shutdown requested by user:", current_user.id)  # Or current_user.email

    os.kill(os.getpid(), signal.SIGTERM)
    return "Server is shutting down..."

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
