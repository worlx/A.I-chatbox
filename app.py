from flask import Flask, render_template, request, jsonify
from extraexamole import chat_with_gemini, load_all_pdfs, retrieve_from_all_pdfs

app = Flask(__name__)

# Load all PDF data once at startup
try:
    all_pdf_text = load_all_pdfs()
    print("✅ PDF data loaded successfully")
except Exception as e:
    print("❌ Error loading PDFs:", e)
    all_pdf_text = {}

# Keep chat history in memory
chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("user_input", "")
        if not user_input:
            return jsonify({"error": "No input received"}), 400

        print(f"\n👤 User asked: {user_input}")

        # Step 1: Extract relevant text from PDF
        context = retrieve_from_all_pdfs(user_input, all_pdf_text)
        print("📄 Context from PDF:", context[:200], "...")

        # Step 2: Generate 3-tone response
        responses = chat_with_gemini(user_input, chat_history, context)
        print("🤖 Gemini responses generated.")

        # Step 3: Format as dictionary to send to frontend
        result = {tone: reply for tone, reply in responses}

        # Step 4: Update chat history
        chat_history.append({"role": "user", "parts": [user_input]})
        chat_history.append({"role": "model", "parts": [result["professional"]]})

        return jsonify(result)

    except Exception as e:
        print("🔥 Server error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
