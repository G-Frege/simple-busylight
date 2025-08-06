# Simple Busylight Daemon and CLI

This is a simple program that runs a **busylight daemon** and provides a **command-line interface (CLI)** for managing various busylights.

For detailed information on supported devices, please refer to the [supported_vendors](./supported_vendors).  
If you encounter any problems or have feature requests, feel free to contact me at **simplebusylightdev@gmail.com**.

---

### Disclaimer

This project is provided **as-is** without any warranties or guarantees. It is a small hobby project, so please use it at your own risk.

---

## Installation

### Arch Linux (AUR)

This program is available in the Arch User Repository (AUR) under the package name `simple-busylight`.  
You can install it using an AUR helper like `yay` or directly with `pacman` after building the package:

```bash
yay -S simple-busylight
# or, if you prefer manual build:
git clone https://aur.archlinux.org/simple-busylight.git
cd simple-busylight
makepkg -si
```

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
See [LICENSE](./LICENSE) for details.

This project uses `busylight-core`, which is licensed under the Apache License 2.0.
See [LICENSES/Apache-2.0.txt](./LICENSES/Apache-2.0.txt) for details.
