from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import get_db, create_tables
from models import Destinasi, Akomodasi, Kuliner, Ulasan
import schemas
import crud

app = FastAPI(
    title="API Web Destinasi",
    description="API untuk aplikasi web destinasi wisata Indonesia",
    version="1.0.0"
)

# CORS middleware untuk koneksi dengan React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# Health check
@app.get("/", tags=["Health"])
def read_root():
    return {"message": "API Web Destinasi berjalan dengan baik!"}

# DESTINASI ENDPOINTS
@app.get("/api/destinasi", response_model=List[schemas.Destinasi], tags=["Destinasi"])
def get_destinasi_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Cari berdasarkan nama tempat, deskripsi, atau alamat"),
    db: Session = Depends(get_db)
):
    """Mengambil daftar destinasi wisata"""
    destinasi = crud.get_destinasi_list(db, skip=skip, limit=limit, search=search)
    return [schemas.Destinasi.from_orm(d) for d in destinasi]

@app.get("/api/destinasi/{destinasi_id}", response_model=schemas.Destinasi, tags=["Destinasi"])
def get_destinasi(destinasi_id: int, db: Session = Depends(get_db)):
    """Mengambil detail destinasi berdasarkan ID"""
    db_destinasi = crud.get_destinasi(db, destinasi_id=destinasi_id)
    if db_destinasi is None:
        raise HTTPException(status_code=404, detail="Destinasi tidak ditemukan")
    return db_destinasi

@app.post("/api/destinasi", response_model=schemas.Destinasi, tags=["Destinasi"])
def create_destinasi(destinasi: schemas.DestinasiCreate, db: Session = Depends(get_db)):
    """Membuat destinasi baru"""
    return crud.create_destinasi(db=db, destinasi=destinasi)

@app.put("/api/destinasi/{destinasi_id}", response_model=schemas.Destinasi, tags=["Destinasi"])
def update_destinasi(destinasi_id: int, destinasi: schemas.DestinasiUpdate, db: Session = Depends(get_db)):
    """Mengupdate destinasi berdasarkan ID"""
    db_destinasi = crud.update_destinasi(db, destinasi_id=destinasi_id, destinasi=destinasi)
    if db_destinasi is None:
        raise HTTPException(status_code=404, detail="Destinasi tidak ditemukan")
    return db_destinasi

@app.delete("/api/destinasi/{destinasi_id}", tags=["Destinasi"])
def delete_destinasi(destinasi_id: int, db: Session = Depends(get_db)):
    """Menghapus destinasi berdasarkan ID"""
    db_destinasi = crud.delete_destinasi(db, destinasi_id=destinasi_id)
    if db_destinasi is None:
        raise HTTPException(status_code=404, detail="Destinasi tidak ditemukan")
    return {"message": "Destinasi berhasil dihapus"}

# AKOMODASI ENDPOINTS
@app.get("/api/akomodasi", response_model=List[schemas.Akomodasi], tags=["Akomodasi"])
def get_akomodasi_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Cari berdasarkan nama, deskripsi, atau alamat"),
    db: Session = Depends(get_db)
):
    """Mengambil daftar akomodasi"""
    akomodasi = crud.get_akomodasi_list(db, skip=skip, limit=limit, search=search)
    return akomodasi

@app.get("/api/akomodasi/{akomodasi_id}", response_model=schemas.Akomodasi, tags=["Akomodasi"])
def get_akomodasi(akomodasi_id: int, db: Session = Depends(get_db)):
    """Mengambil detail akomodasi berdasarkan ID"""
    db_akomodasi = crud.get_akomodasi(db, akomodasi_id=akomodasi_id)
    if db_akomodasi is None:
        raise HTTPException(status_code=404, detail="Akomodasi tidak ditemukan")
    return db_akomodasi

@app.post("/api/akomodasi", response_model=schemas.Akomodasi, tags=["Akomodasi"])
def create_akomodasi(akomodasi: schemas.AkomodasiCreate, db: Session = Depends(get_db)):
    """Membuat akomodasi baru"""
    return crud.create_akomodasi(db=db, akomodasi=akomodasi)

@app.put("/api/akomodasi/{akomodasi_id}", response_model=schemas.Akomodasi, tags=["Akomodasi"])
def update_akomodasi(akomodasi_id: int, akomodasi: schemas.AkomodasiUpdate, db: Session = Depends(get_db)):
    """Mengupdate akomodasi berdasarkan ID"""
    db_akomodasi = crud.update_akomodasi(db, akomodasi_id=akomodasi_id, akomodasi=akomodasi)
    if db_akomodasi is None:
        raise HTTPException(status_code=404, detail="Akomodasi tidak ditemukan")
    return db_akomodasi

