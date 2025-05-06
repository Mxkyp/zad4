import sounddevice as sd
import numpy as np
import analyzer as a
import visualiser as vis
import sys
from scipy.io.wavfile import write

CHANNELS = 1  #  (mono)
DURATION = 3  # record duration 

def record(bitDepth: int, sample_rate: int):
    print("Nagrywanie...")
    audio_data = sd.rec(
        int(DURATION * sample_rate),
        samplerate=sample_rate,
        channels=CHANNELS,
        dtype="int"+str(bitDepth),
    )
    sd.wait()  # czekaj na zakończenie nagrania
    print("Nagrywanie zakończone.")
    return audio_data

"""1-script 2-frequency, 3-depth, 4-quantization bits)"""
def checkInput():
    if len(sys.argv) != 4:
        raise Exception("wrong argc")


# Nagrywanie dźwięku
checkInput()
sample_rate = int(sys.argv[1])
bitDepth = int(sys.argv[2])
quantBits = int(sys.argv[3])
audio_data = record(bitDepth, sample_rate)
quantized_audio = a.quantinize(audio_data, bitDepth, quantBits)

# Zapis do WAV
write("original.wav", sample_rate, audio_data)
write("quantized.wav", sample_rate, quantized_audio)
print("Pliki WAV zapisane: original.wav, quantized.wav")
vis.plotSoundWave(vis.Sample("original", audio_data, sample_rate, bitDepth), vis.Sample("quantized", quantized_audio, sample_rate, quantBits))

reconstructed = a.reconstruct(quantized_audio, quantBits, bitDepth)

snr_value = a.calculate_snr(audio_data, reconstructed)
mse_value = a.calculate_mse(audio_data, reconstructed)

print(f"SNR: {snr_value:.2f} dB")
print(f"MSE: {mse_value:.2f} ")
