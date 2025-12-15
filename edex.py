import time
import random
import psutil
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn

console = Console()

# ================= BOOT =================
BOOT_LINES = [
    "[ OK ] Initializing kernel modules",
    "[ OK ] Mounting /proc",
    "[ OK ] Mounting /sys",
    "[ OK ] Starting udev",
    "[ OK ] Detecting hardware",
    "[ OK ] Loading network stack",
    "[ OK ] Bringing up interfaces",
    "[ OK ] Starting system services",
    "[ OK ] Launching UI shell",
]

ASCII_LOGO = [
    " ███████╗██████╗ ███████╗██╗  ██╗",
    " ██╔════╝██╔══██╗██╔════╝╚██╗██╔╝",
    " █████╗  ██║  ██║█████╗   ╚███╔╝ ",
    " ██╔══╝  ██║  ██║██╔══╝   ██╔██╗ ",
    " ███████╗██████╔╝███████╗██╔╝ ██╗",
    " ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝",
]

def typewriter(text, speed=0.02):
    for c in text:
        console.print(c, end="", style="green")
        time.sleep(speed)
    console.print()

def glitch(text):
    for _ in range(2):
        console.print(text, style=random.choice(["green","bright_green","bright_black"]), end="\r")
        time.sleep(0.05)
    console.print(text, style="green")

def boot():
    console.clear()
    console.print("\n".join(ASCII_LOGO), style="bright_green")
    time.sleep(0.5)

    for line in BOOT_LINES:
        typewriter(line)
        glitch(line)
        with Progress(
            BarColumn(bar_width=30),
            TextColumn("{task.percentage:>3.0f}%"),
            transient=True
        ) as p:
            t = p.add_task("Loading", total=100)
            for i in range(0, 101, random.randint(8, 15)):
                p.update(t, completed=i)
                time.sleep(0.04)

    console.print("\n[bold green]System ready[/bold green]")
    time.sleep(0.6)

# ================= MATRIX =================
HEX = "0123456789ABCDEFabcdefghijklmnopqrstuvwxyz"
FADE = ["bright_green","green","bright_black","black"]

def matrix_line(w):
    return [random.choice(HEX) for _ in range(w)]

# ================= STATS REALI =================
prev_bytes_sent = psutil.net_io_counters().bytes_sent
prev_bytes_recv = psutil.net_io_counters().bytes_recv

def system_stats_table(uptime):
    global prev_bytes_sent, prev_bytes_recv

    cpu = int(psutil.cpu_percent())
    ram = int(psutil.virtual_memory().percent)

    net = psutil.net_io_counters()
    net_up = (net.bytes_sent - prev_bytes_sent) / 1024
    net_down = (net.bytes_recv - prev_bytes_recv) / 1024
    prev_bytes_sent = net.bytes_sent
    prev_bytes_recv = net.bytes_recv

    table = Table.grid(expand=True)
    table.add_column(justify="left")
    table.add_column(justify="right")

    cpu_bar = "█" * (cpu // 2) + "-" * ((100 - cpu) // 2)
    ram_bar = "█" * (ram // 2) + "-" * ((100 - ram) // 2)

    table.add_row("CPU", f"[cyan]{cpu_bar}[/cyan] {cpu}%")
    table.add_row("RAM", f"[magenta]{ram_bar}[/magenta] {ram}%")
    table.add_row("NET ↑", f"{net_up:.1f} kB/s")
    table.add_row("NET ↓", f"{net_down:.1f} kB/s")
    table.add_row("UPTIME", f"{uptime}s")

    return table

# ================= CONSOLE =================
console_log = []

def console_feed(max_lines=12):
    cmds = [
        "[green]scan[/green] 10.0.0.0/24",
        "[yellow]decrypt[/yellow] aes256",
        "[cyan]handshake[/cyan] ok",
        "[red]inject[/red] payload",
        "[magenta]analyzing[/magenta] ports",
        "[bold green]access granted[/bold green]",
        "[bright_yellow]firewall bypassed[/bright_yellow]",
        "[red]warning[/red] anomaly detected",
    ]

    line = random.choice(cmds)
    if random.random() < 0.12:
        line = f"[bright_white]{line}[/bright_white]"

    console_log.append(line)
    if len(console_log) > max_lines:
        console_log.pop(0)

    return "\n".join(console_log)

# ================= MAIN =================
def main():
    boot()

    layout = Layout()
    layout.split_column(
        Layout(name="top", size=12),
        Layout(name="bottom")
    )

    layout["top"].split_row(
        Layout(name="logo"),
        Layout(name="stats")
    )

    layout["bottom"].split_row(
        Layout(name="matrix"),
        Layout(name="console")
    )

    h, w = 20, 40
    buffer = [[(" ", len(FADE)-1) for _ in range(w)] for _ in range(h)]
    uptime = 0

    with Live(layout, refresh_per_second=12, screen=True):
        while True:
            layout["logo"].update(
                Panel(Text("\n".join(ASCII_LOGO), style="bold green"),
                      title="eDEX-UI Python", border_style="green")
            )

            layout["stats"].update(
                Panel(system_stats_table(uptime),
                      title="SYSTEM",
                      border_style="magenta")
            )

            buffer.pop(0)
            buffer.append([(c,0) for c in matrix_line(w)])

            lines = []
            for row in buffer:
                s = ""
                for c,l in row:
                    col = FADE[min(l, len(FADE)-1)]
                    s += f"[{col}]{c}[/{col}]"
                lines.append(s)

            buffer = [[(c,min(l+1,len(FADE)-1)) for c,l in r] for r in buffer]

            layout["matrix"].update(
                Panel("\n".join(lines),
                      title="HEX STREAM",
                      border_style="yellow")
            )

            layout["console"].update(
                Panel(console_feed(),
                      title="CONSOLE",
                      border_style="cyan")
            )

            uptime += 1
            time.sleep(0.3)

if __name__ == "__main__":
    main()
