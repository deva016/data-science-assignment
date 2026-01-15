# 🚀 Quick Setup Guide

## Step 1: Get Free API Keys (5 minutes)

### Claude API Key (Primary - Recommended)
1. Visit: https://console.anthropic.com/
2. Click "Sign Up" (no credit card required)
3. Verify your email
4. Get **$5 FREE credits** automatically
5. Go to "API Keys" tab
6. Click "Create Key"
7. Copy your key (starts with `sk-ant-...`)

### OpenAI API Key (Backup)
1. Visit: https://platform.openai.com/signup
2. Sign up and verify email
3. Get **$5 FREE credits** (valid for 3 months)
4. Go to: https://platform.openai.com/api-keys
5. Click "Create new secret key"
6. Copy your key (starts with `sk-...`)

---

## Step 2: Install Dependencies (2 minutes)

```bash
# Navigate to project folder
cd d:\project\data-science-assignment

# Create virtual environment (recommended)
python -m venv venv

# Activate it
venv\Scripts\activate

# Install all packages
pip install -r requirements.txt
```

Expected output: All packages installed successfully ✅

---

## Step 3: Configure API Keys (1 minute)

```bash
# Copy the template
copy .env.example .env

# Open .env in any text editor (Notepad, VS Code, etc.)
notepad .env
```

Edit these lines:
```bash
ANTHROPIC_API_KEY=sk-ant-PASTE-YOUR-CLAUDE-KEY-HERE
OPENAI_API_KEY=sk-PASTE-YOUR-OPENAI-KEY-HERE
```

**Save and close the file.**

---

## Step 4: Start the Application (30 seconds)

### Terminal 1 - Backend (API)
```bash
python main.py
```

You should see:
```
🚀 Starting Clinical Summary Generator API...
📖 API Documentation: http://localhost:8000/docs
```

### Terminal 2 - Frontend (UI)
```bash
streamlit run app.py
```

Browser will auto-open to: http://localhost:8501

---

## Step 5: Generate Your First Summary! 🎉

1. **In the Streamlit UI:**
   - Select "Patient 1001" from dropdown
   - Keep "Include Citations" checked ✓
   - Click "🚀 Generate Summary"

2. **Wait 10-15 seconds** (AI is thinking...)

3. **View the result:**
   - Clinical summary with sections
   - Citations for every claim
   - Provider used (Claude or OpenAI)

4. **Download:**
   - Click "📥 Download JSON" or "📄 Download Text"

---

## Troubleshooting

### ❌ "Cannot connect to API"
**Solution:** Make sure Terminal 1 (backend) is running
```bash
python main.py
```

### ❌ "API key not configured"
**Solution:** 
1. Check `.env` file exists (not `.env.example`)
2. Verify keys don't have extra spaces
3. Restart `python main.py`

### ❌ "Both LLM providers failed"
**Solution:** Check your API keys are valid:
- Claude: https://console.anthropic.com/settings/keys
- OpenAI: https://platform.openai.com/api-keys

### ❌ "Module not found"
**Solution:** Install dependencies again:
```bash
pip install --upgrade -r requirements.txt
```

---

## Test Checklist

- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Can select patient 1001
- [ ] Summary generates successfully
- [ ] Citations are displayed
- [ ] Can download JSON/TXT
- [ ] Try patient 1002
- [ ] Test fallback (optional)

---

## What to Show Your Assignment Provider

1. **Running Application:**
   - Both terminals running
   - Streamlit UI in browser
   - Generated summary with citations

2. **Code Quality:**
   - Well-structured `src/` package
   - Dual-LLM fallback logic
   - Comprehensive error handling
   - Clean documentation

3. **Features to Highlight:**
   - ✨ Uses Claude 3.5 Sonnet (best for medical)
   - ✨ Automatic OpenAI fallback
   - ✨ Citation tracking (bonus feature)
   - ✨ Production-ready architecture
   - ✨ FastAPI + Streamlit
   - ✨ Downloadable summaries

---

## Next Steps

Want to customize?

- **Change LLM models:** Edit `.env` → `CLAUDE_MODEL` or `OPENAI_MODEL`
- **Force a provider:** Set `FORCE_PROVIDER=claude` or `openai`
- **Adjust creativity:** Change `TEMPERATURE` (0.1 = precise, 0.7 = creative)
- **Add more patients:** Add CSV data to `data/` folder

---

**Need Help?** Check the main [README.md](README.md) for detailed documentation.

**Good luck with your assignment! 🎓**
