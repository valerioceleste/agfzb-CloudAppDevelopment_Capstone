from django.db import models
from datetime import date


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    founded_year = models.IntegerField(null=False)
    country = models.CharField(null=False, max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name 


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
        return f"{self.car_make.name} {self.name}"


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
