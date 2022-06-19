# Octave

The Octave is a 12-key macropad.
It is primarily designed to be a compact keyboard with support for 12 function keys (F1 - F12).

## Status

- [ ] prototype-2: Custom MCU board
  - [ ] Test
  - [x] PCB
- [x] prototype-1

## Specifications

- USB-C (USB2.0, HID)
- Hot-swap sockets for MX compatible switches
- Incremental encoder with push momentary switch
- Stick controller with push momentary switch
- Programmable firmware (CircuitPython)
- No LEDs
- No keycaps
- No switches

## Layout

📄 [layout/keyboard-layout.png](layout/keyboard-layout.png) (rev.2)

![keyboard layout](layout/keyboard-layout.png)

- 12 function keys (F1 - F12)
- 1 momentary layer key (MO)
- 1 incremental encoder (Knob)
- 1 stick controller (Stick)

It is important that there are four rows.
Just like the function keys on many keyboards are divided into four rows each. It is also important that it is easy to operate with one hand.

It is designed to be used with the left hand.
In particular, the incremental encoder and stick controller are placed in easy-to-operate positions.

**RAW data for Keyboard Layout Editor v0.15:**

📄 [layout/keyboard-layout.rawdata.json](layout/keyboard-layout.rawdata.json)

```js
["F1","F2","F3","F4"],
["F5","F6","F7","F8"],
["F9","F10","F11","F12"],
["MO",{x:2,c:"#c8b273"},"Knob"],
[{y:-0.5,x:1.5,c:"#666666",t:"#cccccc"},"Stick"],
```

- 🔗 [Keyboard Layout Editor](http://www.keyboard-layout-editor.com/)

## Schematic

📄 [electronics/Octave_Input_PCB.svg](electronics/Octave_Input_PCB.svg) (rev.5.0.2)

![schematic svg](electronics/Octave_Input_PCB.svg)

I have also designed a custom MCU circuit from prototype-2, the MCU is RP2040 and the software runs on CircuitPython built specifically for it.

📄 [electronics/Octave_Input_PCB/Octave_Input_PCB.kicad_sch](electronics/Octave_Input_PCB/Octave_Input_PCB.kicad_sch)

## PCB

📄 [electronics/Octave_Input_PCB_3D.png](electronics/Octave_Input_PCB_3D.png) (rev.5.0.2)

![pcb 3d png](electronics/Octave_Input_PCB_3D.png)

📄 [electronics/Octave_Input_PCB/Octave_Input_PCB.kicad_pcb](electronics/Octave_Input_PCB/Octave_Input_PCB.kicad_pcb)

## CircuitPython

Software for the Octave (prototype-2) runs on CircuitPython.
You can fetch the CircuitPython source code for the Octave from the following GitHub repo.

**Stable:**

- 🔗 [takayoshiotake/circuitpython:7.3.x-board-octave-rp2040](https://github.com/takayoshiotake/circuitpython/tree/7.3.x-board-octave-rp2040)
  - <https://github.com/takayoshiotake/circuitpython/tree/c3b4d05dc04d74c6229506215eae799fb23f37ce/ports/raspberrypi/boards/takayoshiotake_octave_rp2040>

**Latest:**

- 🔗 [takayoshiotake/circuitpython:board-octave-rp2040](https://github.com/takayoshiotake/circuitpython/tree/board-octave-rp2040)
  - <https://github.com/takayoshiotake/circuitpython/tree/b0170044fc17d5b7c204f4581f8307e8e4ef7431/ports/raspberrypi/boards/takayoshiotake_octave_rp2040>

## BOM & Software

[WIP] prototype-2

**PCB:**

🏷 [prototype-2-pcb](https://github.com/takayoshiotake/octave-12-key-macropad/releases/tag/prototype-2-pcb)

| Material | Unit | Designator | Note | JLCPCB Part # |
|-|-:|-|-|-|
| Octave Input PCB rev.5.0.2 | 1 | n/a | JLCPCB |
| 30pF 0402 | 2 | C15, C16 | PCBA | C1570 |
| 10nF 0402 | 2 | C21, C22 | PCBA | C15195 |
| 100nF 0402 | 10 | C5-14 | PCBA | C307331 |
| 1uF 0402 | 4 | C1-4 | PCBA | C52923 |
| 1N4148WS | 15 | D1-15 | PCBA | C2128 |
| HRO_TYPE-C-31-M-12 | 1 | J1 | PCBA, USB Connector (Type-C) | C165948 |
| WS2812C-2020-V1 | 1 | LED1 | PCBA, NeoPixel | C2976072 |
| 27Ω 0402 | 2 | R3, R4 | PCBA | C352446 |
| 1KΩ 0402 | 2 | R7, R8 | PCBA | C11702 |
| 5.1KΩ 0402 | 2 | R1, R2 | PCBA | C25905 |
| 10KΩ 0402 | 4 | R5, R6, R12, R14 | PCBA | C25744 |
| 100KΩ 0402 | 2 | R11, R13 | PCBA | C25086 |
| AP2112K-3.3 | 1 | U1 | PCBA | C51118 |
| Raspberry Pi RP2040 | 1 | U2 | PCBA | C2040 |
| W25Q64JVSSIQ | 1 | U3 | PCBA | C179171 |
| 12MHz Crystal Resonator SMD-3225 | 1 | Y1 | PCBA, YSX221SL | C9002 |
| CPG151101S11-2 | 13 | SW1-13 | Kailh®︎ hot swap socket (White) |
| RKJXV122400R | 1 | SW14 | Alps Alpine stick controller |
| PEC12R-4217F-S0024-ND | 1 | SW15 | Bourns incremental encoder |
| SKRPANE010 | 1 | SW21, SW22 | PCBA, Alps Alpine tactile switch | C470426 |

**Software:**

- 📄 [software/README.md](software/README.md)

### History

- [[Closed] prototype-1](prototype-1/README.md)
