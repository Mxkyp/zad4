import sounddevice as sd
import numpy as np
import analyzer as a
import visualiser as vis
from scipy.io.wavfile import write

# Parametry nagrywania
SAMPLE_RATE = 44100  # częstotliwość próbkowania
CHANNELS = 1  # liczba kanałów (mono)
DURATION = 5  # czas nagrania w sekundach


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


# Nagrywanie dźwięku
audio_data = record("int16")
quantized_audio = a.quantinize(audio_data, 8)

# Zapis do WAV
write("original_audio.wav", SAMPLE_RATE, audio_data)
write("quantized_audio.wav", SAMPLE_RATE, quantized_audio)
print("Pliki WAV zapisane: original_audio.wav, quantized_audio.wav")
vis.plotSoundWave(vis.Sample("original", audio_data, SAMPLE_RATE, 16), vis.Sample("quantized", quantized_audio, SAMPLE_RATE, 16))

snr_value = a.calculate_snr(audio_data, quantized_audio)
print(f"SNR: {snr_value:.2f} dB")
