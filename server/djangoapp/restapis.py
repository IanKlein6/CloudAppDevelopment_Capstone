import requests
import json
import logging
from .models import CarDealer, CarMake, CarModel, DealerReview
from requests.auth import HTTPBasicAuth

def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    print("1 RESULTS TEST", results)
    if state:
        json_result = get_request(url, state=state)
        print("1.1")
    else:
        json_result = get_request(url)
    print("JSON RETURLS", json_result)
    
    if json_result:
        print("1.2")
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                       short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    if json_result:
        dealers = json_result
        dealer_doc = dealers[0] 
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                       short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj 

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Something went wrong")
    return response

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    print("2 RESULTS", results)
    if id:
        json_result = get_request(url, id=id)
        print("2.1")
    else:
        json_result = get_request(url)

    if json_result:
        print("2.3",json_result)
        data = json_result.get("data")
        print("2.4",data)
        if data:
            reviews = data.get("docs", [])
        else:
            reviews = []

        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            results.append(review_obj)

    return results

def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
