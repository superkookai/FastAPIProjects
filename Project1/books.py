"""
Run app -> uvicorn books:app --reload
Terminate -> Crtl+C
async -> In fact is a default for FastAPI, no need to declare explicitly
/docs -> Go to Swagger docs for API
Path Parameters -> /books/{dynamic_param}
%20 == Space
Order of API endpoint is matter!
Query Parameters -> /books/?name=value
Query Parameters[can mix] -> /books/{param}/?name=value -> Be careful about / in the Path
POST and Body
Body is JSON must use ""
GET cannot have a Body
PUT can have a Body
DELETE
"""

from fastapi import Body,FastAPI

app = FastAPI()

BOOKS = [
{'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
        else:
            return {"message": "no book found"}

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/") ## Be careful about / in the Path
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (book.get("author").casefold() == book_author.casefold()
                and book.get("category").casefold() == category.casefold()):
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return {"message": "new_book created"}


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book

    return {"message": "updated book"}


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

    return {"message": f"deleted book: {book_title}"}



## Assignment

@app.get("/books/author/{book_author}")
async def get_books_by_author(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/query/author/")
async def query_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return





