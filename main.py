from Amsterdam_park_accessibility.data_processing import AmsterdamBoundary
from Amsterdam_park_accessibility.visualization import PlotAmsterdamBoundary

ams = AmsterdamBoundary()
data = ams.download_data()
gdf = ams.to_geodataframe(data)
ams_boundary = ams.filter_amsterdam()

PlotAmsterdamBoundary.plot_boundary(ams_boundary)
