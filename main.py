import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=ENV_PATH)

API_URL = "https://breachdirectory.p.rapidapi.com/"
HEADERS = {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
}
DELAY = 2
INPUT_FILE = "email.txt"
OUTPUT_FILE = "resultado.xlsx"


def load_api_key():
    key = os.environ.get("BREACHDIRECTORY_API_KEY")
    if key:
        return key

    print("Erro: API Key não encontrada no arquivo .env")
    print("Copie .env.example para .env e insira sua API Key:")
    print("  cp .env.example .env")
    return None


def read_emails(filepath):
    emails = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            email = line.strip()
            if email and "@" in email:
                emails.append(email)
    return emails


def check_breach(email, api_key):
    headers = HEADERS.copy()
    headers["X-RapidAPI-Key"] = api_key

    params = {"func": "auto", "term": email}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            found = data.get("found", False)
            sources = data.get("sources", [])
            breaches = ", ".join([s.get("name", s) if isinstance(s, dict) else str(s) for s in sources]) if sources else "-"
            return "VAZADO" if found else "SEGURO", breaches

        elif response.status_code == 429:
            return "ERRO", "Rate limit excedido"

        elif response.status_code == 401:
            return "ERRO", "API Key inválida"

        else:
            return "ERRO", f"HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        return "ERRO", "Timeout"
    except requests.exceptions.RequestException as e:
        return "ERRO", str(e)


def main():
    print("=" * 50)
    print("  VERIFICADOR DE VAZAMENTO DE EMAILS (POC)")
    print("=" * 50)
    print()

    api_key = load_api_key()
    if not api_key:
        print("Erro: API Key não fornecida.")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"Erro: Arquivo '{INPUT_FILE}' não encontrado.")
        return

    emails = read_emails(INPUT_FILE)
    if not emails:
        print("Nenhum email válido encontrado no arquivo.")
        return

    print(f"Encontrados {len(emails)} emails para verificar.\n")

    results = []
    for email in tqdm(emails, desc="Verificando"):
        status, breaches = check_breach(email, api_key)
        results.append({
            "email": email,
            "status": status,
            "breaches": breaches,
            "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        time.sleep(DELAY)

    df = pd.DataFrame(results)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = f"resultado_{now}.xlsx"
    df.to_excel(output_name, index=False)

    print()
    print("=" * 50)
    print("  RESULTADO")
    print("=" * 50)
    print()

    for r in results:
        icon = "[!]" if r["status"] == "VAZADO" else "[OK]" if r["status"] == "SEGURO" else "[?]"
        print(f"  {icon} {r['email']}")
        print(f"      Status: {r['status']}")
        if r["breaches"] != "-":
            print(f"      Breaches: {r['breaches']}")
        print()

    vazados = sum(1 for r in results if r["status"] == "VAZADO")
    seguros = sum(1 for r in results if r["status"] == "SEGURO")
    erros = sum(1 for r in results if r["status"] == "ERRO")

    print(f"  Vazados: {vazados} | Seguros: {seguros} | Erros: {erros}")
    print()
    print(f"  Planilha salva em: {output_name}")
    print("=" * 50)


if __name__ == "__main__":
    main()
