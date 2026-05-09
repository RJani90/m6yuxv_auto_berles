from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# ==========================================
# Autó osztályok
# ==========================================

class Auto(ABC):
    """Absztrakt alaposztály az összes járműnek."""

    def __init__(self, license_plate: str, make: str, car_type: str, engine: float, rental_price: int):
        self.__license_plate = license_plate
        self.__make = make
        self.__car_type = car_type
        self.__engine = engine
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

    @property
    def engine(self):
        return self.__engine

    @abstractmethod
    def info(self):
        pass


class Szemelyauto(Auto):
    """Személyautó osztály."""

    def __init__(self, license_plate: str, make: str, car_type: str, engine: float, passenger_capacity: int, rental_price: int,):
        super().__init__(license_plate, make, car_type, engine, rental_price)
        self.__passenger_capacity = passenger_capacity

    @property
    def passenger_capacity(self):
        return self.__passenger_capacity

    def info(self):
        return f"Car - Plate: {self.license_plate} | Model: {self.make} {self.car_type} | Engine: {self.engine} | Passengers: {self.passenger_capacity} | Price: {self.rental_price} HUF/day"


class Teherauto(Auto):
    """Teherautó osztály."""

    def __init__(self, license_plate: str, make: str, car_type: str, engine:float, cargo_space: float, rental_price: int ):
        super().__init__(license_plate, make, car_type, engine, rental_price)
        self.__cargo_space = cargo_space

    @property
    def cargo_space(self):
        return self.__cargo_space

    def info(self):
        return f"Truck - Plate: {self.license_plate} | Model: {self.make} {self.car_type} | Engine: {self.engine} | Cargo space: {self.__cargo_space} m3 | Price: {self.rental_price} HUF/day"


# ==========================================
# Bérlés osztály
# ==========================================

class Berles:
    """Egy adott bérlés osztálya."""

    def __init__(self, vehicle: Auto, start_date: str, end_date:str, total_price: int):
        self.__vehicle = vehicle
        self.__start_date = start_date
        self.__end_date = end_date
        self.__total_price = total_price

    @property
    def vehicle(self):
        return self.__vehicle

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date

    @property
    def total_price(self):
        return self.__total_price

    def info(self):
        return f"Bérlés rögzítve: {self.vehicle.license_plate} | Dátum: {self.start_date} - {self.end_date} | Fizetendő: {self.total_price} HUF"


# ==========================================
# Company osztály (Autókölcsönző)
# ==========================================

