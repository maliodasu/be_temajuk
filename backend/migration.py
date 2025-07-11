# migration.py
from sqlalchemy.orm import Session
from models import (
    Base, Destination, DestinationTip, DestinationGallery, Facility, destination_facility,
    Activity, destination_activity, PhotoSpot, PhotoSpotTip, PhotoSpotGallery, 
    PhotoSpotNearbyAttraction, Review, TransportRoute, RouteStep, RouteTip,
    Accommodation, Room, AccommodationGallery, accommodation_facility,
    Culinary, CulinarySpecialty, CulinaryGallery,
)
from database import engine

# Create all tables
Base.metadata.create_all(bind=engine)

def migrate_destinations(db: Session, destinations_data):
    for dest_data in destinations_data:
        # Create or get facilities
        facilities = []
        for facility_name in dest_data['facilities']:
            facility = db.query(Facility).filter(Facility.name == facility_name).first()
            if not facility:
                facility = Facility(name=facility_name)
                db.add(facility)
                db.commit()
            facilities.append(facility)
        
        # Create or get activities
        activities = []
        for activity_name in dest_data['activities']:
            activity = db.query(Activity).filter(Activity.name == activity_name).first()
            if not activity:
                activity = Activity(name=activity_name)
                db.add(activity)
                db.commit()
            activities.append(activity)
        
        # Create destination
        destination = Destination(
            id=dest_data['id'],
            title=dest_data['title'],
            description=dest_data['description'],
            full_description=dest_data['fullDescription'],
            image_url=dest_data['imageUrl'],
            category=dest_data['category'],
            price=dest_data['price'],
            location=dest_data['location'],
            open_hours=dest_data['openHours']
        )
        
        # Add facilities and activities
        destination.facilities = facilities
        destination.activities = activities
        
        # Add tips
        for tip_text in dest_data['tips']:
            tip = DestinationTip(tip=tip_text)
            destination.tips.append(tip)
        
        # Add gallery
        for image_url in dest_data['gallery']:
            gallery = DestinationGallery(image_url=image_url)
            destination.gallery.append(gallery)
        
        db.add(destination)
    
    db.commit()

def migrate_photo_spots(db: Session, photo_spots_data):
    for spot_data in photo_spots_data:
        photo_spot = PhotoSpot(
            id=spot_data['id'],
            title=spot_data['title'],
            description=spot_data['description'],
            full_description=spot_data['fullDescription'],
            image_url=spot_data['imageUrl'],
            category=spot_data['category'],
            location=spot_data['location'],
            best_time=spot_data['bestTime']
        )
        
        # Add tips
        for tip_text in spot_data['tips']:
            tip = PhotoSpotTip(tip=tip_text)
            photo_spot.tips.append(tip)
        
        # Add gallery
        for image_url in spot_data['gallery']:
            gallery = PhotoSpotGallery(image_url=image_url)
            photo_spot.gallery.append(gallery)
        
        # Add nearby attractions
        for attraction_name in spot_data['nearbyAttractions']:
            attraction = PhotoSpotNearbyAttraction(name=attraction_name)
            photo_spot.nearby_attractions.append(attraction)
        
        db.add(photo_spot)
    
    db.commit()

def migrate_reviews(db: Session, reviews_data):
    for review_data in reviews_data:
        review = Review(
            id=review_data['id'],
            name=review_data['name'],
            image_url=review_data['imageUrl'],
            date=review_data['date'],
            rating=review_data['rating'],
            text=review_data['text'],
            destination=review_data['destination']
        )
        db.add(review)
    
    db.commit()

