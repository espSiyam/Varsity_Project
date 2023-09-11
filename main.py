# Importing the libraries
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import httpx
import xml.etree.ElementTree as ET
import re

# Basic FastAPI app and Jinja Template setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Endpoint to render the input form
# @app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to make SOAP request and render the response
@app.post("/calculate")
async def calculate(request: Request, intA: int = Form(...), intB: int = Form(...)):

    soap_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soap:Body>
            <tem:Multiply>
                <tem:intA>{intA}</tem:intA> # First input for the multiplication
                <tem:intB>{intB}</tem:intB> # Second input for the multiplication
            </tem:Multiply>
        </soap:Body>
    </soap:Envelope>
    """
    
    async with httpx.AsyncClient() as client: # To make the request to the SOAP web service.
        response = await client.post(
            "http://www.dneonline.com/calculator.asmx",
            data=soap_request,
            headers={"Content-Type": "text/xml; charset=utf-8"},
        )
    
    # Handling the response from the SOAP web service
    if response.status_code == 200:
        soap_response = response.text
    else:
        soap_response = "SOAP request failed"

    # Filtering the response xml to get the result
    cleaned_xml = re.sub(r'<\?xml.*\?>', '', soap_response)
    cleaned_xml = re.sub(r'xmlns="[^"]+"', '', cleaned_xml)
    root = ET.fromstring(cleaned_xml)
    multiply_result_element = root.find(".//MultiplyResult")
    multiply_result_text = multiply_result_element.text

    # Rendering the response template with the result
    return templates.TemplateResponse("result.html", {"request": request, "soap_response": multiply_result_text})