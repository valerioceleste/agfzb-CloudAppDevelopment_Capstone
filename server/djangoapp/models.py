from django.db import models
from django.utils.timezone import now
from django.utils import timezone 


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    founded_year = models.IntegerField(null=False)
    Country = models.CharField(null=False, max_length=50)
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
        ('WAGON', 'Wagon'),]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    year = models.TimeField(default=timezone.now)
    kilometers = models.IntegerField(null=True)
    color = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
