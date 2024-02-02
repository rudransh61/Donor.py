import google.generativeai as genai

def generate_text(input_file,apikey):
    try:
        genai.configure(api_key=apikey)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat()
        # print(code)
            
        response = chat.send_message(f'This is a data from donation system review it and give your recommendations to help people and our society on it like a real person by answering questions like where to donate ? how much to donate ? which place to focus more on and etc ... in short 4 points only, {input_file}')  
        return response.text
    except Exception as e:
        print(f"There was an error: {e}")
