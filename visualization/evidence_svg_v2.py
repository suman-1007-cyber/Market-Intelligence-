from html import escape


def build(points, title="Evidence-linked analysis"):
    width = 900
    height = 500

    valid = [p for p in points if p.get("y") is not None]

    if not valid:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'width="900" height="500">'
            '<text x="40" y="60">No graphable evidence</text>'
            '</svg>'
        )

    values = [float(p["y"]) for p in valid]
    minimum = min(values)
    maximum = max(values)

    if minimum == maximum:
        minimum -= 1
        maximum += 1

    left, right, top, bottom = 70, 30, 60, 70
    plot_width = width - left - right
    plot_height = height - top - bottom

    step = plot_width / (len(valid) - 1) if len(valid) > 1 else 0

    def y_position(value):
        ratio = (float(value) - minimum) / (maximum - minimum)
        return top + plot_height - ratio * plot_height

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}">',
        f'<title>{escape(str(title))}</title>',
        f'<text x="{left}" y="30">{escape(str(title))}</text>',
        f'<line x1="{left}" y1="{top + plot_height}" '
        f'x2="{width - right}" y2="{top + plot_height}" '
        f'stroke="black"/>',
        f'<line x1="{left}" y1="{top}" '
        f'x2="{left}" y2="{top + plot_height}" '
        f'stroke="black"/>',
    ]

    if len(valid) > 1:
        polyline = []

        for index, point in enumerate(valid):
            x = left + step * index
            y = y_position(point["y"])
            polyline.append(f"{x:.2f},{y:.2f}")

        svg.append(
            f'<polyline points="{" ".join(polyline)}" '
            f'fill="none" stroke="black"/>'
        )

    for index, point in enumerate(valid):
        x = left + step * index
        y = y_position(point["y"])

        period = escape(str(point.get("x") or ""))
        source = escape(str(point.get("source_url") or ""))

        svg.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5">'
            f'<title>{period} | source: {source}</title>'
            f'</circle>'
        )

    svg.append("</svg>")

    return "\n".join(svg)
