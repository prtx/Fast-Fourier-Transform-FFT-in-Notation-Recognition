import cmath
from scipy.io.wavfile import read
from matplotlib import pyplot
from pylab import specgram
from math import log
import numpy as np


note_list = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#',]

def freq_2_note(freq):
		
    SEMITONE = 1.059463
    try:
	    interval = int(round(log(freq/440.0, SEMITONE))) % 12
	    return note_list[interval]
    except Exception:
		pass

def omega(p, q):
	return cmath.exp((2.0 * cmath.pi * 1j * q) / p)

def fft(signal):
	
	n = len(signal)
	if n == 1:
		return signal
	else:
		Feven = fft([signal[i] for i in xrange(0, n, 2)])
		Fodd = fft([signal[i] for i in xrange(1, n, 2)])
		combined = [0] * n
        for m in xrange(n/2):
            combined[m] = Feven[m] + omega(n, -m) * Fodd[m]
            combined[m + n/2] = Feven[m] - omega(n, -m) * Fodd[m]
	        
        return combined
	
def main():
	
	frame_rate, amplitude = read('G.wav')
        if type(amplitude[0]) == np.ndarray:
		amplitude = (amplitude[:,0] + amplitude[:,1])/2
	frequencies = [ freq_2_note(abs(freq)) for freq in fft(amplitude)]
	note_count = []
	
	for note in note_list:
		note_count.append(frequencies.count(note))
	
	print 'Notation is', note_list[note_count.index(max(note_count))]
		

if __name__ == '__main__':
	main()
