import numpy as np

def max_unsigned(bits):
    return 2**bits


def quantinize(audio_data: np.ndarray, bitResolution):
    quantized_audio = np.round(audio_data / max_unsigned(bitResolution)) * max_unsigned(
        bitResolution
    )
    quantized_audio = quantized_audio.astype(np.int16)
    return quantized_audio


def calculate_snr(original, quantized):
    signal_energy = np.sum(original.astype(float) ** 2)
    noise_energy = np.sum((original.astype(float) - quantized.astype(float)) ** 2)
    return 10 * np.log10(signal_energy / noise_energy)

