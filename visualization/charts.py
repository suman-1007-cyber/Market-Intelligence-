from pathlib import Path
import html

def _esc(value):
    return html.escape(str(value))

def line(values, path="reports/chart.svg", title="Trend"):
    values = [float(x) for x in values]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    width, height, pad = 900, 500, 70
    if not values:
        values = [0]

    low = min(values)
    high = max(values)
    span = high - low or 1

    points = []
    for i, value in enumerate(values):
        x = pad + (i / max(len(values) - 1, 1)) * (width - 2 * pad)
        y = height - pad - ((value - low) / span) * (height - 2 * pad)
        points.append(f"{x:.1f},{y:.1f}")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{pad}" y="35" font-size="22" font-family="sans-serif">{_esc(title)}</text>
<line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}" stroke="black"/>
<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{height-pad}" stroke="black"/>
<polyline points="{' '.join(points)}" fill="none" stroke="black" stroke-width="3"/>
</svg>"""

    path.write_text(svg, encoding="utf-8")
    return path


def bar(labels, values, path="reports/bar.svg", title="Comparison"):
    labels = list(labels)
    values = [float(x) for x in values]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    width, height, pad = 900, 500, 70
    if not values:
        values = [0]
        labels = ["No data"]

    maximum = max(values) or 1
    slot = (width - 2 * pad) / max(len(values), 1)
    bar_width = slot * 0.65

    rectangles = []
    text = []

    for i, (label, value) in enumerate(zip(labels, values)):
        x = pad + i * slot
        bar_height = (value / maximum) * (height - 2 * pad)
        y = height - pad - bar_height

        rectangles.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" '
            f'height="{bar_height:.1f}" fill="none" stroke="black"/>'
        )

        text.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{height-pad+20}" '
            f'text-anchor="middle" font-size="12" font-family="sans-serif">'
            f'{_esc(label)}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{pad}" y="35" font-size="22" font-family="sans-serif">{_esc(title)}</text>
<line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}" stroke="black"/>
<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{height-pad}" stroke="black"/>
{''.join(rectangles)}
{''.join(text)}
</svg>"""

    path.write_text(svg, encoding="utf-8")
    return path
