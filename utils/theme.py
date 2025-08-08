"""
T4P Competition Law Toolkit - Theme System
Centralized design tokens and color palettes for Trade4People aesthetics.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Palette:
    name: str
    # Core neutrals
    bg: str
    bg_soft: str
    surface: str
    surface_alt: str
    text: str
    text_muted: str
    # Brand accents
    primary: str
    primary_hover: str
    ring: str
    # Semantic
    success: str
    warning: str
    danger: str
    # Borders / outlines
    border: str
    shadow: str


# NOTE: Replace these with exact Trade4People colors later if needed.
T4P_DARK = Palette(
    name="T4P Dark",
    bg="#0f172a",          # slate-900-like
    bg_soft="#111827",     # near slate-900
    surface="#1f2937",     # slate-800
    surface_alt="#273449", # deep desaturated blue-gray
    text="#e5e7eb",        # gray-200
    text_muted="#94a3b8",  # slate-400
    primary="#0ea5a6",     # teal-500-ish
    primary_hover="#0d9488",
    ring="#22d3ee",        # cyan-400 glow
    success="#22c55e",
    warning="#f59e0b",
    danger="#ef4444",
    border="rgba(148,163,184,0.25)",
    shadow="0 8px 24px rgba(0,0,0,0.25)"
)

T4P_LIGHT = Palette(
    name="T4P Light",
    bg="#f8fafc",            # very light
    bg_soft="#eef2f7",
    surface="#ffffff",
    surface_alt="#f3f4f6",
    text="#0b1220",          # darker text for contrast
    text_muted="#334155",    # readable muted
    primary="#0ea5a6",
    primary_hover="#0d9488",
    ring="#0ea5a6",
    success="#16a34a",
    warning="#d97706",
    danger="#dc2626",
    border="rgba(2,6,23,0.12)",
    shadow="0 8px 20px rgba(2,6,23,0.08)"
)

PALETTES = {
    "T4P Dark": T4P_DARK,
    "T4P Light": T4P_LIGHT,
}

CURRENT_THEME_KEY = "t4p_palette"
