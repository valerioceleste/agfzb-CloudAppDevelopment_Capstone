import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

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

def get_dealer_by_id_from_cf(url, id, **kwargs):
    result = {}
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        #print("dealers :",dealers)  
        # For each dealer object
        dealer = dealers[0]
        print("dealer :",dealer)
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                short_name=dealer["short_name"],
                                st=dealer["st"], zip=dealer["zip"])
        result = dealer_obj
    return result

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
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    print('json_result RESTAPIS', json_result)
    if json_result:
        reviews = json_result
        for dealer_review in reviews:
            review_obj = DealerReview(
                dealership=dealer_review.get("dealership"),
                name=dealer_review.get("name"),
                purchase=dealer_review.get("purchase"),
                review=dealer_review.get("review"),
                purchase_date=dealer_review.get("purchase_date"),
                car_make=dealer_review.get("car_make"),
                car_model=dealer_review.get("car_model"),
                car_year=dealer_review.get("car_year"),
                sentiment='',
                id=dealer_review.get("id")
            )
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)
    return results

def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/5bb69077-cc5b-48eb-9f17-ceb25300b5b5"
    api_key = "7XvnkavpYfv-_OTr7Jsn0XoAIu1S7AcW_yGOMvYUzTSf"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    return(label)

def post_review(url, review_json_payload):
    response = post_requests(url, review_json_payload)
    return response