# Measurement Methodology

CoalOmIT (COMIT) combines hardware FLOP counting with regional carbon intensity data to calculate model carbon footprints.

## 1. Energy Footprint Calculation

Energy consumption is calculated using PyTorch 2.x native `FlopCounterMode`:

$$\text{Energy (Wh)} = \frac{\text{FLOPs} \times E_{\text{op\_J}}}{3600}$$

### Precision Energy Constants ($E_{\text{op\_J}}$)
- **FP32**: $5.0 \times 10^{-14}\text{ J/FLOP}$
- **FP16**: $2.5 \times 10^{-14}\text{ J/FLOP}$
- **INT8**: $1.25 \times 10^{-14}\text{ J/FLOP}$
- **INT4**: $0.8 \times 10^{-14}\text{ J/FLOP}$

## 2. Carbon Footprint Projection

$$\text{Carbon Emissions (gCO}_2\text{eq)} = \text{Energy (kWh)} \times \text{Grid Intensity (gCO}_2\text{eq/kWh})$$

Monthly grid intensity averages are maintained across 35+ country regions using static datasets backed by global energy datasets.
