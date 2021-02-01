from random import randint

def check_intersection(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2): # https://silentmatt.com/rectangle-intersection/
    if (ax1 < bx2) and (ax2 > bx1) and (ay1 < by2) and (ay2 > by1):
        return True
    else:
        return False

class Particle():
    def __init__(self, status, x, y, x_movement, y_movement, death_rate, infection_time, recovery_time, infection_radius):
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
        self.death_rate = death_rate
        self.infection_time = infection_time
        self.recovery_time = recovery_time
        self.infection_radius = infection_radius
        self.infection_abssize = 2*infection_radius+1

    def change_status(self, newstatus):
        self.status = newstatus

    def set_status_infected(self, current_tick):
        self.status = "i"
        self.infection_start_tick = current_tick

    def repel_x(self):
        self.x_movement = self.x_movement * (-1)

    def repel_y(self):
        self.y_movement = self.y_movement * (-1)

    def move(self):
        self.x = self.x + self.x_movement
        self.y = self.y + self.y_movement

    def adjust_movement_wallcollision(self, x_border, y_border):
        if self.x - (self.size + 1) + self.x_movement - 1 <= 0 and self.x_movement < 0:
            self.repel_x()
        elif self.x + self.abssize*2 + self.x_movement + 1 >= x_border - self.size and self.x_movement > 0:
            self.repel_x()

        if self.y - (self.size + 1) + self.y_movement - 1 <= 0 and self.y_movement < 0:
            self.repel_y()
        elif self.y + (self.size + 1) + self.y_movement + 1 >= y_border - self.abssize and self.y_movement > 0:
            self.repel_y()


    def update_status(self, tick):
        dead = 0
        recovered = 0
        healthy = 0
        # From infected to recovered or dead
        if (self.infection_start_tick > -1) and (tick - self.infection_start_tick >= self.infection_time):
            self.end_infection(tick)
            if self.status == "d":
                dead += 1
            else:
                recovered += 1

        # from recovered to healthy
        if self.recovery_start_tick > -1 and (tick - self.recovery_start_tick >= self.recovery_time):
            self.change_status("h")
            self.recovery_start_tick = -1
            healthy += 1

        return dead, recovered, healthy

    def end_infection(self, current_tick):
        random = randint(1,100)
        if random/100 <= self.death_rate:      # die
            self.change_status("d")
            self.x_movement = 0
            self.y_movement = 0
            print("particle died")
        else:                               # recover
            self.change_status("r")
            self.recovery_start_tick = current_tick
        self.infection_start_tick = -1

    def collides_with(self, other, tick):
        intersection = check_intersection(self.x-self.abssize, self.y-self.abssize, self.x+self.abssize, self.y+self.abssize, other.x-other.abssize, other.y-other.abssize, other.x+other.abssize, other.y+other.abssize)
        infection_radius_intersection = check_intersection(self.x-self.infection_abssize, self.y-self.infection_abssize, self.x+self.infection_abssize, self.y+self.infection_abssize, other.x-other.infection_abssize, other.y-other.infection_abssize, other.x+other.infection_abssize, other.y+other.infection_abssize)
        new_infections = 0
        if infection_radius_intersection:
            if self.status == "i" and other.status == "h":
                other.set_status_infected(tick)
                new_infections += 1
            elif self.status == "h" and other.status == "i":
                self.set_status_infected(tick)
                new_infections += 1

        if intersection:
            # particles repelling
            self.repel_x()
            self.repel_y()
            other.x_movement = self.x_movement * (-1)
            other.y_movement = self.y_movement * (-1)

            self.move()
            other.move()

        return (intersection, new_infections)
