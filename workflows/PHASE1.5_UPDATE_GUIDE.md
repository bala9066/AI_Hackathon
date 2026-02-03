# Phase 1.5 Production-Grade Workflow Updates

## Quick Reference: Nodes to Update

### 1. AI System Prompt (Improved Block Diagram)
**Node:** `AI - Parse Requirements`
**Update:** Enhanced prompt for detailed block diagram generation

### 2. Component Parsing (Fix Undefined)
**Node:** `Format Options`  
**Line:** 281
**Fix:** Extract `manufacturer_pn` and `part_number` correctly

### 3. Power Budget Generation
**Node:** `Generate Final (FS)`
**Add:** Real power calculations with formulas

### 4. RF Analysis Generation
**Node:** `Generate Final (FS)`
**Add:** Link budget and RF parameter calculations

---

## Implementation Steps

Run these commands in n8n workflow editor:

### Step 1: Update AI Prompt
Edit the **"AI - Parse Requirements"** node system message to:

```
You are an expert hardware design AI. Create detailed block diagrams with pin-level connections.

OUTPUT STRICT JSON:
{
  "parsed_requirements": {
    "system_type": "RF|FPGA|IoT|Mixed-Signal|Power",
    "project_name": "string",
    "specifications": {
      "frequency_range": "5-18GHz",
      "output_power": "40dBm",
      "power_rails": ["1.0V", "1.8V", "3.3V", "28V"],
      "key_interfaces": ["SPI", "GPIO", "RF"]
    }
  },
  "block_diagram": {
    "title": "System Block Diagram",
    "components": [
      {
        "id": "U1",
        "type": "FPGA",
        "name": "Xilinx Artix-7",
        "part_suggestion": "XC7A100T-2FGG484C",
        "pins": {
          "SPI_MOSI": "AA12",
          "SPI_MISO": "AB12",
          "CLK_IN": "H4"
        },
        "power": {
          "VCC_CORE": "1.0V @ 2.5A",
          "VCC_IO": "1.8V @ 0.8A"
        }
      }
    ],
    "connections": [
      {
        "from": "U1",
        "from_pin": "SPI_MOSI",
        "to": "U2",
        "to_pin": "SDI",
        "signal_name": "SPI_DATA",
        "signal_type": "LVTTL 3.3V"
      }
    ],
    "power_rails": [
      {
        "name": "VCC_1V0",
        "voltage": "1.0V",
        "current_budget": "2.5A",
        "components": ["U1_CORE"]
      }
    ]
  },
  "mermaid_diagram": "graph TB\n  subgraph FPGA...",
  "component_categories": [
    {
      "category": "FPGA",
      "search_keywords": ["Xilinx", "Artix-7", "XC7A100T"],
      "quantity": 1,
      "priority": "critical",
      "specifications": "484-pin BGA, -2 speed grade"
    }
  ]
}
```

### Step 2: Import Updated Workflow
The complete updated workflow JSON is too large for this guide.

**Use the automated script instead:**

Run: `update_phase1.5.ps1` (instructions below)

---

## Manual Node Updates

If you prefer manual editing:

### Node: "Format Options"
Replace the jsCode with:
```javascript
const items = $input.all();
const allComponents = [];

items.forEach(item => {
  const data = item.json;
  
  // DigiKey
  if (data.Products) {
    data.Products.slice(0, 3).forEach(p => {
      allComponents.push({
        supplier: 'DigiKey',
        part_number: p.DigiKeyPartNumber,
        manufacturer: p.Manufacturer?.Name || 'Unknown',
        manufacturer_pn: p.ManufacturerPartNumber,
        description: (p.ProductDescription || '').substring(0, 100),
        unit_price: parseFloat(p.UnitPrice) || 0,
        stock: p.QuantityAvailable || 0,
        datasheet: p.PrimaryDatasheet || '',
        category: item.json.category || 'Unknown'
      });
    });
  }
  
  // Mouser
  if (data.SearchResults?.Parts) {
    data.SearchResults.Parts.slice(0, 3).forEach(p => {
      allComponents.push({
        supplier: 'Mouser',
        part_number: p.MouserPartNumber,
        manufacturer: p.Manufacturer || 'Unknown',
        manufacturer_pn: p.ManufacturerPartNumber,
        description: (p.Description || '').substring(0, 100),
        unit_price: parseFloat((p.PriceBreaks?.[0]?.Price || '0').replace(/[^0-9.]/g, '')) || 0,
        stock: parseInt(p.AvailabilityInStock) || 0,
        datasheet: p.DataSheetUrl || '',
        category: item.json.category || 'Unknown'
      });
    });
  }
});

return { json: { component_options: allComponents, original_data: items[0]?.json?.original_data } };
```

### Node: "Generate Final (FS)"
This node needs major updates for Power Budget and RF Analysis.

**See the full code in:** `phase1.5_node_updates.js` (located in `workflows/` folder)

---

## Testing

1. Import `Phase1.5_ProductionGrade.json`
2. Test with: "Design 40dBm RF system with Xilinx FPGA"
3. Verify outputs:
   - ✅ Block diagram has subgraphs and pin details
   - ✅ BOM shows real part numbers (not "undefined")
   - ✅ Power Budget has calculations
   - ✅ RF Analysis has link budget

---

## Next Steps

Due to JSON complexity, I recommend:
1. **Option A:** Use the Python script to auto-update (safest)
2. **Option B:** Manual copy-paste from reference files
3. **Option C:** I'll create a simplified single-file workflow

**Which do you prefer?**
