# nanoparticle_toolkit.py
# OliviaAI™ & TGDK™ | All Rights Reserved.
# Copyright © Sean Tichenor, TGDK.
# License: BFE-TGDK-022ST | Issued: March 21, 2025

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import hashlib

class TGDKNanoparticleLab:
    def __init__(self):
        self.nanoparticles = []
        self.properties = []

    def synthesize_nanoparticle(self, size, shape, material):
        """Simulates nanoparticle synthesis clearly."""
        nanoparticle = {
            "size": size,
            "shape": shape,
            "material": material,
            "reactivity": self.calculate_reactivity(size, shape, material),
        }
        self.nanoparticles.append(nanoparticle)
        print(f"[NanoparticleLab] Synthesized nanoparticle: {nanoparticle}")
        return nanoparticle

    def calculate_reactivity(self, size, shape, material):
        """Clearly calculates reactivity based on nanoparticle parameters."""
        material_hash = int(hashlib.sha256(material.encode()).hexdigest(), 16)
        reactivity = (size * len(shape) * material_hash) % 100
        print(f"[NanoparticleLab] Calculated reactivity ({material}): {reactivity}")
        return reactivity

    def visualize_nanoparticles(self):
        """Generates clear, informative 3D visualizations of nanoparticles."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for nanoparticle in self.nanoparticles:
            ax.scatter(
                nanoparticle["size"],
                len(nanoparticle["shape"]),
                nanoparticle["reactivity"],
                label=f'{nanoparticle["material"]} ({nanoparticle["shape"]})',
                s=50  # clearly visible size
            )

        ax.set_title("3D Visualization of Nanoparticles")
        ax.set_xlabel("Size")
        ax.set_ylabel("Shape Complexity")
        ax.set_zlabel("Material Reactivity")
        ax.legend()
        plt.show()

    def analyze_properties(self):
        """Analyzes synthesized nanoparticle properties clearly."""
        self.properties = [
            {
                "size": np["size"],
                "shape": np["shape"],
                "material": np["material"],
                "reactivity": np["reactivity"],
            }
            for np in self.nanoparticles
        ]
        print(f"[NanoparticleLab] Analyzed properties: {self.properties}")
        return self.properties


# TGDKexpo clearly integrates NanoparticleLab
class TGDKexpo:
    def __init__(self):
        self.nano_lab = TGDKNanoparticleLab()
        self.expo_data = []

    def integrate_nano_lab(self, size, shape, material):
        """Integrates nanoparticles clearly into TGDKexpo."""
        nanoparticle = self.nano_lab.synthesize_nanoparticle(size, shape, material)
        self.expo_data.append(nanoparticle)
        print(f"[TGDKexpo] Integrated nanoparticle: {nanoparticle}")
        return nanoparticle

    def visualize_expo_data(self):
        """Visualizes nanoparticle data clearly within TGDKexpo."""
        self.nano_lab.visualize_nanoparticles()

    def export_data(self, filename="tgdkexpo_nanoparticles.json"):
        """Exports nanoparticle data clearly to a JSON file."""
        with open(filename, "w") as file:
            json.dump(self.expo_data, file, indent=4)
        print(f"[TGDKexpo] Data exported clearly to {filename}")


# Example Usage (for standalone testing)
if __name__ == "__main__":
    # Initialize TGDKexpo with NanoparticleLab
    tgdk_expo = TGDKexpo()

    # Synthesize and integrate nanoparticles
    tgdk_expo.integrate_nano_lab(size=5, shape="sphere", material="gold")
    tgdk_expo.integrate_nano_lab(size=10, shape="cube", material="silver")
    tgdk_expo.integrate_nano_lab(size=7, shape="rod", material="platinum")

    # Visualize data
    tgdk_expo.visualize_expo_data()

    # Export data
    tgdk_expo.export_data()