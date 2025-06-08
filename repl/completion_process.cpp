#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <cstdlib>
#include "json.hpp"

using json = nlohmann::json;

std::string runPythonCompleter(const std::string& input) {
    std::string command = "python3 python_completer.py \"" + input + "\"";
    std::string result;
    char buffer[128];

    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) return "[]";

    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result += buffer;
    }
    pclose(pipe);
    return result;
}

int main() {
    std::string input;
    std::cout << "Redis Command Auto-Completer\nType a partial command (or 'exit'):\n";

    while (true) {
        std::cout << "> ";
        std::getline(std::cin, input);
        if (input == "exit") break;

        std::string json_output = runPythonCompleter(input);
        try {
            auto suggestions = json::parse(json_output);
            if (suggestions.empty()) {
                std::cout << "(no suggestions)\n";
            } else {
                std::cout << "Suggestions:\n";
                for (const auto& s : suggestions) {
                    std::cout << "  " << s.get<std::string>() << "\n";
                }
            }
        } catch (...) {
            std::cerr << "Error parsing Python output.\n";
        }
    }

    return 0;
}
