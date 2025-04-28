import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write


def quantinize(audio_data: np.ndarray):
    # audio_data to tablica shape=(N,channels); spłaszczamy do 1D
    audio_data = audio_data.flatten()
    # Kwantyzacja (zmniejszenie do 8 bitów)
    # dzielimy przez 256, zaokrąglamy, mnożymy z powrotem
    quantized_audio = np.round(audio_data / 256) * 256
    quantized_audio = quantized_audio.astype(np.int16)
    return quantized_audio


def record():
    print("Nagrywanie...")
    audio_data = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
    )
    sd.wait()  # czekaj na zakończenie nagrania
    print("Nagrywanie zakończone.")
    return audio_data


def calculate_snr(original, quantized):
    signal_energy = np.sum(original.astype(float) ** 2)
    noise_energy = np.sum((original.astype(float) - quantized.astype(float)) ** 2)
    return 10 * np.log10(signal_energy / noise_energy)


# Parametry nagrywania
SAMPLE_RATE = 44100  # częstotliwość próbkowania
CHANNELS = 1  # liczba kanałów (mono)
DURATION = 1  # czas nagrania w sekundach
DTYPE = "int16"  # 16-bitowe próbki

# Nagrywanie dźwięku
audio_data = record()
quantized_audio = quantinize(audio_data)

# Zapis do WAV
write("original_audio.wav", SAMPLE_RATE, audio_data)
write("quantized_audio.wav", SAMPLE_RATE, quantized_audio)
print("Pliki WAV zapisane: original_audio.wav, quantized_audio.wav")

# Obliczenie SNR
snr_value = calculate_snr(audio_data, quantized_audio)
print(f"SNR: {snr_value:.2f} dB")
