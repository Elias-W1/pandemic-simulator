from model.Target import *
from model.Constants import *

class VaccineCenter(Target):
    def __init__(self, x, y, vaccine_capacity, restock_time):
        super().__init__(x, y)
        self.vaccine_capacity = vaccine_capacity
        self.restock_time = restock_time

        self.available_vaccines = []
        self.available_vaccine_counts = []
        self.assigned_vaccine_counts = []
        self.vaccine_count_list = []

        self.last_restock_tick = 0
        self.unassigned_vaccines_count = 0

    def refresh_stock(self, tick):
        # Dispose vaccines for inactive diseases.
        for i in range(len(self.available_vaccines)):
            vaccine = self.available_vaccines[i]
            if vaccine.against_disease.active == False:
                self.available_vaccine_counts[i] = 0

        # Restock if restock time is reached since last restock.
        if (tick - self.last_restock_tick) >= self.restock_time:
            self.restock()
            self.last_restock_tick = tick

    def restock(self):
        available = self.get_available_vaccines_count()
        vaccine_count = self.get_active_vaccines_count()
        if (vaccine_count == 0) or (available >= self.vaccine_capacity):            # If capacity is maxed out or no vaccine available yet do nothing.
            self.unassigned_vaccines_count = 0
            self.vaccine_count_list = []
            newly_available = 0
        else:
            newly_available = 0
            new_count = max(self.vaccine_capacity // vaccine_count, 1)
            for i in range(len(self.available_vaccines)):
                    vaccine = self.available_vaccines[i]
                    if vaccine.against_disease.active:
                        newly_available += new_count
                        self.available_vaccine_counts[i] = new_count

        self.unassigned_vaccines_count = newly_available
        self.refresh_vaccine_count_list()


    def get_available_vaccines_count(self): # Get count of all vaccine-dosages a center has.
        return sum(self.available_vaccine_counts)

    def get_active_vaccines_count(self):    # Get Count of all active vaccines a center has.
        sum = 0
        for vaccine in self.available_vaccines:
            if vaccine.against_disease.active:
                sum += 1
        return sum


    def add_vaccine(self, vaccine):
        self.available_vaccines.append(vaccine)
        self.available_vaccine_counts.append(0)
        self.assigned_vaccine_counts.append(0)

    def vaccinate(self, particle, vaccine):
        particle.vaccinate(vaccine)
        index = self.available_vaccines.index(particle.assigned_vaccine)
        self.available_vaccine_counts[index] -= 1
        self.assigned_vaccine_counts[index] -= 1
        particle.assigned_vaccine = None


    def reached(self, particle):
        self.vaccinate(particle, particle.assigned_vaccine)

    def assign_vaccine_to_particle(self, particle):
        # Find first available vaccine and assign it to particle.
        i = 0
        while self.available_vaccine_counts[i] == 0:
            i += 1
        vaccine = self.available_vaccines[i]
        self.assigned_vaccine_counts[i] += 1
        particle.assigned_vaccine = vaccine

    def refresh_vaccine_count_list(self):       # Creates a 2d list with vaccines and their unassigned dosages.
        listobj = []
        for i in range(len(self.available_vaccines)):
            vaccine = self.available_vaccines[i]
            count = self.available_vaccine_counts[i] - self.assigned_vaccine_counts[i]
            if vaccine.against_disease.active == True and count > 0:
                listobj.append((vaccine,count))
        self.vaccine_count_list = listobj



