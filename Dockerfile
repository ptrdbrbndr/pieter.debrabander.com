# Stap 1: nginx-configuratie bouwen met de CSP-hashes uit de HTML.
FROM python:3.12-alpine AS conf
WORKDIR /work
COPY index.html licht-alternatief.html nginx.conf.template ./
COPY scripts/genereer-nginx-conf.py ./scripts/
RUN python3 scripts/genereer-nginx-conf.py

# Stap 2: de statische pagina serveren.
FROM nginx:1.27-alpine
COPY --from=conf /work/default.conf /etc/nginx/conf.d/default.conf
COPY index.html licht-alternatief.html /usr/share/nginx/html/
# De rechten uit de checkout zijn niet te vertrouwen (een Windows-werkboom
# levert 0640 op, en dan geeft nginx een 403). Daarom hier vastzetten.
RUN chmod 0644 /usr/share/nginx/html/index.html /usr/share/nginx/html/licht-alternatief.html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/health || exit 1
