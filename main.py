from fastapi import FastAPI, HTTPException
from math import radians, atan2, sqrt, sin , cos
import sqlite3
from models import AddressModel
from log_function import create_logger

app = FastAPI()

logger = create_logger() 

# Endpoint to create a new address
@app.post("/address")
def create_address(address: AddressModel):
    try:
        # Add the address to the database
        with sqlite3.connect("address.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO address (name, street, city, state, zip_code, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (address.name, address.street, address.city, address.state, address.zip_code, address.latitude, address.longitude))
            conn.commit()
        logger.info("Address created successfully")
        return {"s": "ok", "message": "Address created successfully", "status_code": 201}
    except Exception as e:
        logger.error(f"Error creating address | {str(e)}")
        return {"s": "error", "message": "Something went wrong creating the address", "status_code": 500}

# Endpoint to update an existing address
@app.put("/address/{address_id}")
def update_address(address_id: int, address: AddressModel):
    try:
        # Check if the address exists in the database
        with sqlite3.connect("address.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM address WHERE id=?", (address_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Address not found")
            # Update the address in the database
            cursor.execute("UPDATE address SET name = ?, street=?, city=?, state=?, zip_code=?, latitude=?, longitude=? WHERE id=?",
                        (address.name, address.street, address.city, address.state, address.zip_code, address.latitude, address.longitude, address_id))
            conn.commit()
        logger.info("Address updated successfully")
        return {"s": "ok", "message": "Address updated successfully", "status_code" : 200}
    except Exception as e:
        logger.error(f"Error updating address | {str(e)}")
        return {"s": "error", "message": "Something went wrong updating the address", "status_code" : 500}

# Endpoint to delete an existing address
@app.delete("/address/{address_id}")
def delete_address(address_id: int):
    try:
        # Check if the address exists in the database
        with sqlite3.connect("address.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM address WHERE id=?", (address_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Address details not found")
            # Delete the address from the database
            cursor.execute("DELETE FROM address WHERE id=?", (address_id,))
            conn.commit()
        logger.info("Address deleted successfully")
        return {"s": "ok", "message": "Address deleted successfully", "status_code" : 200}
    except Exception as e:
        logger.error(f"Error deleting address | {str(e)}")
        return {"s": "error", "message": "Something went wrong deleting the address", "status_code" : 500}


# Endpoint to retrieve all address in the database based on co-ordinates and distance (in kilometers)
@app.get("/fetch-address")
async def get_address(latitude: float, longitude: float, distance: float):
    try:
        # Convert distance from km to meters
        distance_m = distance * 1000

        # Query the database for address within the given distance
        with sqlite3.connect("address.db") as conn:
            cur = conn.cursor()
            # As the square function is not available on SqLite, we need to multiply the differences by themselves. No need to calculate the square roots.
            cur.execute(
                "SELECT id, name, street, city, state, zip_code, latitude, longitude FROM address WHERE "
                "((latitude - ?) * (latitude - ?) + "
                "(longitude - ?) * (longitude - ?)) < ? * ?",
                (latitude, latitude, longitude, longitude, distance_m, distance_m)
            )
            
            rows = cur.fetchall()

        # Calculate the distance between each address and the given location
        address = []
        for row in rows:
            lat2, lon2 = float(row[6]), float(row[7])
            lat1, lon1 = latitude, longitude
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance_km = 6371 * c
            if distance_km <= distance:
                address_dict = {"id": row[0], "name": row[1], "street": row[2], "city": row[3], "state": row[4], "pin code": row[5], "distance": f"{round(distance_km,2)} km"}
                address.append(address_dict)

        logger.info("Address fetched successfully")

        # Return the list of address
        if address:
            return {"s": "ok", "message": "fetching the available addresses with in the distance", "data" : address, "status_code" : 200}
        else:
            return {"s": "ok", "message": "No address found within the given distance", "status_code" : 404}

    except Exception as e:
        logger.error(f"Error fetching address | {str(e)}")
        return {"s": "error", "message": "Something went wrong fetching the address", "status_code" : 500}