import numpy as np
import matplotlib.pyplot as plt

def run_readout_speed_test():
    print("--- m107B Readout Latency: Standard HEMT vs TWPA ---")
    
    # Time steps (nanoseconds)
    t = np.linspace(0, 1000, 1000) 
    
    # 1. The Signal (State 5)
    # The signal is a constant voltage arriving at the detector
    signal_strength = 1.0 
    
    # 2. The Noise Levels
    # Standard HEMT Amp adds a lot of noise
    noise_hemt = 3.0
    # TWPA is "Quantum Limited" (very low noise)
    noise_twpa = 0.5
    
    # 3. Simulation: Integrating the signal over time
    # The longer we measure, the more the noise averages out (1/sqrt(t))
    
    # We simulate the "Confidence Level" (Signal-to-Noise Ratio over time)
    # SNR improves with square root of time
    snr_standard = (signal_strength / noise_hemt) * np.sqrt(t)
    snr_twpa = (signal_strength / noise_twpa) * np.sqrt(t)
    
    # 4. The "Confidence Threshold"
    # We need an SNR of 5.0 to be "99.9% Sure" of the data
    threshold = 5.0
    
    # Find the crossing points (where we are fast enough to read)
    # Using argmax to find first index where condition is true
    try:
        time_std = next(x for x, val in enumerate(snr_standard) if val >= threshold)
    except StopIteration:
        time_std = 1000 # Off the chart
        
    try:
        time_twpa = next(x for x, val in enumerate(snr_twpa) if val >= threshold)
    except StopIteration:
        time_twpa = 1000

    print(f"Standard Readout Time: {time_std} ns")
    print(f"TWPA Readout Time:     {time_twpa} ns")
    
    # 5. Visualization
    plt.figure(figsize=(10, 6))
    
    plt.plot(t, snr_standard, 'r--', label='Standard HEMT Amp (Noisy)')
    plt.plot(t, snr_twpa, 'b-', linewidth=3, label='With TWPA (Quiet)')
    
    plt.axhline(y=threshold, color='k', linestyle=':', label='99.9% Confidence Threshold')
    
    # Mark the speedup
    plt.scatter([time_std], [threshold], color='red', s=100, zorder=5)
    plt.scatter([time_twpa], [threshold], color='blue', s=100, zorder=5)
    
    plt.title("m107B Readout Bottleneck Analysis", fontsize=14)
    plt.xlabel("Integration Time (ns)", fontsize=12)
    plt.ylabel("Readout Fidelity (SNR)", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    speedup = time_std / time_twpa
    plt.text(time_std + 20, threshold - 1, f"TWPA is {speedup:.1f}x Faster", 
             bbox=dict(facecolor='white', alpha=0.9))
    
    plt.show()

if __name__ == "__main__":
    run_readout_speed_test()