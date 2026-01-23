# Workflow Execution Guide

## Step-by-Step Execution

### Phase 1: Requirements & Component Selection (Automated - 90 seconds)

**What You Do:**
1. Provide requirements via webhook or UI
2. Answer AI's clarifying questions if prompted
3. Choose components when AI shows 2-3 options

**Example Input:**
```json
{
  "requirements": "Design RF system with Xilinx Artix-7 FPGA, buck-boost converters for power, 40dBm output power, 5-18GHz frequency range, return loss > 10dB"
}
```

**What AI Does:**
- Parses requirements
- Creates block diagram
- Searches components (FPGA, GaN PA, buck-boost converters, RF components)
- Calculates RF link budget and power consumption
- Designs matching networks
- Generates BOM with pricing

**Outputs:**
- ✅ Block diagram (JSON + visual)
- ✅ RF_LinkBudget.xlsx
- ✅ Power_Analysis.xlsx
- ✅ BOM.xlsx (~85 components, ~$850)

---

### Phase 2: HRS Document (Automated - 30 seconds)

**What You Do:**
- Nothing! Just wait

**What AI Does:**
- Adds pin numbers to block diagram
- Generates 50-70 page Hardware Requirements Specification

**Outputs:**
- ✅ HRS.docx (Hardware Requirements Specification)
- ✅ Block_Diagram_Detailed.json (with pin assignments)

---

### Phase 3: Design Constraints & Compliance (Automated - 30 seconds)

**What You Do:**
- Answer simple yes/no questions (e.g., "Is this for military/export?")

**What AI Does:**
- Generates design constraints (power rails, clock requirements, PCB layout rules)
- Checks RoHS compliance
- Checks REACH compliance
- Checks EMC/FCC/CE/Military requirements
- Validates for critical compliance issues

**Outputs:**
- ✅ Design_Constraints.json
- ✅ Compliance_Report.pdf
- ✅ Updated HRS.docx

**Validation Gate:**
- ✅ PASS → Continue to Phase 4
- ❌ FAIL → Must fix compliance issues

---

### Phase 4: Netlist Generation ⭐ KEY PHASE (Automated - 40 seconds)

**What You Do:**
- Nothing! Fully automatic

**What AI Does:**
- Reads block diagram with pin assignments
- Looks up component datasheets
- Generates logical netlist
- Creates EDIF format for EDA tools
- Creates Excel format for humans
- Validates (no floating pins, all power connected, RF paths correct)

**Outputs:**
- ✅ netlist.edif (for Xpedition/Altium/KiCad)
- ✅ netlist.xlsx (human readable - 3 sheets: Nets, Components, Pin Assignments)

**Why Important:**
- Get netlist BEFORE PCB design
- PCB designer can use as reference
- Not dependent on manual PCB work

---

### Phase 5: PCB Design 🔧 MANUAL (8-20 hours)

**What You Do:**
1. **Import** netlist.edif into your PCB tool (Xpedition/Altium/KiCad)
2. **Create schematic** (or verify auto-generated)
3. **Design PCB layout:**
   - 6-layer stackup recommended
   - Component placement (FPGA center, RF section separate)
   - Route traces (50Ω RF, wide power traces, LVDS pairs)
   - Thermal vias under GaN PA (50+ vias)
   - Via stitching around RF section
4. **Run DRC** (Design Rule Check)
5. **Generate manufacturing files:**
   - Gerber files
   - Drill files
   - Pick-and-place CSV
6. **Upload to chat:** Type "PCB complete" and upload files

**What AI Does:**
- Waits for your files
- Can answer design questions

**Your Outputs:**
- Schematic PDF
- Gerber files
- Drill files
- Pick-and-place CSV
- Fabrication drawing

---

### Phase 6: GLR Generation (Automated - 40 seconds + 10 min review)

**What You Do:**
1. Review signal table AI shows you
2. Verify critical signals (PA enable, FPGA reset, SPI chip selects)
3. Type "approve" when done

**What AI Does:**
- Parses netlist for FPGA interface signals
- Identifies signal types (LVDS, SPI, I2C, GPIO)
- Determines voltage level, direction, default condition, I/O standard
- Generates GLR document

