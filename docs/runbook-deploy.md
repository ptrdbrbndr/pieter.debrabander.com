# Runbook: pieter.debrabander.com en de 301 vanaf 0613353835.nl

Bijgewerkt: 13 september 2026.

## De opstelling in één beeld

```
bezoeker ──> 0613353835.nl          (Cloudflare-zone, alleen een 301-regel)
                  │ 301
                  v
             pieter.debrabander.com (Cloudflare, proxied)
                  │ tunnel 4931da40-…
                  v
             Cyberductus-1 ──> Coolify/Traefik ──> nginx-container (poort 80)
```

De contactkaart is statisch. Er is geen database, geen backend en geen staat: de
container serveert twee HTML-bestanden en een `/health`-pad.

## Vaste gegevens

| Wat | Waarde |
| --- | --- |
| Repo | `ptrdbrbndr/pieter.debrabander.com`, branch `main` |
| Coolify-project | `pieter-debrabander` — uuid `grq37l7yyk4veqecffpbuhum` |
| Coolify-app | `pieter-contactkaart` — uuid `glj0oxtzapmqyfu14bshzcdh` |
| Server | Cyberductus-1 — uuid `txh5pu5s190naj4k1uacnild` |
| Buildpack | Dockerfile, poort 80, healthcheck `GET /health` |
| DNS | `pieter` CNAME → `4931da40-8b72-4cc3-8f7e-6802b5e948a5.cfargotunnel.com`, proxied |
| Tunnel-ingress | `https://localhost:443`, `noTLSVerify`, `originServerName=pieter.debrabander.com` |
| Zone `debrabander.com` | `0adaf85eabfad25a4533ad4326890b32` |
| Zone `0613353835.nl` | `21dd0944410594aba73c434ed55e1b50`, nameservers bradley + ollie |
| Page Rule (de 301) | `933ac7ea286b6ddfca4528249e1a085d`: `*0613353835.nl/*` → `https://pieter.debrabander.com/`, 301 |
| GitHub-webhook | id `678547513` → `https://coolify.cyberductus.nl/webhooks/source/github/events/manual` |

## Wijzigen en uitrollen

Een push naar `main` rolt zichzelf uit via de webhook hierboven. Handmatig kan ook:

```bash
curl -s -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
  "http://192.168.68.71:8000/api/v1/deploy?uuid=glj0oxtzapmqyfu14bshzcdh"
```

Let op: het Coolify-token begint met `3|`. Dat overleeft geen `source .env` — de
shell leest de pipe. Lees hem uit het bestand of zet hem tussen aanhalingstekens.
De API zit op `http://192.168.68.71:8000/api/v1`; de waarde van `COOLIFY_API_URL`
in `c:\Projecten\.env` mist het `/api/v1`-deel.

**De QR-code** wordt niet in de browser opgebouwd maar staat als SVG-pad in de
pagina; `scripts/genereer-qr.py` zet hem erin. Verandert de URL van de kaart, dan
moet dat script opnieuw draaien — anders wijst de code naar het oude adres
zonder dat iemand het merkt.

## Wat we onderweg tegenkwamen

**Cloudflare brak de mail-knop.** E-mailobfuscatie staat aan voor de zone: de
`mailto:`-link werd `/cdn-cgi/l/email-protection#…` met een los script om hem weer
leesbaar te maken. Dat script valt buiten de Content-Security-Policy, werd
geblokkeerd, en de knop deed niets meer. De pagina staat daarom tussen
`<!--email_off-->` en `<!--/email_off-->` — de opt-out van Cloudflare zelf. Blijf
die markering behouden, ook bij een nieuw ontwerp.

**Bestandsrechten uit een Windows-werkboom.** De HTML komt als `0640` de build in
en dan geeft nginx een 403. De Dockerfile zet de rechten expliciet op `0644`.

**Het nameserver-paar.** Cloudflare wijst per zone een willekeurig paar toe.
`0613353835.nl` stond bij registratie op bart + olivia, maar de nieuwe zone kreeg
bradley + ollie. Zonder die flip bij mijn.host was de zone nooit actief geworden.
Controleer dus altijd `name_servers` uit het zone-antwoord vóór een NS-wijziging.

**Tokenrechten.** Geen van de Cloudflare-tokens in `c:\Projecten\.env` mag
redirect-regels (rulesets) schrijven; `CLOUDFLARE_ZONE_CREATE_TOKEN` mag wel Page
Rules. Vandaar dat de 301 een Page Rule is en geen Single Redirect.

## Controleren of alles nog staat

```bash
curl -sI https://pieter.debrabander.com/ | head -3
curl -s  https://pieter.debrabander.com/ | grep -c 'mailto:pieter.de.brabander@ductus.nl'   # moet 1 zijn
curl -sI https://0613353835.nl/ | grep -iE 'HTTP/|location'                                  # 301 naar pieter…
```

De mail-controle is de belangrijkste: die vangt het terugkeren van de
Cloudflare-obfuscatie, en dat is het enige stille defect dat deze pagina kent.