def migrate_transport_routes(db: Session, transport_routes_data):
    for route_data in transport_routes_data:
        transport_route = TransportRoute(
            id=route_data['id'],
            title=route_data['title'],
            description=route_data['description'],
            estimated_cost=route_data['estimatedCost'],
            estimated_time=route_data['estimatedTime'],
            difficulty=route_data['difficulty'],
            image_url=route_data['imageUrl']
        )
        
        # Add steps
        for step_data in route_data['steps']:
            step = RouteStep(
                step=step_data['step'],
                description=step_data['description'],
                duration=step_data['duration'],
                cost=step_data['cost'],
                vehicle=step_data['vehicle']
            )
            transport_route.steps.append(step)
        
        # Add tips
        for tip_text in route_data['tips']:
            tip = RouteTip(tip=tip_text)
            transport_route.tips.append(tip)
        
        db.add(transport_route)
    
    db.commit()

def migrate_accommodations(db: Session, accommodations_data):
    for acc_data in accommodations_data:
        # Create or get facilities
        facilities = []
        for facility_name in acc_data['facilities']:
            facility = db.query(Facility).filter(Facility.name == facility_name).first()
            if not facility:
                facility = Facility(name=facility_name)
                db.add(facility)
                db.commit()
            facilities.append(facility)
        
        # Create accommodation
        accommodation = Accommodation(
            id=acc_data['id'],
            title=acc_data['title'],
            description=acc_data['description'],
            full_description=acc_data['fullDescription'],
            image_url=acc_data['imageUrl'],
            category=acc_data['category'],
            price=acc_data['price'],
            location=acc_data['location'],
            contact=acc_data['contact'],
            website=acc_data.get('website')
        )
        
        # Add facilities
        accommodation.facilities = facilities
        
        # Add rooms
        for room_data in acc_data['rooms']:
            room = Room(
                type=room_data['type'],
                price=room_data['price'],
                capacity=room_data['capacity'],
                description=room_data['description']
            )
            accommodation.rooms.append(room)
        
        # Add gallery
        for image_url in acc_data['gallery']:
            gallery = AccommodationGallery(image_url=image_url)
            accommodation.gallery.append(gallery)
        
        db.add(accommodation)
    
    db.commit()

def migrate_culinaries(db: Session, culinaries_data):
    for cul_data in culinaries_data:
        culinary = Culinary(
            id=cul_data['id'],
            title=cul_data['title'],
            description=cul_data['description'],
            full_description=cul_data['fullDescription'],
            image_url=cul_data['imageUrl'],
            category=cul_data['category'],
            price=cul_data['price'],
            location=cul_data['location'],
            open_hours=cul_data['openHours'],
            contact=cul_data.get('contact')
        )
        
        # Add specialties
        for specialty_name in cul_data['specialties']:
            specialty = CulinarySpecialty(name=specialty_name)
            culinary.specialties.append(specialty)
        
        # Add gallery
        for image_url in cul_data['gallery']:
            gallery = CulinaryGallery(image_url=image_url)
            culinary.gallery.append(gallery)
        
        db.add(culinary)
    
    db.commit()

