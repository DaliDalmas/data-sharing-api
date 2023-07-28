from fastapi import FastAPI, Query, Depends, HTTPException, Header
from typing import Optional
from fastapi.responses import Response

app = FastAPI()

# Sample data (you can replace this with your actual data source)
sample_data = [
    {"id": 1, "name": "Item 1", "price": 10},
    {"id": 2, "name": "Item 2", "price": 15},
    {"id": 3, "name": "Item 3", "price": 20},
]

def get_data_as_csv(data):
    csv_content = "id,name,price\n"
    for item in data:
        csv_content += f"{item['id']},{item['name']},{item['price']}\n"
    return csv_content

# Predefined list of valid API keys
VALID_API_KEYS = ["your_api_key_1", "your_api_key_2"]

def validate_api_key(api_key: Optional[str] = Header(None)):
    print(api_key)
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.get("/data/")
async def get_data(item: str = Query(..., description="The item for which data is requested."),
                   quantity: int = Query(1, gt=0, description="The quantity of data to retrieve."),
                   show_info: bool = Query(False, description="Flag to show additional info."),
                   response_format: str = Query("json", regex="^(json|csv)$", description="Response format: json or csv."),
                   api_key: str = Depends(validate_api_key)
                   ):
    """
    An endpoint that accepts query parameters in the URL and returns data in either JSON or CSV format with API key authentication.
    :param item: The item for which data is requested.
    :param quantity: The quantity of data to retrieve (optional, default is 1).
    :param show_info: A flag to determine whether to show additional info (optional, default is False).
    :param response_format: Response format: json or csv (optional, default is json).
    :param api_key: The API key provided by the client for authentication.
    :return: Data in JSON or CSV format based on the query parameter.
    """
    data = sample_data[:quantity]

    if show_info:
        for item_data in data:
            item_data["info"] = f"Additional information about {item_data['name']}."

    if response_format == "csv":
        csv_content = get_data_as_csv(data)
        return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=data.csv"})
    else:
        return data