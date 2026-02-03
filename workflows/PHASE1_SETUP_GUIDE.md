# Phase 1 Setup Guide - Step by Step

## 🔑 Step 1: Get Your API Keys

### Groq API Key (Primary - FREE)
1. Go to: https://console.groq.com/keys
2. Sign up/Login
3. Click "Create API Key"
4. Copy the key (starts with `gsk_...`)
5. Paste in `.env`: `GROQ_API_KEY=gsk_...`

### Google Gemini API Key (Secondary - FREE)
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key
5. Paste in `.env`: `GOOGLE_GEMINI_API_KEY=...`

### DigiKey OAuth2 (Component Search - FREE)
1. Go to: https://developer.digikey.com/
2. Sign up for developer account
3. Create a new application
4. Copy **Client ID** and **Client Secret**
5. Paste in `.env`:
   ```
   DIGIKEY_CLIENT_ID=your-client-id
   DIGIKEY_CLIENT_SECRET=your-client-secret
   ```

### Mouser API Key (Component Search - FREE)
1. Go to: https://www.mouser.com/api-hub/
2. Sign up/Login
3. Request API access
4. Copy your API key
5. Paste in `.env`: `MOUSER_API_KEY=...`

---

## 📥 Step 2: Import Workflow into n8n

1. Start n8n: Double-click `setup_and_start.bat`
2. Open browser: http://localhost:5678
3. Login: `admin` / `admin123`
4. Click **Workflows** (top menu)
5. Click **Import from File**
6. Select: `workflows/Phase1_Requirements_Components.json`
7. Click **Import**

---

## ⚙️ Step 3: Configure Credentials in n8n

### 3.1 Groq API Credential

1. In the workflow, click on the **"Groq LLM"** node
2. Under "Credential to connect with", click **"Create New Credential"**
3. Enter:
   - **Credential Name**: `Groq API`
   - **API Key**: Paste your Groq key from `.env`
4. Click **Save**

**IMPORTANT: Select Model**
- In the Groq LLM node settings:
- **Model**: Select `llama-3.1-70b-versatile` (recommended)
- Alternative: `llama-3.1-405b-reasoning` (more powerful but slower)
- Alternative: `llama3-8b-8192` (faster, less powerful)

### 3.2 DigiKey OAuth2 Credential

1. Click on the **"DigiKey API Search"** node
2. Under "Credential to connect with", click **"Create New Credential"**
3. Select credential type: **OAuth2 API**
4. Enter:
   - **Credential Name**: `DigiKey OAuth2`
   - **Grant Type**: `Authorization Code`
   - **Authorization URL**: `https://api.digikey.com/v1/oauth2/authorize`
   - **Access Token URL**: `https://api.digikey.com/v1/oauth2/token`
   - **Client ID**: From your `.env` file
   - **Client Secret**: From your `.env` file
   - **Scope**: `product_information`
   - **Auth URI Query Parameters**: Leave empty
   - **Authentication**: `Body`
5. Click **Save**
6. Click **Connect my account** and authorize

### 3.3 Mouser API Credential

1. Click on the **"Mouser API Search"** node
2. Under "Credential to connect with", click **"Create New Credential"**
3. Select credential type: **Header Auth API**
4. Enter:
   - **Credential Name**: `Mouser API Key`
   - **Name**: Leave as `Authorization` OR use custom header
   - **Value**: Your Mouser API key from `.env`
5. Click **Save**

**Note:** Mouser API is passed as URL parameter, not header. The workflow handles this automatically.

---

## ✅ Step 4: Activate Workflow

1. In the workflow editor, find the toggle switch (top right)
2. Click to **Activate** the workflow
3. The workflow is now live!

---

## 🧪 Step 5: Test Phase 1

### Test in n8n Chat Interface:

1. Click the **"Chat"** button (bottom right of workflow)
2. Type your requirements:
   ```
   Design RF system with Xilinx Artix-7 FPGA, 
   40dBm output power, 5-18GHz frequency range, 
   buck-boost converters for power
   ```
3. Press Enter
4. Wait ~30 seconds for response

### Expected Response:
- ✅ Parsed system specifications
- ✅ Component list from DigiKey and Mouser
- ✅ BOM with real prices
- ✅ Total cost estimate

---

## 🔧 Troubleshooting

### Issue: "Credentials not configured"
**Solution:** Make sure you created credentials in n8n UI, not just in `.env`

### Issue: "DigiKey OAuth error"
**Solution:** 
- Check Client ID and Secret are correct
- Make sure you clicked "Connect my account"
- Verify your DigiKey developer account is approved

### Issue: "Groq API error"
**Solution:**
- Verify API key in n8n credential (not just .env)
- Check you selected a valid model name
- Try switching to `llama3-8b-8192` if 70b fails

### Issue: "No components found"
**Solution:**
- Check DigiKey/Mouser credentials
- Verify your search keywords are valid
- Check API rate limits (1000/day DigiKey, 10K/day Mouser)

---

## 📊 Groq Model Selection Guide

| Model | Speed | Quality | Free Tokens/Day | Use For |
|-------|-------|---------|-----------------|---------|
| `llama3-8b-8192` | ⚡⚡⚡ Fast | Good | ~500K | Simple parsing |
| `llama-3.1-70b-versatile` | ⚡⚡ Medium | Excellent | ~131K | **Recommended** |
| `llama-3.1-405b-reasoning` | ⚡ Slow | Best | ~131K | Complex RF systems |
| `mixtral-8x7b-32768` | ⚡⚡ Medium | Very Good | ~131K | Alternative |

**Recommendation:** Start with `llama-3.1-70b-versatile` for best balance.

---

## 📝 Summary Checklist

- [ ] Added Groq API key to `.env`
- [ ] Added Gemini API key to `.env` (optional)
- [ ] Added DigiKey Client ID and Secret to `.env`
- [ ] Added Mouser API key to `.env`
- [ ] Imported workflow into n8n
- [ ] Created Groq credential in n8n
- [ ] Selected Groq model: `llama-3.1-70b-versatile`
- [ ] Created DigiKey OAuth2 credential in n8n
- [ ] Created Mouser credential in n8n
- [ ] Activated workflow
- [ ] Tested with sample input
- [ ] Received BOM with real prices

---

**Once all checkboxes are complete, Phase 1 is ready! 🎉**

**Next:** Proceed to Phase 2 (HRS Document Generation)
