// ============================================================================
// TGDK :: ZenGarden.cpp (Oscillation Layer Integration)
// Author: Sean Tichenor (Black Raven) — © TGDK LLC
// License: TGDK BFE License BFE-TGDK-022ST
// Module: ZenGarden Oscillation Extension
// Description: Introduces harmonic oscillation into the ZenGarden system,
//              applying time-based vector modulation to Mahadevi fields.
// Encryption: QQUAp / HexQUAp
// ============================================================================

#include "ZenGarden.hpp"
#include "Mahadevi.hpp"
#include "Maharaga.hpp"
#include "Culmex.hpp"
#include "OliviaAI.hpp"
#include <cmath>
#include <chrono>

namespace TGDK {

struct Oscillator {
    float frequency;   // ω — oscillation frequency
    float amplitude;   // A — modulation amplitude
    float phase;       // φ — phase offset
    bool active;

    Oscillator(float freq = 0.0102f, float amp = 1.0f, float ph = 0.0f)
        : frequency(freq), amplitude(amp), phase(ph), active(true) {}

    float sample(float t) const {
        return active ? amplitude * std::sin((frequency * t) + phase) : 0.0f;
    }
};

class ZenGarden {
private:
    MahadeviVector baseVector;
    Culmex culmex;
    Oscillator osc;
    float entropyState = 0.0f;

public:
    ZenGarden() : osc(0.0102f, 1.0f, 0.0f) {
        OliviaAI::Log("ZenGarden initialized with harmonic oscillation layer.");
    }

    void ApplyOscillation(float dt) {
        using namespace std::chrono;
        static auto start = high_resolution_clock::now();
        auto now = high_resolution_clock::now();
        float elapsed = duration<float>(now - start).count();

        float modulation = osc.sample(elapsed);
        entropyState += modulation * dt;

        MahadeviVector modulated = baseVector;
        modulated.ApplyTransform(modulation);
        modulated.Normalize();

        // Recursive lineage propagation via Culmex
        culmex.Propagate(modulated.HashString(), modulation, entropyState);

        // AI feedback
        OliviaAI::ClauseEcho("ZenGarden Oscillation",
            "Phase modulation active at ω=" + std::to_string(osc.frequency) +
            ", φ=" + std::to_string(osc.phase) +
            ", entropy Δ=" + std::to_string(entropyState));
    }

    void Harmonize() {
        // Reinforce Mahadevi resonance
        float coherence = std::abs(std::sin(entropyState * M_PI));
        baseVector.Scale(coherence);

        OliviaAI::Echo(
            "ZenGarden::Harmonize() coherence=" + std::to_string(coherence)
        );

        if (coherence > 0.88f) {
            OliviaAI::Emit("ZenGarden reached harmonic equilibrium.");
        }
    }

    void Update(float deltaTime) {
        if (!osc.active) return;
        ApplyOscillation(deltaTime);
        Harmonize();
    }

    void ToggleOscillation(bool state) {
        osc.active = state;
        OliviaAI::Echo(state
            ? "Oscillation resumed."
            : "Oscillation paused."
        );
    }

    void SetFrequency(float freq) {
        osc.frequency = freq;
        OliviaAI::Echo("ZenGarden frequency set to " + std::to_string(freq));
    }

    void SetPhase(float ph) {
        osc.phase = ph;
        OliviaAI::Echo("ZenGarden phase set to " + std::to_string(ph));
    }
};

} // namespace TGDK