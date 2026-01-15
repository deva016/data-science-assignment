# 💡 LLM Provider Information

## ✅ Current Setup: Google Gemini (FREE)

This project uses **Google Gemini 2.5 Flash** as the primary LLM provider.

### Why Gemini?
- ✅ **100% FREE** - No credit card required
- ✅ **Generous FREE tier** - 15 requests/minute, 1,500/day
- ✅ **Easy setup** - Get API key in 2 minutes
- ✅ **Excellent performance** - Great for structured JSON outputs

### Get Your FREE Gemini API Key
👉 See **[GET_GEMINI_KEY.md](GET_GEMINI_KEY.md)** for step-by-step instructions

---

## 🔄 Backup Provider (Optional)

The system includes **OpenAI GPT-4o** as an automatic fallback if Gemini fails.

**Note**: OpenAI requires credits after free trial, so Gemini is recommended as the primary provider for this assignment.

---

## 🛠️ Troubleshooting LLM Issues

### "Gemini API Error"
- Verify your API key is correct in `.env`
- Check you have an active internet connection
- Ensure you haven't exceeded rate limits (15/min)

### "Both LLM providers failed"
- Make sure `GEMINI_API_KEY` is set in `.env` file
- Try restarting the backend: `python main.py`

### Need More Help?
See the main **[README.md](README.md)** for complete troubleshooting guide.

