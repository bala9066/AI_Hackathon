# Phase 1: Requirements & Component Selection

## Overview

Phase 1 takes user requirements in natural language and:
1. Parses technical specifications using AI (Groq LLM)
2. Searches components from DigiKey and Mouser APIs
3. Generates a Bill of Materials (BOM) with real pricing

## Workflow Structure

```
Chat Trigger → Initialize → AI Agent → Parse Response
                                           ↓
                              Prepare Component Search
                                    ↓         ↓
                              DigiKey API  Mouser API
                                    ↓         ↓
                                 Merge Results
                                      ↓
                                Generate BOM
                                      ↓
                               Phase 1 Output
```

## Nodes Description

| Node | Type | Purpose |
|------|------|---------|
| Chat Trigger | Langchain Chat | Receives user message |
| Initialize Phase 1 | Code | Sets up execution context |
| AI Agent | Langchain Agent | Parses requirements with Groq LLM |
| Groq LLM | Langchain LLM | Primary language model (FREE) |
| Parse AI Response | Code | Extracts structured JSON from AI |
| Prepare Component Search | Code | Creates search queries |
| DigiKey API Search | HTTP Request | Real component search |
| Mouser API Search | HTTP Request | Alternative supplier search |
| Merge Results | Merge | Combines both supplier results |
| Generate BOM | Code | Creates priced BOM |
| Phase 1 Output | Code | Formats chat response |

## How to Import

1. Open n8n: http://localhost:5678
2. Go to **Workflows** → **Import from File**
3. Select: `workflows/Phase1_Requirements_Components.json`
4. Click **Import**

## Configure Credentials

### 1. Groq API (Primary LLM)
- Go to **Credentials** → **Add Credential**
- Search: "Groq"
- Name: `Groq API`
- Paste your API key from https://console.groq.com/keys

### 2. DigiKey OAuth2
- Go to **Credentials** → **Add Credential**
- Search: "OAuth2"
- Name: `DigiKey OAuth2`
- Client ID: (from .env)
- Client Secret: (from .env)
- Auth URL: `https://api.digikey.com/v1/oauth2/authorize`
- Token URL: `https://api.digikey.com/v1/oauth2/token`

### 3. Mouser API
- Go to **Credentials** → **Add Credential**
- Search: "Header Auth"
- Name: `Mouser API Key`
- Header Name: `Authorization`
- Header Value: Your Mouser API key

## Test Phase 1

### Sample Input:
```
Design RF system with Xilinx Artix-7 FPGA, 
buck-boost converters for power, 
40dBm output power, 
5-18GHz frequency range, 
return loss > 10dB
```

### Expected Output:
- Parsed specifications (FPGA type, frequencies, power)
- Block diagram JSON
- Power budget calculation
- BOM with real prices from DigiKey/Mouser
- Component availability status

## Token Usage

Estimated tokens per run:
- Input: ~2,000 tokens
- Output: ~4,000 tokens
- **Total: ~6,000 tokens**

Groq free tier: 131,000 tokens/day → ~21 runs/day free!

## Troubleshooting

### DigiKey API Error
- Check OAuth2 credentials
- Verify client ID/secret in .env
- Check rate limit (120 req/min)

### Mouser API Error
- Verify API key in .env
- Check rate limit (10K req/day)

### AI Response Parse Error
- Check Groq API key
- Verify model availability
- Try switching to Gemini fallback

## Next Phase

After Phase 1 completes successfully:
- Type "continue" to proceed to Phase 2
- Or answer any clarifying questions
- Phase 2 generates the HRS (Hardware Requirements Specification)
