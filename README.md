# 🏥 Clinical Summary Generator

A sophisticated AI-powered application that generates comprehensive, evidence-based clinical summaries for home health patients with **dual-LLM architecture** and **citation tracking**.

**🔗 Live Repository**: https://github.com/deva016/data-science-assignment

## 🌟 Key Features

- **🤖 Dual-LLM Architecture**: Google Gemini 2.5 Flash (FREE, primary) with OpenAI (fallback)
- **📚 Citation Tracking**: Every clinical claim is backed by source data
- **🔄 Automatic Fallback**: Seamless switching between AI providers
- **📊 Comprehensive Analysis**: Diagnoses, vitals, wounds, medications, functional status
- **🎯 Evidence-Based**: All summaries grounded in actual patient data
- **🚀 Production-Ready**: Robust error handling and resilience
- **💰 FREE to Use**: Primary LLM (Gemini) requires no payment

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │  ← User Interface
└────────┬────────┘
         │
    ┌────▼────┐
    │ FastAPI │  ← REST API Backend
    └────┬────┘
         │
    ┌────▼─────────────┐
    │   Data Layer     │  ← CSV Ingestion
    └────┬─────────────┘
         │
    ┌────▼─────────────┐
    │   LLM Service    │  ← AI Generation
    │                  │
    │  1️⃣ Gemini 2.5   │  (Primary - FREE)
    │  2️⃣ OpenAI       │  (Fallback)
    └──────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- **FREE Google Gemini API Key**: [Get it here](https://aistudio.google.com/apikey) (No credit card!)
- Optional: OpenAI API key for fallback

## ⚡ Quick Start

### 1️⃣ Clone & Setup

```bash
# Navigate to project directory
cd data-science-assignment

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure API Keys

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=AIzaSy...your-actual-gemini-key-here
# 
# Optional: Add OpenAI key for fallback
# OPENAI_API_KEY=sk-your-openai-key
```

**Get FREE Gemini API Key**:
1. Visit: https://aistudio.google.com/apikey
2. Sign in with Google account (no credit card!)
3. Click "Create API key"
4. Copy and paste into `.env` file

### 3️⃣ Start the Backend

```bash
# Terminal 1 - Start FastAPI server
python main.py

# Or use uvicorn directly:
uvicorn main:app --reload
```

**Backend will be available at:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### 4️⃣ Start the Frontend

```bash
# Terminal 2 - Start Streamlit app
streamlit run app.py
```

**Frontend will open automatically at:** http://localhost:8501

## 🎯 Usage

1. **Select Patient**: Choose from available patient IDs (1001, 1002)
2. **Configure**: Enable/disable citation tracking
3. **Generate**: Click "Generate Summary" button
4. **View**: Review comprehensive clinical summary with citations
5. **Download**: Export as JSON or text file

## 📁 Project Structure

```
data-science-assignment/
├── data/                          # Patient data (CSV files)
│   ├── diagnoses.csv             # Medical conditions
│   ├── medications.csv           # Active prescriptions
│   ├── vitals.csv                # Vital sign history
│   ├── notes.csv                 # Clinical notes
│   ├── wounds.csv                # Wound assessments
│   └── oasis.csv                 # Functional status
├── src/                           # Core application code
│   ├── __init__.py               # Package initialization
│   ├── data_layer.py             # CSV loading & querying
│   └── llm_service.py            # Dual-LLM integration
├── main.py                        # FastAPI backend
├── app.py                         # Streamlit frontend
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
└── README.md                      # This file
```

## 📚 Documentation

Comprehensive guides to help you get started:

| Document | Description |
|----------|-------------|
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | 🚀 Quick start guide - Get running in 5 minutes |
| **[GET_GEMINI_KEY.md](GET_GEMINI_KEY.md)** | 🔑 Step-by-step: Get your FREE Gemini API key |
| **[API_CREDITS_SOLUTIONS.md](API_CREDITS_SOLUTIONS.md)** | 💡 LLM provider information and troubleshooting |

**New to the project?** Start with [SETUP_GUIDE.md](SETUP_GUIDE.md) for the fastest path to running the application.

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Primary LLM (Google Gemini - FREE)
GEMINI_API_KEY=AIzaSy...your-key-here

# Backup LLM (OpenAI - Optional)
OPENAI_API_KEY=sk-your-key-here

# Model Configuration
GEMINI_MODEL=gemini-2.5-flash
OPENAI_MODEL=gpt-4o
TEMPERATURE=0.3

# Fallback Settings
USE_FALLBACK=true                  # Enable OpenAI fallback
# FORCE_PROVIDER=gemini            # Force specific provider (optional)
```

## 🚀 API Endpoints

### `GET /patients`
Get list of available patient IDs

```bash
curl http://localhost:8000/patients
```

### `POST /generate_summary`
Generate clinical summary for a patient

```bash
curl -X POST http://localhost:8000/generate_summary \
  -H "Content-Type: application/json" \
  -d '{"patient_id": 1001, "include_citations": true}'
```

### `GET /patient/{patient_id}/data`
Get raw patient data (debugging)

```bash
curl http://localhost:8000/patient/1001/data
```

## 🧪 Testing

### Test Data Layer
```bash
python src/data_layer.py
```

### Test LLM Service
```bash
python src/llm_service.py
```

### Test API
```bash
# Check health
curl http://localhost:8000/health

# List patients
curl http://localhost:8000/patients

# Generate summary
curl -X POST http://localhost:8000/generate_summary \
  -H "Content-Type: application/json" \
  -d '{"patient_id": 1001}'
```

## 🎓 How It Works

### Dual-LLM Fallback Strategy

```python
def generate_summary(patient_data):
    try:
        # 1️⃣ PRIMARY: Try Google Gemini 2.5 Flash (FREE)
        return call_gemini(patient_data)
    except:
        # 2️⃣ BACKUP: Fallback to OpenAI GPT-4o
        return call_openai(patient_data)
```

### Citation Tracking

Each clinical claim is linked to its source:

```json
{
  "content": "Patient has elevated blood pressure (149/98)",
  "citations": ["Source: vitals.csv, Date: 2026-01-02"]
}
```

## 💡 Tips

- **FREE to Use**: Gemini 2.5 Flash is completely free with generous limits
- **Primary Provider**: Gemini optimized for structured JSON outputs
- **Fallback**: If Gemini fails, system automatically uses OpenAI (if configured)
- **Force Provider**: Set `FORCE_PROVIDER=gemini` or `openai` in `.env` to use specific provider

## 🐛 Troubleshooting

### "Cannot connect to API"
- Ensure backend is running: `python main.py`
- Check API URL in Streamlit sidebar

### "API key not configured"
- Create `.env` file from `.env.example`
- Add valid API keys
- Restart backend

### "Both LLM providers failed"
- Check API keys are valid
- Verify internet connection
- Check provider status pages

### "No patients found"
- Verify CSV files exist in `data/` directory
- Run data layer test: `python src/data_layer.py`

## 📊 Sample Output

```
CLINICAL SUMMARY - Patient 1001

Patient presents with Stage IV pressure ulcer on left iliac crest 
and Stage III pressure ulcer on left heel [Source: diagnoses.csv, 
wounds.csv]. Recent vital signs show stable blood pressure ranging 
from 102-126 systolic [Source: vitals.csv, 2025-08-26 to 2025-10-15].

Functional status assessment indicates patient requires assistance 
with all ADLs: grooming (level 2), bathing (level 5), transfer 
(level 3) [Source: oasis.csv, 2025-08-15]...
```

## 🤝 Contributing

This is an assignment project. For questions or issues, contact the assignment provider.

## 📄 License

Educational project for data science assignment.

## 🔗 Resources

- [Google AI Studio (Gemini)](https://aistudio.google.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Built with ❤️ for Home Health Care**
