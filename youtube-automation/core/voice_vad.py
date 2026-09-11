"""Lightweight voice-activity gate for JARVIS microphone chunks.

This intentionally avoids adding another ML dependency. It uses RMS energy
to reject near-silent microphone chunks before sending them to ASR.
"""

from __future__ import annotations

import math
from typing import Iterable


def rms_level(samples: Iterable[int]) -> float:
    values = list(samples)
    if not values:
        return 0.0
    mean_square = sum(float(value) * float(value) for value in values) / len(values)
    return math.sqrt(mean_square)


def is_speech(samples: Iterable[int], threshold: float = 350.0) -> bool:
    return rms_level(samples) >= threshold
