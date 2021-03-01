
class Statistics():
    def __init__(self, particle_count, infected_count):
        self.particle_count = particle_count
        self.stepcounter = 0
        # absolute values history
        self.healthy_count_history  = []
        self.dead_count_history = []
        self.infected_count_history = []
        self.recovered_count_history = []
        # percent values history
        self.healthy_percent_history = []
        self.infected_percent_history = []
        self.recovered_percent_history = []
        self.dead_percent_history = []
        self.add_data(self.particle_count-infected_count, infected_count, 0, 0)

    def get_export_data(self, granularity):
        if self.stepcounter == 0:
            print("Nothing to export.")
            return None

        healthy_count_history_granular = self.adapt_list_to_granularity(self.healthy_count_history, granularity)
        infected_count_history_granular = self.adapt_list_to_granularity(self.infected_count_history, granularity)
        recovered_count_history_granular = self.adapt_list_to_granularity(self.recovered_count_history, granularity)
        dead_count_history_granular = self.adapt_list_to_granularity(self.dead_count_history, granularity)
        granularity_steps = self.create_granularity_step_list(len(healthy_count_history_granular), granularity)

        return granularity_steps, healthy_count_history_granular, infected_count_history_granular, recovered_count_history_granular, dead_count_history_granular

    def add_data(self, healthy_count, infected_count, recovered_count, dead_count):
        self.stepcounter += 1
        # absolute values
        self.healthy_count_history.append(healthy_count)
        self.infected_count_history.append(infected_count)
        self.recovered_count_history.append(recovered_count)
        self.dead_count_history.append(dead_count)
        # percentage values for live statistics. For efficiency reasons saved and not calculated.
        self.healthy_percent_history.append(healthy_count / self.particle_count)
        self.infected_percent_history.append(infected_count / self.particle_count)
        self.recovered_percent_history.append(recovered_count / self.particle_count)
        self.dead_percent_history.append(dead_count / self.particle_count)

    # def get_live_data(self):          # plain live data
    #     return self.stepcounter, self.healthy_percent_history[-1], self.infected_percent_history[-1], self.recovered_percent_history[-1], self.dead_percent_history[-1]

    def get_live_data(self): # stacked graph live data
        infected = self.infected_percent_history[-1]
        healthy = self.healthy_percent_history[-1] + infected
        dead = 1 - self.dead_percent_history[-1]
        recovered = dead - self.recovered_percent_history[-1]

        return self.stepcounter, healthy, infected, recovered, dead

    def adapt_list_to_granularity(self, listobj, granularity):
        newlist = []
        index = 0
        while index <= len(listobj) - 1:
            newlist.append(listobj[index])
            index += granularity

        print("Len:", len(newlist), " | List: ", str(newlist))
        return newlist

    def create_granularity_step_list(self, length, granularity):
        listobj = []
        for i in range(length):
            listobj.append(i * granularity)
        print("Len:", len(listobj), " | List: ", str(listobj))
        return listobj

    def check_graph_value_changed(self):
        if self.stepcounter == 1:
            return True
        changed = False
        if self.infected_count_history[-1] != self.infected_count_history[-2]:
            changed = True
        elif self.healthy_count_history[-1] != self.healthy_count_history[-2]:
            changed = True
        elif self.recovered_count_history[-1] != self.recovered_count_history[-2]:
            changed = True
        elif self.dead_count_history[-1] != self.dead_count_history[-2]:
            changed = True

        return changed

    def check_simulation_finished(self):
        if len(self.healthy_count_history) > 0 and len(self.dead_count_history) > 0:
            if (self.healthy_count_history[-1] + self.dead_count_history[-1]) == self.particle_count:
                return True

        return False
