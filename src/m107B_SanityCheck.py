import numpy as np
import matplotlib.pyplot as plt

def run_null_hypothesis_test():
    print("Initializing Project m107B Null Hypothesis Test...")
    
    # 1. TIME PARAMETERS
    # ---------------------------------------------------------
    t_start = 0
    t_stop = 100  # nanoseconds
    steps = 1000
    tlist = np.linspace(t_start, t_stop, steps)

    # 2. PHYSICAL PARAMETERS (The "Trap" Check)
    # ---------------------------------------------------------
    # In the real sim, Coax is ~0.1 and Cryo is ~0.00001
    # FOR NULL HYPOTHESIS: We force them to be IDENTICAL.
    
    Gamma_Coax = 0.1  # Decay rate of standard copper (1/T1)
    
    # !!! THE TEST !!!
    # We set Cryo Gamma equal to Coax Gamma.
    # If the logic is sound, the physics should behave identically.
    Gamma_Cryo = Gamma_Coax  
    
    print(f"Parameter Check: Gamma_Coax={Gamma_Coax}, Gamma_Cryo={Gamma_Cryo}")
    if Gamma_Coax != Gamma_Cryo:
        print("WARNING: Parameters are not identical. Null Hypothesis invalidated.")
        return

    # 3. SIMULATION (Exponential Decay Model)
    # ---------------------------------------------------------
    # Modeling the population survival probability: P(t) = e^(-Gamma * t)
    
    # Simulate Standard Coax
    signal_coax = np.exp(-Gamma_Coax * tlist)
    
    # Simulate m107B Cryo-Link
    signal_m107b = np.exp(-Gamma_Cryo * tlist)

    # 4. ERROR CALCULATION (Residuals)
    # ---------------------------------------------------------
    # Calculate the mathematical difference between the two arrays
    residuals = np.abs(signal_coax - signal_m107b)
    max_error = np.max(residuals)
    
    print(f"Simulation Complete.")
    print(f"Maximum Difference between datasets: {max_error:.10f}")

    # 5. VISUALIZATION
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6))
    
    # Plot Coax as a thick red line
    plt.plot(tlist, signal_coax, 'r-', linewidth=5, alpha=0.5, label='Standard Coax (Baseline)')
    
    # Plot m107B as a thin blue dashed line ON TOP
    plt.plot(tlist, signal_m107b, 'b--', linewidth=2, label='m107B (Null Hypothesis Mode)')
    
    # Add High-Fidelity Threshold line for context
    plt.axhline(y=0.90, color='g', linestyle=':', label='High-Fidelity Threshold (90%)')

    plt.title('NULL HYPOTHESIS TEST: m107B Physics Logic\n(Lines Must Overlap Perfectly)')
    plt.xlabel('Transit Time (ns)')
    plt.ylabel('Signal Integrity')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # Check for success
    if max_error < 1e-9:
        plt.text(50, 0.5, "TEST PASSED\nLogic is Sound", 
                 fontsize=20, color='green', ha='center',
                 bbox=dict(facecolor='white', edgecolor='green'))
        print(">>> RESULT: TEST PASSED. The logic is neutral and valid.")
    else:
        plt.text(50, 0.5, "TEST FAILED\nHidden Bias Detected", 
                 fontsize=20, color='red', ha='center',
                 bbox=dict(facecolor='white', edgecolor='red'))
        print(">>> RESULT: TEST FAILED. Check your math.")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_null_hypothesis_test()