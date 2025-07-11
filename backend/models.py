from sqlalchemy import Column, Integer, String, Table, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Define common string lengths for consistency
TITLE_LENGTH = 100
DESCRIPTION_LENGTH = 500
LONG_DESCRIPTION_LENGTH = 2000
URL_LENGTH = 255
LOCATION_LENGTH = 255
CATEGORY_LENGTH = 50
PRICE_LENGTH = 50
TIME_LENGTH = 50
CONTACT_LENGTH = 20
NAME_LENGTH = 255
TIP_LENGTH = 500

# Association tables (unchanged)
accommodation_facility = Table(
    'accommodation_facility',
    Base.metadata,
    Column('accommodation_id', String(50), ForeignKey('accommodations.id')),
    Column('facility_id', Integer, ForeignKey('facilities.id'))
)

destination_facility = Table(
    'destination_facility',
    Base.metadata,
    Column('destination_id', String(50), ForeignKey('destinations.id')),
    Column('facility_id', Integer, ForeignKey('facilities.id'))
)

destination_activity = Table(
    'destination_activity',
    Base.metadata,
    Column('destination_id', String(50), ForeignKey('destinations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class Facility(Base):
    __tablename__ = 'facilities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(NAME_LENGTH), nullable=False)
    
    accommodations = relationship("Accommodation", secondary=accommodation_facility, back_populates="facilities")
    destinations = relationship("Destination", secondary=destination_facility, back_populates="facilities")

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(NAME_LENGTH), nullable=False)
    
    destinations = relationship("Destination", secondary=destination_activity, back_populates="activities")

class Room(Base):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_id = Column(String(50), ForeignKey('accommodations.id'))
    type = Column(String(TITLE_LENGTH), nullable=False)
    price = Column(String(PRICE_LENGTH), nullable=False)
    capacity = Column(String(20), nullable=False)
    description = Column(String(DESCRIPTION_LENGTH), nullable=False)
    
    accommodation = relationship("Accommodation", back_populates="rooms")

class AccommodationGallery(Base):
    __tablename__ = 'accommodation_galleries'
    
    id = Column(Integer, primary_key=True)
    accommodation_id = Column(String(50), ForeignKey('accommodations.id'))
    image_url = Column(String(URL_LENGTH), nullable=False)
    
    accommodation = relationship("Accommodation", back_populates="gallery")

class Accommodation(Base):
    __tablename__ = 'accommodations'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(TITLE_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_LENGTH), nullable=False)
    full_description = Column(String(LONG_DESCRIPTION_LENGTH), nullable=False)
    image_url = Column(String(URL_LENGTH), nullable=False)
    category = Column(String(CATEGORY_LENGTH), nullable=False)
    price = Column(String(PRICE_LENGTH), nullable=False)
    location = Column(String(LOCATION_LENGTH), nullable=False)
    contact = Column(String(CONTACT_LENGTH), nullable=False)
    website = Column(String(URL_LENGTH))
    
    facilities = relationship("Facility", secondary=accommodation_facility, back_populates="accommodations")
    rooms = relationship("Room", back_populates="accommodation")
    gallery = relationship("AccommodationGallery", back_populates="accommodation")

class CulinarySpecialty(Base):
    __tablename__ = 'culinary_specialties'
    
    id = Column(Integer, primary_key=True)
    culinary_id = Column(String(50), ForeignKey('culinaries.id'))
    name = Column(String(NAME_LENGTH), nullable=False)
    
    culinary = relationship("Culinary", back_populates="specialties")

class CulinaryGallery(Base):
    __tablename__ = 'culinary_galleries'
    
    id = Column(Integer, primary_key=True)
    culinary_id = Column(String(50), ForeignKey('culinaries.id'))
    image_url = Column(String(URL_LENGTH), nullable=False)
    
    culinary = relationship("Culinary", back_populates="gallery")

class Culinary(Base):
    __tablename__ = 'culinaries'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(TITLE_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_LENGTH), nullable=False)
    full_description = Column(String(LONG_DESCRIPTION_LENGTH), nullable=False)
    image_url = Column(String(URL_LENGTH), nullable=False)
    category = Column(String(CATEGORY_LENGTH), nullable=False)
    price = Column(String(PRICE_LENGTH), nullable=False)
    location = Column(String(LOCATION_LENGTH), nullable=False)
    open_hours = Column(String(TIME_LENGTH), nullable=False)
    contact = Column(String(CONTACT_LENGTH))
    
    specialties = relationship("CulinarySpecialty", back_populates="culinary")
    gallery = relationship("CulinaryGallery", back_populates="culinary")

class DestinationTip(Base):
    __tablename__ = 'destination_tips'
    
    id = Column(Integer, primary_key=True)
    destination_id = Column(String(50), ForeignKey('destinations.id'))
    tip = Column(String(TIP_LENGTH), nullable=False)
    
    destination = relationship("Destination", back_populates="tips")

