import matplotlib.pyplot as plt


class PlotAmsterdamBoundary:
    @staticmethod
    def plot_boundary(ams_boundary):
        fig, ax = plt.subplots(figsize=(8,8))
        ams_boundary.plot(ax=ax, color='none', edgecolor='blue', linewidth=2)
        ax.set_title("Amsterdam Municipality Boundary")
        plt.show()