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
    # NOTE: specs say max length should be 100 but this is more than the allowed length in response.
    EmailID: str = Field(title="ID of the email", max_length=10, examples=["Japan GDP"], min_length=1)
    TitleDescription: str = Field(
        title="Email body",
        max_length=1000,
        examples=[
            "Economic growth in Japan slows down as the country experiences a drop in domestic and corporate spending"
        ])

class EmailClassResponse(BaseModel):
    EmailID: str = Field(title="ID of the email",
                         max_length=10,
                         examples=["Japan GDP"],
                         min_length=1)
    ReturnCode: int = Field(ge=0, le=1)#  0/1
    EmailClass: int
    EmailClassDescrip: str = Field(
        title="Human readable name of classification.",
        max_length=10,
        examples=["Business", "Sports"],
        min_length=1)
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
