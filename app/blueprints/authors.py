from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

authors = Blueprint('authors', __name__)

@authors.route('/authors', methods=['GET', 'POST'])
def author():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new author
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        written_books = request.form['written_books']
        birthdate = request.form['birthdate']

        # Insert the new author into the database
        cursor.execute(
            'INSERT INTO authors (first_name, last_name, written_books, birthdate) VALUES (%s, %s, %s, %s)',
            (first_name, last_name, written_books, birthdate)
        )
        db.commit()

        flash('New author added successfully!', 'success')
        return redirect(url_for('authors.author'))

    # Handle GET request to display all authors
    cursor.execute('SELECT * FROM authors')
    all_authors = cursor.fetchall()
    return render_template('authors.html', all_authors=all_authors)

# Other routes remain unchanged