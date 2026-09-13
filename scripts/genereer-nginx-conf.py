#!/usr/bin/env python3
"""Bouwt de nginx-configuratie en berekent daarbij de CSP-hashes uit de HTML zelf.

Draait tijdens de Docker-build. Omdat de hashes hier uit de bestanden komen,
kunnen ze niet verouderen: wie het inline script of de inline stijl aanpast,
krijgt automatisch de bijbehorende hash in de Content-Security-Policy.
"""
import base64
import hashlib
import io
import re
import sys

HTML_BESTANDEN = ("index.html",)


def hashes(patroon, bronnen):
    gevonden = []
    for naam, inhoud in bronnen:
        blokken = re.findall(patroon, inhoud, re.S)
        if not blokken:
            print("FOUT: geen " + patroon + "-blok in " + naam, file=sys.stderr)
            sys.exit(1)
        for blok in blokken:
            digest = hashlib.sha256(blok.encode("utf-8")).digest()
            gevonden.append("'sha256-" + base64.b64encode(digest).decode() + "'")
    # dubbele hashes maar een keer opnemen
    uniek = []
    for h in gevonden:
        if h not in uniek:
            uniek.append(h)
    return " ".join(uniek)


def main():
    bronnen = [(n, io.open(n, encoding="utf-8").read()) for n in HTML_BESTANDEN]
    script_hashes = hashes(r"<script>(.*?)</script>", bronnen)
    style_hashes = hashes(r"<style>(.*?)</style>", bronnen)

    sjabloon = io.open("nginx.conf.template", encoding="utf-8").read()
    conf = sjabloon.replace("__SCRIPT_HASHES__", script_hashes)
    conf = conf.replace("__STYLE_HASHES__", style_hashes)
    if "__" in conf.replace("__nolint__", ""):
        print("FOUT: niet alle plaatshouders zijn ingevuld", file=sys.stderr)
        sys.exit(1)
    io.open("default.conf", "w", encoding="utf-8", newline="\n").write(conf)
    print("script-src " + script_hashes)
    print("style-src  " + style_hashes)


main()
