import json 
from fuzzywuzzy import process  # For fuzzy matching of commands 
from prompt_toolkit import prompt  # For interactive command-line input
from prompt_toolkit.completion import Completer, Completion  # For implementing auto-completion logic
from prompt_toolkit.styles import Style  # To apply custom colors/styles to suggestions

# Define color styles for command suggestion types
COLOR_EXACT = "ansigreen"  # Color for exact command match
COLOR_FUZZY = "ansiyellow"  # Color for fuzzy/approximate match

# Define supported commands with their expected syntax
COMMANDS = {
    "SET": "SET key val",
    "DEL": "DEL key",
    "SELECT": "SELECT key",
    "SHOW": "SHOW",
    "SHOW LOCAL": "SHOW LOCAL",
    "SHOW WRITE": "SHOW WRITE",
    "MULTI": "MULTI",
    "EXEC": "EXEC",
    "ROLLBACK": "ROLLBACK"
}

# Custom completer class for command-line auto-suggestions
class RedisCompleter(Completer):
    def get_completions(self, document, complete_event):
        # Extract and split user input
        text = document.text.strip()
        tokens = text.split()

        # If no input, suggest all commands
        if not tokens:
            for cmd in sorted(COMMANDS):
                yield Completion(COMMANDS[cmd], style=COLOR_EXACT, start_position=0)
            return

        # Extract command and arguments
        cmd = tokens[0].upper()
        rest = tokens[1:]

        # Handle autocompletion when user has typed only the command
        if len(tokens) == 1:
            # Exact matches (start with the typed text)
            exact_matches = [c for c in COMMANDS if c.startswith(cmd)]
            # Fuzzy matches (similar commands based on fuzzy ratio)
            fuzzy_matches = [m[0] for m in process.extract(cmd, COMMANDS.keys(), limit=5) if m[1] > 70]

            # Yield exact match suggestions
            for c in sorted(set(exact_matches)):
                yield Completion(COMMANDS[c], style=COLOR_EXACT, start_position=-len(tokens[0]))

            # Yield fuzzy match suggestions (if not already exact matches)
            for f in sorted(set(fuzzy_matches) - set(exact_matches)):
                yield Completion(COMMANDS[f], style=COLOR_FUZZY, start_position=-len(tokens[0]))

        # If command is complete and arguments are being typed, suggest the full syntax
        else:
            if cmd in COMMANDS:
                args_hint = COMMANDS[cmd]
                yield Completion(args_hint, style=COLOR_EXACT, start_position=-len(' '.join(tokens)))

# Launch the interactive Redis-style prompt
def redis_prompt():
    # Define prompt style for different match types
    style = Style.from_dict({
        COLOR_EXACT: 'bold #00ff00',     # Green and bold for exact
        COLOR_FUZZY: 'italic #ffff00',   # Yellow and italic for fuzzy
    })

    # Prompt loop
    while True:
        try:
            # Get user input with auto-completion
            user_input = prompt("redis> ", completer=RedisCompleter(), style=style)

            # Exit condition
            if user_input.strip().upper() == "EXIT":
                print("Bye.")
                break
            else:
                # For now, just echo the input (placeholder for actual command execution)
                print(f"Input: {user_input}")

        # Handle Ctrl+C or Ctrl+D to exit 
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

if __name__ == "__main__":
    redis_prompt()
