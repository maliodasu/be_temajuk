from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Destinasi, Akomodasi, TipeKamar, Kuliner, Ulasan
from schemas import (
    DestinasiCreate, DestinasiUpdate,
    AkomodasiCreate, AkomodasiUpdate,
    KulinerCreate, KulinerUpdate,
    UlasanCreate, UlasanUpdate,
)
from typing import List, Optional

# CRUD Destinasi
def get_destinasi(db: Session, destinasi_id: int):
    return db.query(Destinasi).filter(Destinasi.id == destinasi_id).first()

def get_destinasi_list(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(Destinasi)
    if search:
        query = query.filter(or_(
            Destinasi.place.contains(search),
            Destinasi.desc.contains(search),
            Destinasi.alamat.contains(search)
        ))
    return query.offset(skip).limit(limit).all()

def create_destinasi(db: Session, destinasi: DestinasiCreate):
    db_destinasi = Destinasi(**destinasi.dict())
    db.add(db_destinasi)
    db.commit()
    db.refresh(db_destinasi)
    return db_destinasi

def update_destinasi(db: Session, destinasi_id: int, destinasi: DestinasiUpdate):
    db_destinasi = db.query(Destinasi).filter(Destinasi.id == destinasi_id).first()
    if db_destinasi:
        for field, value in destinasi.dict(exclude_unset=True).items():
            setattr(db_destinasi, field, value)
        db.commit()
        db.refresh(db_destinasi)
    return db_destinasi

def delete_destinasi(db: Session, destinasi_id: int):
    db_destinasi = db.query(Destinasi).filter(Destinasi.id == destinasi_id).first()
    if db_destinasi:
        db.delete(db_destinasi)
        db.commit()
    return db_destinasi

# CRUD Akomodasi
def get_akomodasi(db: Session, akomodasi_id: int):
    return db.query(Akomodasi).filter(Akomodasi.id == akomodasi_id).first()

def get_akomodasi_list(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(Akomodasi)
    if search:
        query = query.filter(or_(
            Akomodasi.name.contains(search),
            Akomodasi.desc.contains(search),
            Akomodasi.alamat.contains(search)
        ))
    return query.offset(skip).limit(limit).all()

def create_akomodasi(db: Session, akomodasi: AkomodasiCreate):
    db_akomodasi = Akomodasi(
        kategori=akomodasi.kategori,
        name=akomodasi.name,
        desc=akomodasi.desc,
        alamat=akomodasi.alamat,
        facility=akomodasi.facility,
        nomortelp=akomodasi.nomortelp
    )
    db.add(db_akomodasi)
    db.commit()
    db.refresh(db_akomodasi)
    
    # Add tipe kamar if provided
    if akomodasi.tipe_kamar:
        for tipe_kamar in akomodasi.tipe_kamar:
            db_tipe_kamar = TipeKamar(
                akomodasi_id=db_akomodasi.id,
                **tipe_kamar.dict()
            )
            db.add(db_tipe_kamar)
        db.commit()
        db.refresh(db_akomodasi)
    
    return db_akomodasi

def update_akomodasi(db: Session, akomodasi_id: int, akomodasi: AkomodasiUpdate):
    db_akomodasi = db.query(Akomodasi).filter(Akomodasi.id == akomodasi_id).first()
    if db_akomodasi:
        for field, value in akomodasi.dict(exclude_unset=True).items():
            setattr(db_akomodasi, field, value)
        db.commit()
        db.refresh(db_akomodasi)
    return db_akomodasi

def delete_akomodasi(db: Session, akomodasi_id: int):
    db_akomodasi = db.query(Akomodasi).filter(Akomodasi.id == akomodasi_id).first()
    if db_akomodasi:
        db.delete(db_akomodasi)
        db.commit()
    return db_akomodasi

# CRUD Kuliner
def get_kuliner(db: Session, kuliner_id: int):
    return db.query(Kuliner).filter(Kuliner.id == kuliner_id).first()

def get_kuliner_list(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(Kuliner)
    if search:
        query = query.filter(or_(
            Kuliner.nama.contains(search),
            Kuliner.desc.contains(search),
            Kuliner.alamat.contains(search)
        ))
    return query.offset(skip).limit(limit).all()

def create_kuliner(db: Session, kuliner: KulinerCreate):
    db_kuliner = Kuliner(**kuliner.dict())
    db.add(db_kuliner)
    db.commit()
    db.refresh(db_kuliner)
    return db_kuliner

def update_kuliner(db: Session, kuliner_id: int, kuliner: KulinerUpdate):
    db_kuliner = db.query(Kuliner).filter(Kuliner.id == kuliner_id).first()
    if db_kuliner:
        for field, value in kuliner.dict(exclude_unset=True).items():
            setattr(db_kuliner, field, value)
        db.commit()
        db.refresh(db_kuliner)
    return db_kuliner

def delete_kuliner(db: Session, kuliner_id: int):
    db_kuliner = db.query(Kuliner).filter(Kuliner.id == kuliner_id).first()
    if db_kuliner:
        db.delete(db_kuliner)
        db.commit()
    return db_kuliner

# CRUD Ulasan
def get_ulasan(db: Session, ulasan_id: int):
    return db.query(Ulasan).filter(Ulasan.id == ulasan_id).first()

def get_ulasan_list(db: Session, skip: int = 0, limit: int = 100, destinasi_id: Optional[int] = None):
    query = db.query(Ulasan)
    if destinasi_id:
        query = query.filter(Ulasan.destinasi_id == destinasi_id)
    return query.offset(skip).limit(limit).all()

def create_ulasan(db: Session, ulasan: UlasanCreate):
    db_ulasan = Ulasan(**ulasan.dict())
    db.add(db_ulasan)
    db.commit()
    db.refresh(db_ulasan)
    return db_ulasan

def update_ulasan(db: Session, ulasan_id: int, ulasan: UlasanUpdate):
    db_ulasan = db.query(Ulasan).filter(Ulasan.id == ulasan_id).first()
    if db_ulasan:
        for field, value in ulasan.dict(exclude_unset=True).items():
            setattr(db_ulasan, field, value)
        db.commit()
        db.refresh(db_ulasan)
    return db_ulasan

def delete_ulasan(db: Session, ulasan_id: int):
    db_ulasan = db.query(Ulasan).filter(Ulasan.id == ulasan_id).first()
    if db_ulasan:
        db.delete(db_ulasan)
        db.commit()
    return db_ulasan