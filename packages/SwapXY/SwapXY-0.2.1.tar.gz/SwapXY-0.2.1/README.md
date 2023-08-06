# SwapXY

An OctoPrint plugin to swap the X and Y axes used by the jog controls.

## Setup

Install via the plugin manager using this URL:

    https://gitlab.com/wolframmfg/octoprint-swapxy/-/archive/main/octoprint-swapxy-main.zip

As long as the plugin is enabled, the jog buttons for X and Y will
drive the other axis instead.

To drive one or both of these axes in the opposite direction (negative/positive), enable the reverse option for that axis.

## Config

These options can also be changed from the web UI settings window.

Default config:

```yaml
plugins:
    swapxy:
        reverse:
            X: false
            Y: false
```

---

Developed by

[![Wolfram Manufacturing](wolframmfg.png)](https://wolframmfg.com/)
