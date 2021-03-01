class Vaccine():
    def __init__(self, research_duration, against_disease, effective_percentage_difference):
        self.remaining_research_duration = research_duration
        self.against_disease = against_disease
        self.effective_percentage_difference = effective_percentage_difference

        self.researched = False
        self.effective_diseases = []

    def finish_research(self):
        self.researched = True
        # Create list of diseases the vaccine is effective for.
        if self.against_disease.parent != None:
            for disease in self.against_disease.parent.children:
                if not disease == self.against_disease:
                    difference = self.against_disease.calculate_percentage_difference(disease)
                    print(difference," <= ",self.effective_percentage_difference,":", difference <= self.effective_percentage_difference)
                    if difference <= self.effective_percentage_difference:
                        self.effective_diseases.append(disease)
                        disease.vaccine_ready = True

        self.against_disease.vaccine_ready = True



