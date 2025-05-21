from scipy.io import loadmat
from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

file_path = '' # insert file path here


data = loadmat(file_path)

for side in ['R', 'L']:
    side_data = grf[side]
    print(f"Processing side: {side}")
    
    for i in range(side_data.shape[0]):
        entry = side_data[i, 0]
        
        x = entry['x'][0, 0]
        y = entry['y'][0, 0]
        z = entry['z'][0, 0]
        
x = grf_R[0, 0]['x'][0, 0]
y = grf_R[0, 0]['y'][0, 0]
z = grf_R[0, 0]['z'][0, 0][:, 0] 

peaks, properties = find_peaks(z, height=100, distance=10, prominence=0.5)
print("Peak indices:", peaks)
print("Peak values:", z[peaks])

prominence_values = properties['prominences']
max_prominence_idx = np.argmax(prominence_values)

max_prominence_peak = peaks[max_prominence_idx]
print(f"The peak with the highest prominence is at index {max_prominence_peak}, with a prominence of {prominence_values[max_prominence_idx]}")

plt.figure(figsize=(10, 6))
plt.plot(z, label='Z Data')
plt.plot(peaks, z[peaks], "x", label='Peaks', color='red')  # Mark peaks with 'x'
plt.title("Peak Detection in Z Data")
plt.xlabel("Time (Samples)")
plt.ylabel("Amplitude")
plt.legend()

# Annotate each peak
for i, peak in enumerate(peaks):
    plt.annotate(f"{z[peak]:.2f}", (peak, z[peak]), textcoords="offset points", xytext=(0, 10), ha='center')

plt.show()

# **************************************************************************************************
# finding the vertical loading rate 

sampling_rate = 2500 
time_step = 1 / sampling_rate  
threshold = 10  

stance_phase = z > threshold
z_stance = z[stance_phase]

time_stance = np.arange(len(z_stance)) * time_step

loading_phase_end = np.argmax(z_stance)  
z_loading = z_stance[:loading_phase_end]
time_loading = time_stance[:loading_phase_end]

slope, intercept, r_value, p_value, std_err = linregress(time_loading, z_loading)
print(f"Linear Regression Slope: {slope:.2f} N/s")
print(f"Intercept: {intercept:.2f} N")

z_fit = slope * time_loading + intercept

plt.figure(figsize=(10, 6))
plt.plot(time_loading, z_loading, label="Loading Phase (GRF)", color="blue")
plt.plot(time_loading, z_fit, label="Linear Regression Line", color="red", linestyle="--")
plt.title("Vertical GRF and Linear Regression")
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")
plt.legend()
plt.show()

print(z[peaks[0]])
