from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Base schemas
class FacilityBase(BaseModel):
    name: str

class ActivityBase(BaseModel):
    name: str

# Accommodation related schemas
class RoomBase(BaseModel):
    type: str
    price: str
    capacity: str
    description: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: str
    
    class Config:
        from_attributes = True

class AccommodationGalleryBase(BaseModel):
    image_url: str

class AccommodationGalleryCreate(AccommodationGalleryBase):
    pass

class AccommodationGallery(AccommodationGalleryBase):
    id: int
    
    class Config:
        from_attributes = True

class AccommodationBase(BaseModel):
    title: str
    description: str
    full_description: str
    image_url: str
    category: str
    price: str
    location: str
    contact: str

class AccommodationCreate(AccommodationBase):
    website: Optional[str] = None
    facilities: List[str] = []
    rooms: List[RoomCreate] = []
    gallery: List[AccommodationGalleryCreate] = []

class Accommodation(AccommodationBase):
    id: str
    website: Optional[str] = None
    facilities: List[FacilityBase] = []
    rooms: List[Room] = []
    gallery: List[AccommodationGallery] = []
    
    class Config:
        from_attributes = True

# Culinary related schemas
class CulinarySpecialtyBase(BaseModel):
    name: str

class CulinarySpecialtyCreate(CulinarySpecialtyBase):
    pass

class CulinarySpecialty(CulinarySpecialtyBase):
    id: int
    
    class Config:
        from_attributes = True

class CulinaryGalleryBase(BaseModel):
    image_url: str

class CulinaryGalleryCreate(CulinaryGalleryBase):
    pass

class CulinaryGallery(CulinaryGalleryBase):
    id: int
    
    class Config:
        from_attributes = True

class CulinaryBase(BaseModel):
    title: str
    description: str
    full_description: str
    image_url: str
    category: str
    price: str
    location: str
    open_hours: str

class CulinaryCreate(CulinaryBase):
    contact: Optional[str] = None
    specialties: List[CulinarySpecialtyCreate] = []
    gallery: List[CulinaryGalleryCreate] = []

class Culinary(CulinaryBase):
    id: str
    contact: Optional[str] = None
    specialties: List[CulinarySpecialty] = []
    gallery: List[CulinaryGallery] = []
    
    class Config:
        from_attributes = True

# Destination related schemas
class DestinationTipBase(BaseModel):
    tip: str

class DestinationTipCreate(DestinationTipBase):
    pass

class DestinationTip(DestinationTipBase):
    id: int
    
    class Config:
        from_attributes = True

class DestinationGalleryBase(BaseModel):
    image_url: str

class DestinationGalleryCreate(DestinationGalleryBase):
    pass

class DestinationGallery(DestinationGalleryBase):
    id: int
    
    class Config:
        from_attributes = True

class DestinationBase(BaseModel):
    title: str
    description: str
    full_description: str
    image_url: str
    category: str
    price: str
    location: str
    open_hours: str

class DestinationCreate(DestinationBase):
    facilities: List[str] = []
    activities: List[str] = []
    tips: List[DestinationTipCreate] = []
    gallery: List[DestinationGalleryCreate] = []

class Destination(DestinationBase):
    id: str
    facilities: List[FacilityBase] = []
    activities: List[ActivityBase] = []
    tips: List[DestinationTip] = []
    gallery: List[DestinationGallery] = []
    
    class Config:
        from_attributes = True

# PhotoSpot related schemas
class PhotoSpotTipBase(BaseModel):
    tip: str

class PhotoSpotTipCreate(PhotoSpotTipBase):
    pass

class PhotoSpotTip(PhotoSpotTipBase):
    id: int
    
    class Config:
        from_attributes = True

class PhotoSpotGalleryBase(BaseModel):
    image_url: str

class PhotoSpotGalleryCreate(PhotoSpotGalleryBase):
    pass

class PhotoSpotGallery(PhotoSpotGalleryBase):
    id: int
    
    class Config:
        from_attributes = True

class PhotoSpotNearbyAttractionBase(BaseModel):
    name: str

class PhotoSpotNearbyAttractionCreate(PhotoSpotNearbyAttractionBase):
    pass

