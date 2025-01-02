import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import google.generativeai as genai
from googletrans import Translator

class MultilingualChatbot:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Chatbot")
        self.master.geometry("800x600")

        # Configure API
        genai.configure(api_key="API_KEY")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.translator = Translator()
        self.selected_language = "en"  #By Default in English

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        #Option to selectn the language 
        lang_frame = tk.Frame(self.master)
        lang_frame.pack(pady=5)

        tk.Label(lang_frame, text="Select Language:").pack(side=tk.LEFT, padx=5)

        self.lang_selector = ttk.Combobox(
            lang_frame, 
            values=["en (English)", "es (Spanish)", "fr (French)", "de (German)", "hi (Hindi)"],
            state="readonly",
            width=15
        )
        self.lang_selector.pack(side=tk.LEFT)
        self.lang_selector.set("en (English)")
        self.lang_selector.bind("<<ComboboxSelected>>", self.update_language)

        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled', width=90, height=25)
        self.chat_display.pack(pady=10)

        # User Input
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)
        self.user_input = tk.Entry(input_frame, width=50)
        self.user_input.pack(side=tk.LEFT, padx=5)
        self.user_input.bind('<Return>', self.send_message)

        # Buttons
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message, bg="green", fg="white")
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(input_frame, text="Clear Chat", command=self.clear_chat, bg="orange", fg="black")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(input_frame, text="Save Chat", command=self.save_chat, bg="blue", fg="white")
        self.save_button.pack(side=tk.LEFT, padx=5)

    def update_language(self, event=None):
        lang_code = self.lang_selector.get().split()[0]  # Extract language code
        self.selected_language = lang_code

    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        if not user_message:
            return

        # Display user message
        self.update_chat(f"You: {user_message}")
        self.user_input.delete(0, tk.END)

        # Translate user message to English
        try:
            translated_message = self.translator.translate(user_message, src=self.selected_language, dest="en").text
        except Exception as e:
            self.update_chat(f"Translation Error: {str(e)}")
            return

        # Get AI response
        try:
            response = self.model.generate_content(translated_message)
            translated_response = self.translator.translate(response.text, src="en", dest=self.selected_language).text
            self.update_chat(f"AI: {translated_response}")
        except Exception as e:
            self.update_chat(f"Error: {str(e)}")

    def update_chat(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def clear_chat(self):
        self.chat_display.configure(state='normal')
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.configure(state='disabled')

    def save_chat(self):
        try:
            with open("chat_log.txt", "w") as file:
                file.write(self.chat_display.get("1.0", tk.END))
            messagebox.showinfo("Chat Saved", "Chat log saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save chat: {str(e)}")

def main():
    root = tk.Tk()
    chatbot = MultilingualChatbot(root)
    root.mainloop()

if __name__ == "__main__":
    main()

