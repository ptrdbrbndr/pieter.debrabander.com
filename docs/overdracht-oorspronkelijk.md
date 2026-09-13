# Overdracht: pieter.debrabander.com + 0613353835.nl forward

## Doel
Twee kant-en-klare HTML-ontwerpen (donker & licht) van een persoonlijke contactkaart live zetten op `pieter.debrabander.com`, en het net geregistreerde domein `0613353835.nl` laten doorverwijzen (301, unmasked) naar die pagina.

## Bijgeleverde bestanden
- `donker.html` — blauwdruk-ontwerp, donker thema
- `licht.html` — blauwdruk-ontwerp, licht thema (omgedraaide kleuren)

Beide zijn single-file, zelfstandige HTML (inline CSS + JS, geen build-stap nodig, geen dependencies). Functionaliteit in beide identiek:
- `tel:+31613353835` klik-om-te-bellen
- `https://wa.me/31613353835` WhatsApp-link
- `mailto:pieter.de.brabander@ductus.nl`
- vCard-download (.vcf) via een JS Blob, genereert `pieter.vcf` met naam, org, telefoon, e-mail en URL
- Statustoggle (Bereikbaar/Bezet) — puur visueel, geen backend nodig

## Stap 1 — Definitieve versie
Er is nog geen definitieve keuze gemaakt tussen donker en licht. Vraag dit na bij Pieter voordat je live gaat, of zet bij twijfel de donkere versie als hoofdversie (`index.html`) en bewaar de andere als `licht-alternatief.html` in dezelfde repo, zodat wisselen achteraf triviaal is.

## Stap 2 — Hosting van pieter.debrabander.com
`debrabander.com` heeft al actieve subdomeinen die als precedent dienen:
- `www.debrabander.com` — de Brabander familiestamboom (statische HTML)
- `teams.debrabander.com` — teamplanner-app voor jeugdvoetbal

Volg voor `pieter` hetzelfde hosting-patroon, zodat het beheer van het domein consistent blijft.

1. Achterhaal hoe de bestaande subdomeinen gehost worden (bijv. `dig www.debrabander.com` / `dig teams.debrabander.com`, of het DNS-paneel van de registrar/hosting-provider bekijken).
2. Voeg een `pieter`-subdomein toe volgens datzelfde patroon (A-record of CNAME naar dezelfde provider/host als de andere subdomeinen).
3. Plaats het gekozen HTML-bestand als `index.html` op die hosting.
4. Zorg voor een geldig SSL-certificaat specifiek op `pieter.debrabander.com` (bij de meeste hosting-providers automatisch; bij eigen server via Let's Encrypt/certbot).
5. Test dat `https://pieter.debrabander.com` laadt zonder mixed-content warnings, en dat de bel-, WhatsApp-, mail- en vCard-functies werken.

Als er geen bestaand hosting-patroon te achterhalen is: kies de eenvoudigste route — statische hosting via Vercel of Netlify (gratis tier, automatisch SSL, alleen het HTML-bestand nodig).

## Stap 3 — Forward instellen voor 0613353835.nl
Bij de registrar waar `0613353835.nl` net geregistreerd is:

1. Ga naar de domein-forwarding/redirect-instellingen.
2. Stel een **301-redirect** in naar `https://pieter.debrabander.com`.
3. Zet **masking/framing uit** — de bezoeker moet in de adresbalk `pieter.debrabander.com` zien, niet `0613353835.nl` met de pagina in een iframe. Masking geeft problemen met HTTPS en met het delen van de link.
4. Controleer of de forward zelf ook via HTTPS werkt. Zo niet, meld dit terug aan Pieter — dan is er mogelijk een tussenstap nodig (bijv. via Cloudflare) om een geldige HTTPS-forward te krijgen.
5. Test dat `0613353835.nl` direct doorspringt naar `https://pieter.debrabander.com` en dat de adresbalk dat laatste toont.

## Acceptatiecriteria
- [ ] `pieter.debrabander.com` is live met geldig SSL-certificaat
- [ ] `0613353835.nl` verwijst door (301, unmasked) naar `https://pieter.debrabander.com`
- [ ] Bel-, WhatsApp- en mail-links werken op mobiel en desktop
- [ ] vCard-download levert een correcte `pieter.vcf` op
- [ ] Pagina is goed leesbaar en werkt op mobiel
- [ ] Statustoggle werkt zonder console-errors

## Terugkoppelen aan Pieter
- Welke hosting-provider `debrabander.com` precies gebruikt, als dat niet uit de DNS is af te leiden.
- Welke versie (donker/licht) definitief live is gegaan.
