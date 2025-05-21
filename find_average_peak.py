import numpy as np
import scipy.io
from scipy.signal import find_peaks

file_paths = [
   # insert file paths here
peaksFz2 = []
propForce = []

# Loop through each file path
for file_path in file_paths:
    mat_data = scipy.io.loadmat(file_path)

    z = mat_data['segGRF']['R'][0, 0]['x'][0, 0][:, 0] 
    z = -z
    peaks, _ = find_peaks(z, height=100)
    
    peak_heights = z[peaks]
    print(peak_heights)
    propForce.append(peak_heights)
    
average_prop_force = np.mean(propForce)

print(f"Average of prop Force: {average_prop_force}")


