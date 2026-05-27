import gradio as gr
from gradio.themes.utils import colors, fonts, sizes


def _cyan():
    return colors.Color(
        name="cyan",
        c50="#ecfeff",
        c100="#cffafe",
        c200="#a5f3fc",
        c300="#67e8f9",
        c400="#22d3ee",
        c500="#00d4ff",
        c600="#0891b2",
        c700="#0e7490",
        c800="#155e75",
        c900="#164e63",
        c950="#083344",
    )


def _dark_neutral():
    return colors.Color(
        name="dark_neutral",
        c50="#f0f0f5",
        c100="#d4d4dd",
        c200="#a8a8b8",
        c300="#7c7c94",
        c400="#52526e",
        c500="#3a3a54",
        c600="#2a2a3e",
        c700="#1e1e30",
        c800="#14141f",
        c900="#0e0e16",
        c950="#08080c",
    )


def create_theme():
    return gr.themes.Base(
        primary_hue=_cyan(),
        secondary_hue=_cyan(),
        neutral_hue=_dark_neutral(),
        text_size=sizes.Size(
            name="custom",
            xxs="9px",
            xs="10px",
            sm="12px",
            md="14px",
            lg="16px",
            xl="22px",
            xxl="26px",
        ),
        spacing_size=sizes.Size(
            name="custom",
            xxs="1px",
            xs="2px",
            sm="4px",
            md="6px",
            lg="8px",
            xl="10px",
            xxl="16px",
        ),
        radius_size=sizes.Size(
            name="custom",
            xxs="2px",
            xs="4px",
            sm="8px",
            md="10px",
            lg="14px",
            xl="18px",
            xxl="24px",
        ),
        font=(
            fonts.GoogleFont("Inter"),
            "ui-sans-serif",
            "system-ui",
            "sans-serif",
        ),
        font_mono=(
            fonts.GoogleFont("JetBrains Mono"),
            "ui-monospace",
            "Consolas",
            "monospace",
        ),
    )
