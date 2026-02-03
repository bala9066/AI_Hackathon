# Quick Reference: Credential Configuration

## Issue: "Credentials not configured in nodes"

**Why this happens:** n8n credentials are stored in the n8n database, NOT in the `.env` file. The `.env` file is just for your reference.

**Solution:** You must create credentials in the n8n UI for each node.

---

## 3 Credentials You Need to Create in n8n:

### 1. Groq API (for AI Agent)

**Where:** Click on "Groq LLM" node → Credentials section

**Steps:**
1. Click "Create New Credential"
2. Credential Name: `Groq API`
3. API Key: Paste from `.env` (starts with `gsk_`)
4. Click Save

**Model Selection:**
- In the same node, find "Model" dropdown
- Select: **`llama-3.1-70b-versatile`** ← RECOMMENDED
- This is the best balance of speed and quality

---

### 2. DigiKey OAuth2 (for Component Search)

**Where:** Click on "DigiKey API Search" node → Credentials section

**Steps:**
1. Click "Create New Credential"
2. Select type: "OAuth2 API"
3. Credential Name: `DigiKey OAuth2`
4. Fill in:
   ```
   Grant Type: Authorization Code
   Authorization URL: https://api.digikey.com/v1/oauth2/authorize
   Access Token URL: https://api.digikey.com/v1/oauth2/token
   Client ID: (from .env)
   Client Secret: (from .env)
   Scope: product_information
   Authentication: Body
   ```
5. Click Save
6. Click "Connect my account" button
7. Authorize in DigiKey popup

---

### 3. Mouser API (for Component Search)

**Where:** Click on "Mouser API Search" node → Credentials section

**Steps:**
1. Click "Create New Credential"
2. Select type: "Header Auth API"
3. Credential Name: `Mouser API Key`
4. Name: `Authorization`
5. Value: Your Mouser API key from `.env`
6. Click Save

**Note:** Mouser actually uses URL parameter, not header. The workflow code handles this automatically.

---

## Visual Guide

![Groq Model Selection](C:/Users/HP/.gemini/antigravity/brain/4baeace1-c073-48ae-81f1-f333d01ee3f3/groq_model_selection_*.png)

---

## Common Mistakes

❌ **WRONG:** Only adding keys to `.env` file
✅ **CORRECT:** Create credentials in n8n UI

❌ **WRONG:** Leaving model as default
✅ **CORRECT:** Select `llama-3.1-70b-versatile`

❌ **WRONG:** Using DIGIKEY_API_KEY
✅ **CORRECT:** Only use DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET

---

## Groq Model Comparison

| Model | Speed | Quality | Tokens/Day | Best For |
|-------|-------|---------|------------|----------|
| llama3-8b-8192 | ⚡⚡⚡ | ⭐⭐⭐ | 500K | Simple tasks |
| **llama-3.1-70b-versatile** | ⚡⚡ | ⭐⭐⭐⭐⭐ | 131K | **Phase 1** ✅ |
| llama-3.1-405b-reasoning | ⚡ | ⭐⭐⭐⭐⭐ | 131K | Complex RF |
| mixtral-8x7b-32768 | ⚡⚡ | ⭐⭐⭐⭐ | 131K | Alternative |

**For Phase 1, use: `llama-3.1-70b-versatile`**

---

## Still Having Issues?

1. **Check n8n logs:**
   ```bash
   docker-compose logs -f n8n
   ```

2. **Verify credentials are saved:**
   - Go to n8n → Settings → Credentials
   - You should see: Groq API, DigiKey OAuth2, Mouser API Key

3. **Test each node individually:**
   - Click on a node
   - Click "Test step"
   - Check for errors

---

**After configuring all 3 credentials, Phase 1 will work! 🎉**
