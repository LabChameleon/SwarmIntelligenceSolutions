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

    def neighbor_center(self, neigh):
        center_x = 0
        center_y = 0
        for a in neigh:
            center_x += a.pos[0]
            center_y += a.pos[1]
        avg_x = int(round(center_x / len(neigh)))
        avg_y = int(round(center_y / len(neigh)))
        return (avg_x, avg_y)

    def move_to_center(self, pos):
        if (pos[0] - self.pos[0] == 0 
            or pos[1] - self.pos[1] == 0): 
            return 
        dir_x = (pos[0] - self.pos[0]) // abs(pos[0] - self.pos[0]) 
        dir_y = (pos[1] - self.pos[1]) // abs(pos[1] - self.pos[1])
        new_pos = (self.pos[0] + dir_x, self.pos[1] + dir_y)
        if self.model.grid.is_cell_empty(new_pos):
            self.model.grid.move_agent(self, new_pos)

    def step(self):
        num_close_neigh = len(self.model.grid.get_neighbors(self.pos, True, radius = 2))
        neigh_dist = self.model.grid.get_neighbors(self.pos, True, radius = 6)
        num_dist_neigh = len(neigh_dist)
        if (num_close_neigh > 0 and self.wait == 0 
                and self.free == 0):
            self.wait = pow(num_dist_neigh, self.wait_steps)
            self.to_center = self.neighbor_center(neigh_dist)

        if self.wait > 0:
            self.wait -= 1
            self.move_to_center(self.to_center)
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
