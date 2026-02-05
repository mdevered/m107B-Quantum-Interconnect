import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, mesolve, destroy, expect

def run_decay_check():
    print("--- Starting m107B Decay Validation ---")
    
    # 1. System Constants
    N = 6  # 0-5 Manifold
    times = np.linspace(0, 50, 100)
    
    # 2. Operators
    a = destroy(N)
    H = a.dag() * a 
    
    # 3. Initial State: Max Energy (State 5)
    psi0 = basis(N, 5)
    
    # 4. Define Scenarios
    # Scenario A: Standard Urban Fiber (0.08 decay)
    c_ops_A = [np.sqrt(0.08) * a]
    
    # Scenario B: m107B with Purcell Filter (0.02 decay)
    c_ops_B = [np.sqrt(0.02) * a]
    
    # 5. Run Simulations
    print("1. Simulating Standard Urban Fiber (m107A environment)...")
    result_A = mesolve(H, psi0, times, c_ops_A, [])
    
    print("2. Simulating Purcell-Protected Hardware (m107B environment)...")
    result_B = mesolve(H, psi0, times, c_ops_B, [])
    
    # 6. Extract Data
    # This operator checks "How much of State 5 is left?"
    projector_5 = basis(N, 5) * basis(N, 5).dag()
    
    surv_A = expect(projector_5, result_A.states)
    surv_B = expect(projector_5, result_B.states)
    
    print("3. Generating Comparison Graph...")

    # 7. Visualization
    plt.figure(figsize=(10, 6))
    
    # Plotting
    plt.plot(times, surv_A, 'r--', linewidth=2, label='Standard Fiber (Rate 0.08)')
    plt.plot(times, surv_B, 'b-', linewidth=3, label='m107B Purcell (Rate 0.02)')
    
    # Threshold Line
    plt.axhline(y=0.10, color='k', linestyle=':', alpha=0.5, label='Data Loss Threshold')
    
    plt.title("m107B Hardware Validation: Signal Retention", fontsize=14)
    plt.xlabel("Time (Arbitrary Units)", fontsize=12)
    plt.ylabel("State 5 Retention Probability", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Text Annotation (Fixed to prevent Syntax Error)
    ratio = surv_B[40] / (surv_A[40] + 1e-9) 
    plt.text(25, 0.5, f"m107B Advantage:\n{ratio:.1f}x stronger signal", bbox=dict(facecolor='white', alpha=0.9))
    
    print("Done. Displaying Plot.")
    plt.show()

if __name__ == "__main__":
    run_decay_check()