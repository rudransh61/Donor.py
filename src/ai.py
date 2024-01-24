import google.generativeai as genai

def generate_text(input_file,apikey):
    try:
        genai.configure(api_key=apikey)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat()
        # print(code)
            
        response = chat.send_message(f'This is a data of donation system review it and give your recommendations on it like a real person , {input_file}')  
        return response.text
    except Exception as e:
        print(f"There was an error: {e}")
