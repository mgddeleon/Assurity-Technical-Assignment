import requests
import pytest

url = "https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?catalogue=false"
response = requests.get(url)

def test_api_response():
    #Verify Status code is 200
    assert response.status_code == 200, f"❌ Expected status code 200, got {response.status_code}"

    #Check for valid JSON
    try:
        data = response.json()
    except ValueError:
        pytest.fail("❌ Response is not valid JSON.")

    #Check 'Name' field value
    assert "Name" in data, "❌ 'Name' field is missing."
    assert data["Name"] == "Carbon credits", f"❌ 'Name' is '{data['Name']}', expected 'Carbon credits'."

    #Check 'CanRelist' field value
    assert "CanRelist" in data, "❌ 'CanRelist' field is missing."
    assert data["CanRelist"] is True, f"❌ 'CanRelist' is {data['CanRelist']}, expected True."

    #Check for 'Promotions' element with Name = 'Gallery'
    promotions = data.get("Promotions", [])
    assert isinstance(promotions, list), "❌ 'Promotions' should be a list."

    gallery_promo = next((promo for promo in promotions if promo.get("Name") == "Gallery"), None)
    assert gallery_promo is not None, "❌ No promotion with Name = 'Gallery' found."

    description = gallery_promo.get("Description", "")
    assert "Good position in category" in description, (
        f"❌ 'Gallery' promotion description does not contain 'Good position in category'. "
        f"Actual: '{description}'"
    )