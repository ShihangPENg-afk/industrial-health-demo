from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: dict[str, Any] = Field(
        ...,
        description="Sensor or manufacturing process features",
    )


class PredictResponse(BaseModel):
    prediction: str
    prediction_label: str
    risk_level: str
    recommendation: str
    probabilities: dict[str, float] | None = None
