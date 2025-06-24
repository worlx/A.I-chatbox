# A.I-chatbox
an a.i chatbox whose main motive is to teach

Support
🚀 Overview
This project is an interactive web-based chatbot interface built with Flask (Python) and a modern HTML/CSS/JavaScript frontend, powered by Google's Gemini 1.5 Flash model.

It provides intelligent responses based on:

User input

Custom tones (professional, simple, and action-based)

Knowledge extracted from uploaded PDF documents


gemini_webchat/
├── app.py                ← Flask backend
├── chatbox_gemini.py     ← Gemini + PDF logic
├── pdf_docs/             ← Folder of PDFs
├── static/
│   ├── style.css         ← CSS styles
│   ├── script.js         ← Chat JS logic
│   └── chat_animation.json ← Lottie file
└── templates/
    └── index.html        ← Chat page HTML
