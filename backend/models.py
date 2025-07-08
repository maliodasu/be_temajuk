from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Destinasi(Base):
    __tablename__ = "destinasi"
    
    id = Column(Integer, primary_key=True, index=True)
    place = Column(String(200), nullable=False)
    desc = Column(Text)
    alamat = Column(Text)
    time = Column(String(100))
    price = Column(Float)
    facility = Column(JSON)  # Array of facilities
    activity = Column(JSON)  # Array of activities
    tips = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    ulasan = relationship("Ulasan", back_populates="destinasi_rel")

class Akomodasi(Base):
    __tablename__ = "akomodasi"
    
    id = Column(Integer, primary_key=True, index=True)
    kategori = Column(String(100))
    name = Column(String(200), nullable=False)
    desc = Column(Text)
    alamat = Column(Text)
    facility = Column(JSON)  # Array of facilities
    nomortelp = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    tipe_kamar = relationship("TipeKamar", back_populates="akomodasi")

class TipeKamar(Base):
    __tablename__ = "tipe_kamar"
    
    id = Column(Integer, primary_key=True, index=True)
    akomodasi_id = Column(Integer, ForeignKey("akomodasi.id"))
    tipe = Column(String(100), nullable=False)
    desc = Column(Text)
    kapasitas = Column(Integer)
    harga = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    akomodasi = relationship("Akomodasi", back_populates="tipe_kamar")

class Kuliner(Base):
    __tablename__ = "kuliner"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(200), nullable=False)
    desc = Column(Text)
    alamat = Column(Text)
    jam_buka = Column(String(100))
    price = Column(Float)
    nomortelp = Column(String(20))
    menu = Column(JSON)  # Array of menu items
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Ulasan(Base):
    __tablename__ = "ulasan"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(200), nullable=False)
    destinasi_id = Column(Integer, ForeignKey("destinasi.id"))
    rating = Column(Integer)  # 1-5 rating
    ulasan = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    destinasi_rel = relationship("Destinasi", back_populates="ulasan")