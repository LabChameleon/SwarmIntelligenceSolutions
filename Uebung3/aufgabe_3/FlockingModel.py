from mesa import Agent, Model
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import math
import numpy as np

def relative_pos(base_pos, abs_pos, max_dist, w, h):
    base_pos = np.array(base_pos)
    abs_pos = np.array(abs_pos)
    dist = abs_pos - base_pos
    rel_pos = abs_pos

    if dist[0] > max_dist:
        rel_pos[0] -= w
    elif dist[0] < -max_dist:
        rel_pos[0] += w

    if dist[1] > max_dist:
        rel_pos[1] -= h
    elif dist[1] < -max_dist:
        rel_pos[1] += h
    
    return rel_pos

def normalize_dir(d):
    norm = np.linalg.norm(d)
    if norm == 0:
        return np.array((0,0))
    return d / norm

def compute_agent_dir(agent):
    len_avg = np.linalg.norm(agent.model.avg_dir)
    len_agent = np.linalg.norm(agent.dir)
    if len_avg * len_agent == 0:
        return 0
    cos_of_angle = np.dot(agent.model.avg_dir, agent.dir) / (len_avg * len_agent)
    if cos_of_angle > 0.999999:
        cos_of_angle = 1
    return np.arccos(cos_of_angle)

def compute_average_dir(model):
    direction = np.array((0.,0.))
    agents = model.schedule.agents
    for a in agents:
        direction += a.dir
    return direction / len(agents)

class FlockingAgent(Agent):
    def __init__(self, u_id, model, vision_radius, min_dist, flock_weight, 
                    fly_weight, avoid_weight):
        super().__init__(u_id, model)
        r_dir = [self.model.random.choice([-1,0,1]), 
                    self.model.random.choice([1,-1])]
        self.model.random.shuffle(r_dir)
        self.dir = normalize_dir(np.array((r_dir), dtype = np.float64))

        self.vision_radius = vision_radius
        self.min_dist = min_dist
        self.flock_weight = flock_weight
        self.fly_weight = fly_weight
        self.avoid_weight = avoid_weight

    def center_of_mass_dir(self, agents, dist):
        if len(agents) == 0:
            return np.array((0.,0.))
        p = np.array((0.,0.))
        for a in agents:
            r_pos = relative_pos(self.pos,
                    a.pos, dist,
                    self.model.grid.width,
                    self.model.grid.height)
            p += r_pos
        p = p / len(agents)
        return p - self.pos

    def avg_dir(self, agents):
        l = len(agents) + 1
        direction = self.dir
        for a in agents:
            direction += a.dir
        return direction / l

    def avoid_dir(self, agents):
        avoid = self.center_of_mass_dir(agents,
                    self.min_dist)
        return -avoid

    def flight_dir(self): 
        vision_neigh = self.model.grid.get_neighbors(
                pos = self.pos,
                radius = self.vision_radius, 
                moore = True)
        close_neigh = self.model.grid.get_neighbors(
                pos = self.pos,
                radius = self.min_dist, 
                moore = True)

        avg_dir = self.avg_dir(vision_neigh) 
        avoid_dir = self.avoid_dir(close_neigh)
        flock_dir = self.center_of_mass_dir(vision_neigh, self.vision_radius)
        return (self.flock_weight * flock_dir + 
                self.fly_weight * avg_dir + 
                self.avoid_weight * avoid_dir)

    def move(self):
        pos = self.real_pos 
        new_dir = normalize_dir(self.flight_dir())
        self.dir = normalize_dir(new_dir + 3 * self.dir)
        self.real_pos = pos + self.dir
        actual_pos = np.around(self.real_pos).astype(np.int32)
        t_pos = (actual_pos[0], actual_pos[1]) 
        self.model.grid.move_agent(self, t_pos)

    def step(self): 
        self.move()

class FlockingModel(Model):
    def __init__(self, num_agents, g_width, g_height):
        self.running = True
        self.num_agents = num_agents
        self.grid = Grid(g_width, g_height, True)
        self.schedule = RandomActivation(self)

        for i in range(num_agents):
            a = FlockingAgent(i, self, vision_radius = 6, 
                                min_dist = 2,
                                flock_weight = 3, 
                                fly_weight = 3, 
                                avoid_weight = 10)
            self.grid.place_agent(a, self.random.choice(
                    sorted(self.grid.empties)))
            a.real_pos = np.array(a.pos)
            self.schedule.add(a)

        self.datacollector = DataCollector(
                model_reporters = { "AvgDir": "avg_dir" },
                agent_reporters = { "Dir": compute_agent_dir })

        self.avg_dir = compute_average_dir(self)
        self.datacollector.collect(self)

    def compute_avg_dir(model):
        agents = model.schedule.agents()
        for a in agents:
            avg_dir += a.dir
        return avg_dir / len(agents)
    
    def step(self):
        self.avg_dir = compute_average_dir(self)
        self.datacollector.collect(self)
        self.schedule.step()
