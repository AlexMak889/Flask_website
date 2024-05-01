""" from matplotlib.figure import Figure
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt """

""" def graph(num_x_points=50):
    #Renders the plot on the fly.
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return plt
 """



    
"""     plt.plot(data_x, data_y)  
     plt.xlabel('Index')
     plt.ylabel('Temperature')
     plt.title(label="Sensor Data", fontsize=16, color="green")
      plt.legend()
      plt.show() """
    