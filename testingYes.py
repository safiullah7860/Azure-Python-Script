import matplotlib.pyplot as plt

# Temperatures (sorted)
temperatures = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Accuracy for each model (Gp3.5, Gpt4, Gpt4_32)
accuracy = {
    'Gp3.5':   [76.57, 75.71, 75.55, 74.22, 73.12, 67.55, 67.32, 63.00, 62.46, 59.17, 58.31],
    'Gpt4':    [91.38, 90.99, 91.30, 91.69, 91.11, 91.85, 90.93, 90.00, 89.34, 90.51, 89.81],
    'Gpt4_32': [91.38, 91.14, 91.07, 91.30, 90.99, 90.36, 90.99, 92.00, 89.42, 90.60, 90.36]
}

# Create the plot
plt.figure(figsize=(12, 8))
plt.title("AllYes Experiment", fontsize=16)
plt.xlabel("Temperature", fontsize=14)
plt.ylabel("Accuracy (%)", fontsize=14)

# Plot accuracy for each model
for model, accuracies in accuracy.items():
    plt.plot(temperatures, accuracies, marker='o', label=model)

# Add legend with better placement
plt.legend(title="Models", loc='lower left', fontsize=12, title_fontsize='13')

# Set grid with specific style
plt.grid(True, linestyle='--', alpha=0.7)

# Customize ticks
plt.xticks(temperatures, fontsize=12)
plt.yticks(fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
