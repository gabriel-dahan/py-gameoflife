"""
This example demonstrates ViewBox and AxisItem configuration to plot a correlation matrix.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.Qt import QtCore

class GraphicGOL(QtWidgets.QMainWindow):

    def __init__(self, gol, *args, **kwargs):
        super(GraphicGOL, self).__init__(*args, **kwargs)
        self.__gol = gol
        gr_wid = pg.GraphicsLayoutWidget(show = True)
        self.setCentralWidget(gr_wid)
        self.setWindowTitle('Game Of Life')
        self.show()

        pg.setConfigOption('imageAxisOrder', 'row-major')

        self.__matrix = pg.ImageItem()
        self.__matrix.setImage(self.__gol.get_matrix())

        plot = gr_wid.addPlot()
        plot.invertY(True)
        plot.setDefaultPadding(0.0)
        plot.addItem(self.__matrix)

        plot.getAxis('bottom').setHeight(10)
        plot.showAxes(True, showValues = (True, True, False, False), size = 20)

    def run(self, wait_time: float):
        def to_run():
            self.__gol.next_gen(update_grid = True)
            self.__matrix.setImage(self.__gol.get_matrix())
        timer = QtCore.QTimer()
        timer.timeout.connect(to_run)
        timer.start(wait_time * 1000)
        pg.exec()
        
        