**Outputs:**
- ✅ GLR.json
- ✅ GLR.xlsx (Signal table with Pin#, Voltage, Direction, Default, Standard)

**Validation Gate:**
- Checks voltage compatibility
- ✅ PASS → Continue
- ❌ FAIL → Fix issues

---

### Phase 7: FPGA Implementation 🔧 MANUAL/OPTIONAL (Hours to days)

**What You Do (if using FPGA):**
1. **Implement FPGA logic** in Verilog/VHDL:
   - RF signal processing
   - DAC/ADC interfaces
   - PA control logic (SPI)
   - Monitoring (I2C)
2. **Create RDT (Register Description Table)** in Excel
3. **Create PSQ (Programming Sequence)** in Excel
4. **Upload files:** Type "FPGA complete" and upload RDT.xlsx, PSQ.xlsx

**What You Do (if not using FPGA):**
- Type "Skip FPGA"

**What AI Does:**
- Waits for your files

**Your Outputs:**
- ✅ RDT.xlsx (Register Description Table)
- ✅ PSQ.xlsx (Programming Sequence)
- Vivado project files (optional)

---

### Phase 8: Software Development (Automated - 60 seconds)

**What You Do:**
1. Review generated code preview
2. Request changes if needed: "Add error handling", "Add temperature monitoring function"
3. Type "Code approved" when done

**What AI Does:**
- Generates SRS.docx (Software Requirements Specification)
- Generates SDD.docx (Software Design Document)
- Generates C driver code (rf_driver.c/h)
- Generates C++ driver code (RFDriver.cpp/hpp)
- Generates Qt library (SPI, I2C, Power Management, FPGA, PA classes)
- Generates Qt GUI application (Main window, controls, monitoring)
- Generates unit tests
- Performs code review (static analysis, security check, coding standards)
- Auto-fixes issues
- Generates test cases

**Outputs:**
- ✅ SRS.docx
- ✅ SDD.docx
- ✅ rf_driver.c + rf_driver.h
- ✅ RFDriver.cpp + RFDriver.hpp
- ✅ Qt library source (rfcontrol_lib/)
- ✅ Qt GUI application (RFControlApp/)
- ✅ test_rf_driver.c
- ✅ CODE_REVIEW.json

**Validation Gate:**
- Code compiles
- No critical security issues
- Quality score ≥ 6/10
- ✅ PASS → Complete!
- ❌ FAIL → AI auto-fixes and retries

---

## Complete Timeline

| Phase | You Do | AI Does | Time |
|-------|--------|---------|------|
| 1 | Answer questions, pick options | Component search, BOM generation | 90 sec |
| 2 | Nothing | Generate 70-page HRS document | 30 sec |
| 3 | Answer 1-2 questions | Check compliance (RoHS/REACH/FCC/CE/ITAR) | 30 sec |
| 4 | Nothing | Generate netlist (EDIF + Excel) | 40 sec |
| 5 | **MANUAL** - Design PCB | Wait (answer questions) | 8-20 hrs |
| 6 | Approve defaults | Generate GLR | 40 sec + 10 min |
| 7 | **MANUAL** - Implement FPGA, create RDT/PSQ | Wait | Hours to days |
| 8 | Review code | Generate SRS/SDD/C/C++/Qt | 60 sec |

**Total Automated Time:** ~4 minutes  
**Total Manual Time:** 10-30 hours  
**Total Time:** ~10-30 hours

---

## Final Deliverables (35+ Files)

### Documents (Word/PDF)
1. HRS.docx - Hardware Requirements (70 pages)
2. SRS.docx - Software Requirements (40 pages)
3. SDD.docx - Software Design (50 pages)
4. Compliance_Report.pdf

### Spreadsheets (Excel)
5. BOM.xlsx (5 sheets: parts, pricing, suppliers, lifecycle, power)
6. Power_Analysis.xlsx
7. RF_LinkBudget.xlsx
8. netlist.xlsx (3 sheets: nets, components, pins)
9. GLR.xlsx
10. RDT.xlsx
11. PSQ.xlsx

### Design Files
12. block_diagram.json
13. block_diagram.vsdx (Visio format)
14. netlist.edif (for EDA tools)
15. design_constraints.json

### Code Files
16-20. rf_driver.c/h, RFDriver.cpp/hpp, test_rf_driver.c

### Qt Application
21-22. rfcontrol_lib/, RFControlApp/

### PCB Files (you create)
23-40. Gerber files, drill files, pick-and-place, assembly drawing

### Reports
41-42. CODE_REVIEW.json, validation_reports/

---

## Tips for Success

### For RF Design
- ✅ Proper grounding (solid ground planes, via stitching)
- ✅ 50Ω controlled impedance throughout RF path
- ✅ Thermal management (heatsink, thermal vias)
- ✅ Shielding between RF and digital sections
- ✅ Quality RF connectors (SMA)

### For FPGA
- ✅ Clean power supplies (low noise buck-boost converters)
- ✅ Proper decoupling (bulk + ceramic caps)
- ✅ Clock distribution (low jitter)
- ✅ High-speed I/O (differential pairs, length matching)

### For Power Supply
- ✅ Sequencing (1.0V → 1.8V → 3.3V → 28V)
- ✅ Current capability (28V rail needs 2A for PA)
- ✅ Low ripple on 1.0V FPGA core supply
- ✅ Overcurrent protection on PA supply

### For Safety
- ✅ Temperature monitoring (PA thermal sensor)
- ✅ Emergency shutdown logic
- ✅ Thermal foldback (reduce power if hot)
- ✅ Input power monitoring

---

## Common Questions

**Q: Do I need to know how to code?**  
A: No for Phases 1-6! Just chat naturally. For Phase 7 (FPGA), you need HDL knowledge. For Phase 8, AI generates all code automatically.

**Q: Can I change components mid-process?**  
A: Yes! Just say "Change GaN PA to higher power model" and AI updates everything.

**Q: What if I don't have Xpedition for PCB?**  
A: Use any tool (Altium, KiCad, Eagle) - just import the EDIF netlist.

**Q: Can I skip FPGA phase?**  
A: Not for RF designs - FPGA is core. But you can use a simpler FPGA if budget is tight.

**Q: How much does this cost to run?**  
A: ~$1.50 per complete run (API costs)

**Q: Can I run this multiple times?**  
A: Yes! Iterate as much as needed. Common: 5-8 runs to refine design.

---

**Now you're ready to design your RF/FPGA system! 🚀**
