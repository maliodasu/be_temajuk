-- Script untuk membuat database MySQL
CREATE DATABASE IF NOT EXISTS destinasi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Buat user untuk aplikasi (opsional)
-- CREATE USER 'destinasi_user'@'localhost' IDENTIFIED BY 'your_password';
-- GRANT ALL PRIVILEGES ON destinasi_db.* TO 'destinasi_user'@'localhost';
-- FLUSH PRIVILEGES;

USE destinasi_db;

-- Tabel akan dibuat otomatis oleh SQLAlchemy saat aplikasi dijalankan
-- Tapi jika ingin membuat manual, uncomment script di bawah:

/*
CREATE TABLE destinasi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img VARCHAR(500),
    place VARCHAR(200) NOT NULL,
    desc TEXT,
    alamat TEXT,
    time VARCHAR(100),
    price DECIMAL(10,2),
    facility JSON,
    activity JSON,
    tips TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE akomodasi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kategori VARCHAR(100),
    img VARCHAR(500),
    name VARCHAR(200) NOT NULL,
    desc TEXT,
    alamat TEXT,
    facility JSON,
    nomortelp VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE tipe_kamar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    akomodasi_id INT,
    tipe VARCHAR(100) NOT NULL,
    desc TEXT,
    kapasitas INT,
    harga DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (akomodasi_id) REFERENCES akomodasi(id) ON DELETE CASCADE
);

CREATE TABLE kuliner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(200) NOT NULL,
    desc TEXT,
    alamat TEXT,
    jam_buka VARCHAR(100),
    price DECIMAL(10,2),
    nomortelp VARCHAR(20),
    menu JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE ulasan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(200) NOT NULL,
    destinasi_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    ulasan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (destinasi_id) REFERENCES destinasi(id) ON DELETE CASCADE
);
*/