import os
import fitz  # PyMuPDF
import google.generativeai as genai

# 🔑 Set your Gemini API key
genai.configure(api_key="ADD your A.P.I KEY")  # Replace with your Gemini key

# 📂 Load all text from multiple PDFs using fitz (PyMuPDF)
def load_all_pdfs():
    all_text = ""
    folder = "pdf_docs"
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder, filename)
            doc = fitz.open(filepath)
            for page in doc:
                all_text += page.get_text() + "\n"
            doc.close()
    return all_text

# 🔍 Retrieve relevant lines from PDFs based on query
def retrieve_from_all_pdfs(query, pdf_text):
    lines = pdf_text.split('\n')
    matches = [line for line in lines if query.lower() in line.lower()]
    return '\n'.join(matches[:3])  # Top 3 lines for context

# 🤖 Generate 3 responses: professional, simple, approach
def chat_with_gemini(user_input, chat_history, pdf_context):
    responses = []

    roles = {
    "professional": (
        "You are a professional Google product expert. "
        "try to keep it short 3-4 lines"
        "Keep responses deep and technical, but concise."
        "Do not over-explain simple queries like greetings. "
        "for greeting like hello or hi do not explain give normal responce "
    ),
    "simple": (
        "You're a friendly assistant. "
        "Explain things clearly in plain English. "
        "Respond briefly to greetings. Only elaborate if user asks a detailed question. "
        "Use relatable examples to teach"
        "for greeting like hello or hi do not explain give normal responce "
    ),
    "approach": (
        "Give actionable advice and ask guiding questions. "
        "Avoid repeating info unless asked. "
        "For small inputs, ask for more context instead of over-explaining. "
        "Always suggest Google solutions or next steps."
        "for greeting like hello or hi do not explain give normal responce "
    )
}
    

    for tone, role_prompt in roles.items():
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=chat_history)

        full_prompt = f"{role_prompt}\n\nUse this context if helpful:\n{pdf_context}\n\nUser Query: {user_input}"

        try:
            response = chat.send_message(full_prompt)
            responses.append((tone, response.text))
        except Exception as e:
            responses.append((tone, f"⚠️ Error: {str(e)}"))

    return responses

# 🧠 CLI Chatbot Loop
def main():
    print("🤖 Gemini Chatbot (3 Styles) | PDF (fitz) | Type 'exit' to quit\n")

    all_pdf_text = load_all_pdfs()
    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        pdf_context = retrieve_from_all_pdfs(user_input, all_pdf_text)
       

        responses = chat_with_gemini(user_input, chat_history, pdf_context)

        labels = {
    "professional": "🧠 EXPERT INSIGHT",
    "simple": "🌱 FRIENDLY GUIDE",
    "approach": "🚀 NEXT STEP STRATEGY"
}

        for tone, reply in responses:
         print(f"\n=== {labels[tone]} ===\n{reply}\n")

        chat_history.append({"role": "user", "parts": [user_input]})
        chat_history.append({"role": "model", "parts": [responses[0][1]]})  # Save only professional reply

if __name__ == "__main__":
    main()
