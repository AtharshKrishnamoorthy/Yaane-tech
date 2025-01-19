from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import json
from main import process_crime_info
import uvicorn

app = FastAPI()

# Base Models

class CrimeQuery(BaseModel):
    query : str
    
class CrimeResponse(BaseModel):
    response : str
    

# Creating endpoints

@app.post("/process-crime",response_model=CrimeResponse)
def crime_endpoint(crime_query:CrimeQuery):
    try:
        response = process_crime_info(crime_query.query)
        response_str = response.raw
        return CrimeResponse(response=response_str)
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    
# Add a health check endpoint
@app.get("/")
def read_root():
    return {"status": "healthy", "message": "API is running"}
        

if __name__ == "__main__":
    uvicorn.run(app,port=3000)
    