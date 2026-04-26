from abc import ABC, abstractmethod
from datetime import datetime


# ==========================================
# 1. VEHICLE CLASSES (Autó osztályok)
# ==========================================

class Vehicle(ABC):
    """Absztrakt alaposztály az összes járműnek."""

    def __init__(self, license_plate: str, make: str, car_type: str, rental_price: int):
        self.__license_plate = license_plate
        self.__make = make
        self.__car_type = car_type
        self.__rental_price = rental_price

    @property
    def license_plate(self):
        return self.__license_plate

    @property
    def make(self):
        return self.__make

    @property
    def car_type(self):
        return self.__car_type

    @property
    def rental_price(self):
        return self.__rental_price

    @abstractmethod
    def info(self):
        pass


class Auto(Vehicle):
    """Személyautó osztály."""

    def __init__(self, license_plate: str, make: str, car_type: str, rental_price: int, passenger_capacity: int):
        super().__init__(license_plate, make, car_type, rental_price)
        self.__passenger_capacity = passenger_capacity

    @property
    def passenger_capacity(self):
        return self.__passenger_capacity

    def info(self):
        return f"Car - Plate: {self.license_plate}, Model: {self.make, self.car_type}, Passengers: {self.passenger_capacity}, Price: {self.rental_price} HUF/day"


class Truck(Vehicle):
    """Teherautó osztály."""

    def __init__(self, license_plate: str, make: str, car_type: str, rental_price: int, cargo_space: float):
        super().__init__(license_plate, make, car_type, rental_price)
        self.__cargo_space = cargo_space

    @property
    def cargo_space(self):
        return self.__cargo_space

    def info(self):
        return f"Truck - Plate: {self.license_plate}, Model: {self.make,self.car_type}, Payload: {self.__cargo_space} m3, Price: {self.rental_price} HUF/day"


# ==========================================
# 2. Bérlés osztály
# ==========================================

class Rental:
    """Egy adott bérlés osztálya."""

    def __init__(self, vehicle: Vehicle, date: str):
        self.__vehicle = vehicle
        self.__date = date

    @property
    def vehicle(self):
        return self.__vehicle

    @property
    def date(self):
        return self.__date

    def info(self):
        return f"Bérlés rögzítve: {self.vehicle.license_plate} | Dátum: {self.date} | Fizetendő: {self.vehicle.rental_price} HUF"


"""Kiíratás"""
if __name__ == "__main__":

    car1 = Auto(license_plate = "HKR-219", make = "Toyota", car_type = "Corolla", rental_price = 16000, passenger_capacity = 5)
    truck1 = Truck(license_plate = "TRK-999", make = "Ford", car_type = "Transit", rental_price = 25000, cargo_space = 1.5)

    print(car1.info())
    print(truck1.info())