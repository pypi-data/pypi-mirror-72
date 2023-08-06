import click
from pony.orm import db_session
from trello.trello import Trello
from trello.models import Course, Book
from trello.providers.udemy import Udemy
from trello.providers.goodreads import Goodreads
from trello.settings import *


@click.command()
@click.option('--udemy-user-id', default=None, help='user_id of udemy')
@click.option('--goodreads-user-id', default=None, help='user_id of goodreads')
@click.argument('board_id')
def main(udemy_user_id, goodreads_user_id, board_id):
    if not udemy_user_id and not goodreads_user_id:
        return
    trello = Trello(TRELLO_KEY, TRELLO_TOKEN)
    lists = trello.get_lists(board_id)
    l_courses = None

    if udemy_user_id:
        u = Udemy(udemy_user_id)

        for item in lists:
            if item['name'] == 'Courses':
                l_courses = item['id']
            if item['name'] == 'Books':
                l_books = item['id']

        with db_session:
            for c in u.courses:
                course = Course.new(id=c['id'],
                                    title=c['title'],
                                    url='https://www.udemy.com' + c['url'],
                                    thumbnail=c['image_480x270'])
                if Course.is_course_new(course) and l_courses:
                    card_id = trello.create_card(l_courses, name=course.title, desc=course.url)
                    trello.add_attachment_to_card(card_id, course.thumbnail, name='thumbnail')
                    curriculum = u.get_curriculum(course.id)
                    checklist_id = trello.create_checklist(card_id, name='Content')
                    trello.add_items_to_checklist(checklist_id, curriculum)
                    Course.add_course(course)

    if goodreads_user_id:
        g = Goodreads(GOODREADS_KEY, GOODREADS_SECRET, goodreads_user_id)

        with db_session:
            for b in g.books:
                book = Book.new(title=b['title'],
                                isbn=b['isbn'] or 'NA',
                                author=b['author'],
                                url=b['url'],
                                avg_rating=b['avg_rating'],
                                thumbnail=b['thumbnail'])
                if Book.is_book_new(book):
                    desc = "Title: {}\nISBN: {}\nURL: {}\nAuthor: {}\nAverage Rating: {}".format(book.title, book.isbn,
                                                                                                 book.url, book.author,
                                                                                                 book.avg_rating)
                    if l_books:
                        card_id = trello.create_card(list_id=l_books, name=book.title, desc=desc)
                        trello.add_attachment_to_card(card_id, book.thumbnail, name='thumbnail')
                        Book.add_book(book)


if __name__ == '__main__':
    main()
