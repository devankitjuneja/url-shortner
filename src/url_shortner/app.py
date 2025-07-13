from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
import random
import string
from url_shortner.database import SessionLocal
from url_shortner.models.url import URL

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request body schema
class URLRequest(BaseModel):
    url: HttpUrl

# Response body schema
class URLResponse(BaseModel):
    id: int
    url: str
    shortCode: str
    createdAt: str
    updatedAt: str

class URLStatsResponse(URLResponse):
    accessCount: int

@app.post("/shorten", response_model=URLResponse, status_code=201)
def create_short_url(request: URLRequest, db: Session = Depends(get_db)):
    # Generate a random short code
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Check if the short code already exists
    existing_url = db.query(URL).filter(URL.shortCode == short_code).first()
    if existing_url:
        raise HTTPException(status_code=400, detail="Short code already exists")

    # Create a new URL entry
    new_url = URL(
        url=request.url,
        shortCode=short_code
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return URLResponse(
        id=new_url.id,
        url=new_url.url,
        shortCode=new_url.shortCode,
        createdAt=new_url.createdAt.isoformat(),
        updatedAt=new_url.updatedAt.isoformat()
    )

@app.get("/shorten/{short_code}", response_model=URLResponse, status_code=200)
def get_original_url(short_code: str, db: Session = Depends(get_db)):
    # Retrieve the URL entry by short code
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Increment the access count
    url_entry.accessCount += 1
    db.commit()
    db.refresh(url_entry)

    return URLResponse(
        id=url_entry.id,
        url=url_entry.url,
        shortCode=url_entry.shortCode,
        createdAt=url_entry.createdAt.isoformat(),
        updatedAt=url_entry.updatedAt.isoformat()
    )

@app.put("/shorten/{short_code}", response_model=URLResponse, status_code=200)
def update_short_url(short_code: str, request: URLRequest, db: Session = Depends(get_db)):
    # Retrieve the URL entry by short code
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Update the URL entry
    url_entry.url = request.url
    db.commit()
    db.refresh(url_entry)

    return URLResponse(
        id=url_entry.id,
        url=url_entry.url,
        shortCode=url_entry.shortCode,
        createdAt=url_entry.createdAt.isoformat(),
        updatedAt=url_entry.updatedAt.isoformat()
    )

@app.delete("/shorten/{short_code}", status_code=204)
def delete_short_url(short_code: str, db: Session = Depends(get_db)):
    # Retrieve the URL entry by short code
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Delete the URL entry
    db.delete(url_entry)
    db.commit()

@app.get("/shorten/{short_code}/stats", response_model=URLStatsResponse, status_code=200)
def get_url_statistics(short_code: str, db: Session = Depends(get_db)):
    # Retrieve the URL entry by short code
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return URLStatsResponse(
        id=url_entry.id,
        url=url_entry.url,
        shortCode=url_entry.shortCode,
        createdAt=url_entry.createdAt.isoformat(),
        updatedAt=url_entry.updatedAt.isoformat(),
        accessCount=url_entry.accessCount
    )
