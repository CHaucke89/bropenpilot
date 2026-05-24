"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""
import os


KONIK_API_HOST = "https://api.konik.ai"
KONIK_ATHENA_HOST = "wss://athena.konik.ai"


def apply_konik_env(params) -> None:
  """Override API_HOST / ATHENA_HOST environment variables if Konik API is enabled."""
  if params.get_bool("KonikApi"):
    os.environ.setdefault("API_HOST", KONIK_API_HOST)
    os.environ.setdefault("ATHENA_HOST", KONIK_ATHENA_HOST)


def swap_dongle_for_konik(konik: bool, params) -> None:
  """Stash the current DongleId, then load the saved DongleId if it exists.
  If not, remove the DongleId to trigger registration with the respective API on next boot."""
  current = params.get("DongleId")
  old_dongle_id = "KonikDongleId" if not konik else "CommaDongleId"
  new_dongle_id = "CommaDongleId" if not konik else "KonikDongleId"

  if current:
    params.put(old_dongle_id, current)

  saved = params.get(new_dongle_id)
  if saved:
    params.put("DongleId", saved)
  else:
    params.remove("DongleId")
