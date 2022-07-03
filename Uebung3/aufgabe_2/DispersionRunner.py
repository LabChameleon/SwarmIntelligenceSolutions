from DispersionModel import DispersionModel
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

def agent_potrayal(agent):
    return {    "Shape": "circle",
                "Color": "Red",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5 }

grid_width = 40
grid_height = 40
num_agents = 20
grid = CanvasGrid(agent_potrayal, grid_width, grid_height, 500, 500)
server = ModularServer(DispersionModel, [grid], 
        "Dispersion Model",
        {   "num_agents": 20,
            "width": grid_width,
            "height": grid_height })

server.port = 8521
server.launch()
