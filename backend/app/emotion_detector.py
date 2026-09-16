"""
Wraps DeepFace so the rest of the app only deals with a simple mood string.

Speed notes:
- DeepFace loads its emotion model lazily on first call; we warm it up once
  at server startup (see main.py) so the user's first webcam frame isn't slow.
- Frames are downscaled before analysis — the emotion model doesn't need
  full webcam resolution, and smaller frames analyze several times faster.
- enforce_detection=False so a briefly-missed face (bad angle, low light)
  returns a low-confidence result instead of throwing.

Accuracy notes:
- The underlying FER model is heavily biased toward "neutral" and "happy" —
  they have the clearest facial signatures, so it defaults to them unless an
  expression is strongly exaggerated. BIAS_WEIGHTS discounts those two and
  boosts the harder-to-detect emotions before picking the winner, so a mild
  frown actually registers as "sad" instead of losing to "neutral" every
  time. Tune these if it over- or under-corrects for your face/lighting.
"""
import base64
import io

import cv2
import numpy as np
from PIL import Image
from deepface import DeepFace

MAX_DIM = 400  # longest side, px — lowered from 480 for faster per-frame analysis

BIAS_WEIGHTS = {
    "neutral": 0.55,
    "happy": 0.85,
    "sad": 1.15,
    "angry": 1.2,
    "fear": 1.3,
    "surprise": 1.1,
    "disgust": 1.3,
}


def _decode_base64_image(data_url: str) -> np.ndarray:
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    img_bytes = base64.b64decode(data_url)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    arr = np.array(img)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def _downscale(frame: np.ndarray) -> np.ndarray:
    h, w = frame.shape[:2]
    longest = max(h, w)
    if longest <= MAX_DIM:
        return frame
    scale = MAX_DIM / longest
    return cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)


def warmup():
    """Run one dummy analysis so model weights are loaded before real traffic."""
    dummy = np.zeros((224, 224, 3), dtype=np.uint8)
    try:
        DeepFace.analyze(dummy, actions=["emotion"], enforce_detection=False, silent=True)
    except Exception:
        pass


def detect_mood(image_data_url: str) -> dict:
    frame = _decode_base64_image(image_data_url)
    frame = _downscale(frame)

    result = DeepFace.analyze(
        frame,
        actions=["emotion"],
        enforce_detection=False,
        detector_backend="opencv",  # fastest built-in detector; swap to "retinaface" for higher accuracy if needed
        silent=True,
    )
    # DeepFace returns a list when it finds multiple faces; take the largest/first
    face = result[0] if isinstance(result, list) else result

    raw_scores: dict = face["emotion"]

    # Rebalance toward emotions the model otherwise under-detects, then pick
    # the winner from the adjusted scores instead of DeepFace's raw pick.
    adjusted = {k: float(v) * BIAS_WEIGHTS.get(k, 1.0) for k, v in raw_scores.items()}
    total = sum(adjusted.values()) or 1.0
    normalized = {k: (v / total) * 100 for k, v in adjusted.items()}

    dominant = max(normalized, key=normalized.get)
    confidence = normalized[dominant] / 100.0

    return {
        "mood": dominant,
        "confidence": round(confidence, 4),
        "all_scores": {k: round(v, 2) for k, v in normalized.items()},
    }