# noinspection PyTypeChecker
class Autokolcsonzo:
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

    def add_vehicle(self, vehicle: Auto):
        """Hozzáad egy új járművet a kölcsönzőhöz."""
        self.__vehicles.append(vehicle)

    def remove_vehicle(self, license_plate: str):
        """Töröl egy járművet a rendszerből a rendszám alapján."""

        # Ellenőrizzük, hogy a járműhöz tartozik-e aktív bérlés
        for r in self.__rentals:
            if r.vehicle.license_plate == license_plate:
                return f"Hiba: A {license_plate} rendszámú járműhöz aktív bérlés tartozik, ezért nem törölhető! Próbálja újra a bérleti idő lejárta után."

        # Megkeressük és töröljük a járművet
        vehicle_to_remove = None
        for v in self.__vehicles:
            if v.license_plate == license_plate:
                vehicle_to_remove = v
                break

        if vehicle_to_remove:
            self.__vehicles.remove(vehicle_to_remove)
            return f"Siker: A {license_plate} rendszámú jármű sikeresen törölve a flottából."
        else:
            return "Hiba: Nincs ilyen rendszámú jármű a rendszerben."

    def list_vehicles(self):
        """Kilistázza az elérhető járműveket."""
        print(f"\n--- {self.name} Járműparkja ---")
        for v in self.__vehicles:
            print(v.info())
        print("-" * 30)

    def cancel_rental(self, license_plate: str, start_date_str: str):
        """Lemond egy meglévő bérlést a rendszám és a kezdődátum alapján, esetleges kötbérrel."""

        # Dátum konvertálása és ellenőrzése
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            return "Hiba: Hibás dátumformátum! Használja a YYYY-MM-DD formátumot."

        # Megkeressük a bérlést a rendszerben
        rental_to_cancel = None
        for r in self.__rentals:
            if r.vehicle.license_plate == license_plate and r.start_date == start_date_str:
                rental_to_cancel = r
                break

        if not rental_to_cancel:
            return "Hiba: Nem található ilyen bérlés a rendszerben a megadott adatokkal."

        # Kiszámoljuk a dátumok közötti különbséget
        today = datetime.now().date()
        days_difference = (start_date - today).days

        self.__rentals.remove(rental_to_cancel)

        # Eldöntjük, hogy kell-e büntetést fizetni (ha 1 nap, vagy annál kevesebb van hátra)
        if days_difference <= 1:
            # Kiszámoljuk a teljes ár 25%-át
            # noinspection PyUnresolvedReferences
            penalty = int(rental_to_cancel.total_price * 0.25)
            return f"FIGYELMEZTETÉS (Késői lemondás)! A {license_plate} bérlése törölve. Az 1 napon belüli lemondás miatt a fizetendő kötbér: {penalty} HUF."
        else:
            return f"Sikeres lemondás: A {license_plate} rendszámú jármű {start_date_str} napon kezdődő bérlése díjmentesen törölve."

    def rent_vehicle(self, license_plate: str, start_date_str: str, end_date_str: str):
        """Kikölcsönöz egy járművet egy adott időszakra."""

        # Dátumok formátumának ellenőrzése és konvertálása
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return "Hiba: Érvénytelen naptári nap vagy rossz formátum! Kérem, próbálja újra és valós dátumot adjon meg (YYYY-MM-DD)."

        # Logikai ellenőrzések a dátumokra
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        if start_date < tomorrow:
            return f"Hiba: Csak a holnapi naptól lehet bérlést rögzíteni. Kérem próbálja újra a következő dátumtól: {tomorrow}"

        if end_date < start_date:
            return "Hiba: A bérlés vége dátum nem lehet korábban, mint a bérlés kezdete."

        # Megkeressük a járművet a rendszám alapján
        vehicle_to_rent: Auto = None
        for v in self.__vehicles:
            if v.license_plate == license_plate:
                vehicle_to_rent = v
                break

        if vehicle_to_rent is None:
            return "Hiba: Nincs ilyen rendszámú jármű a rendszerben."

        # Ellenőrizzük, hogy foglalt-e már a megadott időszakban
        for r in self.__rentals:
            if r.vehicle.license_plate == license_plate:
                r_start = datetime.strptime(r.start_date, "%Y-%m-%d").date()
                r_end = datetime.strptime(r.end_date, "%Y-%m-%d").date()

                if start_date <= r_end and end_date >= r_start:
                    return f"Hiba: Ezt a járművet már kibérelték a {r.start_date} - {r.end_date} időszakban. Kérem válasszon a futó foglaláson kívüli időpontot, vagy másik járművet."

        # Ha minden rendben, kiszámoljuk az árat és rögzítjük a bérlést
        days = (end_date - start_date).days
        if days == 0:
            days = 1  # Ha aznap hozza vissza, az is 1 napi díj

        total_price = days * vehicle_to_rent.rental_price

        new_rental = Berles(vehicle_to_rent, start_date_str, end_date_str, total_price)
        self.__rentals.append(new_rental)

        osszesito = (
            f"SIKERES BÉRLÉS RÖGZÍTVE!\n"
            f"\n"
            f"   {'-' * 45}\n"
            f"   Gépjármű:   {vehicle_to_rent.make} {vehicle_to_rent.car_type} ({vehicle_to_rent.license_plate})\n"
            f"   Időszak:    {start_date_str} -tól {end_date_str} -ig\n"
            f"   Időtartam:  {days} nap\n"
            f"   Napi díj:   {vehicle_to_rent.rental_price} HUF / nap\n"
            f"   {'-' * 45}\n"
            f"   FIZETENDŐ:  {total_price} HUF"
        )

        return osszesito

    def list_rentals(self):
        """Kilistázza az összes rögzített bérlést."""
        print(f"\n--- {self.name} Aktuális Bérlései ---")
        if not self.__rentals:
            print("Jelenleg nincs aktív bérlés a rendszerben.")
        else:
            for r in self.__rentals:
                print(r.info())
        print("-" * 30)


