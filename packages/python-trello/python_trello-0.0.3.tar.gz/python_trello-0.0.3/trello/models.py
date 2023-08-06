from pony.orm import Database, PrimaryKey
from pony.orm import Required, Optional
from pony.orm import db_session
from pony.orm import select, delete, commit

from trello.settings import DB_PATH

db = Database()


class Course(db.Entity):
    """
    A class to represent a course
    """
    id = PrimaryKey(int, auto=False)
    title = Required(str, unique=True)
    url = Optional(str, unique=True)
    thumbnail = Optional(str)
    processed = Optional(bool, default=False)

    @staticmethod
    @db_session
    def new(id, title, url='', thumbnail='', processed=False):
        """Return a Course either new or from database"""
        course = select(c for c in Course if c.title == title)[:]
        if course:
            return course[0]
        return Course(id=id, title=title, url=url, thumbnail=thumbnail, processed=processed)

    @staticmethod
    @db_session
    def is_course_new(course):
        """
        Check if the course is new or already in db
        """
        return not course.processed

    @staticmethod
    @db_session
    def add_course(course):
        """Add a course to the database"""
        course.processed = True
        commit()

    @staticmethod
    @db_session
    def count():
        """Get total courses in the database"""
        return len(select(c for c in Course)[:])

    @staticmethod
    @db_session
    def delete_all():
        """Delete all information from the table"""
        delete(c for c in Course)


class Book(db.Entity):
    """
    A class to represent a book
    """
    title = Required(str)
    isbn = Required(str)
    author = Optional(str)
    url = Optional(str)
    avg_rating = Optional(str)
    thumbnail = Optional(str)
    processed = Optional(bool, default=False)

    @staticmethod
    @db_session
    def new(title, isbn, author='', url='', avg_rating='', thumbnail='', processed=False):
        """Return a Course either new or from database"""
        book = select(b for b in Book if b.title == title and b.isbn == isbn)[:]
        if book:
            return book[0]
        return Book(title=title, isbn=isbn, author=author, url=url, avg_rating=avg_rating, thumbnail=thumbnail,
                    processed=processed)

    @db_session
    def is_book_new(book):
        """
        Check if the book is new or already in db
        """
        return not book.processed

    @staticmethod
    @db_session
    def add_book(book):
        """Add a book to the db"""
        book.processed = True
        commit()

    @staticmethod
    @db_session
    def count():
        """Get total books in the database"""
        return len(select(b for b in Book)[:])

    @staticmethod
    @db_session
    def delete_all():
        """Delete all information from the table"""
        delete(b for b in Book)


db.bind(provider='sqlite', filename=DB_PATH, create_db=True)
db.generate_mapping(create_tables=True)
