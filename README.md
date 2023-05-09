# Address Book CRUD Operations
This repository contains the code for Address CRUD(Create, Read, Update and Delete) operation using FastAPI with SQLite.

## Getting Started

Project details:
```
    Python version used : 3.8.10
    Database used: SQLite
    Framework used: FastAPI

```

###  Steps to setup:
  Setup the following environment in local to run the code
 
  ```
    Create a new virtual environment and install the requirments.txt file
    
    commands:
    - create a virtual environment 
      python3 -m venv venv
    
    - activate the environment
      source venv/bin/activate
    
    - install the requirements (project dependent libraries)
      pip install -r requirements.txt
      
    - run the project server
      uvicorn main:app --reload
      
    - create "address" db by running "script_create_db.py" script
      python script_create_db.py
  ```
  
Now you are ready to go !! You can check the docs (http://127.0.0.1:8000/docs) and redoc (http://127.0.0.1:8000/redoc) for more details and running APIs.

