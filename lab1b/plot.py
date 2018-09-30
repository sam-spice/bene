
import pandas as pd
import matplotlib.pyplot as plt


# Class that parses a file and plots several graphs
class Plotter:
    def __init__(self):
        plt.style.use('ggplot')
        pd.set_option('display.width', 1000)
        pass

    def linePlot(self):
        mu = 1000000 // (1000 * 8)
        p_array = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.98]
        empirical = list()
        theoretical_list = list()
        indexes = list()
        for p in p_array:
            csv_file_name = "data/queue-" + "{0:.2f}".format(p) + ".csv"
            csv_data = pd.read_csv(csv_file_name)
            average_delay = csv_data['q_delay'].mean()
            theoretical = p / ((2 * mu) * (1 - p))
            empirical.append(average_delay)
            theoretical_list.append(theoretical)
            indexes.append(p)

        df = pd.DataFrame({
        'empirical': empirical,
        'theoretical': theoretical_list}, index=indexes)

        #plt.figure()
        ax = df.plot()
        ax.set_xlabel("p")
        ax.set_ylabel("Queuing Delay")
        fig = ax.get_figure()
        fig.savefig('graphs/delay.png')


if __name__ == '__main__':
    p = Plotter()
    p.linePlot()