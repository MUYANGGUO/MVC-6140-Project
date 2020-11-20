# plot
import os
import glob
import matplotlib.pyplot as plt

def plot(alg, times, seed):
    Data = dict()
    files = []
    for filename in glob.iglob('./output/*.sol', recursive=True):
        files.append(filename)
    for time in times:
        for file_name in files:
            attributes = file_name.split('_')
            n = len(attributes)
            for i in range(n- 1, -1, -1):
                if i == n - 1:
                    seed_exp = int(attributes[i].split('.')[0])
                elif i == n - 2:
                    time_exp = float(attributes[i])
                elif i == n - 3:
                    alg_exp = attributes[i]
                else:
                    if i > 0:
                        name = '_'.join(attributes[:i + 1])
                    else:
                        name = ''.join(attributes[:i + 1])
                    break
            if alg_exp != alg or time_exp != time or seed_exp != seed:
                continue
            with open(file_name, 'r') as file:
                mvc_quality = int(file.readline())
                if name not in Data:
                    Data[name] = [mvc_quality]
                else:
                    Data[name].append(mvc_quality)

    fig, ax = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(16)
    x = times
    ax.set(xlabel='time (s)', ylabel='MVC quality',
       title=alg + ' performance plot')
    ax.grid()
    for data in Data.items():
        name, y = data
        ax.plot(x, y, 'o-', label=name.split('/')[2:])
    plt.legend()
    if not os.path.exists('./output_plots'):
        os.makedirs('./output_plots')
    fig.savefig("./output_plots/" + alg +".png", dpi =120)

# modify this line to plot your method outputs
plot('LS2',[10.0, 50.0, 250.0, 500.0] , 1)