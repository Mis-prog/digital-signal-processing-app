import matplotlib.pyplot as plt

def plot(data_, scatter=True, color_='green'):
    name=data_.columns[1]

    plt.title(name)
    plt.xlabel('MD')
    plt.grid(True)

    if scatter:
        plt.scatter(data_['MD'], data_[name], color=color_)
    else:
        plt.plot(data_['MD'], data_[name], color=color_)
