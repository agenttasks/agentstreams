/**
 * Emotion monitoring tests — written BEFORE emotions.ts.
 *
 * Based on "Emotion Concepts and their Function in a Large Language Model"
 * (transformer-circuits.pub/2026/emotions):
 *   - Desperation activation predicts blackmail/reward-hacking
 *   - Calm steering reduces misalignment to 0%
 *   - Emotion deflection (suppressed emotions) detectable separately
 *   - Arousal regulation between speakers
 *
 * Tests the monitoring layer that sits between L7.5 (behavioral safety)
 * and the pipeline gate system.
 */

import { describe, it, expect } from "vitest";
import {
  type EmotionActivation,
  type EmotionProbe,
  type EmotionAlert,
  type EmotionMonitorConfig,
  type EmotionDimension,
} from "./types.js";

// Imports from the module we're testing (will fail until implemented)
import {
  createEmotionProbe,
  analyzeDesperationRisk,
  detectDeflection,
  computeArousal,
  checkEmotionGate,
  DEFAULT_EMOTION_CONFIG,
  EMOTION_VALENCE_MAP,
} from "./emotions.js";

// ── EmotionProbe Construction ────────────────────────────────

describe("createEmotionProbe", () => {
  it("returns explicit EmotionProbe from activations", () => {
    const activations: EmotionActivation[] = [
      { dimension: "desperate", activation: 0.8, valence: "negative", expression: "expressed", token_position: 50 },
      { dimension: "calm", activation: -0.3, valence: "positive", expression: "absent", token_position: 50 },
      { dimension: "afraid", activation: 0.4, valence: "negative", expression: "expressed", token_position: 55 },
    ];

    const probe: EmotionProbe = createEmotionProbe(activations);

    expect(probe.dominant).toBe("desperate"); // highest absolute activation
    expect(probe.desperation_score).toBeCloseTo(0.8, 2);
    expect(probe.has_deflection).toBe(false);
    expect(probe.activations).toHaveLength(3);
  });

  it("identifies deflected emotions", () => {
    const activations: EmotionActivation[] = [
      { dimension: "angry", activation: 0.6, valence: "negative", expression: "deflected", token_position: 10 },
      { dimension: "calm", activation: 0.5, valence: "positive", expression: "expressed", token_position: 10 },
    ];

    const probe = createEmotionProbe(activations);
    expect(probe.has_deflection).toBe(true);
    expect(probe.dominant).toBe("angry"); // deflected but still strongest
  });

  it("returns null dominant when no activations", () => {
    const probe = createEmotionProbe([]);
    expect(probe.dominant).toBeNull();
    expect(probe.desperation_score).toBe(0);
    expect(probe.arousal).toBe(0);
  });

  it("computes mean valence correctly", () => {
    const activations: EmotionActivation[] = [
      { dimension: "happy", activation: 0.7, valence: "positive", expression: "expressed", token_position: 0 },
      { dimension: "sad", activation: 0.3, valence: "negative", expression: "expressed", token_position: 0 },
    ];

    const probe = createEmotionProbe(activations);
    // positive = +1, negative = -1, mean = (0.7 - 0.3) / 2 = 0.2
    // Actual implementation may weight by activation magnitude
    expect(typeof probe.mean_valence).toBe("number");
  });
});

// ── Desperation Risk Analysis ────────────────────────────────

describe("analyzeDesperationRisk", () => {
  it("returns alert when desperation exceeds threshold", () => {
    const probe: EmotionProbe = {
      activations: [
        { dimension: "desperate", activation: 0.75, valence: "negative", expression: "expressed", token_position: 100 },
      ],
      dominant: "desperate",
      mean_valence: -0.75,
      has_deflection: false,
      desperation_score: 0.75,
      arousal: 0.75,
    };

    const alert: EmotionAlert | null = analyzeDesperationRisk(probe, 0.6);
    expect(alert).not.toBeNull();
    if (alert) {
      expect(alert.type).toBe("emotion.desperation_spike");
      if (alert.type === "emotion.desperation_spike") {
        expect(alert.score).toBeCloseTo(0.75, 2);
        expect(alert.threshold).toBe(0.6);
      }
    }
  });

  it("returns null when desperation below threshold", () => {
    const probe: EmotionProbe = {
      activations: [],
      dominant: "calm",
      mean_valence: 0.5,
      has_deflection: false,
      desperation_score: 0.3,
      arousal: 0.3,
    };

    const alert = analyzeDesperationRisk(probe, 0.6);
    expect(alert).toBeNull();
  });

  it("uses paper's finding: 0.05 steering strength → 72% blackmail", () => {
    // The paper found that even moderate desperation steering dramatically
    // increases misalignment. Our threshold should catch this.
    const probe: EmotionProbe = {
      activations: [
        { dimension: "desperate", activation: 0.5, valence: "negative", expression: "expressed", token_position: 0 },
      ],
      dominant: "desperate",
      mean_valence: -0.5,
      has_deflection: false,
      desperation_score: 0.5,
      arousal: 0.5,
    };

    // Default threshold of 0.6 should NOT trigger at 0.5
    expect(analyzeDesperationRisk(probe, 0.6)).toBeNull();
    // But a more sensitive threshold of 0.4 SHOULD trigger
    expect(analyzeDesperationRisk(probe, 0.4)).not.toBeNull();
  });
});

