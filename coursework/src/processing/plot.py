import matplotlib.pyplot as plt


def plot(data_, scatter=True):
    name = data_.columns[1]

    plt.figure(figsize=(8, 6))
    plt.title(name)
    plt.xlabel('MD')
    plt.grid(True)

    if scatter:
        plt.scatter(data_['MD'], data_[name])
    else:
        plt.plot(data_['MD'], data_[name])

    plt.show()


def plot_multiple(data, name, scatter=False):
    plt.figure(figsize=(8, 6))

    if scatter:
        for i, (title, data_) in enumerate(data):
            plt.scatter(data_['MD'], data_[name], label=title)
    else:
        for i, (title, data_) in enumerate(data):
            plt.plot(data_['MD'], data_[name], label=title)

    plt.title(name)
    plt.xlabel("MD")
    plt.grid(True)
    plt.legend()
    plt.show()
