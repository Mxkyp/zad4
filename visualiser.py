import matplotlib.pyplot as plt
import numpy as np

class Sample: 
    def __init__(self, sampleName: str, data: np.ndarray, frequency: int, bitDepth: int):
        self.name = sampleName
        self.data = data
        self.freq = frequency
        self.bitDepth = bitDepth


def plotSoundWave(*samples):
    total_plots = len(samples) + 1  # one extra for combined plot
    plt.figure(figsize=(20, 4 * total_plots))  # dynamic height

    # Individual subplots
    for idx, sample in enumerate(samples, start=1):
        plt.subplot(total_plots, 1, idx)
        plt.plot(sample.data, label=sample.name)
        plt.ylim(-(2**(sample.bitDepth-1)), 2**(sample.bitDepth-1))  # Scale to full int16 range
        plt.ylabel("Amplitude")
        plt.title(f"Sample: {sample.name}")
        plt.legend()

    # Combined subplot
    plt.subplot(total_plots, 1, total_plots)
    for sample in samples:
        plt.plot(sample.data, label=sample.name)
        plt.ylim(-(2**(sample.bitDepth-1)), 2**(sample.bitDepth-1))  # Scale to full int16 range
    plt.ylabel("Amplitude")
    plt.title("All Samples Combined")
    plt.legend()

    plt.tight_layout()
    plt.show()
