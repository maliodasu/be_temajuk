# Backend Web Destinasi

Backend API untuk aplikasi web destinasi wisata menggunakan FastAPI, MySQL, dan SQLAlchemy.

## Fitur

- **CRUD Destinasi**: Kelola data destinasi wisata
- **CRUD Akomodasi**: Kelola data akomodasi dengan tipe kamar
- **CRUD Kuliner**: Kelola data tempat makan dan kuliner
- **CRUD Ulasan**: Kelola ulasan pengguna untuk destinasi
- **Dokumentasi Swagger**: Dokumentasi API otomatis
- **CORS Support**: Dukungan untuk koneksi dengan React frontend

## Instalasi

1. **Setup Virtual Environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Di Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Database**
- Buat database MySQL dengan nama `destinasi_db`
- Copy file `.env.example` ke `.env` dan sesuaikan konfigurasi database

4. **Jalankan Server**
```bash
uvicorn main:app --reload
```

Server akan berjalan di `http://localhost:8000`

## Dokumentasi API

Setelah server berjalan, akses dokumentasi Swagger di:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

### Destinasi
- `GET /api/destinasi` - Daftar destinasi
- `GET /api/destinasi/{id}` - Detail destinasi
- `POST /api/destinasi` - Buat destinasi baru
- `PUT /api/destinasi/{id}` - Update destinasi
- `DELETE /api/destinasi/{id}` - Hapus destinasi

### Akomodasi
- `GET /api/akomodasi` - Daftar akomodasi
- `GET /api/akomodasi/{id}` - Detail akomodasi
- `POST /api/akomodasi` - Buat akomodasi baru
- `PUT /api/akomodasi/{id}` - Update akomodasi
- `DELETE /api/akomodasi/{id}` - Hapus akomodasi

### Kuliner
- `GET /api/kuliner` - Daftar kuliner
- `GET /api/kuliner/{id}` - Detail kuliner
- `POST /api/kuliner` - Buat kuliner baru
- `PUT /api/kuliner/{id}` - Update kuliner
- `DELETE /api/kuliner/{id}` - Hapus kuliner

### Ulasan
- `GET /api/ulasan` - Daftar ulasan
- `GET /api/ulasan/{id}` - Detail ulasan
- `POST /api/ulasan` - Buat ulasan baru
- `PUT /api/ulasan/{id}` - Update ulasan
- `DELETE /api/ulasan/{id}` - Hapus ulasan

## Struktur Data

### Destinasi
```json
{
  "img": "string",
  "place": "string",
  "desc": "string",
  "alamat": "string",
  "time": "string",
  "price": 0,
  "facility": ["string"],
  "activity": ["string"],
  "tips": "string"
}
```

### Akomodasi
```json
{
  "kategori": "string",
  "img": "string",
  "name": "string",
  "desc": "string",
  "alamat": "string",
  "facility": ["string"],
  "nomortelp": "string",
  "tipe_kamar": [
    {
      "tipe": "string",
      "desc": "string",
      "kapasitas": 0,
      "harga": 0
    }
  ]
}
```

### Kuliner
```json
{
  "nama": "string",
  "desc": "string",
  "alamat": "string",
  "jam_buka": "string",
  "price": 0,
  "nomortelp": "string",
  "menu": ["string"]
}
```

### Ulasan
```json
{
  "nama": "string",
  "destinasi_id": 0,
  "rating": 0,
  "ulasan": "string"
}
```

## Koneksi dengan React Frontend

Backend sudah dikonfigurasi dengan CORS untuk menerima request dari React dev server (`localhost:3000` dan `localhost:5173`).

Contoh penggunaan di React:
```javascript
// Fetch destinasi
const response = await fetch('http://localhost:8000/api/destinasi');
const destinasi = await response.json();

// Create destinasi
const response = await fetch('http://localhost:8000/api/destinasi', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(destinasiData)
});
```