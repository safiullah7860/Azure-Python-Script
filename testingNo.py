import matplotlib.pyplot as plt

# Temperatures (sorted)
temperatures = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Accuracy for each model (Gp3.5, Gpt4, Gpt4_32)
accuracy = {
    'Gp3.5':   [83.94, 85.70, 84.26, 85.18, 85.35, 85.7, 85.64, 88.0, 86.60, 86.97, 87.85],  # Order adjusted to match temperatures
    'Gpt4':    [80.69, 80.37, 80.56, 80.29, 80.23, 80.6, 80.67,      79.8, 81.15, 81.07, 80.86], # Order adjusted to match temperatures
    'Gpt4_32': [80.78, 80.78, 80.62, 80.48, 80.37, 81.1, 80.51,      80.0, 81.01, 80.97, 80.99]  # Order adjusted to match temperatures
}

# Create the plot
plt.figure(figsize=(12, 8))
plt.title("AllNo Experiment", fontsize=16)
plt.xlabel("Temperature", fontsize=14)
plt.ylabel("Accuracy (%)", fontsize=14)

# Plot accuracy for each model
for model, accuracies in accuracy.items():
    plt.plot(temperatures, accuracies, marker='o', label=model)

# Add legend with better placement
plt.legend(title="Models", loc='center right', fontsize=12, title_fontsize='13')

# Set grid with specific style
plt.grid(True, linestyle='--', alpha=0.7)

# Customize ticks
plt.xticks(temperatures, fontsize=12)
plt.yticks(fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
