#!/usr/bin/env python3

from __future__ import annotations

import argparse
import colorsys
import html
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a simple hand-drawn percent bar SVG."
    )
    parser.add_argument("--title", required=True, help="Title displayed at the top.")
    parser.add_argument(
        "--percent",
        required=True,
        type=float,
        help="Percent value from 0 to 100.",
    )
    parser.add_argument(
        "--output",
        default="percent_bar.svg",
        help="Output SVG filename. Always saved in the current folder.",
    )
    return parser.parse_args()


def clamp_percent(value: float) -> float:
    return max(0.0, min(100.0, value))


def bar_color(percent: float) -> str:
    if percent < 10:
        return "#e53935"
    if percent > 90:
        return "#1e88e5"

    # Sweep from warm to cool across the middle band.
    ratio = percent / 100.0
    hue = 0.02 + (0.72 - 0.02) * ratio
    red, green, blue = colorsys.hsv_to_rgb(hue, 0.75, 0.95)
    return "#{:02x}{:02x}{:02x}".format(
        int(red * 255), int(green * 255), int(blue * 255)
    )


def build_svg(title: str, percent: float) -> str:
    width = 800
    height = 260
    bar_x = 80
    bar_y = 120
    bar_width = 640
    bar_height = 56
    fill_width = int(bar_width * (percent / 100.0))
    color = bar_color(percent)
    safe_title = html.escape(title)
    percent_label = f"{percent:.1f}%"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <style>
      .title {{
        font-family: "Comic Sans MS", "Chalkboard", "Marker Felt", sans-serif;
        font-size: 34px;
        fill: #111111;
      }}
      .label {{
        font-family: "Comic Sans MS", "Chalkboard", "Marker Felt", sans-serif;
        font-size: 26px;
        fill: #111111;
      }}
      .small {{
        font-family: "Comic Sans MS", "Chalkboard", "Marker Felt", sans-serif;
        font-size: 24px;
        fill: #222222;
      }}
      .outline {{
        stroke: #111111;
        stroke-width: 5;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
      }}
    </style>
  </defs>

  <rect width="100%" height="100%" fill="#fcfcf7" />

  <text x="{bar_x}" y="{bar_y - 26}" class="title">{safe_title}</text>
  <text x="{bar_x + bar_width}" y="{bar_y - 26}" text-anchor="end" class="label">{percent_label}</text>

  <rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="{bar_height}" rx="12" fill="#ffffff" stroke="#111111" stroke-width="5" />
  <rect x="{bar_x + 6}" y="{bar_y + 6}" width="{max(fill_width - 12, 0)}" height="{bar_height - 12}" rx="8" fill="{color}" />
</svg>
"""


def main() -> None:
    args = parse_args()
    percent = clamp_percent(args.percent)
    svg = build_svg(args.title, percent)

    output_path = Path.cwd() / Path(args.output).name
    output_path.write_text(svg, encoding="utf-8")
    print(f"Saved {output_path} with percent {percent:.1f}%")


if __name__ == "__main__":
    main()
