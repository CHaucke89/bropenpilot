"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""
import numpy as np
import pyray as rl
from dataclasses import dataclass

from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.lib.text_measure import measure_text_cached


@dataclass
class UiElement:
  value: str
  label: str
  unit: str
  color: rl.Color
  val_text: str = ""
  label_text: str = ""
  unit_text: str = ""
  val_width: float = 0.0
  label_width: float = 0.0
  unit_width: float = 0.0
  total_width: float = 0.0

  def measure(self, font, font_size: int):
    self.label_text = f"{self.label} "
    self.val_text = self.value
    self.unit_text = f" {self.unit}" if self.unit else ""

    self.label_width = measure_text_cached(font, self.label_text, font_size, 0).x
    self.val_width = measure_text_cached(font, self.val_text, font_size, 0).x
    self.unit_width = measure_text_cached(font, self.unit_text, font_size, 0).x if self.unit else 0

    self.total_width = self.label_width + self.val_width + self.unit_width

class FrictionCoefficientElement:
  def __init__(self):
    self.unit = ""

  def update(self, sm, is_metric: bool) -> UiElement:
    if ui_state.enforce_torque_control and ui_state.custom_torque_params and ui_state.torque_override_enabled:
      return UiElement(f"{ui_state.torque_override_friction:.3f}", "FRIC.", self.unit, rl.WHITE)

    ltp = sm['liveTorqueParameters']

    # Display the live friction value being used by the torque controller with speed-dependent learning
    centers = ltp.speedBinCenters
    if centers:
      v_ego = sm['carState'].vEgo
      frictions = ltp.speedBinFrictions
      value = f"{np.interp(v_ego, centers, frictions):.3f}"
      active_bin = int(np.argmin([abs(v_ego - c) for c in centers]))
      live_valid = ltp.speedBinValid[active_bin]
    else:
      value = f"{ltp.frictionCoefficientFiltered:.3f}"
      live_valid = ltp.liveValid

    color = rl.Color(0, 255, 0, 255) if live_valid else rl.WHITE
    return UiElement(value, "FRIC.", self.unit, color)


class LatAccelFactorElement:
  def __init__(self):
    self.unit = ""

  def update(self, sm, is_metric: bool) -> UiElement:
    if ui_state.enforce_torque_control and ui_state.custom_torque_params and ui_state.torque_override_enabled:
      return UiElement(f"{ui_state.torque_override_lat_accel_factor:.3f}", "L.A.F.", self.unit, rl.WHITE)

    ltp = sm['liveTorqueParameters']

    # Display the live LAF value being used by the torque controller with speed-dependent learning
    centers = ltp.speedBinCenters
    if centers:
      v_ego = sm['carState'].vEgo
      factors = ltp.speedBinLatAccelFactors
      value = f"{np.interp(v_ego, centers, factors):.3f}"
      active_bin = int(np.argmin([abs(v_ego - c) for c in centers]))
      live_valid = ltp.speedBinValid[active_bin]
    else:
      value = f"{ltp.latAccelFactorFiltered:.3f}"
      live_valid = ltp.liveValid

    color = rl.Color(0, 255, 0, 255) if live_valid else rl.WHITE
    return UiElement(value, "L.A.F.", self.unit, color)
