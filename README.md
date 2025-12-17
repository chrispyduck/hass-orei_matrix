# Orei HDMI Matrix - Home Assistant Custom Integration

Control your **Orei HDMI Matrix** switch directly from **Home Assistant** via Telnet.

Supports power control, input/output switching, live state updates, and configurable names.
Compatible with multiple Orei models such as **UHD48-EX230-K**, etc.

---

## ✨ Features

- 🧠 **Automatic model detection** (`r type!`)
- 🔌 **Global power control** (on/off via switch)
- 🎛 **Per-output input selection** via select entities
- ✏️ **Configurable input/output names** via text entities
- 🔄 **Manual refresh service** (`orei_matrix.refresh`)
- 🧩 **Dynamic device grouping** (all entities under one device)
- 🪄 **Config Flow setup** (no YAML required)
- 🧰 **Support for 4x4, 8x8, and other Orei matrix models**

---

## 🖼 Example UI

When configured, you'll see a single device in Home Assistant:

> **Orei UHD48-EX230-K**
>
> - 🔌 `switch.orei_matrix_power`
> - 🎛 `select.living_room_input`
> - 🎛 `select.bedroom_input`
> - 🎛 `select.office_input`
> - 🎛 `select.patio_input`
>
> **Configuration**
>
> - ✏️ `text.input_1_name`
> - ✏️ `text.input_2_name`
> - ✏️ `text.input_3_name`
> - ✏️ `text.input_4_name`
> - ✏️ `text.output_1_name`
> - ✏️ `text.output_2_name`
> - ✏️ `text.output_3_name`
> - ✏️ `text.output_4_name`

---

## ⚙️ Installation

### 🧩 HACS (Recommended)

1. Go to **HACS → Integrations → Custom Repositories**
2. Add this repository URL https://github.com/taysuus/hass-orei-matrix as type **Integration**
3. Search for **Orei HDMI Matrix** and install it.
4. Restart Home Assistant.

### 📦 Manual

1. Copy the `custom_components/orei_matrix` folder into: <config>/custom_components/orei_matrix/
2. Restart Home Assistant.

---

## 🧠 Configuration

Set up via the **Home Assistant UI**:

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Orei HDMI Matrix**
3. Enter:

- **Host** (IP of your Orei Matrix)
- **Port** (default: 23)
- **Source Names** (e.g. `"Apple TV"`, `"Blu-ray"`, `"PC"`, `"Game Console"`)
- **Zone Names** (e.g. `"Living Room"`, `"Bedroom"`, `"Patio"`, `"Office"`)

That’s it — entities will be created automatically.

---

## 🧩 Entities

| Entity                     | Description                                               |
| -------------------------- | --------------------------------------------------------- |
| `switch.orei_matrix_power` | Controls main matrix power                                |
| `select.<output>_input`    | Select which input is routed to each output              |
| `text.input_X_name`        | Configure the name for input X (Configuration category)  |
| `text.output_X_name`       | Configure the name for output X (Configuration category) |

### Select Entities

Each output gets a select entity that:

- Shows all available inputs as options
- Displays the currently selected input
- Sends routing commands to the matrix when changed
- Is grayed out when matrix power is off

### Text Entities

Input and output names can be customized via text entities:

- Enter a custom name (1-50 characters)
- Changes are saved to the integration configuration
- The integration automatically reloads to apply new names
- Updated names appear in all select entities and UI elements

---

## 🧰 Services

### `orei_matrix.refresh`

Manually refreshes all matrix states immediately — power, model, and routing.

#### Example usage (Developer Tools → Services)

```yaml
service: orei_matrix.refresh
```
