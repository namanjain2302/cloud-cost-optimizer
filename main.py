import os
import sys
import json
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich.json import JSON
from dotenv import load_dotenv
import shutil
from datetime import datetime
# Internal imports
from src.core_logic import extract_project_profile, generate_mock_billing, generate_optimization_report

# Load environment variables
load_dotenv()

console = Console()

DESCRIPTION_FILE = "project_description.txt"
PROFILE_FILE = "project_profile.json"
BILLING_FILE = "mock_billing.json"
REPORT_FILE = "cost_optimization_report.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_env():
    """Checks if the HF_API_TOKEN is set."""
    token = os.getenv("HF_API_TOKEN")
    if not token:
        console.print(Panel("[bold red]Error: HF_API_TOKEN not found in .env file.[/bold red]\nPlease create a .env file with your Hugging Face API token.", title="Configuration Error"))
        sys.exit(1)

def view_file(filepath, title):
    """Reads and displays a JSON file prettily."""
    if not os.path.exists(filepath):
        console.print(f"[yellow]File {filepath} does not exist yet.[/yellow]")
        return

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        console.print(Panel(JSON.from_data(data), title=title))
    except Exception as e:
        console.print(f"[red]Error reading {filepath}: {e}[/red]")


def export_report():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("exports", exist_ok=True)
    dest = f"exports/cost_optimization_report_{ts}.json"
    shutil.copy(REPORT_FILE, dest)
    console.print(f"[green]Report exported to {dest}[/green]")

def input_description():
    """Step 1: Get user input for project description."""
    clear_screen()
    console.print(Panel("[bold blue]Step 1: Enter Project Description[/bold blue]", subtitle="Input"))
    
    console.print("You can enter the description manually, or press Enter to keep the existing file content if present.")
    
    current_content = ""
    if os.path.exists(DESCRIPTION_FILE):
        with open(DESCRIPTION_FILE, 'r') as f:
            current_content = f.read()
        console.print(f"\n[dim]Current content:[/dim]\n{current_content}\n")
    
    mode = Prompt.ask("Choose mode", choices=["Overwrite", "Keep Existing", "Cancel"], default="Keep Existing")
    
    if mode == "Overwrite":
        console.print("[green]Enter your project description (press Enter twice to finish):[/green]")
        lines = []
        while True:
            line = input()
            if not line and lines and not lines[-1]: # Break on double enter
                break
            lines.append(line)
        
        text = "\n".join(lines).strip()
        if text:
            with open(DESCRIPTION_FILE, 'w') as f:
                f.write(text)
            console.print(f"[bold green]Saved to {DESCRIPTION_FILE}[/bold green]")
        else:
            console.print("[yellow]No text entered. Operation skipped.[/yellow]")

def run_full_analysis():
    """Step 2: Run the full pipeline (Extraction -> Billing -> Analysis)."""
    clear_screen()
    console.print(Panel("[bold blue]Step 2: Running Complete Cost Analysis[/bold blue]", subtitle="Processing"))
    
    # 1. Profile Extraction
    if not os.path.exists(DESCRIPTION_FILE):
        console.print(f"[red]Error: {DESCRIPTION_FILE} not found. Please run Step 1 first.[/red]")
        return

    with console.status("[bold green]Extracting Project Profile from LLM...[/bold green]"):
        try:
            with open(DESCRIPTION_FILE, 'r') as f:
                desc_text = f.read()
            profile = extract_project_profile(desc_text)
            with open(PROFILE_FILE, 'w') as f:
                json.dump(profile, f, indent=4)
            console.print(f"[green]✓ Profile saved to {PROFILE_FILE}[/green]")
        except Exception as e:
            console.print(f"[bold red]Failed to extract profile: {e}[/bold red]")
            return

    # 2. Synthetic Billing
    with console.status("[bold green]Generating Synthetic Billing Data...[/bold green]"):
        try:
            billing_data = generate_mock_billing(profile)
            with open(BILLING_FILE, 'w') as f:
                json.dump(billing_data, f, indent=4)
            console.print(f"[green]✓ Billing data ({len(billing_data)} records) saved to {BILLING_FILE}[/green]")
        except Exception as e:
            console.print(f"[bold red]Failed to generate billing: {e}[/bold red]")
            return

    # 3. Cost Analysis & Recommendations
    with console.status("[bold green]Analyzing Costs & Generating Recommendations...[/bold green]"):
        try:
            report = generate_optimization_report(profile, billing_data)
            with open(REPORT_FILE, 'w') as f:
                json.dump(report, f, indent=4)
            console.print(f"[green]✓ Final Report saved to {REPORT_FILE}[/green]")
        except Exception as e:
            console.print(f"[bold red]Failed to generate report: {e}[/bold red]")
            return

    console.print(Panel("[bold green]Analysis Complete![/bold green]\nYou can now view the recommendations."))

def main_menu():
    check_env()
    while True:
        clear_screen()
        console.print(Panel.fit(
            "[bold cyan]AI-Powered Cloud Cost Optimizer[/bold cyan]\n",
            subtitle="Main Menu"
        ))
        
        console.print("1. [bold]Enter/Edit Project Description[/bold]")
        console.print("2. [bold]Run Complete Cost Analysis[/bold] (Pipeline)")
        console.print("3. [bold]View Generated Recommendations[/bold]")
        console.print("4. [bold]View Intermediate Files[/bold] (Profile/Billing)")
        console.print("5. [bold]Export Report[/bold]")
        console.print("6. [bold]Exit[/bold]")

        
        choice = IntPrompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5"])
        
        if choice == 1:
            input_description()
            Prompt.ask("\nPress Enter to return to menu...")
        elif choice == 2:
            run_full_analysis()
            Prompt.ask("\nPress Enter to return to menu...")
        elif choice == 3:
            clear_screen()
            view_file(REPORT_FILE, "Cost Optimization Report")
            Prompt.ask("\nPress Enter to return to menu...")
        elif choice == 4:
            clear_screen()
            view_file(PROFILE_FILE, "Project Profile")
            console.print("\n")
            view_file(BILLING_FILE, "Synthetic Billing Data")
            Prompt.ask("\nPress Enter to return to menu...")
        elif choice== 5:
            clear_screen()
            export_report()
        elif choice == 6:
            console.print("[green]Goodbye![/green]")
            break

if __name__ == "__main__":
    main_menu()