@app.delete("/api/akomodasi/{akomodasi_id}", tags=["Akomodasi"])
def delete_akomodasi(akomodasi_id: int, db: Session = Depends(get_db)):
    """Menghapus akomodasi berdasarkan ID"""
    db_akomodasi = crud.delete_akomodasi(db, akomodasi_id=akomodasi_id)
    if db_akomodasi is None:
        raise HTTPException(status_code=404, detail="Akomodasi tidak ditemukan")
    return {"message": "Akomodasi berhasil dihapus"}

# KULINER ENDPOINTS
@app.get("/api/kuliner", response_model=List[schemas.Kuliner], tags=["Kuliner"])
def get_kuliner_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Cari berdasarkan nama, deskripsi, atau alamat"),
    db: Session = Depends(get_db)
):
    """Mengambil daftar kuliner"""
    kuliner = crud.get_kuliner_list(db, skip=skip, limit=limit, search=search)
    return kuliner

@app.get("/api/kuliner/{kuliner_id}", response_model=schemas.Kuliner, tags=["Kuliner"])
def get_kuliner(kuliner_id: int, db: Session = Depends(get_db)):
    """Mengambil detail kuliner berdasarkan ID"""
    db_kuliner = crud.get_kuliner(db, kuliner_id=kuliner_id)
    if db_kuliner is None:
        raise HTTPException(status_code=404, detail="Kuliner tidak ditemukan")
    return db_kuliner

@app.post("/api/kuliner", response_model=schemas.Kuliner, tags=["Kuliner"])
def create_kuliner(kuliner: schemas.KulinerCreate, db: Session = Depends(get_db)):
    """Membuat kuliner baru"""
    return crud.create_kuliner(db=db, kuliner=kuliner)

@app.put("/api/kuliner/{kuliner_id}", response_model=schemas.Kuliner, tags=["Kuliner"])
def update_kuliner(kuliner_id: int, kuliner: schemas.KulinerUpdate, db: Session = Depends(get_db)):
    """Mengupdate kuliner berdasarkan ID"""
    db_kuliner = crud.update_kuliner(db, kuliner_id=kuliner_id, kuliner=kuliner)
    if db_kuliner is None:
        raise HTTPException(status_code=404, detail="Kuliner tidak ditemukan")
    return db_kuliner

@app.delete("/api/kuliner/{kuliner_id}", tags=["Kuliner"])
def delete_kuliner(kuliner_id: int, db: Session = Depends(get_db)):
    """Menghapus kuliner berdasarkan ID"""
    db_kuliner = crud.delete_kuliner(db, kuliner_id=kuliner_id)
    if db_kuliner is None:
        raise HTTPException(status_code=404, detail="Kuliner tidak ditemukan")
    return {"message": "Kuliner berhasil dihapus"}

# ULASAN ENDPOINTS
@app.get("/api/ulasan", response_model=List[schemas.Ulasan], tags=["Ulasan"])
def get_ulasan_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    destinasi_id: Optional[int] = Query(None, description="Filter berdasarkan destinasi ID"),
    db: Session = Depends(get_db)
):
    """Mengambil daftar ulasan"""
    ulasan = crud.get_ulasan_list(db, skip=skip, limit=limit, destinasi_id=destinasi_id)
    return ulasan

@app.get("/api/ulasan/{ulasan_id}", response_model=schemas.Ulasan, tags=["Ulasan"])
def get_ulasan(ulasan_id: int, db: Session = Depends(get_db)):
    """Mengambil detail ulasan berdasarkan ID"""
    db_ulasan = crud.get_ulasan(db, ulasan_id=ulasan_id)
    if db_ulasan is None:
        raise HTTPException(status_code=404, detail="Ulasan tidak ditemukan")
    return db_ulasan

@app.post("/api/ulasan", response_model=schemas.Ulasan, tags=["Ulasan"])
def create_ulasan(ulasan: schemas.UlasanCreate, db: Session = Depends(get_db)):
    """Membuat ulasan baru"""
    return crud.create_ulasan(db=db, ulasan=ulasan)

@app.put("/api/ulasan/{ulasan_id}", response_model=schemas.Ulasan, tags=["Ulasan"])
def update_ulasan(ulasan_id: int, ulasan: schemas.UlasanUpdate, db: Session = Depends(get_db)):
    """Mengupdate ulasan berdasarkan ID"""
    db_ulasan = crud.update_ulasan(db, ulasan_id=ulasan_id, ulasan=ulasan)
    if db_ulasan is None:
        raise HTTPException(status_code=404, detail="Ulasan tidak ditemukan")
    return db_ulasan

@app.delete("/api/ulasan/{ulasan_id}", tags=["Ulasan"])
def delete_ulasan(ulasan_id: int, db: Session = Depends(get_db)):
    """Menghapus ulasan berdasarkan ID"""
    db_ulasan = crud.delete_ulasan(db, ulasan_id=ulasan_id)
    if db_ulasan is None:
        raise HTTPException(status_code=404, detail="Ulasan tidak ditemukan")
    return {"message": "Ulasan berhasil dihapus"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)