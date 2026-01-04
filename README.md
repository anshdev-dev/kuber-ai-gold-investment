

🏆 Kuber AI – Gold Investment Demo

This project emulates the **Kuber AI** gold investment workflow from the Simplify Money app. It demonstrates an AI-powered financial assistant that identifies gold-related intent and facilitates digital gold purchases via a microservices architecture.

### 🚀 **Live Deployment**

*[Click here to test the API (Swagger UI)](https://kuber-ai-gold-investment.onrender.com/)
*(The root URL automatically redirects to the interactive documentation for easy review.)*

---

## 📋 Overview

The system is designed to handle the following user journey:

1. **Intent Detection:** Accepts a user query and uses an LLM to detect if it is related to gold investment.
2. **Intelligent Nudge:** If relevant, responds with a factual insight and "nudges" the user toward digital gold.
3. **Transaction Processing:** Allows the user to complete a mock digital gold purchase.
4. **Data Persistence:** Records the transaction and user details in a persistent database.

---

## 🛠 Tech Stack

* **Backend:** Python, FastAPI
* **LLM:** Google Gemini (`google-genai` SDK)
* **Database:** SQLite (Lightweight, file-based persistence)
* **Deployment:** Render (Cloud Hosting)
* **Security:** Header-based API Key authentication

---

## 🔌 API Endpoints

### 1. Health Check

* **Endpoint:** `GET /health`
* **Description:** Verifies that the server is running.

**Response:**

```json
{
  "status": "ok"
}

```

### 2. Chat API (The "Brain")

* **Endpoint:** `POST /chat`
* **Header:** `x-api-key: dev-secret-key`
* **Logic:** Uses Google Gemini to analyze intent. Outputs strict JSON.

**Request:**

```json
{
  "user_id": "u123",
  "message": "Is gold safe during inflation?"
}

```

**Response (Gold Related):**

```json
{
  "is_gold_related": true,
  "confidence": 0.98,
  "response": "Gold is commonly used as a hedge against inflation. You might consider exploring digital gold options.",
  "cta": "Explore Digital Gold",
  "next_action": "BUY_GOLD"
}

```

**Response (General Query):**

```json
{
  "is_gold_related": false,
  "confidence": 0.15,
  "response": "I can help with general financial questions.",
  "cta": null,
  "next_action": "NONE"
}

```

### 3. Buy Digital Gold API (The "Muscle")

* **Endpoint:** `POST /buy-gold`
* **Header:** `x-api-key: dev-secret-key`
* **Logic:** Calculates gold grams based on amount and saves the order to the database.

**Request:**

```json
{
  "user_id": "u123",
  "amount": 100
}

```

**Response:**

```json
{
  "order_id": 1,
  "user_id": "u123",
  "gold_grams": 0.016667,
  "status": "SUCCESS",
  "message": "Digital gold purchased successfully."
}

```

> **Note:** Gold price is mocked at ₹6000/g for this demo. Minimum purchase is ₹10.

---

## 🗄 Database Design

The system uses **SQLite** to keep the assignment self-contained.

| **Table: Users** | **Table: Gold Orders** |
| --- | --- |
| `user_id` (PK, TEXT) | `order_id` (PK, Auto Increment) |
| `created_at` (TIMESTAMP) | `user_id` (FK, TEXT) |
|  | `amount` (REAL) |
|  | `gold_grams` (REAL) |
|  | `status` (TEXT) |
|  | `created_at` (TIMESTAMP) |

---

## 🔒 Security

* **API Protection:** All endpoints require a valid `x-api-key` header.
* **Secret Management:** No secrets are committed to the repository. API keys are injected via environment variables on the deployment server.

**Environment Variables Required:**

```bash
API_KEY=<your_internal_secret_key>
GEMINI_API_KEY=<google_gemini_api_key>

```

---

## 🧪 How to Test (Reviewer Guide)

1. Open the **[Live Deployment Link](https://kuber-ai-gold-investment.onrender.com/)**.
2. Click the **Authorize** button in Swagger UI and enter the provided `x-api-key`.
3. **Test the Flow:**
* Call `/chat` with a question like *"Should I invest in gold?"*.
* Observe the response (`next_action: "BUY_GOLD"`).
* Call `/buy-gold` with an amount (e.g., 100) to complete the cycle.



---

## 💡 Design Decisions

* **Architecture:** Strictly followed the two-API requirement (Chat + Transaction).
* **DX (Developer Experience):** Root endpoint (`/`) redirects immediately to `/docs` so reviewers don't hit a 404 page.
* **Reliability:** LLM output is constrained to JSON mode to prevent parsing errors.
* **Scope:** No frontend UI was built, focusing entirely on robust backend logic and data flow.

---

📦 **GitHub Repository:** [https://github.com/anshdev-dev/kuber-ai-gold-investment](https://github.com/anshdev-dev/kuber-ai-gold-investment)