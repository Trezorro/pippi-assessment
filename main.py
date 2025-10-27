from typing import Union
import logging

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)
LOG.info("API is starting up")

app = FastAPI()


EMAIL_CLASS_DESCRIPTIONS = {
    1: "World",
    2: "Sports",
    3: "Business",
    4: "Sci-Tech",
}

class EmailRequest(BaseModel):
    EmailID: str # Japan GDP
    TitleDescription: str # Economic growth in Japan slows down as the country experiences a drop in domestic and corporate spending

class EmailClassResponse(BaseModel):
    EmailID: str
    ReturnCode: int  #  0/1
    EmailClass: int
    EmailClassDescrip: str
    ErrorMessage: str | None


@app.get("/")
def read_root():
    return {"Instruction": "Please use this endpoint via POST request with an EmailID and TitleDescription in the request body. Or go to /docs"}


@app.post("/", operation_id="EmailClassifier")
def GetEmailClassRequest(email_request: EmailRequest):
    label = get_classification(email_request.TitleDescription)
    return EmailClassResponse(
        EmailID=email_request.EmailID,
        ReturnCode=0,
        EmailClass=label,
        EmailClassDescrip=EMAIL_CLASS_DESCRIPTIONS[label],
        ErrorMessage=None)


def get_classification(email: str):
    """Placeholder function for when we have the model."""
    LOG.info("Email first char number is %d", ord(email[0]))
    return (ord(email[0]) % 4) + 1
