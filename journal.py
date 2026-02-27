from fastapi import APIRouter, Depends, HTTPException, Query
from schema import JournalCreate
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from dependencies import get_db, get_curr_user
from model import JournalEntry

router = APIRouter()

@router.post("/create", response_model=JournalCreate)
def journal_entry(data: JournalCreate, db: Session = Depends(get_db), current_user = Depends(get_curr_user)):
    db_journal = JournalEntry(
        title= data.title, 
        content= data.content, 
        owner_id= current_user.id
    )

    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return db_journal

@router.get("/get", response_model=list[JournalCreate])
def journal_get(db: Session = Depends(get_db), current_user = Depends(get_curr_user)):
    db_journal = db.query(JournalEntry).filter(current_user.id == JournalEntry.owner_id).all()
    return db_journal

@router.get("/getbytitle/{id}", response_model=JournalCreate)
def journal_get_by_title(id: int, db: Session = Depends(get_db), curent_user = Depends(get_curr_user)):
    db_journal = db.query(JournalEntry).filter((curent_user.id == JournalEntry.owner_id), (id == JournalEntry.id)).first()

    if not db_journal:
        raise HTTPException(status_code=400, detail="invalid details")
    
    return db_journal

@router.get("/getbyque")
def journal_getting(title: str, db: Session = Depends(get_db), current_user = Depends(get_curr_user)):
    db_journal = db.query(JournalEntry).filter((current_user.id == JournalEntry.owner_id), (title == JournalEntry.title)).all()

    if not db_journal:
        raise HTTPException(status_code=400, detail="invalid details")
    
    return db_journal

@router.get("/sort")
def sort(sort_by: str = Query(..., description="enter title here to sort accordingly"), order_by: str = Query('asc'), db: Session = Depends(get_db), current_user = Depends(get_curr_user)):

    column = getattr(JournalEntry, sort_by)

    if order_by == "desc":
        column = desc(column)
    else:
        column = asc(column)

    sort_db = db.query(JournalEntry).filter(current_user.id == JournalEntry.owner_id).order_by(column).all()

    return sort_db

@router.get("/prac")
def prac(title: str, order_by: str, db: Session = Depends(get_db), current_user = Depends(get_curr_user)):

    col = getattr(JournalEntry, title)

    if order_by == "desc":
        col = desc(col)
    else:
        col = asc(col)
    
    db_sorts = db.query(JournalEntry).filter(JournalEntry.owner_id == current_user.id).order_by(col).all()

    return db_sorts

@router.get("/getpara/{id}", response_model=JournalCreate)
def getpara(id: int, db: Session = Depends(get_db), curr_user = Depends(get_curr_user)):
    db_user = db.query(JournalEntry).filter(JournalEntry.owner_id == curr_user.id, JournalEntry.id == id).first()

    return db_user