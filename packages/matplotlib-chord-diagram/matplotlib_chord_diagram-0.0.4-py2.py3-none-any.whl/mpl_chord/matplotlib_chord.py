import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

import numpy as np

LW = 0.3


def polar2xy(r, theta):
    return np.array([r * np.cos(theta), r * np.sin(theta)])


def hex2rgb(c):
    return tuple(int(c[weight : weight + 2], 16) / 256.0 for weight in (1, 3, 5))


def ideogram_arc(start=0, end=60, radius=1.0, width=0.2, ax=None, color=(1, 0, 0)):
    # start, end should be in [0, 360)
    vertices = get_vertices(end, radius, start, width)

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]

    if ax is None:
        return vertices, codes
    else:
        path = Path(vertices, codes)
        patch = patches.PathPatch(
            path, facecolor=color + (0.5,), edgecolor=color + (0.4,), lw=LW
        )
        ax.add_patch(patch)


def get_vertices(end, radius, start, width):
    if start > end:
        start, end = end, start
    start *= np.pi / 180.0
    end *= np.pi / 180.0
    # optimal distance to the control points
    # https://stackoverflow.com/questions/1734745/how-to-create-circle-with-b%C3%A9zier-curves
    opt = 4.0 / 3.0 * np.tan((end - start) / 4.0) * radius
    inner = radius * (1 - width)
    vertices = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start + 0.5 * np.pi),
        polar2xy(radius, end) + polar2xy(opt, end - 0.5 * np.pi),
        polar2xy(radius, end),
        polar2xy(inner, end),
        polar2xy(inner, end) + polar2xy(opt * (1 - width), end - 0.5 * np.pi),
        polar2xy(inner, start) + polar2xy(opt * (1 - width), start + 0.5 * np.pi),
        polar2xy(inner, start),
        polar2xy(radius, start),
    ]
    return vertices


def chord_arc(
    start1=0,
    end1=60,
    start2=180,
    end2=240,
    radius=1.0,
    chord_width=0.7,
    ax=None,
    color=(1, 0, 0),
):
    # start, end should be in [0, 360)
    if start1 > end1:
        start1, end1 = end1, start1
    if start2 > end2:
        start2, end2 = end2, start2
    start1 *= np.pi / 180.0
    end1 *= np.pi / 180.0
    start2 *= np.pi / 180.0
    end2 *= np.pi / 180.0
    opt1 = 4.0 / 3.0 * np.tan((end1 - start1) / 4.0) * radius
    opt2 = 4.0 / 3.0 * np.tan((end2 - start2) / 4.0) * radius
    chord_radius = radius * (1 - chord_width)
    vertices = [
        polar2xy(radius, start1),
        polar2xy(radius, start1) + polar2xy(opt1, start1 + 0.5 * np.pi),
        polar2xy(radius, end1) + polar2xy(opt1, end1 - 0.5 * np.pi),
        polar2xy(radius, end1),
        polar2xy(chord_radius, end1),
        polar2xy(chord_radius, start2),
        polar2xy(radius, start2),
        polar2xy(radius, start2) + polar2xy(opt2, start2 + 0.5 * np.pi),
        polar2xy(radius, end2) + polar2xy(opt2, end2 - 0.5 * np.pi),
        polar2xy(radius, end2),
        polar2xy(chord_radius, end2),
        polar2xy(chord_radius, start1),
        polar2xy(radius, start1),
    ]

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    if ax is None:
        return vertices, codes
    else:
        path = Path(vertices, codes)
        patch = patches.PathPatch(
            path, facecolor=color + (0.5,), edgecolor=color + (0.4,), lw=LW
        )
        ax.add_patch(patch)


