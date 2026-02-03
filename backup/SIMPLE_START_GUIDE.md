# 🎯 SIMPLE START GUIDE - 3 EASY STEPS

**You have many files. Start here! Follow these 3 steps only.**

---

## ✅ STEP 1️⃣: Setup API Key (2 minutes)

### 1a. Get Your OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-...`)

### 1b. Edit Your .env File
1. **Double-click** the file named `.env` in this folder
2. Find this line:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   ```
3. Replace `sk-your-openai-key-here` with your actual key
4. **Save and close** the file

---

## 🚀 STEP 2️⃣: Run Setup (1 click)

**Double-click this file:**
```
setup_and_start.bat
```

This will automatically:
- ✅ Check if Docker is installed
- ✅ Start Docker if needed
- ✅ Start n8n (the workflow engine)
- ✅ Open your browser to http://localhost:5678

**Login with:**
- Username: `admin`
- Password: `admin123`

---

## 📥 STEP 3️⃣: Import the Workflow (1 minute)

In the n8n web interface:

1. Click **"Workflows"** (top menu)
2. Click **"Import from File"**
3. Select the file: `AI_Hardware_Pipeline_Workflow.json`
4. Click **"Import"**
5. Click on any "OpenAI" node → Add credential → Paste your API key
6. Click the **"Activate"** toggle (top right, switch to ON)

---

## 🎉 DONE! Now Test It

**Double-click this file:**
```
test_workflow.bat
```

This sends a test request to your AI workflow!

---

## 📊 What Will Happen?

Your AI will design a complete hardware system:
- ✅ Component selection
- ✅ Block diagrams
- ✅ Price estimates (BOM)
- ✅ 70-page technical documents
- ✅ PCB netlists
- ✅ Software code (C/C++/Qt)

**Automated time:** ~4 minutes  
**Your manual work:** 10-30 hours (PCB design + optional FPGA)

---

## 🆘 Problems?

### Docker not installed?
- Download: https://www.docker.com/products/docker-desktop
- Install it
- Restart your computer
- Run `setup_and_start.bat` again

### Port 5678 already in use?
- Edit `docker-compose.yml`
- Change `5678:5678` to `8080:5678`
- Use http://localhost:8080 instead

### API errors?
- Make sure you added your OpenAI API key to `.env`
- Check you have credits in your OpenAI account

---

## 📚 Want More Details?

- **Quick guide:** Read `QUICKSTART.md`
- **Full details:** Read `START_HERE.md`
- **How it works:** Read `WORKFLOW_GUIDE.md`

---

## 🎯 Your Next Steps After Testing

1. Think about what hardware you want to design
2. Edit your requirements
3. Run the workflow
4. Get 35+ files of professional design documents
5. Win your hackathon! 🏆

---

**That's it! Keep it simple. Start with Step 1. 🚀**
