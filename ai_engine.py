import google.generativeai as genai

# --- CONFIGURATION ---
# 🔴 IMPORTANT: Paste your API Key inside the quotes below
GEMINI_API_KEY = "AIzaSyDH28Zr1JhrYoKWw7ZkvnyYS3Rt3684ETc"

genai.configure(api_key=GEMINI_API_KEY)

def get_ai_reflection(code_snapshot: str, thinking_style: str, complexity: int, errors: list):
    try:
        # --- NEW: AUTO-DETECT THE BEST MODEL ---
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return "DevMirror Error: No compatible AI models found for this API key."
        
        # We pick the best one available (usually gemini-1.5-flash)
        model_name = available_models[0] 
        model = genai.GenerativeModel(model_name)

        prompt = f"""
        You are DevMirror, an expert AI coding mentor.
        Thinking Style: "{thinking_style}"
        Code Complexity: {complexity}
        Anti-patterns: {errors}
        
        CODE:
        {code_snapshot}
        
        TASK:
        Give a 2-sentence reflection. 
        1. Mirror their mental state.
        2. Give one specific coding tip for that code.
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"DevMirror is offline (AI Error): {str(e)}"