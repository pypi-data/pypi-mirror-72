"""
SCPlotLib
=========

A Python plotting library for SingleCell objects. This library is designed
to provide easy functions for visualizing single-cell RNA-seq data stored
in the SingleCell object. For more information and documentation on SingleCell
class see https://github.com/edwinv87/singlecelldata. 

This library can generate various plot types such as:

1. Core plots - line plots, bar plots, scatter plots
2. Visualizing high dimensional data - t-SNE plots, PCA plots
3. Specialized plots - heatmaps, silhouette plots, outlier score plots

See https://github.com/edwinv87/scplotlib for more information and documentation. 

"""

from .scp_pcaplot import PCAPlot
from .scp_tsneplot import tSNEPlot
from .scp_silhouetteplot import SilhouettePlot
from .scp_heatmap import GeneExpHeatmap
from .scp_outlierplots import PlotOutlierScores
from .scp_core import LinePlot, ScatterPlot, BarPlot


__all__ = ['PCAPlot', 'tSNEPlot', 'SilhouettePlot', 'GeneExpHeatmap', 'PlotOutlierScores', 'LinePlot', 'ScatterPlot', 'BarPlot']