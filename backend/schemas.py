from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Destinasi Schemas
class DestinasiBase(BaseModel):
    place: str
    desc: Optional[str] = None
    alamat: Optional[str] = None
    time: Optional[str] = None
    price: Optional[float] = None
    facility: Optional[List[str]] = None
    activity: Optional[List[str]] = None
    tips: Optional[str] = None

class DestinasiCreate(DestinasiBase):
    pass

class DestinasiUpdate(BaseModel):
    place: Optional[str] = None
    desc: Optional[str] = None
    alamat: Optional[str] = None
    time: Optional[str] = None
    price: Optional[float] = None
    facility: Optional[List[str]] = None
    activity: Optional[List[str]] = None
    tips: Optional[str] = None

class Destinasi(DestinasiBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Tipe Kamar Schemas
class TipeKamarBase(BaseModel):
    tipe: str
    desc: Optional[str] = None
    kapasitas: Optional[int] = None
    harga: Optional[float] = None

class TipeKamarCreate(TipeKamarBase):
    pass

class TipeKamar(TipeKamarBase):
    id: int
    akomodasi_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Akomodasi Schemas
class AkomodasiBase(BaseModel):
    kategori: Optional[str] = None
    name: str
    desc: Optional[str] = None
    alamat: Optional[str] = None
    facility: Optional[List[str]] = None
    nomortelp: Optional[str] = None

class AkomodasiCreate(AkomodasiBase):
    tipe_kamar: Optional[List[TipeKamarCreate]] = None

class AkomodasiUpdate(BaseModel):
    kategori: Optional[str] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    alamat: Optional[str] = None
    facility: Optional[List[str]] = None
    nomortelp: Optional[str] = None

class Akomodasi(AkomodasiBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tipe_kamar: List[TipeKamar] = []
    
    class Config:
        orm_mode = True

# Kuliner Schemas
class KulinerBase(BaseModel):
    nama: str
    desc: Optional[str] = None
    alamat: Optional[str] = None
    jam_buka: Optional[str] = None
    price: Optional[float] = None
    nomortelp: Optional[str] = None
    menu: Optional[List[str]] = None

class KulinerCreate(KulinerBase):
    pass

class KulinerUpdate(BaseModel):
    nama: Optional[str] = None
    desc: Optional[str] = None
    alamat: Optional[str] = None
    jam_buka: Optional[str] = None
    price: Optional[float] = None
    nomortelp: Optional[str] = None
    menu: Optional[List[str]] = None

class Kuliner(KulinerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Ulasan Schemas
class UlasanBase(BaseModel):
    nama: str
    destinasi_id: int
    rating: int
    ulasan: Optional[str] = None

class UlasanCreate(UlasanBase):
    pass

class UlasanUpdate(BaseModel):
    nama: Optional[str] = None
    destinasi_id: Optional[int] = None
    rating: Optional[int] = None
    ulasan: Optional[str] = None

class Ulasan(UlasanBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True