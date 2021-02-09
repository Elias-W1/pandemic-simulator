from random import randint
from model.Constants import *

def check_intersection(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2): # https://silentmatt.com/rectangle-intersection/
    if (ax1 < bx2) and (ax2 > bx1) and (ay1 < by2) and (ay2 > by1):
        return True
    else:
        return False

def normalize(value):
    return value / abs(value)



class Particle():
    def __init__(self, status, x, y, x_movement, y_movement, infection_radius, disease ):
        print("Initializing {status} particle at {x},{y}".format(status=status,x=x,y=y))
        self.status = status
        self.x = x
        self.y = y
        self.x_movement = x_movement       # movement on X. negative = left and positive = right. Absolute value = speed.
        self.y_movement = y_movement
        self.size = 2          # size = radius.
        self.abssize = 2*self.size+1
        self.infection_start_tick = -1
        self.recovery_start_tick = -1
        self.infection_radius = infection_radius
        self.infection_abssize = 2*infection_radius+3
        self.sd_radius = SOCIAL_DISTANCING_RADIUS_MULTIPLIER * self.infection_radius
        self.sd_abssize = 2*self.sd_radius+1
        self.disease = disease
        self.outlined = False
        self.last_outlined_tick = -1
        self.stepsize_multiplier = 1

        self.movement = Movement.DIAGONAL
        self.target = None
        self.masked = False
        self.sd = False
        self.collided_list = [] # saves all particles it has infection radius intersection with until there is no infection radius intersection with them anymore


    def change_status(self, newstatus):
        self.status = newstatus

    def set_status_infected(self, current_tick):
        self.status = Status.INFECTED
        self.infection_start_tick = current_tick

    def repel_x(self):
        self.x_movement = self.x_movement * (-1)

    def repel_y(self):
        self.y_movement = self.y_movement * (-1)

    def move(self):
        if self.movement == Movement.DIAGONAL:
            self.move_x(self.x_movement)
            self.move_y(self.y_movement)
        elif self.movement == Movement.UNDIRECTED:
            self.move_x(((-1) ** randint(0,1) * (self.x_movement)))
            self.move_y(((-1) ** randint(0,1) *(self.y_movement)))
        elif self.movement == Movement.DIRECTED:
            # if self.x_movement == 0:
            #     self.x_movement = self.stepsize_multiplier
            #
            # if self.y_movement == 0:
            #     self.y_movement = self.stepsize_multiplier

            if self.target.x > self.x:
                self.x_movement = abs(self.x_movement)
            elif self.target.x < self.x:
                self.x_movement = (-1) * abs(self.x_movement)
            elif self.target.x == self.x:
                self.x_movement = 0

            if self.target.y > self.y:
                self.y_movement = abs(self.y_movement)
            elif self.target.y < self.y:
                self.y_movement = (-1) * abs(self.y_movement)
            elif self.target.y == self.y:
                self.y_movement = 0

            self.move_x(self.x_movement)
            self.move_y(self.y_movement)


    def move_x(self, move_addition):
        x_border = 600
        self.x_movement = move_addition
        if (self.x - (self.size + 1) + move_addition - 1 <= 0 and move_addition < 0):
                self.repel_x()
        elif (self.x + self.abssize*2 + move_addition + 1 >= x_border - self.abssize and move_addition > 0):
                self.repel_x()

        self.x += self.x_movement

    def move_y(self, move_addition):
        y_border = 600
        self.y_movement = move_addition
        if (self.y - (self.size + 1) + self.y_movement - 1 <= self.abssize and self.y_movement < 0):
                self.repel_y()
        elif self.y + (self.size + 1) + self.y_movement + 1 >= y_border - self.abssize and self.y_movement > 0:
                self.repel_y()

        self.y += self.y_movement

    def adjust_movement_wallcollision(self, x_border, y_border):
        pass



    def update_status(self, tick):
        dead = 0
        recovered = 0
        healthy = 0
        # From infected to recovered or dead
        if (self.infection_start_tick > -1) and (tick - self.infection_start_tick >= self.disease.infection_time):
            self.end_infection(tick)
            if self.status == Status.DEAD:
                dead += 1
            else:
                recovered += 1

        # from recovered to healthy
        if self.recovery_start_tick > -1 and (tick - self.recovery_start_tick >= self.disease.recovery_time):
            self.change_status(Status.HEALTHY)
            self.recovery_start_tick = -1
            healthy += 1

        return dead, recovered, healthy

    def end_infection(self, current_tick):
        random = randint(1,100)
        if random/100 <= self.disease.death_rate:      # die
            self.change_status(Status.DEAD)
            self.outlined = False
            self.x_movement = 0
            self.y_movement = 0
        else:                               # recover
            self.change_status(Status.RECOVERED)
            self.recovery_start_tick = current_tick
        self.infection_start_tick = -1

    def collides_with(self, other, tick):
        intersection = check_intersection(self.x-self.abssize, self.y-self.abssize, self.x+self.abssize, self.y+self.abssize, other.x-other.abssize, other.y-other.abssize, other.x+other.abssize, other.y+other.abssize)
        infection_radius_intersection = check_intersection(self.x-self.infection_abssize, self.y-self.infection_abssize, self.x+self.infection_abssize, self.y+self.infection_abssize, other.x-other.infection_abssize, other.y-other.infection_abssize, other.x+other.infection_abssize, other.y+other.infection_abssize)
        new_infections = 0
        new_disease = None


        # Infection radius collision.
        if infection_radius_intersection:
            if not self.check_in_collided(other):

                if (self.status == Status.INFECTED and other.status == Status.HEALTHY):
                    random = randint(1, 100)
                    infection_rate = self.disease.infection_rate
                    if self.masked:
                        infection_rate = self.disease.infection_rate - MASK_INFECTION_REDUCTION
                    if random / 100 <= infection_rate:
                        new_disease = self.disease.infect_particle(other, tick)
                        new_infections += 1
                    self.set_outline(tick)
                    other.set_outline(tick)
                    self.add_to_collided(other)
                    other.add_to_collided(self)
                elif (self.status == Status.HEALTHY and other.status == Status.INFECTED):
                    random = randint(1, 100)
                    infection_rate = self.disease.infection_rate
                    if self.masked:
                        infection_rate = self.disease.infection_rate - MASK_INFECTION_REDUCTION
                    if random / 100 <= infection_rate:
                        other.set_status_infected(tick)
                        new_disease = other.disease.infect_particle(self, tick)
                        new_infections += 1
                    self.set_outline(tick)
                    other.set_outline(tick)
                    self.add_to_collided(other)
                    other.add_to_collided(self)
        else:
            if self.check_in_collided(other):
                self.remove_from_collided(other)

        # Particle in Social Distancing radius.
        sd_radius_intersection = False
        if self.sd:
                sd_radius_intersection = check_intersection(self.x - self.sd_abssize, self.y - self.sd_abssize,
                                                            self.x + self.sd_abssize, self.y + self.sd_abssize,
                                                            other.x - other.sd_abssize, other.y - other.sd_abssize,
                                                            other.x + other.sd_abssize, other.y + other.sd_abssize)

                # not working yet better approach
                # if sd_radius_intersection:
                #     x_sd_intersection = normalize(self.x_movement) != normalize(other.x_movement)
                #     y_sd_intersection = normalize(self.y_movement) != normalize(other.y_movement)
                #     if x_sd_intersection and y_sd_intersection:
                #         self.y_movement = (-1) * normalize(self.y_movement) * 5
                #         self.move_y(self.y_movement)
                #     else:
                #         if x_sd_intersection:
                #             self.x_movement = normalize(other.x_movement) * abs(self.x_movement) * 2
                #             self.move_x(self.x_movement)
                #             self.x_movement = self.x_movement / 2
                #
                #         if y_sd_intersection:
                #             self.y_movement = normalize(other.y_movement) * abs(self.y_movement) * 2
                #             self.move_y(self.y_movement)
                #             self.y_movement = self.y_movement / 2

                if sd_radius_intersection:
                    self.repel_x()
                    self.repel_y()
                    self.move_x(self.x_movement)
                    self.move_y(self.y_movement)









        # Particle collision.
        if intersection:
            # particles repelling
            self.repel_x()
            self.repel_y()

            self.move_x(self.x_movement)
            self.move_y(self.y_movement)

            other.x_movement = self.x_movement * (-1)
            other.y_movement = self.y_movement * (-1)

            other.move_x(self.x_movement * (-1))
            other.move_y(self.y_movement * (-1))






        return_values = {}
        return_values["collision"] = intersection
        return_values["new_infections"] = new_infections
        return_values["new_disease"] = new_disease
        return_values["sd_collision"] = sd_radius_intersection




        return return_values


    def infect_with(self, disease, tick):
        self.set_status_infected(tick)
        self.disease = disease
        self.disease.add_infected()

    def reset_outline(self, tick):
        if  tick - self.last_outlined_tick > 10:
            self.outlined = False

    def set_outline(self, tick):
        self.outlined = True
        self.last_outlined_tick = tick

    def mask(self):
        self.masked = True
        # print("Before: ",self.infection_abssize, "Particle size: ", self.abssize)
        # self.infection_abssize = self.infection_abssize * (1-MASK_RADIUS_REDUCTION)
        # print("After: ",self.infection_abssize)

    def unmask(self):
        self.masked = False


    def enable_social_distancing(self):
        self.sd = True

    def add_to_collided(self, other):
        if not other in self.collided_list:
            self.collided_list.append(other)

    def check_in_collided(self, other):
        return other in self.collided_list

    def remove_from_collided(self, other):
        self.collided_list.pop(self.collided_list.index(other))

    def distance_to_other(self, other):
        return abs(self.x-other.x)+abs(self.y-other.y)
