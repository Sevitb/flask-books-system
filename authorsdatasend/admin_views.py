from datetime import datetime
import json
from authorsdatasend import app, db
from flask import Flask, flash, url_for, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from .models import AuthorsTable, Books, Chapters, User
from .forms import LoginForm

prefix='/adm'

@app.route(prefix, methods=['POST','GET'])
@login_required
def admin():
    return render_template('admin/dashboard/dashboard.html', title="Админ-панель")

# Books

@app.route(prefix + '/books', methods=['POST','GET'])
@login_required
def adminBooks():

    books = Books.query.order_by(Books.Title).all()

    if request.method == 'POST':

        bookTitle = str(request.form.get('booktitle'))

        book = Books(Title = bookTitle)

        try:
            db.session.add(book)
            db.session.commit()
            return redirect("#")
        except:
            return "Ошибка при добавления книги."
    else:
        return render_template('admin/books/books.html', title="Список книг", books=books)

@app.route(prefix + '/book/edit', methods=['POST','GET'])
@login_required
def adminBookEdit():

    book_id = int(request.args.get('book_id'))

    if request.method == 'POST':
        new_title = str(request.form.get('new'))

        book = Books.query.filter(Books.id == book_id).first()
        chapters = Chapters.query.filter(Chapters.bookID == book_id).all()

        book.Title = new_title

        for chapter in chapters:
            chapter.bookTitle = new_title

        try:
            db.session.commit()
            return redirect(url_for('adminBooks'))

        except:
            return "Ошибка при изменении!"
    else:
        book = Books.query.get(book_id)
        return render_template('admin/book/edit.html', title="Редактировать книгу", book=book)

# Chapters

@app.route(prefix + '/chapters', methods=['POST','GET'])
@login_required
def adminChapters():

    book_id = int(request.args.get('book_id'))

    if request.method == 'POST':

        chapterTitle = str(request.form.get('chaptername'))
        authorsMaxCount = int(str(request.form.get('count')))
        title = str(Books.query.filter(Books.id == book_id).first().Title)

        chapter_info = Chapters(bookTitle=title, chapterTitle=chapterTitle, authorsCount=0, authorsCountMax=authorsMaxCount, bookID = book_id)

        try:
            db.session.add(chapter_info)
            db.session.commit()
            return redirect('#')

        except:
            return "Ошибка при добавлении главы."
    else:
        all_chapters_filters = []

        if (book_id):
            all_chapters_filters.append(Chapters.bookID == book_id)

        chapters = Chapters.query.order_by(Chapters.chapterTitle).filter(*all_chapters_filters).all()
        return render_template('admin/chapters/chapters.html', title="Список глав", chapters=chapters, book_id=book_id)

@app.route(prefix + '/chapter/edit', methods=['POST','GET'])
@login_required
def adminChapterEdit():

    chapter_id = int(request.args.get('chapter_id'))

    if request.method == 'POST':
        new_title = str(request.form.get('new'))
        new_authors_count = int(str(request.form.get('count')))

        chapter = Chapters.query.filter(Chapters.id == chapter_id).first()

        chapter.chapterTitle = new_title
        chapter.authorsCountMax = new_authors_count

        try:
            db.session.commit()
            return redirect(url_for('adminChapters'))
        except:
            return "Ошибка при изменении!"
    else:
        chapter = Chapters.query.get(chapter_id)
        return render_template('admin/chapter/edit.html', title="Редактировать главу", chapter=chapter)

# Authors

@app.route(prefix + '/authors', methods=['POST','GET'])
@login_required
def adminAuthors():

    chaptersQuery = Chapters.query

    all_authors_filters = []
    all_chapters_filters = []

    if request.method =='POST':
        chapter_id = int(request.form.get('chapter_id'))
        all_authors_filters.append(AuthorsTable.chapterID == chapter_id)

    if request.args.get('book_id'):
        all_chapters_filters.append(Chapters.bookID == request.args.get('book_id'))
        all_authors_filters.append(AuthorsTable.bookID == request.args.get('book_id'))
    
    authors = db.session.query(AuthorsTable).filter(*all_authors_filters).all()
    chapters = db.session.query(Chapters).filter(*all_chapters_filters).all()

    return render_template('admin/authors/authors.html', title="Список авторов" ,authors=authors, chapters=chapters)