def self_chord_arc(
    start=0, end=60, radius=1.0, chord_width=0.7, ax=None, color=(1, 0, 0)
):
    # start, end should be in [0, 360)
    if start > end:
        start, end = end, start
    start *= np.pi / 180.0
    end *= np.pi / 180.0
    opt = 4.0 / 3.0 * np.tan((end - start) / 4.0) * radius
    chord_radius = radius * (1 - chord_width)
    vertices = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start + 0.5 * np.pi),
        polar2xy(radius, end) + polar2xy(opt, end - 0.5 * np.pi),
        polar2xy(radius, end),
        polar2xy(chord_radius, end),
        polar2xy(chord_radius, start),
        polar2xy(radius, start),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    if ax is None:
        return vertices, codes
    else:
        path = Path(vertices, codes)
        patch = patches.PathPatch(
            path, facecolor=color + (0.5,), edgecolor=color + (0.4,), lw=LW
        )
        ax.add_patch(patch)


def chord_diagram(flux, ax=None, colors=None, width=0.1, pad=2, chord_width=0.7):
    """Plot a chord diagram

    Parameters
    ----------
    flux :
        flux data, X[i, j] is the flux from i to j
    ax :
        matplotlib `axes` to show the plot
    colors : optional
        user defined colors in rgb format. Use function hex2rgb() to convert hex color to rgb color. Default: d3.js category10
    width : optional
        width/thickness of the ideogram arc
    pad : optional
        gap pad between two neighboring ideogram arcs, unit: degree, default: 2 degree
    chord_width : optional
        position of the control points for the chords, controlling the shape of the chords
    """

    if ax is None:
        fig, ax = plt.subplots(1)
        ax.set_aspect(1)
        ax.axis("off")

    # X[i, j]:  i -> j
    x = flux.sum(axis=1)  # sum over rows
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    if colors is None:
        # use d3.js category10 https://github.com/d3/d3-3.x-api-reference/blob/master/Ordinal-Scales.md#category10
        colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]
        if len(x) > 10:
            print("x is too large! Use x smaller than 10")
        colors = [hex2rgb(colors[i]) for i in range(len(x))]

    # find position for each start and end
    y = x / np.sum(x).astype(float) * (360 - pad * len(x))

    pos = {}
    arc = []
    nodePos = []
    start = 0
    for i in range(len(x)):
        end = start + y[i]
        arc.append((start, end))
        angle = 0.5 * (start + end)
        # print(start, end, angle)
        if -30 <= angle <= 210:
            angle -= 90
        else:
            angle -= 270
        nodePos.append(
            tuple(polar2xy(1.1, 0.5 * (start + end) * np.pi / 180.0)) + (angle,)
        )
        z = (flux[i, :] / x[i].astype(float)) * (end - start)
        ids = np.argsort(z)
        z0 = start
        for j in ids:
            pos[(i, j)] = (z0, z0 + z[j])
            z0 += z[j]
        start = end + pad

    for i in range(len(x)):
        start, end = arc[i]
        ideogram_arc(
            start=start, end=end, radius=1.0, ax=ax, color=colors[i], width=width
        )
        start, end = pos[(i, i)]
        self_chord_arc(
            start,
            end,
            radius=1.0 - width,
            color=colors[i],
            chord_width=chord_width * 0.7,
            ax=ax,
        )
        for j in range(i):
            color = colors[i]
            if flux[i, j] > flux[j, i]:
                color = colors[j]
            start1, end1 = pos[(i, j)]
            start2, end2 = pos[(j, i)]
            chord_arc(
                start1,
                end1,
                start2,
                end2,
                radius=1.0 - width,
                color=colors[i],
                chord_width=chord_width,
                ax=ax,
            )

    # print(nodePos)
    return nodePos


##################################
if __name__ == "__main__":
    fig = plt.figure(figsize=(6, 6))
    flux = np.array(
        [
            [11975, 5871, 8916, 2868],
            [1951, 10048, 2060, 6171],
            [8010, 16145, 8090, 8045],
            [1013, 990, 940, 6907],
        ]
    )

    ax = plt.axes([0, 0, 1, 1])

    nodePos = chord_diagram(flux, ax)
    ax.axis("off")
    prop = dict(fontsize=16 * 0.8, ha="center", va="center")
    nodes = ["non-crystal", "FCC", "HCP", "BCC"]
    for i in range(4):
        ax.text(nodePos[i][0], nodePos[i][1], nodes[i], rotation=nodePos[i][2], **prop)

    plt.savefig(
        "example.png", dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.02
    )
