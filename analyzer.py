import numpy as np

def max_unsigned(bits):
    return 2**bits


def quantinize(audio_data: np.ndarray, bitResolution):
    audio_data_float = audio_data / 2**16 # 16 bit audio

    audio_data_8bit = audio_data_float * 2**bitResolution
    audio_data_8bit = audio_data_8bit.astype(int)

    return audio_data_8bit 


def calculate_snr(original, quantized):
    signal_energy = np.sum(original.astype(float) ** 2)
    noise_energy = np.sum((original.astype(float) - quantized.astype(float)) ** 2)
    return 10 * np.log10(signal_energy / noise_energy)

