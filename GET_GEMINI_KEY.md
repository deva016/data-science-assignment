# 🔑 Get Your FREE Google Gemini API Key

## Step 1: Visit Google AI Studio
Go to: **https://aistudio.google.com/apikey**

## Step 2: Sign In
- Sign in with your Google account
- No credit card required!

## Step 3: Create API Key
1. Click **"Get API key"** or **"Create API key"**
2. Select "Create API key in new project" (or use existing project)
3. Copy your API key (looks like: `AIza...`)

## Step 4: Add to .env File
Open `.env` file and replace this line:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

With your actual key:
```
GEMINI_API_KEY=AIzaSyABC123...your-actual-key
```

## Step 5: Test It!
```bash
python src/llm_service.py
```

You should see: ✓ Gemini API call successful

---

## Free Tier Limits

- **15 requests per minute (RPM)**
- **1 million tokens per minute (TPM)**
- **1,500 requests per day (RPD)**

More than enough for your assignment! 🎉

---

**Ready?** Get your key now: https://aistudio.google.com/apikey