class DestinationGallery(Base):
    __tablename__ = 'destination_galleries'
    
    id = Column(Integer, primary_key=True)
    destination_id = Column(String(50), ForeignKey('destinations.id'))
    image_url = Column(String(URL_LENGTH), nullable=False)
    
    destination = relationship("Destination", back_populates="gallery")

class Destination(Base):
    __tablename__ = 'destinations'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(TITLE_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_LENGTH), nullable=False)
    full_description = Column(String(LONG_DESCRIPTION_LENGTH), nullable=False)
    image_url = Column(String(URL_LENGTH), nullable=False)
    category = Column(String(CATEGORY_LENGTH), nullable=False)
    price = Column(String(PRICE_LENGTH), nullable=False)
    location = Column(String(LOCATION_LENGTH), nullable=False)
    open_hours = Column(String(TIME_LENGTH), nullable=False)
    
    facilities = relationship("Facility", secondary=destination_facility, back_populates="destinations")
    activities = relationship("Activity", secondary=destination_activity, back_populates="destinations")
    tips = relationship("DestinationTip", back_populates="destination")
    gallery = relationship("DestinationGallery", back_populates="destination")

class PhotoSpotTip(Base):
    __tablename__ = 'photo_spot_tips'
    
    id = Column(Integer, primary_key=True)
    photo_spot_id = Column(String(50), ForeignKey('photo_spots.id'))
    tip = Column(String(TIP_LENGTH), nullable=False)
    
    photo_spot = relationship("PhotoSpot", back_populates="tips")

class PhotoSpotGallery(Base):
    __tablename__ = 'photo_spot_galleries'
    
    id = Column(Integer, primary_key=True)
    photo_spot_id = Column(String(50), ForeignKey('photo_spots.id'))
    image_url = Column(String(URL_LENGTH), nullable=False)
    
    photo_spot = relationship("PhotoSpot", back_populates="gallery")

class PhotoSpotNearbyAttraction(Base):
    __tablename__ = 'photo_spot_nearby_attractions'
    
    id = Column(Integer, primary_key=True)
    photo_spot_id = Column(String(50), ForeignKey('photo_spots.id'))
    name = Column(String(NAME_LENGTH), nullable=False)
    
    photo_spot = relationship("PhotoSpot", back_populates="nearby_attractions")

class PhotoSpot(Base):
    __tablename__ = 'photo_spots'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(TITLE_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_LENGTH), nullable=False)
    full_description = Column(String(LONG_DESCRIPTION_LENGTH), nullable=False)
    image_url = Column(String(URL_LENGTH), nullable=False)
    category = Column(String(CATEGORY_LENGTH), nullable=False)
    location = Column(String(LOCATION_LENGTH), nullable=False)
    best_time = Column(String(TIME_LENGTH), nullable=False)
    
    tips = relationship("PhotoSpotTip", back_populates="photo_spot")
    gallery = relationship("PhotoSpotGallery", back_populates="photo_spot")
    nearby_attractions = relationship("PhotoSpotNearbyAttraction", back_populates="photo_spot")

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(NAME_LENGTH), nullable=False)
    image_url = Column(String(URL_LENGTH), nullable=False)
    date = Column(String(20), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(String(LONG_DESCRIPTION_LENGTH), nullable=False)
    destination = Column(String(TITLE_LENGTH), nullable=False)

class RouteStep(Base):
    __tablename__ = 'route_steps'
    
    id = Column(Integer, primary_key=True)
    route_id = Column(String(50), ForeignKey('transport_routes.id'))
    step = Column(Integer, nullable=False)
    description = Column(String(DESCRIPTION_LENGTH), nullable=False)
    duration = Column(String(20), nullable=False)
    cost = Column(String(PRICE_LENGTH), nullable=False)
    vehicle = Column(String(50), nullable=False)
    
    transport_route = relationship("TransportRoute", back_populates="steps")

class RouteTip(Base):
    __tablename__ = 'route_tips'
    
    id = Column(Integer, primary_key=True)
    route_id = Column(String(50), ForeignKey('transport_routes.id'))
    tip = Column(String(TIP_LENGTH), nullable=False)
    
    transport_route = relationship("TransportRoute", back_populates="tips")

class TransportRoute(Base):
    __tablename__ = 'transport_routes'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(TITLE_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_LENGTH), nullable=False)
    estimated_cost = Column(String(PRICE_LENGTH), nullable=False)
    estimated_time = Column(String(TIME_LENGTH), nullable=False)
    difficulty = Column(String(20), nullable=False)
    image_url = Column(String(URL_LENGTH), nullable=False)
    
    steps = relationship("RouteStep", back_populates="transport_route")
    tips = relationship("RouteTip", back_populates="transport_route")