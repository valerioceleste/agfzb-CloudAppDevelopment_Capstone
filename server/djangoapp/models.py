from django.db import models
from datetime import date


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    founded_year = models.IntegerField(null=False)
    country = models.CharField(null=False, max_length=50)
    description = models.TextField(null=True)
    def __str__(self):
        return (
            "Name: " + self.name + ", " + 
            "Founded Year: " + self.founded_year + ", " + 
            "Country: " + self.country + ", " + 
            "Description: " + self.description
        )


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('CONVERTIBLE', 'Convertible'),
        ('WAGON', 'Wagon'),]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    year = models.DateField()
    kilometers = models.IntegerField()
    color = models.CharField(max_length=20)
    def __str__(self):
        return (
            "Car Manufacturer: " + self.car_make + ", " + 
            "Model Name: " + self.type + ", " + 
            "Year: " + self.year + ", " + 
            "Kilometers: " + self.kilometers + ", " + 
            "Color: " + self.color
        )


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self,dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.id = id 
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    def __str__(self):
        return (
            "Dealer Name: " + self.name + ", " + 
            "Purchase: " + self.purchase + ", " + 
            "Purchase Date: " + self.purchase_date + ", " + 
            "Review: " + self.review + ", " + 
            "Sentiment: " + self.sentiment
        )