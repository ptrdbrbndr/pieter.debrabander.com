# pieter.debrabander.com

Persoonlijke contactkaart van Pieter de Brabander, in de vorm van een technische
tekening: bellen, WhatsApp, mail en het contact bewaren als vCard. Het domein
`0613353835.nl` verwijst met een 301 naar deze pagina.

## Wat staat waar

| Bestand | Rol |
| --- | --- |
| `index.html` | de pagina die live staat — donkere variant |
| `licht-alternatief.html` | dezelfde kaart in de lichte variant, bereikbaar op `/licht-alternatief.html` |
| `nginx.conf.template` | de webserverconfiguratie, met plaatshouders voor de CSP-hashes |
| `scripts/genereer-nginx-conf.py` | vult die plaatshouders tijdens de build met de hashes uit de HTML |
| `Dockerfile` | tweetrapsbuild: eerst de configuratie, dan een nginx die de twee bestanden serveert |

Beide HTML-bestanden zijn zelfstandig: inline CSS en JS, geen bouwstap, geen
afhankelijkheden buiten Google Fonts. Je kunt ze los openen of ergens anders
neerzetten en ze werken.

## Van licht naar donker wisselen

De twee bestanden verschillen alleen in hun kleurvariabelen. Wisselen is dus
omwisselen:

```bash
git mv index.html donker.html
git mv licht-alternatief.html index.html
git mv donker.html licht-alternatief.html
git commit -am "Lichte variant als hoofdversie"
git push
```

Pas daarna in de nieuwe `index.html` de `theme-color` aan (`#0B2A4A` voor donker,
`#FAF8F2` voor licht). De CSP-hashes hoef je niet aan te raken: die worden bij
elke build opnieuw uit de bestanden berekend.

## Contactgegevens wijzigen

Telefoonnummer, WhatsApp-link, e-mailadres en de vCard staan in beide
HTML-bestanden. Zoek op `31613353835` en op `pieter.de.brabander@ductus.nl` en
pas ze in allebei aan, anders lopen de varianten uiteen.

## Live zetten

Zie `docs/runbook-deploy.md`.
