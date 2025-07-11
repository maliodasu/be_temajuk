from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models import (
    Destination, DestinationTip, DestinationGallery, destination_facility, destination_activity,
    Accommodation, Room, AccommodationGallery, accommodation_facility,
    Culinary, CulinarySpecialty, CulinaryGallery,
    Review,
    PhotoSpot, PhotoSpotTip, PhotoSpotGallery, PhotoSpotNearbyAttraction,
    TransportRoute, RouteStep, RouteTip,
    Facility, Activity
)
from schemas import (
    DestinationCreate, DestinationUpdate,
    AccommodationCreate, AccommodationUpdate, RoomCreate,
    CulinaryCreate, CulinaryUpdate, CulinarySpecialtyCreate,
    ReviewCreate, ReviewUpdate,
    PhotoSpotCreate, PhotoSpotUpdate,
    TransportRouteCreate, TransportRouteUpdate, RouteStepCreate, RouteTipCreate
)
from typing import List, Optional

# Utility functions
def get_or_create_facilities(db: Session, facility_names: List[str]) -> List[Facility]:
    facilities = []
    for name in facility_names:
        facility = db.query(Facility).filter(Facility.name == name).first()
        if not facility:
            facility = Facility(name=name)
            db.add(facility)
            db.commit()
            db.refresh(facility)
        facilities.append(facility)
    return facilities

def get_or_create_activities(db: Session, activity_names: List[str]) -> List[Activity]:
    activities = []
    for name in activity_names:
        activity = db.query(Activity).filter(Activity.name == name).first()
        if not activity:
            activity = Activity(name=name)
            db.add(activity)
            db.commit()
            db.refresh(activity)
        activities.append(activity)
    return activities

# Destination CRUD
def get_destination(db: Session, destination_id: str) -> Optional[Destination]:
    return db.query(Destination).filter(Destination.id == destination_id).first()

