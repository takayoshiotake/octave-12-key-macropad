# NOTE

- Hot-swap sockets for MX compatible switches
  - Kailh CPG151101S11-x
    - <http://www.kailh.com/en/Products/Ks/HPC/>

- Incremental encoder with push momentary switch
  - Bourns PEC11R-4xxxF-Sxxxx
    - <https://www.bourns.com/products/encoders/contacting-encoders/product/PEC11R>
  - Bourns PEC12R-4xxxF-Sxxxx
    - <https://www.bourns.com/products/encoders/contacting-encoders/product/PEC12R>

- Stick Controller
  - Alps Alpine RKJXV/RKJX2 Series - RKJXV122400R
    - <https://tech.alpsalpine.com/prod/e/html/multicontrol/potentiometer/rkjxk/rkjxk_list.html>

- Tactile Switch
  - Alps Alpine SKRP Series - SKRPANE010, SKRPABE010
    - <https://tech.alpsalpine.com/prod/e/html/tact/surfacemount/skrp/skrp_list.html>

- Programmable firmware (CircuitPython)
  - <https://circuitpython.org/>
  - <https://docs.circuitpython.org/en/latest/BUILDING.html>

- Adafruit QT Py RP2040
  - <https://www.adafruit.com/product/4900>
  - <https://circuitpython.org/board/adafruit_qtpy_rp2040/>

- Pimoroni PGA2040
  - <https://shop.pimoroni.com/products/pga2040?variant=39359629656147>
  - <https://circuitpython.org/board/pimoroni_pga2040/>

- Seeed XIAO RP2040
  - <https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html>

- RP2040
  - <https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf>

- Serial NOR Flash
  - Windbond W25Q64JVSSIQ
    - <https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/index.html?__locale=en&partNo=W25Q64JV>

- USB-C
  - To use USB2.0 with USB-C, the CC1 and CC2 pins need pull down 5.1K.
    - <https://www.microchip.com/en-us/application-notes/an1914>
  - Molex 1054500101
    - <https://www.molex.com/molex/products/part-detail/io_connectors/1054500101>
  - Korean Hroparts Electronics TYPE-C-31-M-12
    - <http://www.krhro.com/USBjack/20180124/764.html>

- Power
  - Diodes AP2112K-3.3
    - <https://www.diodes.com/part/view/AP2112/>

- Crystal Resonator
  - Yangxing Tech YSX321SL 12Mhz (SMD3225-4)
    - <https://www.yangxing.hk/products-detail/ysx321sl>
  - `CL = (C1 * C2) / (C1 + C2) + C(~5pF) => C1 = C2 = (CL - 5pF) * 2`
    - `CL = 20pF => C = 30pF`

- LED
  - WS2812C-2020-V1
    - <http://www.world-semi.com/solution/list-4-1.html>
    - <https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_Worldsemi-WS2812C-2020-V1_C2976072.html>

- General-purpose case
  - WSC10-14-5W
    - <https://www.takachi-el.co.jp/products/WSC>

- FFC
  - Molex 15166012x (0.5mm pitch, 12 circuits, Type D)
    - <https://www.molex.com/molex/products/part-detail/cable/0151660122>
    - <https://www.molex.com/molex/products/part-detail/cable/0151660126>

## PCB

- JLCPCB
  - RP2040: <https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=RP2040>
  - ATMEGA32U4-MU: <https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=ATMEGA32U4-MU>
  - AFC01-S08FCC-00: <https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=AFC01-S08FCC-00>
  - AFC01-S12FCC-00: <https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=AFC01-S12FCC-00>
