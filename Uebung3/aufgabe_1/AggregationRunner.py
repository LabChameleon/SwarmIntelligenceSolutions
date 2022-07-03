import sys
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from AggregationModel_1 import AggregationModel as model_1
from AggregationModel_2 import AggregationModel as model_2

if sys.argv[1] == "model_1":
    model = model_1
elif sys.argv[1] == "model_2": 
    model = model_2
else:
    print("invalid input:" + sys.argv[1])
    quit()

def agent_potrayal(agent):
    portrayal = {   "Shape": "circle",
                    "Color": "Red",
                    "Filled": "true",
                    "Layer": 0,
                    "r": 0.5 }
    return portrayal

grid_width = 40
grid_height = 40
grid = CanvasGrid(agent_potrayal, grid_width, grid_height, 500, 500)
server = ModularServer(model,
                        [grid],
                        "Aggregation Model",
                        {   "num_agents": 20, 
                            "grid_width": grid_width,
                            "grid_height": grid_height })
server.port = 8521
server.launch()
