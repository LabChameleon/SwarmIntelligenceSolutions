from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, BarChartModule
from FlockingModel import FlockingModel 

def agent_portrayal(agent):
    return {    "Shape": "circle",
                "r": 0.6,
                "Color": "Red",
                "Filled": "true",
                "Layer": 0 }

grid_width = 40
grid_height = 40

canvas = CanvasGrid(agent_portrayal, grid_width, grid_height, 
        canvas_width = 800, canvas_height = 800)
barchart = BarChartModule(scope = "agent", fields = [
                            { "Label": "Dir",
                            "Color": "blue" } ],
                data_collector_name = "datacollector")

server = ModularServer(FlockingModel, [canvas, barchart], name = "FlockingModel",
            model_params = {    "num_agents": 50,
                                "g_width": grid_width,
                                "g_height": grid_height })
server.launch()
