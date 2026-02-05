import numpy as np
import matplotlib.pyplot as plt
import sys

# --- m107B Universal Readout Simulator ---

def run_simulation():
    print("--- INITIALIZING SIMULATION ---")
    
    # 1. Generate the "Blobs" (Noisy Data)
    print("Generating data packets...")
    n_shots = 2000
    noise_level = 0.35 
    
    centers = [
        (0, 0), (1, 1), (0, 2), 
        (-1, 1), (-2, 0), (-1, -1)
    ]
    
    X = []
    y = []
    
    for state_idx, (cx, cy) in enumerate(centers):
        ix = np.random.normal(cx, noise_level, n_shots)
        iy = np.random.normal(cy, noise_level, n_shots)
        for i in range(n_shots):
            X.append([ix[i], iy[i]])
            y.append(state_idx)
            
    X = np.array(X)
    y = np.array(y)
    
    # 2. CHOOSE ENGINE (AI vs Simple)
    try:
        from sklearn.svm import SVC
        from sklearn.model_selection import train_test_split
        print(">> SUCCESS: 'sklearn' found.")
        print(">> Running FPGA AI Neural Mode.")
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        clf = SVC(kernel='rbf', C=10, gamma='scale')
        clf.fit(X_train, y_train)
        
        def predict_func(coords):
            return clf.predict(coords)
            
        accuracy = clf.score(X_test, y_test)
        mode_title = "Neural AI Discrimination"
        
    except ImportError:
        print(">> NOTICE: 'sklearn' not found.")
        print(">> Switching to Backup Euclidean Mode.")
        
        def predict_one(px, py):
            dists = []
            for (cx, cy) in centers:
                val = (px-cx)**2 + (py-cy)**2
                dists.append(np.sqrt(val))
            return np.argmin(dists)
        
        def predict_func(coords):
            res = []
            for p in coords:
                res.append(predict_one(p[0], p[1]))
            return res

        correct = 0
        preds = predict_func(X)
        for i in range(len(X)):
            if preds[i] == y[i]: correct += 1
        accuracy = correct / len(X)
        mode_title = "Standard Distance Logic"

    print(f"Fidelity Achieved: {accuracy:.2%}")

    # 3. VISUALIZATION
    print("--- RENDERING GRAPH ---")
    plt.figure(figsize=(10, 8))
    
    # Plot Scatter
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
    for i in range(6):
        subset = X[y == i]
        lbl = f"State {i}"
        # Plot only first 300 points
        plt.scatter(subset[:300, 0], subset[:300, 1], c=colors[i], alpha=0.4, label=lbl, s=10)

    # Plot Background Decision Boundaries
    h = .05 
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    
    # Create meshgrid
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    
    # Predict over the meshgrid
    Z = np.array(predict_func(np.c_[xx.ravel(), yy.ravel()]))
    Z = Z.reshape(xx.shape)
    
    # Draw contours
    plt.contourf(xx, yy, Z, alpha=0.2, levels=np.arange(-0.5, 6, 1), colors=colors)
    
    # Labels
    plt.title(f"m107B Readout: {mode_title} (Fidelity: {accuracy:.2%})")
    plt.xlabel("In-Phase (I)")
    plt.ylabel("Quadrature (Q)")
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    print(">> DONE. Displaying Plot.")
    plt.show()

if __name__ == "__main__":
    run_simulation()