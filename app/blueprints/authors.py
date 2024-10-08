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

@authors.route('/update_author/<int:author_id>', methods=['GET', 'POST'])
def update_author(author_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Retrieve updated values from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        written_books = request.form['written_books']
        birthdate = request.form['birthdate']

        # Update the author's details in the database
        cursor.execute(
            'UPDATE authors SET first_name = %s, last_name = %s, written_books = %s, birthdate = %s WHERE author_id = %s',
            (first_name, last_name, written_books, birthdate, author_id)
        )
        db.commit()

        flash('Author updated successfully!', 'success')
        return redirect(url_for('authors.author'))

    # GET method: fetch author's current data for pre-populating the form
    cursor.execute('SELECT * FROM authors WHERE author_id = %s', (author_id,))
    author = cursor.fetchone()
    # app/blueprints/authors.py
    return render_template('update_authors.html', author=author)
@authors.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the author
    cursor.execute('DELETE FROM authors WHERE author_id = %s', (author_id,))
    db.commit()

    flash('Author deleted successfully!', 'danger')
    return redirect(url_for('authors.author'))
