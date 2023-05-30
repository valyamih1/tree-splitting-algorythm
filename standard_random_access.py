import numpy as np
import matplotlib.pyplot as plt


def simulate_LTE_random_access(n, m, t):
    device_status = np.zeros(n)  # 0 = not connected, 1 = connected
    device_delays = np.zeros(n)  # delay for each device
    contention_window = 20  # random backoff time in ms
    response_time = 3  # response time in ms
    contention_resolution = 48  # contention resolution time in ms
    for time in np.arange(0, t, response_time + contention_resolution):
        # devices that are not yet connected select a random access channel
        selections = np.random.choice(m, n) + 1
        for i in range(n):
            if device_status[i] == 0:  # if the device is not yet connected
                backoff = np.random.randint(contention_window)  # random backoff
                # check if any other device selected the same channel
                same_channel = np.where(selections == selections[i])[0]
                if len(same_channel) == 1:  # no other device selected the same channel
                    device_status[i] = 1  # the device is now connected
                    device_delays[i] = time
                else:
                    device_delays[i] += backoff + response_time + contention_resolution
    successful_devices = np.sum(device_status)
    mean_throughput = successful_devices / t
    mean_delay = np.mean(device_delays[device_status == 1])
    return successful_devices, mean_throughput, mean_delay
def graphs():
    n = 500  # number of devices
    m = 54  # number of random access channels
    t = 100000  # total simulation time in ms
    successful_devices_steps = []
    throughput_steps = []
    delay_steps = []
    K = np.arange(1, 506, 5)
    for k in K:
        successful_devices, mean_throughput, mean_delay = simulate_LTE_random_access(k, m, t)
        successful_devices_steps.append(successful_devices)
        throughput_steps.append(mean_throughput)
        delay_steps.append(mean_delay)
        print("Number of successful devices:", successful_devices)
        print("Mean throughput:", mean_throughput)
        print("Mean delay for one device in ms:", mean_delay)

    plt.figure(1)
    plt.plot(K, successful_devices_steps, label='devices', marker=".", linewidth=2, markersize=7, linestyle='-.')
    plt.xlabel('Number of devices')
    plt.ylabel('Number of successful devices')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.figure(2)
    plt.plot(K, throughput_steps, label='throughput', marker=".", linewidth=2, markersize=7, linestyle=':')
    plt.xlabel('Number of devices')
    plt.ylabel('Throughput')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.figure(3)
    plt.plot(K, delay_steps, label='delay', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.xlabel('Number of devices')
    plt.ylabel('Delay, ms')
    plt.grid(True)
    plt.legend()
    plt.show()


def theory():
    number_of_devices = 30000
    number_of_preambles = 54
    M = np.arange(1, 301, 1)
    p_0s = []
    p_1s = []
    p_2s = []
    for number_of_devices in M:
        p_0 = pow(1 - 1 / number_of_preambles, number_of_devices)
        p_1 = (number_of_devices/number_of_preambles) * pow(1 - 1/number_of_preambles, number_of_devices - 1)
        p_2 = 1 - p_0 - p_1
        p_0s.append(number_of_preambles * p_1)
        p_1s.append(number_of_preambles * (1 - p_0))
        p_2s.append(number_of_preambles * p_2)

    plt.figure(1)
    plt.plot(M, p_0s, label='successful preambles', linewidth=2, markersize=7, linestyle='-.')
    plt.plot(M, p_1s, label='all detected preambles', linewidth=2, markersize=7, linestyle='--')
    plt.plot(M, p_2s, label='wasted preambles', linewidth=2, markersize=7, linestyle=':')
    plt.xlabel('Number of devices')
    plt.ylabel('Number of preambles')
    plt.grid(True)
    plt.legend()
    plt.show()