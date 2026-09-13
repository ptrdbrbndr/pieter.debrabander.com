# pieter.debrabander.com

Persoonlijke contactkaart van Pieter de Brabander, in de vorm van een technische
tekening: bellen, WhatsApp, mail, het contact bewaren als vCard, en een QR-code
om de kaart door te geven. Het domein `0613353835.nl` verwijst met een 301 naar
deze pagina.

## Wat staat waar

| Bestand | Rol |
| --- | --- |
| `index.html` | de hele kaart — één zelfstandig bestand, beide kleurstellingen inbegrepen |
| `scripts/genereer-qr.py` | schrijft de QR-code als SVG-pad in `index.html` |
| `nginx.conf.template` | de webserverconfiguratie, met plaatshouders voor de CSP-hashes |
| `scripts/genereer-nginx-conf.py` | vult die plaatshouders tijdens de build met de hashes uit de HTML |
| `Dockerfile` | tweetrapsbuild: eerst de configuratie, dan een nginx die de pagina serveert |

`index.html` is zelfstandig: inline CSS en JS, geen bouwstap, geen
afhankelijkheden buiten Google Fonts. Je kunt het los openen of ergens anders
neerzetten en het werkt.

## Licht en donker

De kaart volgt standaard de instelling van het toestel van de bezoeker. Met de
schakelaar `Weergave` kiest hij zelf; die keuze gaat naar `localStorage` en
overleeft een herlading. Zolang er geen eigen keuze is, beweegt de kaart mee als
het toestel overdag licht en 's avonds donker wordt.

In CSS staat het lichte palet op `:root` en het donkere twee keer: onder
`@media (prefers-color-scheme: dark)` voor wie niets kiest, en onder
`:root[data-thema="donker"]` voor wie de schakelaar gebruikt. Wie een kleur
verandert, moet dat dus op beide plekken doen.

De QR-code houdt in beide gevallen donkere blokjes op een lichte ondergrond, met
vier modules rust eromheen. Dat is geen smaakkwestie: een omgekeerde code of een
te krappe marge krijgt lang niet elke camera gelezen.

## Contactgegevens wijzigen

Telefoonnummer, WhatsApp-link, e-mailadres en de vCard staan in `index.html`.
Zoek op `31613353835` en op `pieter.de.brabander@ductus.nl`.

Wijzigt de URL van de kaart zelf, draai dan ook:

```bash
python3 scripts/genereer-qr.py https://nieuwe-url/
```

Dat vervangt alleen wat tussen de qr-markeringen staat. De CSP-hashes hoef je
nooit met de hand bij te werken: die worden bij elke build opnieuw uit de HTML
berekend.

## Live zetten

Een push naar `main` rolt zichzelf uit. Zie `docs/runbook-deploy.md`.
