from typing import List, Optional, Any

from beanie import Document
from pydantic import BaseModel
from .admin import User


class Lead(Document):
    """A lead represent the actual ECG info.
    """
    name: str
    sample_count: Optional[int]
    signal: List[float]


class ExecutionData(Document):
    """ExecutionData contains the ECG info from different samples.
    """
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
                        "signal": [3.45, -4.3]
                    },
                    {
                        "name": "I",
                        "signal": [3.45, -4.3, 1.2, 3.4, 0.5, -1.7]
                    }
                ]
            }
        }


class ExecutionStatus(Document):
    """ExecutionStatus containes the information from the
    executed to be calcullated or calcullated.
    """
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
