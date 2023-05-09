from pydantic import BaseModel

# Define the Address model
class AddressModel(BaseModel):
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float
    
class GetAddressModel(BaseModel):
    latitude: float
    longitude: float
    distance_km: float