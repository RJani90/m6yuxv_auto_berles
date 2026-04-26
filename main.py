from abc import ABC, abstractmethod
from datetime import datetime

class Auto(ABC):
    def __init__(self, license_plate: str, make: str, type: str, engine: int, cylinder: str, rent: str):
        self.license_plate = license_plate
        self.make = make
        self.type = type
        self.engine = engine
        self.cylinder = cylinder
        self.rent = rent

    @property
    def license_plate(self):
        return self._license_plate

    @license_plate.setter
    def license_plate(self, new_license_plate):
        self._license_plate = new_license_plate

auto1 = Auto("HKR-219","Toyota","Corolla","1,2","Hengerelrendezés: soros","Bérleti díj: 16000")
print(auto1.license_plate,auto1.make,auto1.type,auto1.engine,auto1.cylinder,auto1.rent)

auto1.make = "Jeep"
print(auto1.make)
print(auto1.license_plate)
