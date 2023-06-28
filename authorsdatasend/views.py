from authorsdatasend import app, db
from flask import render_template, request, redirect
from .models import AuthorsTable, Books, Chapters, User
from .utils import send_mail


@app.route('/')
def books():
    books = Books.query.order_by(Books.Title).filter(Books.allowRegistration == 1).all()
    return render_template('pages/books/books.html', title='Книги', books=books)

@app.route('/chapters')
def chapters():

    book_id = int(request.args.get('book_id'))

    chapters = Chapters.query.filter(Chapters.bookID == book_id, Chapters.authorsCount < Chapters.authorsCountMax, Chapters.allowRegistration == 1).all()

    return render_template('pages/chapters/chapters.html', title="Главы", chapters=chapters, book_id=book_id)

@app.route('/register-form', methods = ['GET', 'POST'])
def registerForm():

    chapter_id = int(request.args.get('chapter_id'))
    book_id = int(request.args.get('book_id'))

    if request.method =='POST':
        lastName = str(request.form.get('lastName'))
        firstName = str(request.form.get('firstName'))
        midName = str(request.form.get('midName'))
        lastNameTranslit = str(request.form.get('lastNameTranslit'))
        firstNameTranslit = str(request.form.get('firstNameTranslit'))
        midNameTranslit = str(request.form.get('midNameTranslit'))[0]+'.'
        bookTitle = str(Books.query.filter(Books.id == book_id).first().Title)
        chapterId = chapter_id
        chapterTitle = str(Chapters.query.filter(Chapters.bookID == book_id, Chapters.id == chapterId).first().chapterTitle)
        phoneNumber = str(request.form.get('phoneNumber'))
        emailAdress = str(request.form.get('email'))
        orcid = str(request.form.get('ORCID'))
        jba = str(request.form.get('jobAddress'))
        jba1 = str(request.form.get('jobAddress1'))
        authorComment = str(request.form.get('comment'))

        if  chapterTitle == "non_selected":
            return redirect("#okno_choose")

        else:
            chapter = Chapters.query.filter(Chapters.bookID == book_id, Chapters.id == chapterId).first()

            if(chapter.authorsCount >= chapter.authorsCountMax):
                return redirect("#okno_bad")

            chapter.increaseAuthCount()

            authorData = AuthorsTable(lastName=lastName, firstName=firstName, midName=midName, lastNameTranslit=lastNameTranslit,
                                      firstNameTranslit=firstNameTranslit, midNameTranslit=midNameTranslit, bookTitle=bookTitle,
                                      chapterTitle=chapterTitle, phoneNumber=phoneNumber, emailAdress=emailAdress, ORCID=orcid,
                                      jobAddress = jba, jobAddress1 = jba1, authorComment=authorComment, bookID = book_id, chapterID = chapterId,paid = False)

            try:
                db.session.add(authorData)
                db.session.commit()
                
                send_mail("Спасибо за заявку!",emailAdress,"mail/author-letter.html",author=authorData)
                # send_mail("Заявка к книге (authorsdatasend.ru)!",['iscvolga@yandex.ru],["mail/isc-letter.html"],"isc-letter.html")

                return redirect('#okno_good')
            except:
                return redirect('#okno_bad')
    else:

        return render_template("pages/register-form/register-form.html", title="Подать заявку", info = {"Title":Books.query.filter(Books.id == book_id).first().Title,
                                                        "Chapter":Chapters.query.filter(Chapters.bookID==book_id,
                                                                                        Chapters.id==chapter_id).first().chapterTitle})


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(500)
def not_found(error):
    return render_template('error.html'), 500