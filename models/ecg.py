from typing import List, Optional, Any

from beanie import Document
from pydantic import BaseModel
from .admin import User


class Lead(Document):
    name: str
    sample_count: Optional[int]
    signal: List[float]
    

class ExecutionData(Document):
    date: str
    leads: List[Lead]
    
    class Config:
        schema_extra = {
            "example": {
                "date": "2022/07/12",
                "leads": [
                    {
                        "name": "I",
                        "sample_count": 2,
                        "signal": [ 3.45, -4.3]
                    },
                    {
                        "name": "I",
                        "signal": [ 3.45, -4.3, 1.2, 3.4, 0.5, -1.7]
                    }
                ]
            }
        }


class ExecutionStatus(Document):
    status: str = "QUEUED"
    result: Optional[Any]
    user: User
        

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]
    execution_id: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }