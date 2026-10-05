from statistics import mean, pstdev


def observe(points):
    if not points:
        return {
            "status": "NO_DATA",
            "observations": [],
        }

    ordered = sorted(
        points,
        key=lambda p: str(p.get("x", "")),
    )

    values = []
    valid_points = []

    for point in ordered:
        try:
            value = float(point["y"])
            values.append(value)
            valid_points.append(point)
        except (KeyError, TypeError, ValueError):
            continue

    if not values:
        return {
            "status": "NO_NUMERIC_DATA",
            "observations": [],
        }

    observations = []

    if len(values) >= 2:
        first = values[0]
        last = values[-1]

        if last > first:
            direction = "up"
        elif last < first:
            direction = "down"
        else:
            direction = "flat"

        change = last - first

        if first != 0:
            change_pct = (change / abs(first)) * 100.0
        else:
            change_pct = None

        observations.append({
            "type": "trend",
            "direction": direction,
            "first_value": first,
            "last_value": last,
            "change": change,
            "change_pct": change_pct,
            "source_urls": sorted({
                p.get("source_url")
                for p in valid_points
                if p.get("source_url")
            }),
        })

    if len(values) >= 3:
        changes = [
            values[i] - values[i - 1]
            for i in range(1, len(values))
        ]

        if len(changes) >= 2:
            acceleration = changes[-1] - changes[0]

            if acceleration > 0:
                acceleration_direction = "accelerating"
            elif acceleration < 0:
                acceleration_direction = "decelerating"
            else:
                acceleration_direction = "stable"

            observations.append({
                "type": "momentum",
                "direction": acceleration_direction,
                "change_from_first_interval": changes[0],
                "change_in_latest_interval": changes[-1],
                "acceleration": acceleration,
            })

    maximum = max(values)
    minimum = min(values)

    peak_index = values.index(maximum)
    trough_index = values.index(minimum)

    observations.append({
        "type": "peak",
        "value": maximum,
        "x": valid_points[peak_index].get("x"),
        "source_url": valid_points[peak_index].get("source_url"),
    })

    observations.append({
        "type": "trough",
        "value": minimum,
        "x": valid_points[trough_index].get("x"),
        "source_url": valid_points[trough_index].get("source_url"),
    })

    if len(values) >= 3:
        avg = mean(values)
        deviation = pstdev(values)

        if deviation == 0:
            outlier_indexes = []
        else:
            outlier_indexes = [
                i
                for i, value in enumerate(values)
                if abs(value - avg) > (2 * deviation)
            ]

        for index in outlier_indexes:
            point = valid_points[index]
            observations.append({
                "type": "outlier",
                "x": point.get("x"),
                "value": values[index],
                "source_url": point.get("source_url"),
            })

        observations.append({
            "type": "volatility",
            "mean": avg,
            "standard_deviation": deviation,
            "range": maximum - minimum,
        })

    largest_move = None

    if len(values) >= 2:
        moves = [
            (abs(values[i] - values[i - 1]), i)
            for i in range(1, len(values))
        ]

        magnitude, index = max(moves)

        largest_move = {
            "from_x": valid_points[index - 1].get("x"),
            "to_x": valid_points[index].get("x"),
            "from_value": values[index - 1],
            "to_value": values[index],
            "absolute_change": values[index] - values[index - 1],
            "magnitude": magnitude,
            "source_urls": sorted({
                valid_points[index - 1].get("source_url"),
                valid_points[index].get("source_url"),
            } - {None}),
        }

        observations.append({
            "type": "largest_movement",
            **largest_move,
        })

    return {
        "status": "OBSERVED",
        "point_count": len(valid_points),
        "metric": valid_points[0].get("metric"),
        "unit": valid_points[0].get("unit"),
        "observations": observations,
    }
