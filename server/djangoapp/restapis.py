import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

watson_url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/d15a87f6-318d-4f07-97bf-84503f7d0e9f"
watson_api_key = "A7Evk7Tq9ecLnX3ZHW4zAXPsxXl-NtOWnCqCcA6Nwdh-"


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_requests(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(
            url, headers={"Content-Type": "application/json"}, json=json_payload
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



def get_dealers_from_cf(url):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result
        print(dealers)
        for dealer in dealers:
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                zip=dealer["zip"]
            )
            results.append(dealer_obj)
    return results

def get_dealer_by_id(url, dealerId):
    results = []
    json_result = get_request(url, id=dealerId)

    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results

def get_dealers_by_state(url, state):
    results = []
    json_result = get_request(url,st=state)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, id=kwargs["dealerId"])
    if json_result:
        reviews = json_result
        print(reviews)
        for review in reviews:
            dealer_review = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment="",
                id=review["id"],
            )
            dealer_review.sentiment = analyze_review_sentiments(dealer_review.review)
            results.append(dealer_review)
            print(dealer_review)
    return results

def analyze_review_sentiments(dealerreview):
    body = {"text": dealerreview, "features": {"sentiment": {"document": True}}}
    print(dealerreview)
    response = requests.post(
        watson_url + "/v1/analyze?version=2019-07-12",
        headers={"Content-Type": "application/json"},
        json=body,  # Use json parameter for automatic conversion
        auth=HTTPBasicAuth("apikey", watson_api_key),
    )

    # Check if request was successful
    if response.status_code == 200:
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
    return "n/a"

def post_review(url, review_json_payload):
    response = post_requests(url, review_json_payload)
    return response