def main():
    # Sample data from your TypeScript files (you'll need to convert these to Python dictionaries)
    destinations_data = [
        {
            "id": "pantai-temajuk",
            "title": "Pantai Temajuk",
            "description": "Pantai eksotis dengan pasir putih dan air jernih yang membentang sepanjang 6 km di ujung barat Indonesia.",
            "fullDescription": "Pantai Temajuk adalah pantai eksotis yang terletak di ujung barat Indonesia...",
            "imageUrl": "https://images.pexels.com/photos/1450353/pexels-photo-1450353.jpeg",
            "category": "Pantai",
            "price": "Rp 10.000",
            "location": "Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas, Kalimantan Barat",
            "openHours": "24 jam (terbaik dikunjungi pagi atau sore hari)",
            "facilities": ["Area Parkir", "Toilet Umum", "Warung Makan", "Penyewaan Perahu"],
            "activities": ["Berenang", "Melihat Sunset", "Berkemah", "Snorkeling", "Memancing"],
            "tips": [
                "Bawalah perlengkapan seperti sunblock, topi, dan kacamata untuk melindungi diri dari sinar matahari",
                "Jika ingin bermalam, sebaiknya memesan penginapan terlebih dahulu karena ketersediaan terbatas",
                "Kunjungi pada hari kerja untuk menghindari keramaian"
            ],
            "gallery": [
                "https://images.pexels.com/photos/1921336/pexels-photo-1921336.jpeg",
                "https://images.pexels.com/photos/1619317/pexels-photo-1619317.jpeg",
                "https://images.pexels.com/photos/1295036/pexels-photo-1295036.jpeg"
            ]
        },
        {
            "id": "tugu-perbatasan",
            "title": "Tugu Perbatasan Indonesia-Malaysia",
            "description": "Monumen perbatasan yang menandai wilayah Indonesia dan Malaysia di ujung barat Pulau Kalimantan.",
            "fullDescription": "Tugu Perbatasan Indonesia-Malaysia adalah monumen yang terletak tepat di garis perbatasan antara Indonesia dan Malaysia di ujung barat Pulau Kalimantan. Tugu ini menjadi saksi bisu perjalanan sejarah kedua negara dan merupakan simbol kedaulatan negara. Pengunjung dapat berfoto dengan latar belakang tugu sambil menginjak dua negara sekaligus. Tugu ini dikelilingi oleh hutan tropis yang masih asri dan menawarkan pengalaman wisata yang unik dan berbeda.",
            "imageUrl": "https://images.pexels.com/photos/2166553/pexels-photo-2166553.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "category": "Monumen",
            "price": "Rp 5.000",
            "location": "Perbatasan Indonesia-Malaysia, Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "openHours": "08.00 - 17.00 WIB",
            "facilities": ["Area Parkir", "Toilet Umum", "Pos Penjagaan"],
            "activities": ["Berfoto", "Melihat Pemandangan", "Trekking"],
            "tips": [
            "Bawalah identitas diri (KTP/SIM/Paspor) saat berkunjung",
            "Patuhi aturan dan jangan melewati batas negara tanpa izin",
            "Bawalah air minum yang cukup karena perjalanan menuju tugu cukup melelahkan"
            ],
            "gallery": [
            "https://images.pexels.com/photos/2559941/pexels-photo-2559941.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/2471970/pexels-photo-2471970.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/1576937/pexels-photo-1576937.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            ]
        },
        {
            "id": "hutan-mangrove",
            "title": "Hutan Mangrove Temajuk",
            "description": "Ekosistem mangrove yang menjadi habitat berbagai flora dan fauna serta menawarkan jalur susur mangrove.",
            "fullDescription": "Hutan Mangrove Temajuk adalah kawasan hutan bakau yang terletak di pesisir pantai Temajuk. Ekosistem mangrove ini menjadi rumah bagi berbagai flora dan fauna, termasuk burung-burung langka dan kepiting bakau. Pengunjung dapat menjelajahi hutan mangrove melalui jalur susur kayu yang telah disediakan. Pemandangan akar-akar pohon mangrove yang menjulang dari air adalah pemandangan yang menarik untuk diabadikan. Selain nilai estetikanya, hutan mangrove juga berperan penting dalam melindungi pesisir dari abrasi dan menjaga ekosistem laut.",
            "imageUrl": "images/batu-nenek-aluwi.jpg",
            "category": "Alam",
            "price": "Rp 15.000",
            "location": "Pesisir Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "openHours": "07.00 - 18.00 WIB",
            "facilities": ["Jalur Susur Mangrove", "Toilet Umum", "Pos Informasi", "Area Parkir"],
            "activities": ["Tracking Mangrove", "Fotografi", "Pengamatan Burung", "Edukasi Lingkungan"],
            "tips": [
            "Kenakan pakaian yang nyaman dan sepatu yang sesuai untuk tracking",
            "Bawalah obat anti nyamuk",
            "Jangan membuang sampah sembarangan untuk menjaga kelestarian ekosistem"
            ],
            "gallery": [
            "https://images.pexels.com/photos/2583852/pexels-photo-2583852.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/5232048/pexels-photo-5232048.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/14199312/pexels-photo-14199312.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            ]
        },
        {
            "id": "bukit-maung",
            "title": "Bukit Maung",
            "description": "Bukit dengan pemandangan spektakuler Laut Natuna dan bentangan hutan tropis yang luas.",
            "fullDescription": "Bukit Maung adalah salah satu destinasi wisata alam yang menawarkan pemandangan spektakuler di Temajuk. Dari puncak bukit, pengunjung dapat menikmati panorama Laut Natuna yang membentang luas serta hamparan hutan tropis yang mengelilingi kawasan Temajuk. Tracking menuju puncak bukit membutuhkan waktu sekitar 1-2 jam, namun keindahan pemandangan di puncak akan membayar semua usaha Anda. Bukit Maung adalah tempat ideal untuk melihat matahari terbit dan menikmati udara segar pegunungan.",
            "imageUrl": "https://images.pexels.com/photos/1770809/pexels-photo-1770809.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "category": "Alam",
            "price": "Rp 10.000",
            "location": "Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "openHours": "06.00 - 18.00 WIB",
            "facilities": ["Jalur Pendakian", "Pos Istirahat", "Area Camping"],
            "activities": ["Trekking", "Camping", "Fotografi", "Melihat Sunrise"],
            "tips": [
                "Bawalah air minum dan bekal yang cukup",
                "Kenakan sepatu trekking dan pakaian yang nyaman",
                "Untuk melihat sunrise, sebaiknya mendaki pada malam hari dan bermalam di puncak"
            ],
            "gallery": [
                "https://images.pexels.com/photos/1666012/pexels-photo-1666012.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "https://images.pexels.com/photos/1624438/pexels-photo-1624438.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "https://images.pexels.com/photos/2224956/pexels-photo-2224956.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            ]
        },
        {
            "id": "teluk-atong",
            "title": "Teluk Atong",
            "description": "Pantai ini dikenal karena atong adalah orang pertama yang mendirikan penginapan di kawasan ini.",
            "fullDescription": "Pantai ini dikenal karena atong adalah orang pertama yang mendirikan penginapan di kawasan ini, daerah yang dulunya paling ujung dan dekat dengan hutan lindung Tanjung Datuk. Sekarang semakin ramai karena jalur menuju atong bahari sudah menjadi jalur utama wisata Desa Temajuk. Karakteristik pantai ini sama dengan pantai Camar Bulan, namun perbedaannya adalah ketika surut batu karang akan terhampar luas didepan pantai dan ketika air pasang kita bisa melakukan snorkeling disekitar pantai ini.",
            "imageUrl": "https://jadesta.com/imgpost/35189.jpg",
            "category": "Teluk",
            "price": "Rp 15.000",
            "location": "Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "openHours": "08.00 - 17.00 WIB",
            "facilities": ["Area Parkir", "Toilet Umum", "Gazebo", "Warung Makan"],
            "activities": ["Berenang", "Fotografi", "Piknik", "Bersantai"],
            "tips": [
                "Bawalah baju ganti jika berencana berenang",
                "Waspada terhadap kedalaman danau di beberapa bagian",
                "Jangan membuang sampah sembarangan untuk menjaga kebersihan pantai"
            ],
            "gallery": [
                "https://images.pexels.com/photos/2159538/pexels-photo-2159538.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "https://images.pexels.com/photos/1903702/pexels-photo-1903702.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "https://images.pexels.com/photos/1586298/pexels-photo-1586298.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            ]
        },
        {
            "id": "air-terjun-coras",
            "title": "Air Terjun Carocok Antu Soreh (Coras)",
            "description": "Air terjun bertingkat yang berada di tengah hutan belantara dengan air yang jernih dan sejuk.",
            "fullDescription": "Air Terjun Carocok Antu Soreh atau yang biasa disingkat Coras adalah air terjun bertingkat yang terletak di tengah hutan belantara Temajuk. Air terjun ini memiliki beberapa tingkatan dengan kolam-kolam alami yang dapat digunakan untuk berendam. Air yang jernih dan sejuk serta suara gemericik air yang menenangkan menciptakan atmosfer yang sangat menyegarkan. Perjalanan menuju air terjun ini melalui jalur trekking yang cukup menantang, namun keindahan alam sepanjang perjalanan dan keindahan air terjun akan membuat segala usaha terbayarkan.",
            "imageUrl": "https://images.pexels.com/photos/358457/pexels-photo-358457.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "category": "Air Terjun",
            "price": "Rp 20.000",
            "location": "Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "openHours": "08.00 - 16.00 WIB",
            "facilities": ["Jalur Trekking", "Area Istirahat", "Toilet Umum"],
            "activities": ["Trekking", "Berendam", "Fotografi", "Menikmati Alam"],
            "tips": [
                "Kenakan sepatu yang sesuai untuk trekking",
                "Bawalah air minum yang cukup",
                "Datanglah pagi hari untuk menghindari hujan sore yang biasa terjadi di kawasan hutan"
            ],
            "gallery": [
                "https://images.pexels.com/photos/358457/pexels-photo-358457.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "https://images.pexels.com/photos/460621/pexels-photo-460621.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
                "https://images.pexels.com/photos/1650227/pexels-photo-1650227.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            ]
        }
        # Add other destinations similarly...
    ]
    
    photo_spots_data = [
        {
            "id": "sunset-point",
            "title": "Sunset Point Temajuk",
            "description": "Titik ideal untuk menikmati dan mengabadikan keindahan matahari terbenam dengan latar belakang laut Natuna.",
            "fullDescription": "Sunset Point Temajuk adalah spot terbaik untuk menikmati keindahan matahari terbenam di Temajuk...",
            "imageUrl": "https://images.pexels.com/photos/635279/pexels-photo-635279.jpeg",
            "category": "Pantai",
            "location": "Bagian Barat Pantai Temajuk, Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "bestTime": "16.00 - 18.30 WIB",
            "tips": [
                "Datang 1 jam sebelum sunset untuk mendapatkan posisi terbaik",
                "Bawa tripod untuk hasil foto yang lebih stabil",
                "Gunakan filter ND untuk hasil foto sunset yang lebih dramatis",
                "Sediakan jaket tipis karena angin pantai bisa cukup kencang saat sore hari"
            ],
            "gallery": [
                "https://images.pexels.com/photos/3310691/pexels-photo-3310691.jpeg",
                "https://images.pexels.com/photos/33545/sunrise-phu-quoc-island-ocean.jpg",
                "https://images.pexels.com/photos/1705254/pexels-photo-1705254.jpeg"
            ],
            "nearbyAttractions": [
                "Pantai Temajuk",
                "Warung Seafood Pak Rahman",
                "Kedai Kopi Ujung Negeri"
            ]
        },
        # Add other photo spots similarly...
    ]
    
    reviews_data = [
        {
            "id": "1",
            "name": "Budi Santoso",
            "imageUrl": "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg",
            "date": "12 Mei 2023",
            "rating": 5,
            "text": "Temajuk adalah surga tersembunyi yang wajib dikunjungi! Pantainya bersih dengan pasir putih dan air laut yang jernih...",
            "destination": "Pantai Temajuk"
        },
        # Add other reviews similarly...
    ]
    
    transport_routes_data = [
        {
            "id": "pontianak-temajuk",
            "title": "Pontianak ke Temajuk",
            "description": "Rute perjalanan dari Kota Pontianak (ibukota Provinsi Kalimantan Barat) menuju Desa Temajuk.",
            "estimatedCost": "Rp 350.000 - Rp 500.000 per orang",
            "estimatedTime": "10-12 jam",
            "difficulty": "Sedang",
            "imageUrl": "https://images.pexels.com/photos/2942172/pexels-photo-2942172.jpeg",
            "steps": [
                {
                    "step": 1,
                    "description": "Dari Pontianak, ambil bus atau travel menuju Kota Sambas...",
                    "duration": "4-5 jam",
                    "cost": "Rp 100.000 - Rp 150.000",
                    "vehicle": "Bus / Travel"
                },
                # Add other steps...
            ],
            "tips": [
                "Berangkat pagi hari dari Pontianak untuk menghindari terjebak malam di perjalanan",
                # Add other tips...
            ]
        },
        # Add other transport routes similarly...
    ]
    
    accommodations_data = [
        {
            "id": "temajuk-beach-resort",
            "title": "Temajuk Beach Resort",
            "description": "Resort tepi pantai dengan pemandangan laut yang menakjubkan dan fasilitas lengkap untuk liburan keluarga.",
            "fullDescription": "Temajuk Beach Resort adalah akomodasi mewah yang terletak tepat di tepi Pantai Temajuk...",
            "imageUrl": "https://images.pexels.com/photos/338504/pexels-photo-338504.jpeg",
            "category": "Resort",
            "price": "Rp 800.000 - Rp 2.500.000",
            "location": "Jl. Pantai Temajuk, Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "facilities": ["Kolam Renang", "Restoran", "WiFi", "AC", "TV", "Parkir", "24-hour Front Desk", "Spa"],
            "contact": "+62 8123 4567 890",
            "website": "www.temajukbeachresort.com",
            "gallery": [
                "https://images.pexels.com/photos/189296/pexels-photo-189296.jpeg",
                # Add other gallery images...
            ],
            "rooms": [
                {
                    "type": "Kamar Standard",
                    "price": "Rp 800.000/malam",
                    "capacity": "2 orang",
                    "description": "Kamar nyaman dengan tempat tidur queen size, kamar mandi pribadi, dan balkon kecil."
                },
                # Add other rooms...
            ]
        },
        # Add other accommodations similarly...
    ]
    
    culinaries_data = [
        {
            "id": "warung-seafood-pak-rahman",
            "title": "Warung Seafood Pak Rahman",
            "description": "Warung seafood dengan menu ikan dan seafood segar langsung dari nelayan lokal Temajuk.",
            "fullDescription": "Warung Seafood Pak Rahman adalah tempat makan populer di Temajuk yang menyajikan berbagai hidangan seafood segar...",
            "imageUrl": "https://images.pexels.com/photos/566345/pexels-photo-566345.jpeg",
            "category": "Seafood",
            "price": "Rp 25.000 - Rp 100.000",
            "location": "Jl. Pantai Temajuk No. 10, Desa Temajuk, Kecamatan Paloh, Kabupaten Sambas",
            "openHours": "11.00 - 21.00 WIB",
            "contact": "+62 8123 4567 890",
            "specialties": [
                "Ikan Bakar Bumbu Khas",
                "Cumi Goreng Tepung",
                "Udang Asam Manis",
                "Sup Ikan Kuah Asam"
            ],
            "gallery": [
                "https://images.pexels.com/photos/1148086/pexels-photo-1148086.jpeg",
                # Add other gallery images...
            ]
        },
        # Add other culinaries similarly...
    ]

    # Connect to database and run migrations
    db = Session(bind=engine)
    
    try:
        # Migrate each data type
        migrate_destinations(db, destinations_data)
        migrate_photo_spots(db, photo_spots_data)
        migrate_reviews(db, reviews_data)
        migrate_transport_routes(db, transport_routes_data)
        migrate_accommodations(db, accommodations_data)
        migrate_culinaries(db, culinaries_data)
        
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()