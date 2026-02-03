# Phase 1 Interactive V2 - Setup Guide

## Overview

This is the redesigned Phase 1 workflow with:
- ✅ Block diagram generation with approval gate
- ✅ Component search with selection gate
- ✅ Datasheet info extraction
- ✅ All files saved to `output/` folder

## Workflow Flow

```
User Input → Parse Requirements → Generate Block Diagram
                                         ↓
                              Save: block_diagram.json, .md
                                         ↓
                              ⏸️ WAIT FOR APPROVAL
                                         ↓
                              User: "approve" / "change X"
                                         ↓
                              Search Components (DigiKey + Mouser)
                                         ↓
                              Save: component_options.csv
                                         ↓
                              ⏸️ WAIT FOR SELECTION
                                         ↓
                              User: "approve" / "use option 2"
                                         ↓
                              Generate BOM + Power + RF
                                         ↓
                              Save: BOM.csv, Power_Budget.csv, RF_Analysis.csv
                                         ↓
                              Phase 1 Complete → Phase 2
```

## Files Generated

All files are saved to: `/home/node/.n8n/output/` (inside Docker)

| File | Format | When Created |
|------|--------|--------------|
| `block_diagram.json` | JSON | After parsing requirements |
| `block_diagram.md` | Markdown | After parsing requirements |
| `component_options.csv` | CSV | After DigiKey/Mouser search |
| `BOM.csv` | CSV | After component approval |
| `Power_Budget.csv` | CSV | After component approval |
| `RF_Analysis.csv` | CSV | After component approval |

## How to Use

### Step 1: Import Workflow
1. Open n8n: http://localhost:5678
2. Import: `workflows/Phase1_Interactive_V2.json`
3. Configure Groq credential
4. For Mouser: Add parameter `mouserKey` with your API key
5. Activate workflow

### Step 2: Start Chat
Type your requirements:
```
Design RF system with Xilinx Artix-7 FPGA, 
40dBm output power, 5-18GHz frequency range, 
buck-boost converters for power
```

### Step 3: Review Block Diagram
AI will generate and show:
- Component list
- Connections
- Power rails

**Your options:**
- `approve` - Continue to component search
- `change PA to higher power` - Modify diagram
- `add temperature sensor` - Add component

### Step 4: Select Components
AI will show 2-3 options per category from DigiKey and Mouser.

**Your options:**
- `approve` - Use recommended (⭐) options
- `use option 2 for FPGA` - Select specific option
- `search again for PA` - Re-search

### Step 5: Final Outputs
After approval:
- BOM with pricing
- Power budget analysis
- RF analysis (if applicable)
- All saved as CSV files

## Approval Commands

| Command | Action |
|---------|--------|
| `approve` | Accept current step |
| `yes` / `ok` | Same as approve |
| `change X to Y` | Modify X component |
| `add component Z` | Add new component |
| `use option N for X` | Select specific option |
| `search again for X` | Re-search component |

## Access Output Files

### Option 1: Docker Volume
```bash
docker exec -it n8n ls /home/node/.n8n/output/
docker cp n8n:/home/node/.n8n/output/ ./output/
```

### Option 2: Mount Output Folder
Add to `docker-compose.yml`:
```yaml
volumes:
  - ./output:/home/node/.n8n/output
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

## Troubleshooting

### "Waiting for approval" but nothing happens
- The workflow waits for your next chat message
- Type `approve` or your selection

### Files not appearing in output/
- Check Docker volume mounting
- Use `docker cp` to copy files out

### DigiKey/Mouser errors
- Verify API credentials
- Check rate limits

## Token Usage

| Step | Estimated Tokens |
|------|------------------|
| Parse Requirements | ~3,000 |
| Block Diagram | ~2,000 |
| Component Formatting | ~1,000 |
| BOM Generation | ~1,000 |
| **Total** | **~7,000 tokens** |

Within Groq free tier (131K/day) = ~18 runs/day

---

**Ready to use! Import and test with your requirements.**