class PhotoSpotNearbyAttraction(PhotoSpotNearbyAttractionBase):
    id: int
    
    class Config:
        from_attributes = True

class PhotoSpotBase(BaseModel):
    title: str
    description: str
    full_description: str
    image_url: str
    category: str
    location: str
    best_time: str

class PhotoSpotCreate(PhotoSpotBase):
    tips: List[PhotoSpotTipCreate] = []
    gallery: List[PhotoSpotGalleryCreate] = []
    nearby_attractions: List[PhotoSpotNearbyAttractionCreate] = []

class PhotoSpot(PhotoSpotBase):
    id: str
    tips: List[PhotoSpotTip] = []
    gallery: List[PhotoSpotGallery] = []
    nearby_attractions: List[PhotoSpotNearbyAttraction] = []
    
    class Config:
        from_attributes = True

# Review related schemas
class ReviewBase(BaseModel):
    name: str
    image_url: str
    date: str
    rating: int
    text: str
    destination: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: str
    
    class Config:
        from_attributes = True

# TransportRoute related schemas
class RouteStepBase(BaseModel):
    step: int
    description: str
    duration: str
    cost: str
    vehicle: str

class RouteStepCreate(RouteStepBase):
    pass

class RouteStep(RouteStepBase):
    id: int
    
    class Config:
        from_attributes = True

class RouteTipBase(BaseModel):
    tip: str

class RouteTipCreate(RouteTipBase):
    pass

class RouteTip(RouteTipBase):
    id: int
    
    class Config:
        from_attributes = True

class TransportRouteBase(BaseModel):
    title: str
    description: str
    estimated_cost: str
    estimated_time: str
    difficulty: str
    image_url: str

class TransportRouteCreate(TransportRouteBase):
    steps: List[RouteStepCreate] = []
    tips: List[RouteTipCreate] = []

class TransportRoute(TransportRouteBase):
    id: str
    steps: List[RouteStep] = []
    tips: List[RouteTip] = []
    
    class Config:
        from_attributes = True

# Update schemas
class DestinationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    location: Optional[str] = None
    open_hours: Optional[str] = None
    facilities: Optional[List[str]] = None
    activities: Optional[List[str]] = None
    tips: Optional[List[DestinationTipCreate]] = None
    gallery: Optional[List[DestinationGalleryCreate]] = None

class AccommodationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    location: Optional[str] = None
    contact: Optional[str] = None
    website: Optional[str] = None
    facilities: Optional[List[str]] = None
    rooms: Optional[List[RoomCreate]] = None
    gallery: Optional[List[AccommodationGalleryCreate]] = None

class RoomUpdate(BaseModel):
    type: Optional[str] = None
    price: Optional[str] = None
    capacity: Optional[str] = None
    description: Optional[str] = None

class CulinaryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    location: Optional[str] = None
    open_hours: Optional[str] = None
    contact: Optional[str] = None
    specialties: Optional[List[CulinarySpecialtyCreate]] = None
    gallery: Optional[List[CulinaryGalleryCreate]] = None

class CulinarySpecialtyUpdate(BaseModel):
    name: Optional[str] = None

class ReviewUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    date: Optional[str] = None
    rating: Optional[int] = None
    text: Optional[str] = None
    destination: Optional[str] = None

class PhotoSpotUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    best_time: Optional[str] = None
    tips: Optional[List[PhotoSpotTipCreate]] = None
    gallery: Optional[List[PhotoSpotGalleryCreate]] = None
    nearby_attractions: Optional[List[PhotoSpotNearbyAttractionCreate]] = None

class TransportRouteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    estimated_cost: Optional[str] = None
    estimated_time: Optional[str] = None
    difficulty: Optional[str] = None
    image_url: Optional[str] = None
    steps: Optional[List[RouteStepCreate]] = None
    tips: Optional[List[RouteTipCreate]] = None

class RouteStepUpdate(BaseModel):
    step: Optional[int] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    cost: Optional[str] = None
    vehicle: Optional[str] = None

class RouteTipUpdate(BaseModel):
    tip: Optional[str] = None