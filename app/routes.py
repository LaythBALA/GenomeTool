from flask import render_template, redirect, url_for, flash, request,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from app.models import Comment
from werkzeug.security import generate_password_hash, check_password_hash
import requests # pip install requests


@app.route('/submit_comment', methods=['POST'])
@login_required  # Ensure the user is authenticated to submit comments
def submit_comment():
    comment_text = request.form.get('comment')
    position = request.form.get('position')
    
    if comment_text and position:
        # Create a new comment and save it to the database
        new_comment = Comment(user_id=current_user.id, comment=comment_text, position=position)
        db.session.add(new_comment)
        db.session.commit()
        
        # Return the newly created comment as a JSON response
        return jsonify({'comment': {
            'user': {'username': current_user.username},
            'comment': comment_text
        }})
    
    return jsonify({'error': 'Invalid data'}), 400
# Registration Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if username or email already exist
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists.', 'error')
            return redirect(url_for('signup'))

        # Create new user
        try:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            db.session.rollback()  # Rollback the session to undo any changes

        flash('Account created successfully!', 'success')
        return redirect(url_for('login.html'))
    
    return render_template('signup.html', user=current_user)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))  # Change to your desired redirect URL
        
        flash('Invalid email or password.', 'error')

    return render_template('login.html', user=current_user)

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))  # Change to your desired redirect URL

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/genome_browser')
def genome_browser():
    return render_template('genome_browser.html')

#Annotation Routes

def fetch_gene_info(gene_id):
    api_url = f'https://rest.ensembl.org/lookup/id/{gene_id}?content-type=application/json'
    response = requests.get(api_url)

    if response.status_code == 200:
        gene_info = response.json()
        return gene_info
    else:
        print(f"API request failed with status code: {response.status_code}")
        return None

@app.route('/annotation')
@app.route('/annotation/<param_value>')
def annotation(param_value=""):
    # gene_id = request.args.get('gene_id')  # Get gene ID from query parameter
    # gene_info = fetch_gene_info('gene_id')  # Replace with your method to get gene information
    gene_info=param_value
    comments = Comment.query.filter_by(position=gene_info).all()
    
    if gene_info:
        # genome_map_url = f"https://www.ensembl.org/Homo_sapiens/Gene/Summary?g={gene_id}"
        genome_map_url = f"https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&position={gene_info}"
    else:
        genome_map_url = None

    return render_template('annotation.html', gene_info=gene_info, genome_map_url=genome_map_url, comments=comments)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/search_genome', methods=['POST'])
def search_genome():
    search_term = request.form.get('search_term')
    species = 'homo_sapiens'  # You can specify the species here, e.g., 'homo_sapiens' for human
    api_url = f'https://rest.ensembl.org/lookup/symbol/{species}/{search_term}?content-type=application/json'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        print(api_url)
        print(data)
        return render_template('genome_browser.html', search_results=data)
    else:
        print(f"API request failed with status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return 'Error: Unable to retrieve genome data'