if __name__ == "__main__":
    # Kölcsönző létrehozása
    company = Autokolcsonzo("OOP Autókölcsönző")

    # Autók létrehozása
    car1 = Szemelyauto(license_plate="HKR-219", make="Toyota", car_type="Corolla", engine=1.6, rental_price=16000, passenger_capacity=5)
    car2 = Szemelyauto(license_plate="JGF-342", make="Skoda", car_type="Octavia", engine=2.2, rental_price=18000, passenger_capacity=5)
    car3 = Szemelyauto(license_plate="MBN-555", make="Volkswagen", car_type="Golf", engine=1.4, rental_price=15000, passenger_capacity=5)
    car4 = Szemelyauto(license_plate="PTA-112", make="Suzuki", car_type="Vitara", engine=1.2, rental_price=17000, passenger_capacity=5)
    car5 = Szemelyauto(license_plate="KJL-987", make="Opel", car_type="Astra", engine=1.4, rental_price=13000, passenger_capacity=5)
    car6 = Szemelyauto(license_plate="RWC-404", make="Kia", car_type="Ceed", engine=1.6, rental_price=16000, passenger_capacity=5)
    car7 = Szemelyauto(license_plate="TXZ-777", make="Ford", car_type="Focus", engine=1.8, rental_price=14000, passenger_capacity=5)
    car8 = Szemelyauto(license_plate="AA-BB-123", make="Hyundai", car_type="Tucson", engine=1.4, rental_price=22000, passenger_capacity=5)

    # Teherautók létrehozása
    truck1 = Teherauto(license_plate="TRK-999", make="Ford", car_type="Transit", engine=2.6, rental_price=25000, cargo_space=1.5)
    truck2 = Teherauto(license_plate="LKH-890", make="Mercedes", car_type="Sprinter", engine=3.0, rental_price=32000, cargo_space=3.5)
    truck3 = Teherauto(license_plate="GTR-221", make="Fiat", car_type="Ducato", engine=2.2, rental_price=27000, cargo_space=3.0)
    truck4 = Teherauto(license_plate="VBN-444", make="Renault", car_type="Master", engine=2.6, rental_price=28000, cargo_space=2.8)
    truck5 = Teherauto(license_plate="WQA-101", make="Iveco", car_type="Daily", engine=2.4, rental_price=35000, cargo_space=4.2)
    truck6 = Teherauto(license_plate="SDF-654", make="Peugeot", car_type="Boxer", engine=2.8, rental_price=26000, cargo_space=2.5)
    truck7 = Teherauto(license_plate="XCV-998", make="Citroen", car_type="Jumper", engine=2.2, rental_price=26000, cargo_space=2.5)
    truck8 = Teherauto(license_plate="AA-TC-999", make="Volkswagen", car_type="Crafter", engine=2.6, rental_price=31000, cargo_space=3.2)


    # Autók hozzáadása a kölcsönzőhöz
    # noinspection DuplicatedCode
    company.add_vehicle(car1)
    company.add_vehicle(car2)
    company.add_vehicle(car3)
    company.add_vehicle(car4)
    company.add_vehicle(car5)
    company.add_vehicle(car6)
    company.add_vehicle(car7)
    company.add_vehicle(car8)

    # Teherautók hozzáadása a kölcsönzőhöz
    # noinspection DuplicatedCode
    company.add_vehicle(truck1)
    company.add_vehicle(truck2)
    company.add_vehicle(truck3)
    company.add_vehicle(truck4)
    company.add_vehicle(truck5)
    company.add_vehicle(truck6)
    company.add_vehicle(truck7)
    company.add_vehicle(truck8)

    # Bérlések létrehozása
    company.rent_vehicle("HKR-219", "2026-12-20", "2026-12-22")
    company.rent_vehicle("JGF-342", "2026-10-01", "2026-10-05")
    company.rent_vehicle("TRK-999", "2026-11-15", "2026-11-15")
    company.rent_vehicle("WQA-101", "2026-09-18", "2026-10-25")

    # === FELHASZNÁLÓI INTERFÉSZ  ===
    print("\nÜdvözöljük az OOP Autókölcsönző Rendszerben!")

    while True:
        print("\n" + "=" * 40)
        print("Válasszon az alábbi műveletek közül:")
        print("1. Elérhető járművek listázása")
        print("2. Jármű hozzáadása a flottához")
        print("3. Jármű TÖRLÉSE a flottából")
        print("4. Jármű bérlése")
        print("5. Bérlés lemondása")
        print("6. Aktuális bérlések listázása")
        print("7. Kilépés")
        print("=" * 40)

        valasztas = input("Adja meg a kívánt menüpont számát (1-7): ")

        if valasztas == "1":
            company.list_vehicles()

        elif valasztas == "2":
            print("\n--- Új jármű rögzítése ---")
            tipus = input("Milyen típusú járművet szeretne hozzáadni? (1: Személyautó, 2: Teherautó): ")

            if tipus not in ["1", "2"]:
                print("-> Hiba: Érvénytelen választás. Kérem 1-es vagy 2-es gombot nyomjon.")
                continue

            rendszam = input("Kérem a rendszámot (pl. ABC-123): ").upper()

            # Ellenőrizzük, hogy van-e már ilyen rendszám
            if any(v.license_plate == rendszam for v in company.vehicles):
                print("-> Hiba: Ez a rendszám már szerepel a rendszerben!")
                continue

            new_make = input("Márka (pl. Ford): ")
            new_car_type = input("Típus (pl. Focus): ")
            new_engine = (float(input("Motor (pl. 1.6): ")))

            try:
                price = int(input("Napi bérleti díj (HUF): "))
                if tipus == "1":
                    capacity = int(input("Utasok száma (pl. 5): "))
                    uj_auto = Szemelyauto(rendszam, new_make, new_car_type, new_engine, capacity, price)
                    company.add_vehicle(uj_auto)
                    print(f"-> SIKER: A {rendszam} rendszámú személyautó hozzáadva a flottához!")
                elif tipus == "2":
                    cargo = float(input("Raktér mérete (m3, pl. 3.5): "))
                    uj_teher = Teherauto(rendszam, new_make, new_car_type, new_engine, cargo, price)
                    company.add_vehicle(uj_teher)
                    print(f"-> SIKER: A {rendszam} rendszámú teherautó hozzáadva a flottához!")
            except ValueError:
                print("-> Hiba: A díjnak, kapacitásnak és raktérnek számnak kell lennie. Kérem próbálja újra!")


        elif valasztas == "3":

            rendszam = input("Kérem a TÖRÖLNI kívánt jármű rendszámát: ").upper()
            print(f"\nFIGYELEM! Biztosan törölni szeretné a(z) {rendszam} rendszámú járművet a flottából?")

            ack = input(
                "Írja be, hogy 'IGEN' a folytatáshoz, vagy nyomjon bármi mást a megszakításhoz: ").upper()

            if ack == "IGEN":

                eredmeny = company.remove_vehicle(rendszam)

                print(f"\n-> {eredmeny}")
            else:

                print(f"\n-> A törlés megszakítva. A(z) {rendszam} jármű az adatbázisban maradt.")

            # -----------------------------

        elif valasztas == "4":
            rendszam = input("Kérem a bérelni kívánt jármű rendszámát (pl. HKR-219): ").upper()

            car_exist = any(v.license_plate == rendszam for v in company.vehicles)
            if not car_exist:
                print(
                    "\n-> Hiba: Nincs ilyen rendszámú jármű a rendszerben! Kérem, ellenőrizze a listát az 1-es menüpontban.")
                continue

            kezdo_datum = input("Kérem a bérlés KEZDŐ dátumát (YYYY-MM-DD): ")
            veg_datum = input("Kérem a bérlés VÉGSŐ dátumát (YYYY-MM-DD): ")
            eredmeny = company.rent_vehicle(rendszam, kezdo_datum, veg_datum)
            print(f"\n{eredmeny}")

        elif valasztas == "5":
            rendszam = input("Kérem a lemondani kívánt jármű rendszámát: ").upper()

            car_exist = any(v.license_plate == rendszam for v in company.vehicles)
            if not car_exist:
                print("\n-> Hiba: Nincs ilyen rendszámú jármű a rendszerben!")
                continue

            kezdo_datum = input("Kérem a lemondani kívánt bérlés KEZDŐ dátumát (YYYY-MM-DD): ")
            eredmeny = company.cancel_rental(rendszam, kezdo_datum)
            print(f"\n-> {eredmeny}")

        elif valasztas == "6":
            company.list_rentals()

        elif valasztas == "7":
            print("\nKöszönjük, hogy az OOP Autókölcsönző rendszert használta! Viszontlátásra!")
            break

        else:
            print("\n-> Hiba: Érvénytelen választás. Kérem, 1 és 7 közötti számot adjon meg.")