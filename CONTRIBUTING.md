# Contributing to Build Your Own AI Agent

First off, thank you for considering contributing to **Build Your Own AI Agent**! It's people like you who make this project a great resource for the community.

We welcome all types of contributions, from fixing typos in the documentation to proposing new agent architectures.

---

## 🚀 How to Contribute

1.  **Fork** the repository on GitHub.
2.  **Clone** your fork to your local machine.
3.  **Create a branch** for your changes: `git checkout -b feature/your-feature-name` or `fix/your-fix-name`.
4.  **Make your changes** (ensure they follow our [Code Style](#-code-style) guidelines).
5.  **Commit** your changes with a clear and concise message: `feat(01): fix streaming bug` or `docs: update project table`.
6.  **Push** to your fork: `git push origin feature/your-feature-name`.
7.  **Open a Pull Request** (PR) against the `main` branch of the original repository.

---

## 🛠️ Development Setup

To set up the project locally:

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/your-username/build-your-own-ai-agent.git
    cd build-your-own-ai-agent
    ```
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 📂 Project Structure

The repository is organized into numbered project directories (e.g., `01-simple-chatbot/`). Each project is designed to be **self-contained**:

-   `main.py`: The entry point and core logic.
-   `requirements.txt`: Project-specific dependencies.
-   `README.md`: Detailed explanation of the project's concepts and architecture.

---

## 🎨 Code Style

To keep the codebase educational and easy to follow, we adhere to these rules:

-   **Language**: Use Python 3.10+.
-   **Simplicity**: Avoid heavy frameworks. Use pure Python and standard libraries whenever possible.
-   **Size**: Keep `main.py` (and other core files) under **200 lines**.
-   **Documentation**: Include clear docstrings for functions and classes. Use English for all comments and documentation.
-   **Async**: Use `async/await` for LLM calls and I/O operations.

---

## 🆕 Adding a New Project

If you'd like to propose a new agent project:

1.  Create a new directory with the next available number: `13-your-project-name/`.
2.  Include a `main.py` that implements the agent logic.
3.  Include a `requirements.txt` with pinned versions of all necessary libraries.
4.  Include a `README.md` following the standard project template (What/Why/How/Architecture).
5.  Update the main `README.md` project table.

---

## 📝 Issue Reporting

-   **Check existing issues** before opening a new one.
-   **Be specific**: Include your Python version, OS, and steps to reproduce the bug.
-   **Provide logs**: If there's an error, paste the full traceback.

---

## ✅ Pull Request Guidelines

-   **One feature per PR**: Keep PRs focused and small.
-   **Describe your changes**: Explain *why* the change is needed and *how* you implemented it.
-   **Verify your code**: Ensure `python -m py_compile main.py` passes for any modified files.

---

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and professional environment. Please be kind and helpful to fellow contributors.

**Happy Coding! 🤖**
