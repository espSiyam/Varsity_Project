from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import httpx
import xml.etree.ElementTree as ET
import re

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define an endpoint to render the HTML form
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define an endpoint to process the form submission
@app.post("/calculate")
async def calculate(request: Request, intA: int = Form(...), intB: int = Form(...)):
    # Define the SOAP request XML
    soap_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soap:Body>
            <tem:Multiply>
                <tem:intA>{intA}</tem:intA>
                <tem:intB>{intB}</tem:intB>
            </tem:Multiply>
        </soap:Body>
    </soap:Envelope>
    """
    
    async with httpx.AsyncClient() as client:
        # Make a POST request to the SOAP service endpoint
        response = await client.post(
            "http://www.dneonline.com/calculator.asmx",
            data=soap_request,
            headers={"Content-Type": "text/xml; charset=utf-8"},
        )
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract and return the result from the SOAP response
        soap_response = response.text
    else:
        # Handle errors here
        soap_response = "SOAP request failed"
    print(soap_response)

    # Remove the XML declaration
    cleaned_xml = re.sub(r'<\?xml.*\?>', '', soap_response)

    # Remove namespaces from elements
    cleaned_xml = re.sub(r'xmlns="[^"]+"', '', cleaned_xml)

    # Parse the cleaned XML
    root = ET.fromstring(cleaned_xml)

    # Find the MultiplyResult element and get its text content
    multiply_result_element = root.find(".//MultiplyResult")
    if multiply_result_element is not None:
        multiply_result_text = multiply_result_element.text
        print("Value extracted from <MultiplyResult>:", multiply_result_text)
    else:
        print("MultiplyResult element not found in the XML")

    return templates.TemplateResponse("result.html", {"request": request, "soap_response": multiply_result_text})