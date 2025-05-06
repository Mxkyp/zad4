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

def convert_bit_depth(audio_in: np.ndarray, src_bit_depth: int, target_bit_depth: int):
    # Step 1: Normalize input to float [-1.0, 1.0]
    max_src_value = (2 ** (src_bit_depth - 1)) - 1
    audio_float = audio_in.astype(np.float32) / max_src_value

    # Step 2: Scale to target bit depth
    max_target_value = (2 ** (target_bit_depth - 1)) - 1
    audio_scaled = np.clip(audio_float * max_target_value, -max_target_value, max_target_value)

    # Step 3: Convert to appropriate int type
    audio_scaled = audio_scaled.astype(get_dtype_for_bit_depth(target_bit_depth))

    return audio_scaled

def get_dtype_for_bit_depth(bit_depth: int):
    if bit_depth <= 8:
        return np.int8
    elif bit_depth <= 16:
        return np.int16
    elif bit_depth <= 32:
        return np.int32
    else:
        raise ValueError("Unsupported bit depth")

def calculate_snr(original, quantized, bitDepth, quantBits):
    
    # Reconstruct quantized signal back to original bit depth
    reconstructed = convert_bit_depth(quantized, quantBits, bitDepth)

    # Always subtract directly
    noise = original.astype(np.float64) - reconstructed.astype(np.float64)

    # Signal and noise power (use float to avoid overflow)
    signal_power = np.mean(original.astype(np.float64) ** 2)
    noise_power = np.mean(noise ** 2)

    # Avoid division by zero
    if noise_power == 0:
        return np.inf  # perfect SNR

    snr = 10 * np.log10(signal_power / noise_power)

    return snr
