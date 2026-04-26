from abc import ABC, abstractmethod
from datetime import datetime

class Auto:
    def __init__(self, license_plate: str, make: str, car_type: str, engine: str, cylinder: str, rent: str):
        self.license_plate = license_plate
        self.make = make
        self.car_type = car_type
        self.engine = engine
        self.cylinder = cylinder
        self.rent = rent

    @property
    def license_plate(self):
        return self._license_plate

    @license_plate.setter
    def license_plate(self, new_license_plate):
        self._license_plate = new_license_plate

class Truck:
    def __init__(self, license_plate: str, make: str, car_type: str, engine: str, cargo_space: str, rent: str):
        self.license_plate = license_plate
        self.make = make
        self.car_type = car_type
        self.engine = engine
        self.cargo_space = cargo_space
        self.rent = rent

auto1 = Auto("HKR-219","Toyota","Corolla","1,2","In-Line","16000")
print(auto1.license_plate,auto1.make,auto1.car_type,auto1.engine,auto1.cylinder,auto1.rent)

truck1 = Truck("KGB-123","Iveco","Daily","2,8","Extended","30000")
print(truck1.license_plate,truck1.make,truck1.car_type,truck1.engine,truck1.cargo_space,truck1.rent)

