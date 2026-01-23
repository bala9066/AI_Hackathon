# AI Hardware Pipeline - n8n Workflow

## 🎯 Overview

This is a complete **n8n workflow** that automates an **AI-powered hardware design pipeline** for RF/FPGA systems. The workflow implements **8 phases** from requirements gathering through software generation.

## 🏗️ System Architecture

### **8-Phase Pipeline:**

1. **Phase 1: Requirements & Component Selection** - AI parses requirements, searches components (FPGA, GaN PA, buck-boost converters), generates BOM
2. **Phase 2: HRS Document Generation** - Generates 50-70 page Hardware Requirements Specification
3. **Phase 3: Design Constraints & Compliance** - Checks RoHS/REACH/FCC/CE/ITAR compliance
4. **Phase 4: Netlist Generation** - Creates EDIF and Excel netlists from block diagram
5. **Phase 5: PCB Design (Manual)** - User designs PCB in their tool
6. **Phase 6: GLR Generation** - Generates Gate-Level Requirements for FPGA I/O
7. **Phase 7: FPGA Implementation (Manual/Optional)** - User implements FPGA logic
8. **Phase 8: Software Development** - AI generates C/C++/Qt code, tests, documentation

## 📋 Prerequisites

- Docker Desktop installed and running
- OpenAI API key (for GPT-4)
- Optional: DigiKey/Mouser API keys for component search
- Optional: Anthropic API key (for Claude integration)

## 🚀 Quick Start

### 1. Setup Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
notepad .env
```

**Required API Keys:**
- `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys
- `DIGIKEY_API_KEY` - Optional, from https://developer.digikey.com/
- `MOUSER_API_KEY` - Optional, from https://www.mouser.com/api-hub/

### 2. Start Docker Container

```bash
# Start n8n with Docker Compose
docker-compose up -d

# Check if container is running
docker ps
```

### 3. Access n8n Interface

Open your browser and go to:
```
http://localhost:5678
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

### 4. Import Workflow

1. In n8n, click **"Workflows"** → **"Import from File"**
2. Select `AI_Hardware_Pipeline_Workflow.json`
3. Click **"Import"**

### 5. Configure Credentials

1. Go to **Credentials** in n8n
2. Add **OpenAI** credential:
   - Name: `OpenAI API`
   - API Key: Your OpenAI key from `.env`
3. Save credentials

### 6. Activate Workflow

1. Open the imported workflow
2. Click **"Activate"** toggle in top right
3. The workflow is now ready to receive requests

## 📡 Usage

### Trigger the Workflow

You can trigger the workflow via:

#### Method 1: HTTP Request (Recommended)

```bash
curl -X POST http://localhost:5678/webhook/ai-hardware-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "requirements": "Design RF system with Xilinx Artix-7 FPGA, buck-boost converters for power, 40dBm output power, 5-18GHz frequency range, return loss > 10dB"
  }'
