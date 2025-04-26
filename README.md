# Lil' Chatty Setup Wizard 🚀

[![Lil' Chatty OG Image](static/images/lilchatty-og.png)](https://lilchatty.com/)

Your friendly, local ChatGPT-like app setup wizard!

Lil' Chatty helps you quickly set up [Open WebUI](https://github.com/open-webui/open-webui) (a popular self-hosted web UI for LLMs) on your local machine using Docker or Colima. It checks your system RAM, recommends suitable local AI models, and provides the correct `docker run` command.

## Quick Start (MacOS)

Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) running, or have [Homebrew](https://brew.sh/) installed.

Open your terminal and run this single command:

```bash
curl -fsSL https://raw.githubusercontent.com/bensig/lilchatty/main/run.sh | bash
```

This will download and run the setup script, which will:

0.  Check if you have Python 3 and pip installed.
1.  Install the required `Flask` dependency.
2.  Run the Python setup wizard (`app.py`) - a temporary local web app.

This will guide you through:

1.  **Prerequisite Check:** Verifies if Docker is running. If not, it checks for Homebrew and guides you on installing/starting Colima (a Docker Desktop alternative).
2.  **Setup Options:** Choose between running models locally or connecting to external APIs.
3.  **Web Search:** Optionally enable web search capabilities (requires manual Google API key setup later).
4.  **Results:** Provides the appropriate `docker run` command based on your choices and recommends AI models based on your system RAM.
5.  **Instructions:** Guides you on running the Docker command and accessing Open WebUI at `http://localhost:3000`.

## Alternative Setup: Docker Compose (for advanced users)

If you prefer using Docker Compose, a `docker-compose.yml` file is included in the repository. It provides profiles for different setups:

*   **Run with bundled Ollama (Local Profile):**
    ```bash
    # Clone the repository first if you haven't already
    # git clone https://github.com/bensig/lilchatty.git
    # cd lilchatty

    docker compose --profile local up -d
    ```
*   **Run Web UI only (Cloud/Default Profile - configure external connections later):**
    ```bash
    # Clone the repository first if you haven't already
    # git clone https://github.com/bensig/lilchatty.git
    # cd lilchatty

    docker compose up -d
    # or explicitly: docker compose --profile cloud up -d
    ```

This method requires you to clone the repository manually first, unlike the one-line setup script.

## Features

*   Simple, interactive setup wizard run from the terminal.
*   Checks for Docker or Colima prerequisites.
*   Provides guidance for installing Homebrew/Colima if needed.
*   Recommends local LLMs based on available RAM (8GB, 16GB, 32GB, 32GB+).
*   Generates the correct `docker run` command for Open WebUI (with or without local Ollama volume).
*   Includes instructions for setting up Google Programmable Search Engine for web search within Open WebUI.
*   Modern UI using a custom color palette.

## How it Works

The Python script uses the Flask micro-framework to create a temporary local web server (`http://localhost:5000`). You interact with the setup wizard through your web browser. Once you complete the steps, it displays the necessary commands and instructions, and the Flask server's job is done.

## Contributing

(Optional: Add contribution guidelines later if desired)

## License

(Optional: Add a license file later, e.g., MIT License) 