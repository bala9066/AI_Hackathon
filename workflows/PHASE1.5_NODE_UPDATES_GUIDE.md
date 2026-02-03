# Phase 1.5 Node Updates - Usage Guide

## Quick Reference

The file `phase1.5_node_updates.js` contains the enhanced JavaScript code for the **"Generate Final (FS)"** node in your Phase 1.5 workflow.

## What's Included

### ✅ Enhanced BOM Generation
- Real part numbers (manufacturer PN, supplier PN)
- Proper CSV formatting with all fields
- Cost calculations and totals
- Datasheet links

### ✅ Power Budget Analysis  
- Voltage rail calculations
- Current and power per rail
- Efficiency calculations (85% default)
- Input power requirements
- Total system power

### ✅ RF Analysis (for RF systems)
- Frequency range and output power
- **Link budget calculations**
- PA specifications and efficiency
- DC power requirements
- **Thermal analysis** (heat dissipation)
- Signal chain breakdown

## How to Use

### Option 1: Copy to n8n Node (Recommended)

1. Open your workflow in n8n
2. Find the **"Generate Final (FS)"** node
3. Click to edit
4. Copy **all code** from `phase1.5_node_updates.js`
5. Paste into the node's code editor
6. Save the workflow

### Option 2: Import Updated Workflow

The easier approach is to just import `Phase1.5_ProductionGrade.json` which already has this code:

1. Import workflow: `workflows/Phase1.5_ProductionGrade.json`
2. Configure credentials
3. Test immediately

## Output Files

After running Phase 1.5, you'll get:

| File | Contents |
|------|----------|
| `BOM.csv` | Full bill of materials with real part numbers and pricing |
| `Power_Budget.csv` | Voltage rails, current, power calculations with efficiency |
| `RF_Analysis.csv` | Link budget, PA specs, thermal analysis (RF systems only) |

## Key Improvements Over Phase 1

| Feature | Phase 1 | Phase 1.5 |
|---------|---------|-----------|
| BOM Part Numbers | "undefined" | Real manufacturer PNs |
| Power Budget | Placeholder text | Calculated voltage/current/power |
| RF Analysis | Placeholder text | Link budget + thermal analysis |
| Calculations | None | Formulas for all parameters |
| Datasheet Links | Missing | Included in BOM |

## Testing

Test with this input:
```
Design RF system with Xilinx Artix-7 FPGA, 
40dBm output power, 5-18GHz frequency range, 
buck-boost converters for power
```

**Expected Results:**
- BOM has real Xilinx part numbers
- Power Budget shows voltage rails (1.0V, 1.8V, 3.3V, 28V)
- RF Analysis includes PA efficiency, thermal calculations
- No "undefined" values anywhere

## Extract Files from Docker

```bash
docker cp n8n:/home/node/.n8n/BOM.csv ./output/
docker cp n8n:/home/node/.n8n/Power_Budget.csv ./output/
docker cp n8n:/home/node/.n8n/RF_Analysis.csv ./output/
```

---

**Next Steps:** Import Phase1.5_ProductionGrade.json and test!
