import numpy as np

def getDType(bitResolution):
    if bitResolution <= 8:
        return np.uint8
    if bitResolution == 16:
        return np.int16
    if bitResolution == 32:
        return np.int32


def quantinize(audio_data: np.ndarray, audioBitDepth, quantBits):
    audio_data_float = audio_data / 2**audioBitDepth # 16 bit audio

    quantized = audio_data_float * 2**quantBits
    dtype = getDType(quantBits)
    quantized = quantized.astype(dtype)

    return quantized 


def calculate_snr(original, quantized):
    signal_energy = np.sum(original.astype(float) ** 2)
    noise_energy = np.sum((original.astype(float) - quantized.astype(float)) ** 2)
    return 10 * np.log10(signal_energy / noise_energy)

