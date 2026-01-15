# 🔑 Getting Your FREE Gemini API Key

## Quick Start (2 Minutes)

### Step 1: Visit Google AI Studio
**Go to**: https://aistudio.google.com/apikey

### Step 2: Sign In
- Use your **Google account**
- ✅ **No credit card required!**

### Step 3: Create API Key
1. Click **"Get API key"** or **"Create API key"**
2. Select **"Create API key in new project"**
3. **Copy** your key (starts with `AIza...`)

### Step 4: Add to Your Project
Open `d:\project\data-science-assignment\.env` and add:

```bash
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

### Step 5: Restart Backend
```bash
# Stop the current backend (Ctrl+C)
# Then restart:
python main.py
```

---

## ✅ FREE Tier Limits

Google Gemini offers generous free limits:
- **15 requests per minute**
- **1 million tokens per minute**  
- **1,500 requests per day**

More than enough for development and this assignment! 🎉

---

## 🔐 Security Note

**Never commit your API key to GitHub!**

The `.gitignore` file is already configured to exclude `.env`, keeping your key safe.

---

## 🆘 Troubleshooting

**API key not working?**
- Ensure no extra spaces in `.env` file
- Key should start with `AIza`
- Restart the backend after adding the key

**Need more help?**  
See the [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions.

