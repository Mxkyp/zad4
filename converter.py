import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Parametry nagrywania
SAMPLE_RATE = 44100  # częstotliwość próbkowania
CHANNELS = 1  # liczba kanałów (mono)
DURATION = 5  # czas nagrania w sekundach


def max_unsigned(bits):
    return 2**bits


def quantinize(audio_data: np.ndarray, bitResolution):
    # Kwantyzacja (zmniejszenie do bitResolution bitów)
    quantized_audio = np.round(audio_data / max_unsigned(bitResolution)) * max_unsigned(
        bitResolution
    )
    quantized_audio = quantized_audio.astype(np.int16)
    return quantized_audio

    # audio_data to tablica shape=(N,channels); spłaszczamy do 1D


def record(dtype: str):
    print("Nagrywanie...")
    audio_data = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=dtype,
    )
    sd.wait()  # czekaj na zakończenie nagrania
    print("Nagrywanie zakończone.")
    return audio_data


def calculate_snr(original, quantized):
    signal_energy = np.sum(original.astype(float) ** 2)
    noise_energy = np.sum((original.astype(float) - quantized.astype(float)) ** 2)
    return 10 * np.log10(signal_energy / noise_energy)


# Nagrywanie dźwięku
audio_data = record("int16")
quantized_audio = quantinize(audio_data, 8)

# Zapis do WAV
write("original_audio.wav", SAMPLE_RATE, audio_data)
write("quantized_audio.wav", SAMPLE_RATE, quantized_audio)
print("Pliki WAV zapisane: original_audio.wav, quantized_audio.wav")

snr_value = calculate_snr(audio_data, quantized_audio)
print(f"SNR: {snr_value:.2f} dB")
