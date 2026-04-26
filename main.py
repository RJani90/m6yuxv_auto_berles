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
        return f"Car - Plate: {self.license_plate} | Model: {self.make} {self.car_type} | Passengers: {self.passenger_capacity} | Price: {self.rental_price} HUF/day"


class Truck(Vehicle):
    """Teherautó osztály."""

    def __init__(self, license_plate: str, make: str, car_type: str, rental_price: int, cargo_space: float):
        super().__init__(license_plate, make, car_type, rental_price)
        self.__cargo_space = cargo_space

    @property
    def cargo_space(self):
        return self.__cargo_space

    def info(self):
        return f"Truck - Plate: {self.license_plate} | Model: {self.make} {self.car_type} | Cargo space: {self.__cargo_space} m3 | Price: {self.rental_price} HUF/day"


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


# ==========================================
# 3. Company osztály (Autókölcsönző)
# ==========================================

class Company:
    """A kölcsönzőt és az üzleti logikát kezelő főosztály."""

    def __init__(self, name: str):
        self.name = name
        self.__vehicles = []  # Autók (Vehicle objektumok)
        self.__rentals = []  # Bérlések (Rental objektumok)

    @property
    def vehicles(self):
        return self.__vehicles

    @property
    def rentals(self):
        return self.__rentals

    def add_vehicle(self, vehicle: Vehicle):
        """Hozzáad egy új járművet a kölcsönzőhöz."""
        self.__vehicles.append(vehicle)

    def list_vehicles(self):
        """Kilistázza az elérhető járműveket."""
        print(f"\n--- {self.name} Járműparkja ---")
        for v in self.__vehicles:
            print(v.info())
        print("-" * 30)



"""Kiíratás és Tesztelés"""
if __name__ == "__main__":
    # Kölcsönző létrehozása
    company = Company("OOP Autókölcsönző")

    # Autók létrehozása
    car1 = Auto(license_plate="HKR-219", make="Toyota", car_type="Corolla", rental_price=16000, passenger_capacity=5)
    car2 = Auto(license_plate="JGF-342", make="Skoda", car_type="Octavia", rental_price=18000, passenger_capacity=5)
    car3 = Auto(license_plate="MBN-555", make="Volkswagen", car_type="Golf", rental_price=15000, passenger_capacity=5)
    car4 = Auto(license_plate="PTA-112", make="Suzuki", car_type="Vitara", rental_price=17000, passenger_capacity=5)
    car5 = Auto(license_plate="KJL-987", make="Opel", car_type="Astra", rental_price=13000, passenger_capacity=5)
    car6 = Auto(license_plate="RWC-404", make="Kia", car_type="Ceed", rental_price=16000, passenger_capacity=5)
    car7 = Auto(license_plate="TXZ-777", make="Ford", car_type="Focus", rental_price=14000, passenger_capacity=5)
    car8 = Auto(license_plate="AA-BB-123", make="Hyundai", car_type="Tucson", rental_price=22000, passenger_capacity=5)

    # Teherautók létrehozása
    truck1 = Truck(license_plate="TRK-999", make="Ford", car_type="Transit", rental_price=25000, cargo_space=1.5)
    truck2 = Truck(license_plate="LKH-890", make="Mercedes", car_type="Sprinter", rental_price=32000, cargo_space=3.5)
    truck3 = Truck(license_plate="GTR-221", make="Fiat", car_type="Ducato", rental_price=27000, cargo_space=3.0)
    truck4 = Truck(license_plate="VBN-444", make="Renault", car_type="Master", rental_price=28000, cargo_space=2.8)
    truck5 = Truck(license_plate="WQA-101", make="Iveco", car_type="Daily", rental_price=35000, cargo_space=4.2)
    truck6 = Truck(license_plate="SDF-654", make="Peugeot", car_type="Boxer", rental_price=26000, cargo_space=2.5)
    truck7 = Truck(license_plate="XCV-998", make="Citroen", car_type="Jumper", rental_price=26000, cargo_space=2.5)
    truck8 = Truck(license_plate="AA-TC-999", make="Volkswagen", car_type="Crafter", rental_price=31000,cargo_space=3.2)


    # Autók hozzáadása a kölcsönzőhöz
    company.add_vehicle(car1)
    company.add_vehicle(car2)
    company.add_vehicle(car3)
    company.add_vehicle(car4)
    company.add_vehicle(car5)
    company.add_vehicle(car6)
    company.add_vehicle(car7)
    company.add_vehicle(car8)
    # Teherautók hozzáadása a kölcsönzőhöz
    company.add_vehicle(truck1)
    company.add_vehicle(truck2)
    company.add_vehicle(truck3)
    company.add_vehicle(truck4)
    company.add_vehicle(truck5)
    company.add_vehicle(truck6)
    company.add_vehicle(truck7)
    company.add_vehicle(truck8)

    # A kölcsönző járműparkjának listázása
    company.list_vehicles()