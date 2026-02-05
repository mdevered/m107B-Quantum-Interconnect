import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, mesolve, destroy, expect

def run_cryolink_sim():
    print("--- m107B Phase 2: Cryogenic Waveguide Validation ---")
    
    # 1. System Constants
    N = 6  # 0-5 Manifold
    # We simulate a longer timeframe (100ns) to show long-distance stability
    times = np.linspace(0, 100, 200) 
    
    # 2. Operators
    a = destroy(N)
    H = a.dag() * a 
    
    # 3. Initial State: Max Energy (State 5)
    psi0 = basis(N, 5)
    
    # 4. Define Scenarios
    # Scenario A: Standard SMA Coaxial Cable (Lossy)
    # Attenuation ~5dB/meter -> represents significant loss over distance
    decay_coax = 0.1
    c_ops_coax = [np.sqrt(decay_coax) * a]
    
    # Scenario B: m107B Superconducting Waveguide (Lossless)
    # Niobium-Titanium at 4 Kelvin -> Near zero resistance
    decay_waveguide = 0.001 # Effectively zero on this timescale
    c_ops_waveguide = [np.sqrt(decay_waveguide) * a]
    
    # 5. Run Simulations
    print("1. Simulating Standard Coax Link...")
    result_coax = mesolve(H, psi0, times, c_ops_coax, [])
    
    print("2. Simulating Cryo-Waveguide Link...")
    result_waveguide = mesolve(H, psi0, times, c_ops_waveguide, [])
    
    # 6. Extract Data
    projector_5 = basis(N, 5) * basis(N, 5).dag()
    surv_coax = expect(projector_5, result_coax.states)
    surv_waveguide = expect(projector_5, result_waveguide.states)
    
    print("3. Generating Comparison Graph...")

    # 7. Visualization
    plt.figure(figsize=(10, 6))
    
    # Plotting
    plt.plot(times, surv_coax, 'r--', linewidth=2, label='Standard Coax (Lossy)')
    plt.plot(times, surv_waveguide, 'b-', linewidth=4, label='m107B Cryo-Link (Superconducting)')
    
    # Threshold Line
    plt.axhline(y=0.90, color='g', linestyle=':', alpha=0.5, label='High-Fidelity Threshold (90%)')
    
    plt.title("Interconnect Performance: Coax vs. Cryo-Waveguide", fontsize=14)
    plt.xlabel("Transit Time (ns)", fontsize=12)
    plt.ylabel("Signal Integrity (State 5)", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Annotation
    # Calculate difference at end of simulation
    final_coax = surv_coax[-1]
    final_wave = surv_waveguide[-1]
    
    # Avoid divide by zero if coax is dead
    if final_coax < 0.0001: final_coax = 0.0001 
    
    factor = final_wave / final_coax
    
    plt.text(40, 0.5, f"Cryo-Link Advantage:\nSignal is {factor:.0f}x stronger\nafter 100ns", 
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='blue'))
    
    print("Done. Displaying Plot.")
    plt.show()

if __name__ == "__main__":
    run_cryolink_sim()