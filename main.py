"""Simple GUI application with buttons to shut down or restart the computer."""

import platform
import subprocess
import tkinter as tk
from tkinter import messagebox


def _run_command(command: list[str]) -> None:
    """Run a system command and handle potential errors gracefully."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        messagebox.showerror("Error", f"No se pudo ejecutar el comando: {exc}")
    except FileNotFoundError as exc:
        messagebox.showerror("Error", f"Comando no encontrado: {exc}")


def shutdown() -> None:
    """Shut down the computer using the appropriate command for the OS."""
    system = platform.system()
    if system == "Windows":
        _run_command(["shutdown", "/s", "/t", "0"])
    elif system in {"Linux", "Darwin"}:
        _run_command(["sudo", "shutdown", "-h", "now"])
    else:
        messagebox.showerror("Error", f"Sistema operativo no soportado: {system}")


def restart() -> None:
    """Restart the computer using the appropriate command for the OS."""
    system = platform.system()
    if system == "Windows":
        _run_command(["shutdown", "/r", "/t", "0"])
    elif system in {"Linux", "Darwin"}:
        _run_command(["sudo", "shutdown", "-r", "now"])
    else:
        messagebox.showerror("Error", f"Sistema operativo no soportado: {system}")


class PowerControlApp(tk.Tk):
    """Main application window with power control buttons."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Control de Energía")
        self.geometry("300x150")
        self.configure(padx=20, pady=20)

        label = tk.Label(
            self,
            text="Seleccione una acción",
            font=("Arial", 14),
        )
        label.pack(pady=(0, 10))

        shutdown_button = tk.Button(
            self,
            text="Apagar PC",
            command=self._confirm_shutdown,
            width=15,
            height=2,
            bg="#e74c3c",
            fg="white",
        )
        shutdown_button.pack(pady=5)

        restart_button = tk.Button(
            self,
            text="Reiniciar PC",
            command=self._confirm_restart,
            width=15,
            height=2,
            bg="#3498db",
            fg="white",
        )
        restart_button.pack(pady=5)

    def _confirm_shutdown(self) -> None:
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas apagar el PC?"):
            shutdown()

    def _confirm_restart(self) -> None:
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas reiniciar el PC?"):
            restart()


def main() -> None:
    app = PowerControlApp()
    if platform.system() in {"Linux", "Darwin"}:
        info = tk.Label(
            app,
            text=(
                "Puede que necesites ejecutar el programa\n"
                "con privilegios de administrador para que funcione."
            ),
            font=("Arial", 9),
            fg="#7f8c8d",
        )
        info.pack(pady=(10, 0))
    app.mainloop()


if __name__ == "__main__":
    main()
