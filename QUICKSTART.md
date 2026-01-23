# 🚀 QUICKSTART GUIDE

## Get Started in 5 Minutes!

### Step 1: Verify Setup (30 seconds)
```bash
# Double-click this file:
verify_setup.bat
```

This will check:
- ✅ Docker installed and running
- ✅ All required files present
- ✅ Directory structure created

---

### Step 2: Configure API Keys (2 minutes)

1. **Get OpenAI API Key:**
   - Go to: https://platform.openai.com/api-keys
   - Create new key
   - Copy the key (starts with `sk-...`)

2. **Edit .env file:**
   ```bash
   # Right-click .env → Edit with Notepad
   # Or double-click .env
   
   # Replace this line:
   OPENAI_API_KEY=sk-your-openai-key-here
   
   # With your actual key:
   OPENAI_API_KEY=sk-proj-abc123xyz...
   ```

3. **Save and close .env**

> **Optional:** Add DigiKey/Mouser API keys for real-time component pricing

---

### Step 3: Start n8n (1 minute)

```bash
# Double-click this file:
start.bat
```

This will:
- Start n8n Docker container
- Open http://localhost:5678 in browser
- Show you the login page

**Login credentials:**
- Username: `admin`
- Password: `admin123`

---

### Step 4: Import Workflow (1 minute)

1. Click **"Workflows"** in the top menu
2. Click **"Import from File"**
3. Select: `AI_Hardware_Pipeline_Workflow.json`
4. Click **"Import"**

---

### Step 5: Configure OpenAI Credentials (1 minute)

1. Click **"Credentials"** in the left sidebar
2. Click **"Add Credential"**
3. Search for **"OpenAI"**
4. Fill in:
   - **Credential Name:** `OpenAI API`
   - **API Key:** Your OpenAI key from .env
5. Click **"Save"**

---

### Step 6: Activate Workflow (10 seconds)

1. Open the imported workflow
2. Click the **"Activate"** toggle (top right)
3. Workflow is now live! 🎉

---

### Step 7: Test It! (30 seconds)

**Option A: Use Test Script**
```bash
# Double-click:
test_workflow.bat
```

**Option B: Manual Test**
```bash
curl -X POST http://localhost:5678/webhook/ai-hardware-pipeline ^
  -H "Content-Type: application/json" ^
  -d "{\"requirements\": \"Design IoT sensor with ESP32, temperature sensor, battery powered\"}"
```

**Option C: Test in n8n UI**
1. Click on "Webhook" node
2. Click "Test step"
3. Paste this JSON:
```json
{
  "requirements": "Design RF system with Xilinx Artix-7 FPGA, 40dBm output, 5-18GHz"
}
```

---

## 🎉 You're Ready!

### What Happens Next?

The AI will:
1. ✅ Parse your requirements (10 sec)
2. ✅ Search for components (20 sec)
3. ✅ Generate block diagram (15 sec)
4. ✅ Create BOM with pricing (30 sec)
5. ✅ Generate HRS document (30 sec)
6. ✅ Check compliance (30 sec)
7. ✅ Generate netlist (40 sec)
8. ⏸️ Wait for you to design PCB (8-20 hours)
9. ✅ Generate GLR (40 sec)
10. ⏸️ Wait for you to implement FPGA (optional)
11. ✅ Generate complete software package (60 sec)

**Total automated time: ~4 minutes**  
**Total manual time: 10-30 hours (PCB + FPGA)**

---

## 📊 Example Outputs

After running the workflow, you'll get:

### Documents
- `HRS.docx` - 70-page Hardware Requirements Specification
- `SRS.docx` - 40-page Software Requirements
- `SDD.docx` - 50-page Software Design
- `Compliance_Report.pdf` - RoHS/REACH/FCC/CE/ITAR

### Spreadsheets
- `BOM.xlsx` - Bill of Materials (~$850 for RF system)
- `Power_Analysis.xlsx` - Power consumption (45W typical)
- `RF_LinkBudget.xlsx` - RF performance calculations
- `netlist.xlsx` - Human-readable netlist
- `GLR.xlsx` - Gate-Level Requirements
- `RDT.xlsx` - Register Description Table
- `PSQ.xlsx` - Programming Sequence

### Design Files
- `block_diagram.json` - System architecture
- `netlist.edif` - For PCB tool import
- `design_constraints.json` - PCB layout rules

### Code
- `rf_driver.c/h` - C driver
- `RFDriver.cpp/hpp` - C++ driver
- `RFControlApp/` - Qt GUI application
- `test_rf_driver.c` - Unit tests

---

## 🆘 Troubleshooting

### Docker not running?
```bash
# Start Docker Desktop manually
# Then run: start.bat
```

### n8n won't start?
```bash
# Check logs:
docker-compose logs -f n8n

# Restart:
stop.bat
start.bat
```

### API errors?
- Check your OpenAI API key in .env
- Make sure you have credits in OpenAI account
- Verify credentials are configured in n8n

### Port 5678 in use?
Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5678"  # Change to different port
```

---

## 📚 Next Steps

1. ✅ **Read WORKFLOW_GUIDE.md** - Detailed phase-by-phase guide
2. ✅ **Read README.md** - Full documentation
3. ✅ **Try example inputs** - Test with different requirements
4. ✅ **Design your system** - Start your AI hackathon project!

---

## 💡 Tips

### For best results:
- Be specific with requirements (FPGA type, frequency range, power levels)
- Use technical terms (GaN PA, buck-boost, return loss, etc.)
- Ask follow-up questions if AI needs clarification
- Review AI outputs before moving to manual phases

### Example requirements:
```
"Design RF transmitter with Xilinx Zynq FPGA, 
Software Defined Radio architecture,
400MHz to 6GHz tunable frequency,
30dBm output power,
Multi-rail power supply (1.0V, 1.8V, 3.3V, 12V),
Gigabit Ethernet interface,
PCIe Gen2 x4 host interface"
```

---

## 🎯 Goals

- ✅ Generate complete hardware design in minutes
- ✅ Get professional documentation (HRS, SRS, SDD)
- ✅ Automated compliance checking
- ✅ Ready-to-use software drivers and GUI
- ✅ PCB netlist for easy layout
- ✅ Win your AI hackathon! 🏆

---

**Questions? Check README.md or WORKFLOW_GUIDE.md**

**Happy Building! 🚀⚡**
