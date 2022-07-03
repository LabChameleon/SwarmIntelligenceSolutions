from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

class DispersionAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def calc_move_dir(self):
        neigh = self.model.grid.get_neighbors(self.pos,True, radius = 5)
        if len(neigh) == 0:
            return 0,0
        d_x = 0
        d_y = 0
        for a in neigh:
            d_x += a.pos[0] - self.pos[0]
            d_y += a.pos[1] - self.pos[1]
        d_x /= len(neigh) 
        d_y /= len(neigh)
        return -d_x, -d_y

    def move(self):
        d_x, d_y = self.calc_move_dir()
        print(str(d_x) + ", " + str(d_y))
        n_x, n_y = (0,0)
        if d_x < 0:
            if d_y < 0:
                n_x = self.pos[0] - 1
                n_y = self.pos[1] - 1
            elif d_y > 0:
                n_x = self.pos[0] - 1
                n_y = self.pos[1] + 1
            else:
                n_x = self.pos[0] - 1
                n_y = self.pos[1]
        elif d_x > 0:
            if d_y < 0:
                n_x = self.pos[0] + 1
                n_y = self.pos[1] - 1
            elif d_y > 0:
                n_x = self.pos[0] + 1
                n_y = self.pos[1] + 1
            else:
                n_x = self.pos[0] + 1
                n_y = self.pos[1]
        elif d_x == 0:
            if d_y < 0:
                n_x = self.pos[0] 
                n_y = self.pos[1] - 1
            elif d_y > 0:
                n_x = self.pos[0] 
                n_y = self.pos[1] + 1
            else:
                n_x = self.pos[0]
                n_y = self.pos[1]

        if self.model.grid.is_cell_empty((n_x % self.model.grid.width, 
                            n_y % self.model.grid.height)):
            self.model.grid.move_agent(self, (n_x, n_y))

    def step(self):
        self.move()
        
class DispersionModel(Model):
    def __init__(self, num_agents, width, height):
        super().__init__()
        self.num_agents = num_agents
        self.grid = SingleGrid(width, height, True)
        self.scheduler = RandomActivation(self)

        for i in range(num_agents):
            agent = DispersionAgent(i, self)
            self.scheduler.add(agent)
            self.grid.position_agent(agent, (i%4)-2 + width // 2, i//4-2 + height // 2)

    def step(self):
        self.scheduler.step()