def get_destinations(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Destination]:
    query = db.query(Destination)
    if search:
        query = query.filter(
            or_(
                Destination.title.ilike(f"%{search}%"),
                Destination.description.ilike(f"%{search}%"),
                Destination.location.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_destination(db: Session, destination: DestinationCreate) -> Destination:
    db_destination = Destination(
        id=destination.id,
        title=destination.title,
        description=destination.description,
        full_description=destination.full_description,
        image_url=destination.image_url,
        category=destination.category,
        price=destination.price,
        location=destination.location,
        open_hours=destination.open_hours
    )
    
    # Handle facilities
    if destination.facilities:
        facilities = get_or_create_facilities(db, destination.facilities)
        db_destination.facilities = facilities
    
    # Handle activities
    if destination.activities:
        activities = get_or_create_activities(db, destination.activities)
        db_destination.activities = activities
    
    # Handle tips
    if destination.tips:
        for tip in destination.tips:
            db_tip = DestinationTip(tip=tip.tip)
            db_destination.tips.append(db_tip)
    
    # Handle gallery
    if destination.gallery:
        for image in destination.gallery:
            db_gallery = DestinationGallery(image_url=image.image_url)
            db_destination.gallery.append(db_gallery)
    
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

def update_destination(db: Session, destination_id: str, destination: DestinationUpdate) -> Optional[Destination]:
    db_destination = get_destination(db, destination_id)
    if db_destination:
        for var, value in vars(destination).items():
            if value is not None:
                setattr(db_destination, var, value)
        
        # Update facilities if provided
        if destination.facilities is not None:
            facilities = get_or_create_facilities(db, destination.facilities)
            db_destination.facilities = facilities
        
        # Update activities if provided
        if destination.activities is not None:
            activities = get_or_create_activities(db, destination.activities)
            db_destination.activities = activities
        
        db.commit()
        db.refresh(db_destination)
    return db_destination

def delete_destination(db: Session, destination_id: str) -> bool:
    db_destination = get_destination(db, destination_id)
    if db_destination:
        db.delete(db_destination)
        db.commit()
        return True
    return False

# Accommodation CRUD
def get_accommodation(db: Session, accommodation_id: str) -> Optional[Accommodation]:
    return db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()

def get_accommodations(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Accommodation]:
    query = db.query(Accommodation)
    if search:
        query = query.filter(
            or_(
                Accommodation.title.ilike(f"%{search}%"),
                Accommodation.description.ilike(f"%{search}%"),
                Accommodation.location.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_accommodation(db: Session, accommodation: AccommodationCreate) -> Accommodation:
    db_accommodation = Accommodation(
        id=accommodation.id,
        title=accommodation.title,
        description=accommodation.description,
        full_description=accommodation.full_description,
        image_url=accommodation.image_url,
        category=accommodation.category,
        price=accommodation.price,
        location=accommodation.location,
        contact=accommodation.contact,
        website=accommodation.website
    )
    
    # Handle facilities
    if accommodation.facilities:
        facilities = get_or_create_facilities(db, accommodation.facilities)
        db_accommodation.facilities = facilities
    
    # Handle rooms
    if accommodation.rooms:
        for room in accommodation.rooms:
            db_room = Room(
                type=room.type,
                price=room.price,
                capacity=room.capacity,
                description=room.description
            )
            db_accommodation.rooms.append(db_room)
    
    # Handle gallery
    if accommodation.gallery:
        for image in accommodation.gallery:
            db_gallery = AccommodationGallery(image_url=image.image_url)
            db_accommodation.gallery.append(db_gallery)
    
    db.add(db_accommodation)
    db.commit()
    db.refresh(db_accommodation)
    return db_accommodation

def update_accommodation(db: Session, accommodation_id: str, accommodation: AccommodationUpdate) -> Optional[Accommodation]:
    db_accommodation = get_accommodation(db, accommodation_id)
    if db_accommodation:
        for var, value in vars(accommodation).items():
            if value is not None:
                setattr(db_accommodation, var, value)
        
        # Update facilities if provided
        if accommodation.facilities is not None:
            facilities = get_or_create_facilities(db, accommodation.facilities)
            db_accommodation.facilities = facilities
        
        db.commit()
        db.refresh(db_accommodation)
    return db_accommodation

def delete_accommodation(db: Session, accommodation_id: str) -> bool:
    db_accommodation = get_accommodation(db, accommodation_id)
    if db_accommodation:
        db.delete(db_accommodation)
        db.commit()
        return True
    return False

# Room CRUD
def get_room(db: Session, room_id: str) -> Optional[Room]:
    return db.query(Room).filter(Room.id == room_id).first()

def get_rooms_by_accommodation(db: Session, accommodation_id: str, skip: int = 0, limit: int = 100) -> List[Room]:
    return db.query(Room).filter(Room.accommodation_id == accommodation_id).offset(skip).limit(limit).all()

def create_room(db: Session, accommodation_id: str, room: RoomCreate) -> Room:
    db_room = Room(
        accommodation_id=accommodation_id,
        type=room.type,
        price=room.price,
        capacity=room.capacity,
        description=room.description
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room(db: Session, room_id: str, room: RoomCreate) -> Optional[Room]:
    db_room = get_room(db, room_id)
    if db_room:
        for var, value in vars(room).items():
            setattr(db_room, var, value)
        db.commit()
        db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: str) -> bool:
    db_room = get_room(db, room_id)
    if db_room:
        db.delete(db_room)
        db.commit()
        return True
    return False

# Culinary CRUD
def get_culinary(db: Session, culinary_id: str) -> Optional[Culinary]:
    return db.query(Culinary).filter(Culinary.id == culinary_id).first()

def get_culinaries(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Culinary]:
    query = db.query(Culinary)
    if search:
        query = query.filter(
            or_(
                Culinary.title.ilike(f"%{search}%"),
                Culinary.description.ilike(f"%{search}%"),
                Culinary.location.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_culinary(db: Session, culinary: CulinaryCreate) -> Culinary:
    db_culinary = Culinary(
        id=culinary.id,
        title=culinary.title,
        description=culinary.description,
        full_description=culinary.full_description,
        image_url=culinary.image_url,
        category=culinary.category,
        price=culinary.price,
        location=culinary.location,
        open_hours=culinary.open_hours,
        contact=culinary.contact
    )
    
    # Handle specialties
    if culinary.specialties:
        for specialty in culinary.specialties:
            db_specialty = CulinarySpecialty(name=specialty.name)
            db_culinary.specialties.append(db_specialty)
    
    # Handle gallery
    if culinary.gallery:
        for image in culinary.gallery:
            db_gallery = CulinaryGallery(image_url=image.image_url)
            db_culinary.gallery.append(db_gallery)
    
    db.add(db_culinary)
    db.commit()
    db.refresh(db_culinary)
    return db_culinary

def update_culinary(db: Session, culinary_id: str, culinary: CulinaryUpdate) -> Optional[Culinary]:
    db_culinary = get_culinary(db, culinary_id)
    if db_culinary:
        for var, value in vars(culinary).items():
            if value is not None:
                setattr(db_culinary, var, value)
        db.commit()
        db.refresh(db_culinary)
    return db_culinary

def delete_culinary(db: Session, culinary_id: str) -> bool:
    db_culinary = get_culinary(db, culinary_id)
    if db_culinary:
        db.delete(db_culinary)
        db.commit()
        return True
    return False

# Review CRUD
def get_review(db: Session, review_id: str) -> Optional[Review]:
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 100, destination: str = None) -> List[Review]:
    query = db.query(Review)
    if destination:
        query = query.filter(Review.destination == destination)
    return query.offset(skip).limit(limit).all()

def create_review(db: Session, review: ReviewCreate) -> Review:
    db_review = Review(
        id=review.id,
        name=review.name,
        image_url=review.image_url,
        date=review.date,
        rating=review.rating,
        text=review.text,
        destination=review.destination
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: str, review: ReviewUpdate) -> Optional[Review]:
    db_review = get_review(db, review_id)
    if db_review:
        for var, value in vars(review).items():
            if value is not None:
                setattr(db_review, var, value)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: str) -> bool:
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    return False

# PhotoSpot CRUD
def get_photo_spot(db: Session, photo_spot_id: str) -> Optional[PhotoSpot]:
    return db.query(PhotoSpot).filter(PhotoSpot.id == photo_spot_id).first()

def get_photo_spots(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[PhotoSpot]:
    query = db.query(PhotoSpot)
    if search:
        query = query.filter(
            or_(
                PhotoSpot.title.ilike(f"%{search}%"),
                PhotoSpot.description.ilike(f"%{search}%"),
                PhotoSpot.location.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_photo_spot(db: Session, photo_spot: PhotoSpotCreate) -> PhotoSpot:
    db_photo_spot = PhotoSpot(
        id=photo_spot.id,
        title=photo_spot.title,
        description=photo_spot.description,
        full_description=photo_spot.full_description,
        image_url=photo_spot.image_url,
        category=photo_spot.category,
        location=photo_spot.location,
        best_time=photo_spot.best_time
    )
    
    # Handle tips
    if photo_spot.tips:
        for tip in photo_spot.tips:
            db_tip = PhotoSpotTip(tip=tip.tip)
            db_photo_spot.tips.append(db_tip)
    
    # Handle gallery
    if photo_spot.gallery:
        for image in photo_spot.gallery:
            db_gallery = PhotoSpotGallery(image_url=image.image_url)
            db_photo_spot.gallery.append(db_gallery)
    
    # Handle nearby attractions
    if photo_spot.nearby_attractions:
        for attraction in photo_spot.nearby_attractions:
            db_attraction = PhotoSpotNearbyAttraction(name=attraction.name)
            db_photo_spot.nearby_attractions.append(db_attraction)
    
    db.add(db_photo_spot)
    db.commit()
    db.refresh(db_photo_spot)
    return db_photo_spot

def update_photo_spot(db: Session, photo_spot_id: str, photo_spot: PhotoSpotUpdate) -> Optional[PhotoSpot]:
    db_photo_spot = get_photo_spot(db, photo_spot_id)
    if db_photo_spot:
        for var, value in vars(photo_spot).items():
            if value is not None:
                setattr(db_photo_spot, var, value)
        db.commit()
        db.refresh(db_photo_spot)
    return db_photo_spot

def delete_photo_spot(db: Session, photo_spot_id: str) -> bool:
    db_photo_spot = get_photo_spot(db, photo_spot_id)
    if db_photo_spot:
        db.delete(db_photo_spot)
        db.commit()
        return True
    return False

# TransportRoute CRUD
def get_transport_route(db: Session, route_id: str) -> Optional[TransportRoute]:
    return db.query(TransportRoute).filter(TransportRoute.id == route_id).first()

def get_transport_routes(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[TransportRoute]:
    query = db.query(TransportRoute)
    if search:
        query = query.filter(
            or_(
                TransportRoute.title.ilike(f"%{search}%"),
                TransportRoute.description.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_transport_route(db: Session, route: TransportRouteCreate) -> TransportRoute:
    db_route = TransportRoute(
        id=route.id,
        title=route.title,
        description=route.description,
        estimated_cost=route.estimated_cost,
        estimated_time=route.estimated_time,
        difficulty=route.difficulty,
        image_url=route.image_url
    )
    
    # Handle steps
    if route.steps:
        for step in route.steps:
            db_step = RouteStep(
                step=step.step,
                description=step.description,
                duration=step.duration,
                cost=step.cost,
                vehicle=step.vehicle
            )
            db_route.steps.append(db_step)
    
    # Handle tips
    if route.tips:
        for tip in route.tips:
            db_tip = RouteTip(tip=tip.tip)
            db_route.tips.append(db_tip)
    
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

def update_transport_route(db: Session, route_id: str, route: TransportRouteUpdate) -> Optional[TransportRoute]:
    db_route = get_transport_route(db, route_id)
    if db_route:
        for var, value in vars(route).items():
            if value is not None:
                setattr(db_route, var, value)
        db.commit()
        db.refresh(db_route)
    return db_route

def delete_transport_route(db: Session, route_id: str) -> bool:
    db_route = get_transport_route(db, route_id)
    if db_route:
        db.delete(db_route)
        db.commit()
        return True
    return False