from pydantic import BaseModel

class PassengerInfo(BaseModel):
    name: str
    age: int
    gender: str
    train_id: str
    travel_date: str
