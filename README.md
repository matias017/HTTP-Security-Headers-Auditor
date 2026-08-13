#  HTTP-Security-Headers-Auditor

Script en Python que audita las cabeceras de seguridad HTTP de cualquier sitio web y genera una puntuación de "postura de seguridad web", simulando una tarea real de hardening/auditoría que se le pide a un analista SOC junior.

## ¿Qué problema resuelve?

Muchas configuraciones inseguras de un sitio web no vienen de una vulnerabilidad de código, sino de **cabeceras HTTP mal configuradas o ausentes**. Este script automatiza la verificación de 6 cabeceras clave, algo que en una auditoría manual llevaría revisar una por una con DevTools o `curl -I`.

## Cabeceras evaluadas

| Cabecera | Qué previene |
|---|---|
| `Strict-Transport-Security` | Ataques Man-in-the-Middle (fuerza el uso de HTTPS) |
| `Content-Security-Policy` | Ataques XSS e inyección de contenido |
| `X-Frame-Options` | Clickjacking |
| `X-Content-Type-Options` | MIME sniffing / interpretación incorrecta de tipos de archivo |
| `Referrer-Policy` | Fuga de información a través del header Referer |
| `Permissions-Policy` | Acceso no autorizado a cámara, micrófono, geolocalización, etc. |

## Cómo funciona

1. Recibe un dominio o URL por input.
2. Hace un `GET` request al sitio.
3. Compara las cabeceras de la respuesta contra el set de 6 cabeceras esperadas.
4. Muestra en consola (con colores vía `colorama`) cuáles están presentes y cuáles faltan, junto con el riesgo asociado a cada ausencia.
5. Calcula un score simple: `(cabeceras presentes / 6) * 100`.

## Instalación

```bash
git clone https://github.com/tu-usuario/HTTP-Security-Headers-Auditor.git
cd HTTP-Security-Headers-Auditor
pip install -r requirements.txt
```

## Uso

```bash
python header_audit.py
Ingresa el dominio a auditar (ej. google.com)
```

También se puede adaptar fácilmente para recibir el dominio como argumento en vez de input interactivo (ver sección "Posibles mejoras").

## Ejemplo de salida

Ver en la carpeta de eidencia

## Alcance y consideraciones éticas

Este script solo hace un `GET` request estándar y lee las cabeceras de la respuesta HTTP — es exactamente lo mismo que hace cualquier navegador al visitar una página. No envía payloads, no intenta explotar nada y no realiza ningún tipo de escaneo intrusivo. Es seguro correrlo contra cualquier sitio público.

## Limitaciones actuales

- No valida el *contenido* de las cabeceras presentes, solo si existen (por ejemplo, no chequea si el `Content-Security-Policy` está bien configurado o es demasiado permisivo, tipo `default-src *`).
- No sigue redirecciones de forma explícita ni compara `http://` vs `https://`.
- El scoring es una métrica simple (conteo), no pondera cabeceras por criticidad.

## Posibles mejoras (roadmap)

- [ ] Validar el contenido de `Content-Security-Policy` y marcar como riesgo configuraciones demasiado permisivas.
- [ ] Aceptar el dominio como argumento CLI (`argparse`) en vez de input interactivo, para poder integrarlo en scripts de automatización.
- [ ] Exportar el resultado a JSON/CSV para poder auditar múltiples dominios en batch.
- [ ] Sumar chequeo de versión de TLS/certificado como complemento.

## Stack

- Python 3.10+
- [`requests`](https://pypi.org/project/requests/) — cliente HTTP
- [`colorama`](https://pypi.org/project/colorama/) — salida en color por terminalTP-Security-Headers-Auditor
