#!/usr/bin/env python3
"""Zet de QR-code voor de kaart-URL in index.html.

De code wordt als SVG-pad in de pagina geschreven, niet als plaatje en niet via
een bibliotheek in de browser: de kaart blijft daarmee een zelfstandig bestand
zonder netwerkverkeer of extra vertrouwensrelatie. Draai dit script opnieuw als
de URL verandert; het vervangt alleen wat tussen de qr-markeringen staat.

    python3 scripts/genereer-qr.py [url]
"""
import io
import re
import sys

import segno

STANDAARD_URL = "https://pieter.debrabander.com/"
BESTAND = "index.html"
START = "<!-- qr:start -->"
EIND = "<!-- qr:end -->"


def svg_pad(matrix):
    """Zet de modules om in een pad van horizontale stukken."""
    delen = []
    for y, rij in enumerate(matrix):
        x = 0
        breedte = len(rij)
        while x < breedte:
            if rij[x]:
                lengte = 1
                while x + lengte < breedte and rij[x + lengte]:
                    lengte += 1
                delen.append("M{0} {1}h{2}v1h-{2}z".format(x, y, lengte))
                x += lengte
            else:
                x += 1
    return "".join(delen)


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else STANDAARD_URL
    qr = segno.make(url, error="m")
    matrix = [list(rij) for rij in qr.matrix]
    maat = len(matrix)
    # Een QR-code hoort vier modules rust om zich heen te hebben. Op een donkere
    # kaart is die rust er alleen als hij in de tekening zelf zit: zonder deze
    # marge vindt een camera de code niet terug tegen de donkere ondergrond.
    rust = 4
    kader = maat + rust * 2
    svg = (
        '<svg viewBox="-{4} -{4} {3} {3}" role="img" aria-label="QR-code naar {1}" '
        'shape-rendering="crispEdges"><path fill="var(--qr-fg)" d="{2}"/></svg>'
    ).format(maat, url, svg_pad(matrix), kader, rust)

    html = io.open(BESTAND, encoding="utf-8").read()
    patroon = re.compile(re.escape(START) + ".*?" + re.escape(EIND), re.S)
    if not patroon.search(html):
        print("FOUT: de qr-markeringen staan niet in " + BESTAND, file=sys.stderr)
        sys.exit(1)
    html = patroon.sub(START + svg + EIND, html, count=1)
    io.open(BESTAND, "w", encoding="utf-8", newline="\n").write(html)
    print("QR bijgewerkt: {0} | versie {1} | {2}x{2} modules | {3} tekens pad".format(
        url, qr.version, maat, len(svg)))


main()