```

#### Method 2: Test in n8n UI

1. Open the workflow
2. Click on "Webhook" node
3. Click "Test step"
4. Provide JSON input:
```json
{
  "requirements": "Design RF system with Xilinx Artix-7 FPGA, buck-boost converters, 40dBm output, 5-18GHz, return loss > 10dB"
}
```

### Example Requirements Input

**Simple IoT Device:**
```json
{
  "requirements": "Design IoT sensor board with ESP32, temperature/humidity sensor, LoRa connectivity, battery powered"
}
```

**Complex RF System:**
```json
{
  "requirements": "Design RF system with Xilinx Artix-7 XC7A100T FPGA CSG324 package, GaN power amplifier 40dBm output, 5-18GHz wideband operation, buck-boost converters for 1.0V/1.8V/3.3V/28V rails, return loss > 10dB, SPI/I2C interfaces"
}
```

## 📂 Output Files

The workflow generates **35+ files** including:

### Documents
- `HRS.docx` - Hardware Requirements Specification (70 pages)
- `SRS.docx` - Software Requirements Specification (40 pages)
- `SDD.docx` - Software Design Document (50 pages)
- `Compliance_Report.pdf` - RoHS/REACH/FCC/CE/ITAR compliance

### Spreadsheets
- `BOM.xlsx` - Bill of Materials with pricing
- `Power_Analysis.xlsx` - Power consumption and thermal analysis
- `RF_LinkBudget.xlsx` - RF performance calculations
- `netlist.xlsx` - Human-readable netlist
- `GLR.xlsx` - Gate-Level Requirements
- `RDT.xlsx` - Register Description Table
- `PSQ.xlsx` - Programming Sequence

### Design Files
- `block_diagram.json` - System architecture
- `netlist.edif` - For PCB tool import
- `design_constraints.json` - PCB layout rules

### Code Files
- `rf_driver.c/h` - C driver implementation
- `RFDriver.cpp/hpp` - C++ driver implementation
- `test_rf_driver.c` - Unit tests
- `rfcontrol_lib/` - Qt library
- `RFControlApp/` - Qt GUI application

## 🔧 Customization

### Modify AI Models

Edit the workflow nodes to use different AI models:

- **GPT-4 Turbo** (default) - Best quality, slower
- **GPT-3.5 Turbo** - Faster, lower cost
- **Claude 3** - Alternative provider

### Add Component Search APIs

To enable real-time component search:

1. Get API keys from DigiKey and Mouser
2. Add to `.env` file
3. Create API nodes in workflow to query component databases

### Adjust Output Formats

Modify the code nodes to change output formats:
- Convert markdown to Word/PDF
- Generate different CAD formats
- Custom BOM templates

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check Docker is running
docker --version

# Check logs
docker-compose logs -f n8n

# Restart container
docker-compose restart
```

### Workflow Errors

1. **"OpenAI API Error"** - Check your API key in credentials
2. **"Timeout"** - Increase timeout in node settings
3. **"Out of tokens"** - Reduce maxTokens parameter or upgrade OpenAI plan

### Can't Access n8n

```bash
# Check if port 5678 is in use
netstat -ano | findstr :5678

# Use different port in docker-compose.yml
ports:
  - "8080:5678"  # Change to 8080
```

## 📊 Performance

- **Phase 1-4 (Automated):** ~4 minutes
- **Phase 5 (Manual PCB):** 8-20 hours
- **Phase 7 (Manual FPGA):** Hours to days
- **Phase 8 (Automated):** ~60 seconds

**Total:** 10-30 hours (mostly manual PCB/FPGA work)

## 💰 Cost Estimates

### API Costs (per run)
- GPT-4 Turbo: ~$0.50-$1.50 per complete workflow
- GPT-3.5 Turbo: ~$0.05-$0.15 per workflow

### Component Costs (Example RF System)
- Total BOM: ~$850
- PCB fabrication: $200-$500 (6-layer)
- Assembly: $300-$800

### Certification Costs
- FCC Part 15: ~$15,000
- CE RED: ~$20,000
- Military: $50,000+

## 🔒 Security

### Production Deployment

1. **Change default credentials** in docker-compose.yml:
```yaml
- N8N_BASIC_AUTH_USER=your_username
- N8N_BASIC_AUTH_PASSWORD=your_secure_password
```

2. **Use HTTPS** with reverse proxy (nginx/Traefik)

3. **Enable PostgreSQL backend** for production:
```yaml
- DB_TYPE=postgresdb
- DB_POSTGRESDB_HOST=postgres
```

4. **Restrict network access** with firewall rules

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [DigiKey API Guide](https://developer.digikey.com/)
- [Xilinx FPGA Resources](https://www.xilinx.com/)

## 🤝 Support

For issues or questions:
1. Check workflow execution logs in n8n
2. Review error messages in each node
3. Check API quotas and limits
4. Verify all credentials are configured

## 📝 License

This workflow is provided as-is for AI hackathon use.

## 🎉 Next Steps

1. ✅ Docker container running
2. ✅ Workflow imported
3. ✅ Credentials configured
4. ✅ Test with example requirements
5. 🚀 Start designing your RF/FPGA system!

---

**Happy Building! 🛠️⚡**
