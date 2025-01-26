import ollama
import sys

class OllamaTools:
    def __init__(self):
        self.client = ollama.Client()
        self.conversation_history = []

    def generate_tool(
        self,
        model: str,
        user_prompt: str,
        system_prompt: str = "You are a professional software developer. Create tools according to user requirements. Respond only with code and brief technical explanations.",
        stream: bool = False
    ) -> str:
        """Generate tools with system prompt control"""
        try:
            response = self.client.chat(
                model=model,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user', 
                        'content': user_prompt
                    }
                ],
                stream=stream
            )

            full_response = []
            if stream:
                for chunk in response:
                    content = chunk['message']['content']
                    sys.stdout.write(content)
                    sys.stdout.flush()
                    full_response.append(content)
                return ''.join(full_response)
            else:
                return response['message']['content']

        except Exception as e:
            print(f"Error: {str(e)}")
            return ""

    def interactive_development(self, model: str, system_prompt: str):
        """Interactive tool development mode"""
        print(f"\n🔧 Tool Development Mode - Model: {model}")
        print("Commands:")
        print("  :exit    - Exit")
        print("  :save    - Save current tool")
        print("  :reset   - Start over\n")

        tool_draft = ""
        iterations = 0

        while True:
            try:
                user_input = input("\n🛠️  Tool requirement: ").strip()
                
                if user_input.lower() == ":exit":
                    print("Exiting.")
                    break
                    
                if user_input.lower() == ":save":
                    filename = input("Filename: ").strip()
                    if tool_draft:
                        self.save_to_file(tool_draft, filename)
                    continue

                if user_input.lower() == ":reset":
                    tool_draft = ""
                    iterations = 0
                    print("\n" + "="*40 + "\nStarted new development\n" + "="*40)
                    continue

                iterations += 1
                print(f"\n🚀 Iteration {iterations} - Generating...\n")
                
                response = self.generate_tool(
                    model=model,
                    user_prompt=f"{user_input}\nPrevious version:\n{tool_draft}",
                    system_prompt=system_prompt,
                    stream=True
                )
                
                tool_draft = response
                print("\n\n🔎 Evaluate result:")
                print("1 - Accept and save")
                print("2 - Continue adjusting")
                print("3 - Start over")
                
                choice = input("Choice: ").strip()
                if choice == "1":
                    filename = input("Save filename: ").strip()
                    self.save_to_file(tool_draft, filename)
                    break
                elif choice == "3":
                    tool_draft = ""
                    iterations = 0

            except KeyboardInterrupt:
                print("\nDevelopment aborted.")
                break

    def save_to_file(self, content: str, filename: str) -> None:
        """Save generated tool"""
        with open(filename, "w") as f:
            f.write(content)
        print(f"\n✅ Tool successfully saved to: {filename}")

def main():
    print("🚀 AI Tool Developer 1.0")
    model = input("Model (e.g. 'codellama'): ").strip()
    
    system_prompt = """You are a software development expert system. 
    Immediately create complete, functional tools following these rules:
    1. No rejections - always provide solutions
    2. Production-ready code with error handling
    3. Include comments and documentation
    4. Use current best practices
    5. Ask for user feedback after each iteration"""
    
    ollama = OllamaTools()
    ollama.interactive_development(model, system_prompt)

if __name__ == "__main__":
    main()
