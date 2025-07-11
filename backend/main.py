from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import get_db, create_tables
from models import (
    Destination, DestinationTip, DestinationGallery, Facility, destination_facility,
    Activity, destination_activity, PhotoSpot, PhotoSpotTip, PhotoSpotGallery, 
    PhotoSpotNearbyAttraction, Review, TransportRoute, RouteStep, RouteTip,
    Accommodation, Room, AccommodationGallery, accommodation_facility,
    Culinary, CulinarySpecialty, CulinaryGallery
)
import schemas
import crud

app = FastAPI(title="Temajuk Tourism API", 
              description="API for Temajuk Tourism Information System")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
@app.on_event("startup")
def on_startup():
    create_tables()

# Health check endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Temajuk Tourism API"}

# --------------------------
# DESTINATION ENDPOINTS
# --------------------------
@app.post("/destinations/", response_model=schemas.Destination, status_code=status.HTTP_201_CREATED, tags=["Destinations"])
def create_destination(destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
    return crud.create_destination(db=db, destination=destination)

@app.get("/destinations/", response_model=List[schemas.Destination], tags=["Destinations"])
def read_destinations(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    destinations = crud.get_destinations(db, skip=skip, limit=limit, search=search)
    if category:
        destinations = [d for d in destinations if d.category == category]
    return destinations

@app.get("/destinations/{destination_id}", response_model=schemas.Destination, tags=["Destinations"])
def read_destination(destination_id: str, db: Session = Depends(get_db)):
    db_destination = crud.get_destination(db, destination_id=destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return db_destination

@app.put("/destinations/{destination_id}", response_model=schemas.Destination, tags=["Destinations"])
def update_destination(
    destination_id: str, 
    destination: schemas.DestinationUpdate, 
    db: Session = Depends(get_db)
):
    db_destination = crud.update_destination(db, destination_id=destination_id, destination=destination)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return db_destination

@app.delete("/destinations/{destination_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Destinations"])
def delete_destination(destination_id: str, db: Session = Depends(get_db)):
    success = crud.delete_destination(db, destination_id=destination_id)
    if not success:
        raise HTTPException(status_code=404, detail="Destination not found")
    return None

# --------------------------
# ACCOMMODATION ENDPOINTS
# --------------------------
@app.post("/accommodations/", response_model=schemas.Accommodation, status_code=status.HTTP_201_CREATED, tags=["Accommodations"])
def create_accommodation(accommodation: schemas.AccommodationCreate, db: Session = Depends(get_db)):
    return crud.create_accommodation(db=db, accommodation=accommodation)

@app.get("/accommodations/", response_model=List[schemas.Accommodation], tags=["Accommodations"])
def read_accommodations(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    accommodations = crud.get_accommodations(db, skip=skip, limit=limit, search=search)
    if category:
        accommodations = [a for a in accommodations if a.category == category]
    return accommodations

@app.get("/accommodations/{accommodation_id}", response_model=schemas.Accommodation, tags=["Accommodations"])
def read_accommodation(accommodation_id: str, db: Session = Depends(get_db)):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation

@app.put("/accommodations/{accommodation_id}", response_model=schemas.Accommodation, tags=["Accommodations"])
def update_accommodation(
    accommodation_id: str, 
    accommodation: schemas.AccommodationUpdate, 
    db: Session = Depends(get_db)
):
    db_accommodation = crud.update_accommodation(db, accommodation_id=accommodation_id, accommodation=accommodation)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation

@app.delete("/accommodations/{accommodation_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Accommodations"])
def delete_accommodation(accommodation_id: str, db: Session = Depends(get_db)):
    success = crud.delete_accommodation(db, accommodation_id=accommodation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return None

# Room endpoints
@app.post("/accommodations/{accommodation_id}/rooms/", response_model=schemas.Room, status_code=status.HTTP_201_CREATED, tags=["Accommodations"])
def create_room_for_accommodation(
    accommodation_id: str, 
    room: schemas.RoomCreate, 
    db: Session = Depends(get_db)
):
    return crud.create_room(db=db, accommodation_id=accommodation_id, room=room)

@app.get("/accommodations/{accommodation_id}/rooms/", response_model=List[schemas.Room], tags=["Accommodations"])
def read_rooms_for_accommodation(accommodation_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_rooms_by_accommodation(db, accommodation_id=accommodation_id, skip=skip, limit=limit)

# --------------------------
# CULINARY ENDPOINTS
# --------------------------
@app.post("/culinaries/", response_model=schemas.Culinary, status_code=status.HTTP_201_CREATED, tags=["Culinaries"])
def create_culinary(culinary: schemas.CulinaryCreate, db: Session = Depends(get_db)):
    return crud.create_culinary(db=db, culinary=culinary)

@app.get("/culinaries/", response_model=List[schemas.Culinary], tags=["Culinaries"])
def read_culinaries(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    culinaries = crud.get_culinaries(db, skip=skip, limit=limit, search=search)
    if category:
        culinaries = [c for c in culinaries if c.category == category]
    return culinaries

@app.get("/culinaries/{culinary_id}", response_model=schemas.Culinary, tags=["Culinaries"])
def read_culinary(culinary_id: str, db: Session = Depends(get_db)):
    db_culinary = crud.get_culinary(db, culinary_id=culinary_id)
    if db_culinary is None:
        raise HTTPException(status_code=404, detail="Culinary not found")
    return db_culinary

@app.put("/culinaries/{culinary_id}", response_model=schemas.Culinary, tags=["Culinaries"])
def update_culinary(
    culinary_id: str, 
    culinary: schemas.CulinaryUpdate, 
    db: Session = Depends(get_db)
):
    db_culinary = crud.update_culinary(db, culinary_id=culinary_id, culinary=culinary)
    if db_culinary is None:
        raise HTTPException(status_code=404, detail="Culinary not found")
    return db_culinary

@app.delete("/culinaries/{culinary_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Culinaries"])
def delete_culinary(culinary_id: str, db: Session = Depends(get_db)):
    success = crud.delete_culinary(db, culinary_id=culinary_id)
    if not success:
        raise HTTPException(status_code=404, detail="Culinary not found")
    return None

# --------------------------
# REVIEW ENDPOINTS
# --------------------------
@app.post("/reviews/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED, tags=["Reviews"])
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)

@app.get("/reviews/", response_model=List[schemas.Review], tags=["Reviews"])
def read_reviews(
    skip: int = 0, 
    limit: int = 100,
    destination: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_reviews(db, skip=skip, limit=limit, destination=destination)

@app.get("/reviews/{review_id}", response_model=schemas.Review, tags=["Reviews"])
def read_review(review_id: str, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.put("/reviews/{review_id}", response_model=schemas.Review, tags=["Reviews"])
def update_review(
    review_id: str, 
    review: schemas.ReviewUpdate, 
    db: Session = Depends(get_db)
):
    db_review = crud.update_review(db, review_id=review_id, review=review)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Reviews"])
def delete_review(review_id: str, db: Session = Depends(get_db)):
    success = crud.delete_review(db, review_id=review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return None

# --------------------------
# PHOTO SPOT ENDPOINTS
# --------------------------
@app.post("/photo-spots/", response_model=schemas.PhotoSpot, status_code=status.HTTP_201_CREATED, tags=["Photo Spots"])
def create_photo_spot(photo_spot: schemas.PhotoSpotCreate, db: Session = Depends(get_db)):
    return crud.create_photo_spot(db=db, photo_spot=photo_spot)

@app.get("/photo-spots/", response_model=List[schemas.PhotoSpot], tags=["Photo Spots"])
def read_photo_spots(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    photo_spots = crud.get_photo_spots(db, skip=skip, limit=limit, search=search)
    if category:
        photo_spots = [p for p in photo_spots if p.category == category]
    return photo_spots

@app.get("/photo-spots/{photo_spot_id}", response_model=schemas.PhotoSpot, tags=["Photo Spots"])
def read_photo_spot(photo_spot_id: str, db: Session = Depends(get_db)):
    db_photo_spot = crud.get_photo_spot(db, photo_spot_id=photo_spot_id)
    if db_photo_spot is None:
        raise HTTPException(status_code=404, detail="Photo spot not found")
    return db_photo_spot

@app.put("/photo-spots/{photo_spot_id}", response_model=schemas.PhotoSpot, tags=["Photo Spots"])
def update_photo_spot(
    photo_spot_id: str, 
    photo_spot: schemas.PhotoSpotUpdate, 
    db: Session = Depends(get_db)
):
    db_photo_spot = crud.update_photo_spot(db, photo_spot_id=photo_spot_id, photo_spot=photo_spot)
    if db_photo_spot is None:
        raise HTTPException(status_code=404, detail="Photo spot not found")
    return db_photo_spot

@app.delete("/photo-spots/{photo_spot_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Photo Spots"])
def delete_photo_spot(photo_spot_id: str, db: Session = Depends(get_db)):
    success = crud.delete_photo_spot(db, photo_spot_id=photo_spot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photo spot not found")
    return None

# --------------------------
# TRANSPORT ROUTE ENDPOINTS
# --------------------------
@app.post("/transport-routes/", response_model=schemas.TransportRoute, status_code=status.HTTP_201_CREATED, tags=["Transport Routes"])
def create_transport_route(route: schemas.TransportRouteCreate, db: Session = Depends(get_db)):
    return crud.create_transport_route(db=db, route=route)

@app.get("/transport-routes/", response_model=List[schemas.TransportRoute], tags=["Transport Routes"])
def read_transport_routes(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    routes = crud.get_transport_routes(db, skip=skip, limit=limit, search=search)
    if difficulty:
        routes = [r for r in routes if r.difficulty == difficulty]
    return routes

@app.get("/transport-routes/{route_id}", response_model=schemas.TransportRoute, tags=["Transport Routes"])
def read_transport_route(route_id: str, db: Session = Depends(get_db)):
    db_route = crud.get_transport_route(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Transport route not found")
    return db_route

@app.put("/transport-routes/{route_id}", response_model=schemas.TransportRoute, tags=["Transport Routes"])
def update_transport_route(
    route_id: str, 
    route: schemas.TransportRouteUpdate, 
    db: Session = Depends(get_db)
):
    db_route = crud.update_transport_route(db, route_id=route_id, route=route)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Transport route not found")
    return db_route

@app.delete("/transport-routes/{route_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Transport Routes"])
def delete_transport_route(route_id: str, db: Session = Depends(get_db)):
    success = crud.delete_transport_route(db, route_id=route_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transport route not found")
    return None

# --------------------------
# FACILITY & ACTIVITY ENDPOINTS (for admin)
# --------------------------
@app.get("/facilities/", response_model=List[schemas.FacilityBase], tags=["Admin"])
def read_facilities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Facility).offset(skip).limit(limit).all()

@app.get("/activities/", response_model=List[schemas.ActivityBase], tags=["Admin"])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Activity).offset(skip).limit(limit).all()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)