# Utils

@app.route(prefix + "/book/change-state", methods=['GET'])
@login_required
def adminBookChangeState():

    book_id = int(request.args.get('book_id'))

    book = Books.query.filter(Books.id == book_id).first()

    if book.allowRegistration:
        book.allowRegistration = False
    else:
        book.allowRegistration = True

    try:
        db.session.commit()
    except:
        return "Ошибка изменения статуса"


    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route(prefix + "/book/delete", methods=['GET'])
@login_required
def adminBookDelete():
    book_id = int(request.args.get('book_id'))

    Books.query.filter(Books.id == book_id).delete()
    Chapters.query.filter(Chapters.bookID == book_id).delete()

    try:
        db.session.commit()
        return redirect('/adm/books')

    except:
        return "Ошибка при удалении!"

@app.route(prefix + "/chapter/change-state", methods=['GET'])
@login_required
def adminChapterChangeState():

    chapter_id = int(request.args.get('chapter_id'))

    chapter = Chapters.query.filter(Chapters.id == chapter_id).first()

    if chapter.allowRegistration:
        chapter.allowRegistration = False
    else:
        chapter.allowRegistration = True

    try:
        db.session.commit()
    except:
        return "Ошибка изменения статуса"


    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route(prefix + "/chapter/delete", methods=['GET'])
@login_required
def adminChapterDelete():
    chapter_id = int(request.args.get('chapter_id'))
    book_id = int(request.args.get('book_id'))

    Books.query.filter(Books.id == chapter_id).delete()
    Chapters.query.filter(Chapters.id == chapter_id).delete()

    try:
        db.session.commit()
        return redirect(url_for('adminChapters',book_id=book_id))

    except:
        return "Ошибка при удалении!"

@app.route(prefix + "/author/delete", methods=['GET'])
@login_required
def adminAuthorDelete():
    author_id = int(request.args.get('author_id'))

    author = AuthorsTable.query.filter(AuthorsTable.id == author_id).first()

    chapter = Chapters.query.filter(Chapters.id == author.chapterID).first()

    if (chapter):
        chapter.authorsCount -= 1

    AuthorsTable.query.filter(AuthorsTable.id == author_id).delete()

    try:
        db.session.commit()
        return redirect(url_for('adminAuthors',book_id=chapter.bookID))

    except:
        return "Ошибка при удалении!"
    
@app.route(prefix + "/author/set-paid", methods=['GET'])
@login_required
def adminAuthorSetPaid():
    author_id = int(request.args.get('author_id'))

    author = AuthorsTable.query.filter(AuthorsTable.id == author_id).first()

    if author.paid:
        author.paid = False
    else:
        author.paid = True

    try:
        db.session.commit()
    except:
        return "Ошибка изменения статуса"
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route(prefix + "/author/add-comment", methods=['GET'])
@login_required
def adminAuthorAddComment():
    author_id = int(request.args.get('author_id'))
    comment = str(request.args.get('comment'))

    author = AuthorsTable.query.filter(AuthorsTable.id == author_id).first()

    if comment != "":
        author.comment += '('+datetime.today().strftime('%Y-%m-%d') + ' ' + comment + ')\n'
    else:
        return redirect('Комментарий пуст')

    try:
        db.session.commit()

    except:
        return redirect('Ошибка. Что-то пошло не так.')


    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route(prefix + '/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))

        flash("Неправильное имя пользователя/пароль", 'error')
        return redirect(url_for('login'))
    return render_template('admin/auth/login/login.html', title="Вход",form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли.")
    return redirect(url_for('login'))