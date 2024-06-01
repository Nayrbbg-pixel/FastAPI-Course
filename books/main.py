from pydantic import BaseModel,Field
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional

app = FastAPI()

Books = {
    'book1':{'title':'Book1','author':'Author1','category':'Computer Science'},
    'book1.3':{'title':'Book1.3','author':'Author1','category':'Computer Science'},
    'book2':{'title':'Book2','author':'Author2','category':'Physics'},
    'book3':{'title':'Book3','author':'Author3','category':'Maths'},
    'book4':{'title':'Book4','author':'Author2','category':'Chemistry'},
    'book5':{'title':'Book5','author':'Author5','category':'History'},
    'book6':{'title':'Book6','author':'Author6','category':'science'}
}

@app.get('/books')
async def get_books():
    return Books

@app.get('/book/{book_title}')
async def get_specific_book(book_title : str):
    if book_title.lower() not in Books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The book was not found.')
    return JSONResponse(content=jsonable_encoder(Books[book_title.lower()]),status_code=status.HTTP_200_OK)

@app.get('/books/')
async def get_query_results(book_category:str):
    results = []
    for i in Books:
        if book_category.lower() in Books[i]['category'].lower():
            results.append(Books[i])
            continue
        continue

    return jsonable_encoder( results)

class Book(BaseModel):
    title : str = Field(...,max_length=100,min_length=2)
    author : str = Field(...,max_length=200,min_length=2)
    category : str = Field(...,max_length=100,min_length=2)

    class Config:
        json_schema_extra = {
            'example':{
                'title':'Enter the title of your book.',
                'author':'Enter the name of the author',
                'category':'Enter the category your book falls in'
            }
        }

@app.post('/create-book')
async def create_book_data(book:Book):
    Books[book.title.lower()] = {'title':book.title,'author':book.author,'category':book.category}
    return {'Status':'Success','status_code':status.HTTP_201_CREATED}

class Update_Book(BaseModel):
    title : Optional[str | None] = None
    author : Optional[str | None] = None
    category : Optional[str | None] = None


@app.put('/update-book/{book_title}')
async def update_book(book_title:str,book:Update_Book):
    if book.author != None:
        Books[book_title.lower()]['author'] = book.author
    if book.title != None:
        Books[book_title.lower()]['title'] = book.title
    if book.category != None:
        Books[book_title.lower()]['category'] = book.category
    return {'Change Status':'Success','status_code':status.HTTP_200_OK}

@app.delete('/delete-book/{book_title}')
async def delete_book(book_title:str):
    if book_title not in Books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Book not found')
    del Books[book_title.lower()]
    return {'Status':'Success','status_code':status.HTTP_200_OK} 

@app.get('/get-books-author/')
async def get_query_results(book_author:str):
    results = []
    for i in Books:
        if book_author.lower() in Books[i]['author'].lower():
            results.append(Books[i])
            continue
        continue

    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Author not found')

    return jsonable_encoder( results)