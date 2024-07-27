import matplotlib.pyplot as plt

# Temperatures (sorted)
temperatures = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Accuracy for each model (Gp3.5, Gpt4, Gpt4_32)
accuracy = {
    'Gp3.5': [80.25, 80.71, 79.91, 79.7, 79.23, 76.62, 76.48, 75.5, 74.53, 73.07, 73.08],
    'Gpt4':    [86.03, 85.68, 85.93, 85.99, 85.67, 86.22, 85.8, 84.9, 85.25, 85.79, 85.34],
    'Gpt4_32': [86.08, 85.96, 85.84, 85.89, 85.68, 85.73, 85.75, 86.0, 85.22, 85.78, 85.67],
    'Gpt4-o':  [86.05, 86.4, 86.37, 85.7, 85.81, 86.09, 85.31, 85.81, 85.38, 84.91, 84.91]
    }

# Create the plot
plt.figure(figsize=(12, 8))
plt.title("GPT Models' Average Performance", fontsize=16)
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
