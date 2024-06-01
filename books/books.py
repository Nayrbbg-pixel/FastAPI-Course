from typing import Optional
from fastapi import FastAPI, status, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, model_validator,field_validator
from datetime import datetime

app = FastAPI()

# Book object
class Book:
    id : int
    title : str
    author : str
    description : str
    ratings : int
    published_date : int

    def __init__(self,id,title,author,description,ratings,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.ratings = ratings
        self.published_date = published_date

# Fake database for testing.
Books = {
    'book1':Book(1,'Book1','author1','this is a great book!',5,2024),
    'book2':Book(2,'Book2','author2','this is an okay book!',3,2013),
    'book3':Book(3,'Book3','author3','this is a terrible book!',1,2009),
    'book4':Book(4,'Book4','author4','Nice book!',4,2001),
    'book5':Book(5,'Book5','author5','this book is really bad',4,2009)
}

# <-------------------------------- API Endpoints ---------------------------------->

@app.get('/books/get-all-books',response_class=JSONResponse)
async def get_books():
    return jsonable_encoder(Books)

class Book_body(BaseModel):
    id : int | None = Field(default=(len(Books)+1))
    title : str = Field(...,max_length=100,min_length=2)
    author : str = Field(...,max_length=200,min_length=2)
    description : str = Field(...,max_length=300,min_length=2)
    published_date : int = Field(max_length=4,min_length=4)
    ratings : int = Field(gt=-1,lt=6)

    class Config:
        json_schema_extra = {
            'example':{
                'title':'Enter the title of your book.',
                'author':'Enter the name of the author',
                'description':'Enter a description of your book',
                'published_date':'Enter the year of publishing',
                'ratings': 0
            }
        }

    @model_validator(mode='after')
    def check_id(cls,value):
        value.id = len(Books) + 1
        return value   

@app.post('/books/post-books')
async def post_books(post_data:Book_body)->dict:
    try:
        if post_data.title.lower() in Books:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Book already exists.')
        Books[post_data.title.lower()] = Book(**post_data.model_dump())
        
        return {'Status':'Success','status_code':status.HTTP_201_CREATED}
    except:
        raise HTTPException
    
@app.get('/books/books-by-id/')
async def get_book_by_id(id : int):
    for i in Books:
        if Books[i].id == id:
            return Books[i]
        continue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid id!')

@app.get('/books/books-by-rating/')
async def get_book_by_rating(rating : int = Query(gt=-1,lt=6))->list:
    query_result = []

    # Retrieving the data from the database
    for i in Books:
        if Books[i].ratings == rating:
            data = jsonable_encoder(Books[i])
            query_result.append(data)

    # Checking the query results found. 
    # If 'query_result' is not 0 then we are returning it else an HTTPException.
    if len(query_result) != 0:
        return query_result
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No match with rating {format} was found!')

@app.get('/books/book-by-year/{book_year}')
async def get_book_by_year(book_year : int)->list:
    query_results = []
    for i in Books:
        if Books[i].published_date == book_year:
            query_results.append(jsonable_encoder(Books[i]))
        continue
    if len(query_results) != 0:
        return query_results
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='No book was found that was published in that year. ')

class UpdateBook(BaseModel):
    title : Optional[str] = Field(default=None,max_length=150)
    description : Optional[str] = Field(default=None,max_length=300)

    class Config:
        json_schema_extra = {
            'example':{
                'title':'Enter the title of your book.',
                'description':'Enter a description of your book',
            }
        } 

@app.put('/books/update-book/{book_id}')
async def update_book(updated_book : UpdateBook,book_id : int = Path(gt=-1))->dict:
    if book_id > len(Books):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book could not be found. The id could be invalid.')
    for i in Books:
        if Books[i].id == book_id:

            if updated_book.description is not None:
                Books[i].description = updated_book.description
            
            if updated_book.title is not None:
                Books[i].title = updated_book.title

            return jsonable_encoder(Books[i])
        
        continue

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail='Book not found!')

@app.delete('/books/delete-book/{book_id}')
async def delete_book(book_id : int = Path(gt=0))->dict:

    if book_id > len(Books):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='ID does not exist!')

    for i in Books:
        if Books[i].id == book_id:
            del Books[i]
            return {'status':'Success!',
                    'msg':'Book successfully delelted.',
                    'status_code':status.HTTP_200_OK
                    }
        continue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='ID is invalid. Book not found!')