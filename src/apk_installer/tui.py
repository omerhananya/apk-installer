from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Label
from apk_installer.adb import Device

class MatrixApp(App):
    """The core selection matrix TUI."""
    
    CSS = """
    DataTable {
        height: 1fr;
        border: solid green;
    }
    """
    
    def __init__(self, apks: list[str], devices: list[Device]):
        super().__init__()
        self.apks = apks
        self.devices = devices

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Select APKs to install on {len(self.devices)} devices")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("APK", width=30)
        for dev in self.devices:
            table.add_column(f"{dev.model}\n({dev.serial})")
        
        for apk in self.apks:
            table.add_row(apk, *["[ ]" for _ in self.devices])
