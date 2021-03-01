from random import randint
from model.Constants import *
from math import sqrt

def check_cirlce_intersection(x1, y1, r1, x2, y2, r2):
    distance = sqrt((((x2 - x1) ** 2) + ((y2 - y1) ** 2)))
    return (distance < (r1+r2))

def check_intersection(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2): # https://silentmatt.com/rectangle-intersection/
    if (ax1 < bx2) and (ax2 > bx1) and (ay1 < by2) and (ay2 > by1):
        return True
    else:
        return False



def get_sign(value):
    if value < 0:
        return -1
    else:
        return 1

class Particle():
    def __init__(self, status, x, y, x_border, y_border, x_movement, y_movement, infection_radius, disease, particle_diameter):
        self.status = status
        self.x = x
        self.y = y
        self.x_border = x_border
        self.y_border = y_border
        self.x_movement = x_movement       # movement on X. negative = left and positive = right. Absolute value = speed.
        self.y_movement = y_movement
        self.abssize = particle_diameter
        self.size = particle_diameter // 2
        self.infection_start_tick = -1
        self.recovery_start_tick = -1
        self.infection_radius = infection_radius
        self.infection_abssize = 2*infection_radius+3
        self.sd_radius = SOCIAL_DISTANCING_RADIUS_MULTIPLIER * self.infection_radius
        self.sd_abssize = 2*self.sd_radius+1
        self.sd_x_move = 0  # Sum up all movements which would be done by social distancing and then move particles in suiting direction with suiting speed later.
        self.sd_y_move = 0
        self.disease = disease
        self.outlined = False
        self.last_outlined_tick = -1
        self.stepsize_multiplier = 1

        self.movement = Movement.DIAGONAL
        self.masked = False
        self.sd = False
        self.collided_list = [] # saves all particles it has infection radius intersection with until there is no infection radius intersection with them anymore

        self.vaccines = []
        self.immunities = []

        self.target = None
        self.reached_target_ticks = 0

        self.assigned_vaccine = None


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
        if self.status == Status.DEAD:
            return

        if  self.sd and (self.sd_x_move + self.sd_y_move != 0):
            x_move = get_sign(self.sd_x_move) * max(1, min(abs(self.x_movement), abs(self.sd_x_move)))
            y_move = get_sign(self.sd_y_move) * max(1, min(abs(self.y_movement), abs(self.sd_y_move)))
            self.move_x(x_move)
            self.move_y(y_move)
            self.sd_x_move = 0
            self.sd_y_move = 0
        if self.movement == Movement.DIAGONAL:
            self.move_x(self.x_movement)
            self.move_y(self.y_movement)
        elif self.movement == Movement.UNDIRECTED:
            self.move_x(((-1) ** randint(0,1) * (self.x_movement)))
            self.move_y(((-1) ** randint(0,1) *(self.y_movement)))
        elif self.movement == Movement.DIRECTED:
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

            # If target is reached add one tick to target already reached duration.
            if (self.target.x-(VACCINE_CENTER_SIZE//2) <= self.x and self.target.x+(VACCINE_CENTER_SIZE//2) >= self.x) and (self.target.y-(VACCINE_CENTER_SIZE//2) <= self.y and self.target.y+(VACCINE_CENTER_SIZE//2) >= self.y):
                self.reached_target_ticks += 1

            if self.assigned_vaccine != None and (self.x_movement + self.y_movement) == 0 and self.reached_target_ticks == 0 and self.reached_target_ticks == 0:  # If first time reaching target and vaccine is assigned then vaccinate self.
                self.target.reached(self)


            # If waiting duration is over return to normal movement, otherwise just move with previously calculated movement.
            if self.reached_target_ticks >= self.target.waiting_duration and self.status != Status.DEAD:
                self.x_movement = self.stepsize_multiplier
                self.y_movement = self.stepsize_multiplier
                self.remove_target()
            else:
                self.move_x(self.x_movement)
                self.move_y(self.y_movement)



    def move_x(self, move_addition):
        self.x_border
        self.x_movement = move_addition
        if (self.x - (self.size + 1) + move_addition - 1 <= 0 and move_addition < 0):
                self.repel_x()
        elif (self.x + self.abssize*2 + move_addition + 1 >= self.x_border - self.abssize and move_addition > 0):
                self.repel_x()

        self.x += self.x_movement

    def move_y(self, move_addition):
        self.y_border
        self.y_movement = move_addition
        if (self.y - (self.size + 1) + self.y_movement - 1 <= self.abssize and self.y_movement < 0):
                self.repel_y()
        elif self.y + (self.size + 1) + self.y_movement + 1 >= self.y_border - self.abssize and self.y_movement > 0:
                self.repel_y()

        self.y += self.y_movement



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
        self.disease.remove_infected()
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
        infection_radius_intersection = check_cirlce_intersection(self.x,self.y,self.infection_abssize,other.x,other.y,other.infection_radius)
        new_infections = 0
        new_disease = None


        # Infection radius collision.
        if infection_radius_intersection:
            if not self.check_in_collided(other):
                if (self.status == Status.INFECTED and other.status == Status.HEALTHY):                 # If one particle is healthy and the other infected, then infect the healthy one if it's not effectively vaccinated.
                    random = randint(1, 100)
                    infection_rate = self.disease.infection_rate
                    if self.masked:
                        infection_rate = self.disease.infection_rate - MASK_INFECTION_REDUCTION
                    if random / 100 <= infection_rate:
                        if not self.disease in other.immunities:
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
                        if not other.disease in self.immunities:
                            other.set_status_infected(tick)
                            new_disease = other.disease.infect_particle(self, tick)
                            new_infections += 1
                    self.set_outline(tick)
                    other.set_outline(tick)
                    self.add_to_collided(other)
                    other.add_to_collided(self)
        else:                                                                                           # Else just remove from collision list without new infections.
            if self.check_in_collided(other):
                self.remove_from_collided(other)

        # Particle in Social Distancing radius.
        sd_radius_intersection = False
        if self.sd:
                sd_radius_intersection = check_intersection(self.x - self.sd_abssize, self.y - self.sd_abssize, self.x + self.sd_abssize, self.y + self.sd_abssize, other.x - other.sd_abssize, other.y - other.sd_abssize, other.x + other.sd_abssize, other.y + other.sd_abssize)

                if sd_radius_intersection:
                    # if one particle is right of other move the particle to right direction and other particle moves to left direction.
                    if self.x >= other.x:
                        self.sd_x_move += 1
                        other.sd_x_move -= 1
                    else:
                        self.sd_x_move -= 1
                        other.sd_x_move += 1

                    # Same as above but if one particle is above other move up and other down.
                    if self.y >= other.y:
                        self.sd_y_move += 1
                        other.sd_y_move -= 1
                    else:
                        self.sd_y_move -= 1
                        other.sd_y_move += 1

        # Particle collision.
        intersection = check_cirlce_intersection(self.x, self.y, self.abssize, other.x, other.y, other.abssize)
        if intersection:
            for i in range(2):                              # otherwise particles can glitch into each other in a way that the collision will not be resolved by one iteration, which makes particles stuck.
                if check_cirlce_intersection(self.x, self.y, self.abssize, other.x, other.y, other.abssize):
                    # particles repelling
                    self.repel_x()
                    self.repel_y()

                    self.move_x(self.x_movement)
                    self.move_y(self.y_movement)

                    other.x_movement = get_sign(self.x_movement) * other.stepsize_multiplier * (-1)
                    other.y_movement =  get_sign(self.y_movement) * other.stepsize_multiplier * (-1)

                    other.move_x(other.x_movement)
                    other.move_y(other.y_movement)

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
        if  tick - self.last_outlined_tick > OUTLINED_DURATION_TICKS:
            self.outlined = False

    def set_outline(self, tick):
        self.outlined = True
        self.last_outlined_tick = tick

    def mask(self):
        self.masked = True
        self.infection_abssize = round(self.infection_abssize * (1-MASK_RADIUS_REDUCTION))
        if self.infection_abssize % 2 == 0:
            self.infection_abssize += 1

    def unmask(self):
        self.masked = False
        self.infection_abssize = self.infection_radius*2 + 3


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

    def vaccinate(self, vaccine):
        self.vaccines.append(vaccine)
        self.immunities.append(vaccine.against_disease)
        self.immunities.extend(vaccine.effective_diseases)


    def set_target(self, target):
        self.target = target
        self.movement = Movement.DIRECTED
        self.target.add_visitor(self)

    def remove_target(self):
        self.target = None
        self.reached_target_ticks = 0
        self.movement = Movement.DIAGONAL