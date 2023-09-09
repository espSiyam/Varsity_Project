from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from xml.etree import ElementTree as ET
import httpx

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Custom Jinja2 filters
def parse_xml(value):
    return ET.fromstring(value)

def extract_result(xml_element):
    result_element = xml_element.find(".//AddResult")
    if result_element is not None:
        return result_element.text
    else:
        return "Result not found in SOAP response"

templates.env.filters["parse_xml"] = parse_xml
templates.env.filters["extract_result"] = extract_result

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
        # Extract and return the SOAP response as is
        soap_response = response.text
    else:
        # Handle errors here
        soap_response = "SOAP request failed"

    return templates.TemplateResponse("result.html", {"request": request, "soap_response": soap_response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
