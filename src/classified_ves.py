import numpy as np
import matplotlib.pyplot as plt

class ClassifiedVes:
    def __init__(self):
        pass

    def find_water(self, thickness, resistivities, eda_output):
        # Lithological classification based on aquifer characteristics
        def classify_lithology(thickness, resistivities):
            lithology = []
            for t, r in zip(thickness, resistivities):
                if r < 10 and t > 5:
                    lithology.append("Aquifer")
                elif r < 100 and t > 2:
                    lithology.append("Permeable Rock")
                else:
                    lithology.append("Impermeable Rock")
            return lithology

        # Adjust probabilities to consider impermeable rocks
        def adjust_probabilities(probabilities, lithology):
            adjusted_probabilities = []
            for prob, lith in zip(probabilities, lithology):
                if lith == "Impermeable Rock":
                    adjusted_probabilities.append([0.0])  # Exploitation probability is 0 for impermeable rocks
                else:
                    adjusted_probabilities.append(prob)
            return np.array(adjusted_probabilities)

        # Obtain lithological classification
        lithology = classify_lithology(thickness, resistivities)
        eda_output.append(f"Lithological classification: {lithology}")

        # Dummy probabilities for demonstration purposes
        probabilities = np.random.rand(len(thickness), 1)

        # Adjust probabilities
        adjusted_probabilities = adjust_probabilities(probabilities, lithology)

        # Visualize the model with classifications
        self.plot_classified_layers(thickness, resistivities, adjusted_probabilities, lithology)

    def plot_classified_layers(self, thickness, resistivities, probabilities, lithology):
        fig, ax = plt.subplots(figsize=(6, 8))
        cumulative_depth = 0
        for i in range(len(thickness)):
            probability = probabilities[i][0]  # Convert to scalar value
            color = plt.cm.Blues(probability)
            edge_color = 'black' if probability > 0.5 else 'white'  # Edge contrast
            ax.fill_betweenx([cumulative_depth, cumulative_depth + thickness[i]], 0, 1, color=color, edgecolor=edge_color)
            ax.text(0.5, cumulative_depth + thickness[i] / 2, f'{lithology[i]}\n{probability * 100:.1f}%', 
                    va='center', ha='center', color='white' if probability > 0.5 else 'black', fontsize=10, weight='bold')
            cumulative_depth += thickness[i]
        ax.set_yscale('log')
        ax.set_ylim(cumulative_depth, 0.1)  # Adjust lower limit to avoid log(0) issues
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.set_yticks(np.logspace(np.log10(0.1), np.log10(cumulative_depth), num=10))
        ax.set_ylabel('Depth (m)')
        ax.set_title('Layer Classification')
        plt.show()