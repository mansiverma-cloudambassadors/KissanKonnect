#🍅 KissanKonnect – Nutrigenie Recipe Suggestion API

KissanKonnect (Nutrigenie) is an AI-powered recipe suggestion and nutrition analysis system built on Google’s Gemini AI. It leverages Google’s Gemini AI for natural language recipe generation and ingredient analysis, built on a scalable FastAPI backend and integrated with a modern React-based frontend. It intelligently processes both text and image inputs to identify ingredients, analyze nutritional values, and generate personalized recipes. The backend is powered by FastAPI, while a modern React-based frontend ensures an interactive user experience.
This project is designed for seamless cooking assistance and to demonstrate how AI can bridge everyday cooking with smart, nutrition-driven decisions.

✨ **Key Features**

* **Task 1 – Ingredient & Nutrition Analysis**
  * Input: Image or text (list of ingredients).
  * Output: Identified ingredients with nutritional values.

* **Task 2 – Recipe Generation & Gap Analysis**
  * Input: JSON list of ingredients.
  * Output: Suggested recipes and missing items to be purchased.

* **Auto-Flow API Design**: Output from `/suggestions/` feeds directly into `/recipe/` for a smooth workflow.
* **Structured JSON Responses**: Ensures clean integration for applications and dashboards.
* **Cloud-Native & Scalable**: FastAPI backend is containerized with Docker and deployable on Google Cloud Run.
* **User-Friendly Web UI**: React-based interface for ingredient entry, recipe viewing, and nutritional insights.

🛠️ **Tech Stack**

* **Backend**: Python, FastAPI, Pydantic, Google Generative AI (Gemini), Uvicorn
* **Frontend**: React, JavaScript, Axios, Tailwind CSS
* * **Database / State Mgmt.**: In-memory (future-ready for SQL integration)

🚀 **Usage Workflow**

### 🔹 Task 1 – Ingredient & Nutrition Analysis

Identify Ingredients & Nutrition
* Provide input as text list or upload an image of ingredients.
* Gemini analyzes the input to recognize ingredients and return their nutritional values.

### 🔹 Task 2 – Recipe Suggestion & Gap Analysis

Get Recipe Suggestions
* Use `/suggestions/` endpoint or UI input box.
* Example: Input → `["tomato", "onion", "paneer"]`
* Output → Suggested dishes like *Paneer Masala, Tomato Curry, Stuffed Paratha*.

Select a Dish
* Pass selection to `/recipe/` endpoint.
* System returns full recipe with step-by-step cooking instructions.

Get Missing Items
* API highlights unavailable ingredients.
* Suggests items that need to be purchased to complete the recipe.

📋 **Prerequisites**
Make sure you have the following installed:

* Python (3.9+)
* Fast API
* Google Cloud SDK (`gcloud`)
* Gemini API key (Vertex AI access required)

⚙️ **Configuration & Setup**

### 1. Google Cloud Setup
* Create a **Google Cloud Project** and enable billing.
* Enable these APIs:

  * Vertex AI API
  * Cloud Run Admin API
  * Cloud Build API
  * Artifact Registry API
  * Secret Manager API
    
* Create a **Service Account** with roles:
  * Vertex AI User (Gemini model access)
  * Secret Manager Accessor
    
* Generate and download the service account JSON key.

### 2. Backend Setup

```bash
git clone https://github.com/your-username/kissankonnect-nutrigenie.git
cd kissankonnect-nutrigenie/backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` with:

```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

Start backend:

```bash
uvicorn main:app --reload
```

Backend and Frontend runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

✅ **Example API Calls**

* **Get Suggestions**

```bash
curl -X POST http://127.0.0.1:8000/suggestions/ \
  -H "Content-Type: application/json" \
  -d '{"ingredients": ["potato", "onion", "capsicum"]}'
```

* **Get Recipe**

```bash
curl -X POST http://127.0.0.1:8000/recipe/ \
  -H "Content-Type: application/json" \
  -d '{"dish": "Aloo Capsicum Curry"}'
```

This makes KissanKonnect Nutrigenie your **personal cooking assistant**, bridging AI with everyday kitchen needs. 🍲✨
