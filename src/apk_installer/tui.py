from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Label
from textual import on
from apk_installer.adb import Device, install_apk
import asyncio

class MatrixApp(App):
    """The core selection matrix TUI."""
    
    BINDINGS = [
        ("i", "install", "Install Selected"),
        ("q", "quit", "Quit"),
    ]
    
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
        # selection_matrix[apk_index][device_index] = bool
        self.selections = [[False for _ in devices] for _ in apks]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Select APKs to install. Press 'i' to start installation.")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "cell"
        table.add_column("APK", width=30)
        for dev in self.devices:
            table.add_column(f"{dev.model}\n({dev.serial})")
        
        for apk in self.apks:
            table.add_row(apk, *["[ ]" for _ in self.devices])

    @on(DataTable.CellSelected)
    def toggle_cell(self, event: DataTable.CellSelected) -> None:
        """Toggle the selection state of a cell."""
        table = event.data_table
        row_index = event.coordinate.row
        col_index = event.coordinate.column
        
        # Skip the first column (APK names)
        if col_index == 0:
            return
            
        device_idx = col_index - 1
        current_state = self.selections[row_index][device_idx]
        new_state = not current_state
        self.selections[row_index][device_idx] = new_state
        
        new_label = "[x]" if new_state else "[ ]"
        table.update_cell_at(event.coordinate, new_label)

    async def action_install(self) -> None:
        """Run the installation process for all selected combinations."""
        self.notify("Starting installation...")
        tasks = []
        for apk_idx, apk in enumerate(self.apks):
            for dev_idx, device in enumerate(self.devices):
                if self.selections[apk_idx][dev_idx]:
                    tasks.append(self.install_and_update(device, apk, apk_idx, dev_idx + 1))
        
        if not tasks:
            self.notify("No installations selected!", severity="warning")
            return
            
        await asyncio.gather(*tasks)
        self.notify("All installations complete!")

    async def install_and_update(self, device: Device, apk: str, row: int, col: int) -> None:
        """Install a single APK and update the table with results."""
        table = self.query_one(DataTable)
        table.update_cell_at((row, col), "[...]") # Installing
        
        success, stdout, stderr = await install_apk(device.serial, apk)
        
        if success:
            table.update_cell_at((row, col), "[OK]")
        else:
            table.update_cell_at((row, col), "[ERR]")
            # We could log error details here if needed
