from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

class AggregationAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wait_steps = 2
        self.free_steps = 3
        self.wait = 0
        self.free = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,
                        moore = True,
                        include_center = False)
        self.random.shuffle(possible_steps)
        for pos in possible_steps:
            if self.model.grid.is_cell_empty(pos):
                self.model.grid.move_agent(self, pos)
                break

    def step(self):
        num_close_neigh = len(self.model.grid.get_neighbors(self.pos, True, radius = 2))
        neigh_dist = self.model.grid.get_neighbors(self.pos, True, radius = 6)
        num_dist_neigh = len(neigh_dist)
        if (num_close_neigh > 0 and self.wait == 0 
                and self.free == 0):
            self.wait = pow(self.wait_steps, num_dist_neigh)

        if self.wait > 0:
            self.wait -= 1
            if self.wait == 0:
                self.free = self.free_steps

        if self.wait == 0: 
            if self.free > 0:
                self.free -= 1
            self.move()

class AggregationModel(Model):
    def __init__(self, num_agents, grid_width, grid_height):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(grid_width, grid_height, True)
        self.running = True

        for i in range(self.num_agents):
            a = AggregationAgent(i, self)
            self.schedule.add(a)
            self.grid.position_agent(a, x = "random", y = "random")


    def step(self):
        self.schedule.step()
