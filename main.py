from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define an endpoint to render the HTML form
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define an endpoint to process the form submission
@app.post("/calculate")
async def calculate(request: Request, intA: int, intB: int):
    # Define the SOAP request XML
    soap_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soap:Body>
            <tem:Add>
                <tem:intA>{intA}</tem:intA>
                <tem:intB>{intB}</tem:intB>
            </tem:Add>
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

    return templates.TemplateResponse("result.html", {"request": request, "soap_response": soap_response})
