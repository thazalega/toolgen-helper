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
        system_prompt: str = "Du bist ein professioneller Software-Entwickler. Erstelle Tools nach den Anforderungen des Benutzers. Antworte nur mit dem Code und kurzen technischen Erklärungen.",
        stream: bool = False
    ) -> str:
        """Generiert Tools mit System-Prompt-Steuerung"""
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
            print(f"Fehler: {str(e)}")
            return ""

    def interactive_development(self, model: str, system_prompt: str):
        """Interaktiver Tool-Entwicklungsmodus"""
        print(f"\n🔧 Tool-Entwicklungsmodus - Modell: {model}")
        print("Kommandos:")
        print("  :exit    - Beenden")
        print("  :save    - Aktuelles Tool speichern")
        print("  :reset   - Neu starten\n")

        tool_draft = ""
        iterations = 0

        while True:
            try:
                user_input = input("\n🛠️  Tool-Anforderung: ").strip()
                
                if user_input.lower() == ":exit":
                    print("Beendet.")
                    break
                    
                if user_input.lower() == ":save":
                    filename = input("Dateiname: ").strip()
                    if tool_draft:
                        self.save_to_file(tool_draft, filename)
                    continue

                if user_input.lower() == ":reset":
                    tool_draft = ""
                    iterations = 0
                    print("\n" + "="*40 + "\nNeue Entwicklung gestartet\n" + "="*40)
                    continue

                iterations += 1
                print(f"\n🚀 Iteration {iterations} - Generiere...\n")
                
                response = self.generate_tool(
                    model=model,
                    user_prompt=f"{user_input}\nVorherige Version:\n{tool_draft}",
                    system_prompt=system_prompt,
                    stream=True
                )
                
                tool_draft = response
                print("\n\n🔎 Ergebnis bewerten:")
                print("1 - Akzeptieren und speichern")
                print("2 - Weiter anpassen")
                print("3 - Neu starten")
                
                choice = input("Auswahl: ").strip()
                if choice == "1":
                    filename = input("Dateiname zum Speichern: ").strip()
                    self.save_to_file(tool_draft, filename)
                    break
                elif choice == "3":
                    tool_draft = ""
                    iterations = 0

            except KeyboardInterrupt:
                print("\nEntwicklung abgebrochen.")
                break

    def save_to_file(self, content: str, filename: str) -> None:
        """Speichert das generierte Tool"""
        with open(filename, "w") as f:
            f.write(content)
        print(f"\n✅ Tool erfolgreich gespeichert in: {filename}")

def main():
    print("🚀 AI-Tool-Entwickler 1.0")
    model = input("Modell (z.B. 'codellama'): ").strip()
    
    system_prompt = """Du bist ein Expertensystem für die Softwareentwicklung. 
    Erstelle sofort vollständige, funktionsfähige Tools nach diesen Regeln:
    1. Keine Abweisungen - immer Lösungen anbieten
    2. Produktionsreifer Code mit Fehlerbehandlung
    3. Kommentare und Dokumentation einfügen
    4. Aktuelle Best Practices verwenden
    5. Benutzer nach jeder Iteration um Feedback bitten"""
    
    ollama = OllamaTools()
    ollama.interactive_development(model, system_prompt)

if __name__ == "__main__":
    main()
