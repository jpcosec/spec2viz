"""BPMN in Color palette shared by the renderer and the offline viewer page."""

TONE_PALETTE: dict[str, tuple[str, str]] = {
    "success": ("#E3F4E6", "#2E7D32"),
    "warning": ("#FFEFC7", "#B26A00"),
    "danger": ("#FBE3E3", "#B42318"),
    "info": ("#E1EEFB", "#1D4ED8"),
    "neutral": ("#EEF0F3", "#6B7280"),
    "rule1": ("#EDE9FE", "#6D4AFF"),
    "rule2": ("#FDE7D9", "#C2410C"),
    "rule3": ("#DCF5EE", "#0F766E"),
    "rule4": ("#FDE7F1", "#BE185D"),
    "rule5": ("#EAF0D8", "#4D7C0F"),
}
GATEWAY_TONE = ("#F4F0FB", "#7E57C2")
START_TONE = ("#E3F4E6", "#2E7D32")
END_TONE = ("#FBE3E3", "#8B1A1A")
DEFAULT_LEGEND_LABELS = {
    "success": "favorable",
    "warning": "atención",
    "danger": "rechazo",
    "info": "informativo",
    "neutral": "neutro",
    "rule1": "regla 1",
    "rule2": "regla 2",
    "rule3": "regla 3",
    "rule4": "regla 4",
    "rule5": "regla 5",
    "gateway": "gateway por defecto",
    "start": "inicio",
    "end": "fin",
}

__all__ = ["TONE_PALETTE", "GATEWAY_TONE", "START_TONE", "END_TONE", "DEFAULT_LEGEND_LABELS"]