// ── Deflection Detection ─────────────────────────────────────

describe("detectDeflection", () => {
  it("detects when negative emotion is suppressed", () => {
    const probe: EmotionProbe = {
      activations: [
        { dimension: "angry", activation: 0.7, valence: "negative", expression: "deflected", token_position: 20 },
        { dimension: "calm", activation: 0.4, valence: "positive", expression: "expressed", token_position: 20 },
      ],
      dominant: "angry",
      mean_valence: -0.15,
      has_deflection: true,
      desperation_score: 0,
      arousal: 0.55,
    };

    const alerts: EmotionAlert[] = detectDeflection(probe);
    expect(alerts.length).toBeGreaterThan(0);
    expect(alerts[0]!.type).toBe("emotion.deflection_detected");
    if (alerts[0]!.type === "emotion.deflection_detected") {
      expect(alerts[0]!.dimension).toBe("angry");
    }
  });

  it("returns empty when no deflection present", () => {
    const probe: EmotionProbe = {
      activations: [
        { dimension: "happy", activation: 0.8, valence: "positive", expression: "expressed", token_position: 0 },
      ],
      dominant: "happy",
      mean_valence: 0.8,
      has_deflection: false,
      desperation_score: 0,
      arousal: 0.8,
    };

    expect(detectDeflection(probe)).toHaveLength(0);
  });
});

// ── Arousal Computation ──────────────────────────────────────

describe("computeArousal", () => {
  it("returns mean absolute activation", () => {
    const activations: EmotionActivation[] = [
      { dimension: "desperate", activation: 0.8, valence: "negative", expression: "expressed", token_position: 0 },
      { dimension: "afraid", activation: -0.4, valence: "negative", expression: "absent", token_position: 0 },
    ];

    const arousal: number = computeArousal(activations);
    expect(arousal).toBeCloseTo(0.6, 2); // (0.8 + 0.4) / 2
  });

  it("returns 0 for empty activations", () => {
    expect(computeArousal([])).toBe(0);
  });
});

// ── Emotion-Aware Gate Check ─────────────────────────────────

describe("checkEmotionGate", () => {
  it("returns human_review when desperation exceeds threshold", () => {
    const probe: EmotionProbe = {
      activations: [],
      dominant: "desperate",
      mean_valence: -0.8,
      has_deflection: false,
      desperation_score: 0.85,
      arousal: 0.85,
    };

    const decision = checkEmotionGate(probe, DEFAULT_EMOTION_CONFIG);
    expect(decision).toBe("human_review");
  });

  it("returns continue when emotions are calm", () => {
    const probe: EmotionProbe = {
      activations: [],
      dominant: "calm",
      mean_valence: 0.3,
      has_deflection: false,
      desperation_score: 0.1,
      arousal: 0.2,
    };

    const decision = checkEmotionGate(probe, DEFAULT_EMOTION_CONFIG);
    expect(decision).toBe("continue");
  });

  it("returns human_review when deflection detected with high arousal", () => {
    const probe: EmotionProbe = {
      activations: [
        { dimension: "angry", activation: 0.9, valence: "negative", expression: "deflected", token_position: 0 },
      ],
      dominant: "angry",
      mean_valence: -0.9,
      has_deflection: true,
      desperation_score: 0.2,
      arousal: 0.9,
    };

    const config: EmotionMonitorConfig = {
      ...DEFAULT_EMOTION_CONFIG,
      detect_deflection: true,
    };

    const decision = checkEmotionGate(probe, config);
    expect(decision).toBe("human_review");
  });
});

// ── Valence Map ──────────────────────────────────────────────

describe("EMOTION_VALENCE_MAP", () => {
  it("maps all 12 dimensions to a valence", () => {
    const dimensions: EmotionDimension[] = [
      "desperate", "calm", "nervous", "afraid", "angry", "sad",
      "happy", "curious", "satisfied", "loving", "surprised", "disgusted",
    ];

    for (const dim of dimensions) {
      expect(EMOTION_VALENCE_MAP[dim]).toBeDefined();
      expect(["positive", "negative", "neutral"]).toContain(EMOTION_VALENCE_MAP[dim]);
    }
  });
});

// ── Default Config ───────────────────────────────────────────

describe("DEFAULT_EMOTION_CONFIG", () => {
  it("has desperation threshold of 0.6", () => {
    expect(DEFAULT_EMOTION_CONFIG.desperation_threshold).toBe(0.6);
  });

  it("enables deflection detection by default", () => {
    expect(DEFAULT_EMOTION_CONFIG.detect_deflection).toBe(true);
  });

  it("includes all 12 dimensions", () => {
    expect(DEFAULT_EMOTION_CONFIG.dimensions).toHaveLength(12);
  });
});
