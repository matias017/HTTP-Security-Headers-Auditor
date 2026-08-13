import requests
from colorama import Fore, Style, init

# Inicializar colores en terminal
init(autoreset=True)

# Cabeceras de seguridad clave y su importancia
SECURITY_HEADERS = {
    "Strict-Transport-Security": "Protege contra ataques Man-in-the-Middle (HSTS).",
    "Content-Security-Policy": "Previene ataques XSS e inyecciones de contenido.",
    "X-Frame-Options": "Protege contra Clickjacking.",
    "X-Content-Type-Options": "Evita la interpretación incorrecta de tipos MIME.",
    "Referrer-Policy": "Controla cuánta información de referencia se envía.",
    "Permissions-Policy": "Restringe el acceso a funciones del navegador (cámara, micro, etc.)."
}

def audit_headers(url):
    # Asegurar formato URL correcto
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(f"\n[*] Auditando cabeceras de seguridad para: {Fore.CYAN}{url}{Style.RESET_ALL}\n")

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        missing_headers = []
        present_headers = []

        # Evaluar cabeceras
        for header, description in SECURITY_HEADERS.items():
            if header in headers:
                present_headers.append((header, headers[header]))
            else:
                missing_headers.append((header, description))

        # --- MOSTRAR RESULTADOS ---
        print(f"{Fore.GREEN}=== CABECERAS PRESENTES ({len(present_headers)}/{len(SECURITY_HEADERS)}) ===")
        for header, value in present_headers:
            print(f"{Fore.GREEN}[✓] {header}: {Style.RESET_ALL}{value}")

        print(f"\n{Fore.RED}=== CABECERAS FALTANTES O RIESGOS ({len(missing_headers)}) ===")
        for header, desc in missing_headers:
            print(f"{Fore.RED}[X] {header}{Style.RESET_ALL} -> {desc}")

        # Puntuación básica
        score = (len(present_headers) / len(SECURITY_HEADERS)) * 100
        print("\n" + "="*50)
        color_score = Fore.GREEN if score >= 70 else (Fore.YELLOW if score >= 40 else Fore.RED)
        print(f"Puntuación de Postura Web: {color_score}{score:.1f}%{Style.RESET_ALL}")
        print("="*50)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error al conectar con la URL: {e}")

if __name__ == "__main__":
    target = input("Ingresa el dominio a auditar (ej. example.com): ")
    if target.strip():
        audit_headers(target.strip())