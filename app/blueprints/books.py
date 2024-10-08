from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

books = Blueprint('books', __name__)

@books.route('/book', methods=['GET', 'POST'])
def book():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new book
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publication_date = request.form['publication_date']  # Make sure this matches the input name in HTML
        price = request.form['price']

        # Insert the new book into the database
        cursor.execute(
            'INSERT INTO books (title, author, genre, publication_date, price) VALUES (%s, %s, %s, %s, %s)',
            (title, author, genre, publication_date, price)
        )
        db.commit()

        flash('New book added successfully!', 'success')
        return redirect(url_for('books.book'))

    # Handle GET request to display all books
    cursor.execute('SELECT * FROM books')
    all_books = cursor.fetchall()
    return render_template('books.html', all_books=all_books)

@books.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the book's details
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publication_date = request.form['publication_date']  # Make sure this matches the input name in HTML
        price = request.form['price']

        cursor.execute(
            'UPDATE books SET title = %s, author = %s, genre = %s, publication_date = %s, price = %s WHERE book_id = %s',
            (title, author, genre, publication_date, price, book_id)
        )
        db.commit()

        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.book'))

    # GET method: fetch book's current data for pre-populating the form
    cursor.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
    book = cursor.fetchone()
    return render_template('update_book.html', book=book)

@books.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the book
    cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
    db.commit()

    flash('Book deleted successfully!', 'danger')
    return redirect(url_for('books.book'))
