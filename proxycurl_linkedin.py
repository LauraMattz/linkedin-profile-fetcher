import os
import requests
import shelve
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text


# Configuração da API ProxyCurl:
PROXYCURL_API_URL = "https://nubela.co/proxycurl/api/v2/linkedin"
PROXYCURL_API_PIC_URL = "https://nubela.co/proxycurl/api/linkedin/person/profile-picture"
PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")  # <--- Use variável de ambiente

if not PROXYCURL_API_KEY:
    raise ValueError("A chave de API PROXYCURL_API_KEY não foi configurada. Defina-a como variável de ambiente.")

# Defina aqui as URLs dos perfis LinkedIn
LINKEDIN_URLS = [
    "https://www.linkedin.com/in/taisdeverdade/",
]

# Cache local em arquivo usando shelve
CACHE_PATH = Path.cwd() / "linkedin_cache.db"

console = Console()

def format_period(start, end):
    start_month = start.get('month', 'N/A')
    start_year = start.get('year', 'N/A')
    if end:
        end_month = end.get('month', '')
        end_year = end.get('year', '')
        end_str = f"{end_month}/{end_year}" if end_month and end_year else "Atualmente"
    else:
        end_str = "Atualmente"
    return f"{start_month}/{start_year} - {end_str}"


def fetch_data(linkedin_url):
    """
    Busca dados do perfil do LinkedIn via ProxyCurl ou do cache local.
    """
    with shelve.open(str(CACHE_PATH)) as cache:
        key = f"data:{linkedin_url}"
        if key in cache:
            console.print(f"[grey]Usando cache para dados de {linkedin_url}[/grey]")
            return cache[key]

        console.print(f"🔄 Requisição de dados para {linkedin_url}...")
        headers = {"Authorization": f"Bearer {PROXYCURL_API_KEY}"}
        params = {"url": linkedin_url}
        resp = requests.get(PROXYCURL_API_URL, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        experiences = []
        for exp in data.get("experiences", []):
            start = exp.get('starts_at') or {}
            end = exp.get('ends_at') or {}
            experiences.append({
                "empresa": exp.get("company", "N/A"),
                "cargo": exp.get("title", "N/A"),
                "local": exp.get("location", "N/A"),
                "periodo": format_period(start, end)
            })
        profile = {
            "nome": data.get("full_name", "N/A"),
            "cargo_atual": data.get("occupation", "N/A"),
            "headline": data.get("headline", "N/A"),
            "resumo": data.get("summary", "N/A"),
            "localizacao": f"{data.get('city','N/A')}, {data.get('state','N/A')}, {data.get('country_full_name','N/A')}",
            "experiencias": experiences
        }
        cache[key] = profile
        return profile


def display_profile(profile, idx):
    # Cabeçalho
    header = Text(f"{profile['nome']}\n", style="bold magenta")
    header.append(f"{profile['cargo_atual']}", style="bold yellow")
    panel = Panel(header, title=f"✨ Perfil {idx} ✨", expand=False, border_style="blue")
    console.print(panel)

    # Informações básicas
    info_table = Table.grid(padding=1)
    info_table.add_column(justify="right", style="cyan", no_wrap=True)
    info_table.add_column()
    info_table.add_row("📰 Headline:", profile['headline'])
    info_table.add_row("📍 Localização:", profile['localizacao'])
    console.print(info_table)

    # Resumo
    console.print(Panel(profile['resumo'], title="📝 Resumo", border_style="green"))

    # Experiências
    exp_table = Table(title="💼 Experiências Profissionais", show_lines=True)
    exp_table.add_column("Empresa", style="bold green")
    exp_table.add_column("Cargo", style="green")
    exp_table.add_column("Local", style="green")
    exp_table.add_column("Período", style="green")
    for exp in profile['experiencias']:
        exp_table.add_row(exp['empresa'], exp['cargo'], exp['local'], exp['periodo'])
    console.print(exp_table)

if __name__ == "__main__":
    console.print(f"[bold]Usando cache em: {CACHE_PATH}\n[/bold]")
    for idx, url in enumerate(LINKEDIN_URLS, start=1):
        console.rule(f"Processando perfil {idx}")
        try:
            profile = fetch_data(url)
            display_profile(profile, idx)
        except Exception as e:
            console.print(f"[bold red]Erro no perfil {idx}: {e}[/bold red]")
