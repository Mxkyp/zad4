run:
	python3 converter.py $(f) $(b) $(q)

po:
	aplay original.wav

pq:
	aplay quantized.wav

clean:
	rm *.wav
