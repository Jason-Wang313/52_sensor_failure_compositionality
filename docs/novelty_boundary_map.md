# Novelty Boundary Map

## What Survives

Sensor robustness evaluations should report how failures compose. Isolated corruption curves and missing-modality tests are marginal slices, not guarantees about combined sensor failures.

## What V2 Breaks

The pairwise law is not a universal solution. On the held-out triple-failure cell:

- Pairwise-only regime: pairwise MAE 0.000.
- Hidden mild triple: pairwise MAE 0.284.
- Hidden strong triple: pairwise MAE 0.758.

This means a low-order law can be dangerously overconfident when common-cause or higher-order failures are omitted.

## Workshop-Safe Framing

- Present the original pairwise experiment as a minimal diagnostic.
- Present v2 as the reason to stress higher-order and common-cause cells.
- Claim a reporting protocol: interaction order, composed-failure coverage, and omitted-order stress.

## Unsafe Framing

- "Pairwise composition solves sensor failure robustness."
- "The method has real-robot evidence."
- "The zero-error synthetic result is algorithmic superiority."
- "Composed-failure evaluation is complete without high-order stress."
