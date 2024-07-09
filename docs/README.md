# Discord Bot UHM

This project is a Discord bot made for a community server: "Lux Nightclub". It is made to help the creator make personalized commands that no other server has. For example, instead of a basic verification with a captcha when entering the server, the creator decided to let people create a server ID Card with the captcha in it.

## How to use it
To use it, you can modify the prefix of the bot (line 22) or just use it as it is (lux). You can also use slash commands when implemented.

## How to contribute
The only contributor, as I write this (July 9th, 2024), is myself, "Badis213" on GitHub.

We welcome contributions from the community! Here’s how you can get started:

1. **Fork the Repository**: Click the "Fork" button at the top right of this page to create a copy of this repository under your GitHub account.

2. **Clone Your Fork**: Clone your forked repository to your local machine.

    ```sh
    git clone https://github.com/<your-username>/Discord-Bot-UHM.git
    cd Discord-Bot-UHM
    ```

3. **Create a Branch**: Create a new branch for your feature or bugfix.

    ```sh
    git checkout -b my-new-feature
    ```

4. **Make Your Changes**: Make your changes to the code. Be sure to follow the existing coding style and add comments as necessary.

5. **Commit Your Changes**: Commit your changes with a clear and concise commit message.

    ```sh
    git add .
    git commit -m "Add a new feature"
    ```

6. **Push to Your Fork**: Push your changes to your forked repository.

    ```sh
    git push origin my-new-feature
    ```

7. **Create a Pull Request**: Go to the original repository and create a pull request from your forked repository. Be sure to include a description of your changes and any relevant information.

### Reporting Issues

If you find any bugs or have suggestions for improvements, please create an issue on the GitHub repository. When reporting an issue, please include as much detail as possible, including steps to reproduce the problem and any relevant information about your setup.

### Coding Guidelines

To maintain a consistent codebase, please follow these guidelines:
- Follow the PEP 8 style guide for Python code.
- Write clear, concise commit messages.
- Document your code with comments where necessary.
- Ensure your code passes all existing tests and write new tests for any new functionality.

### Setting Up Your Development Environment

1. **Install Dependencies**: Ensure you have Python installed, then install the required dependencies.

    ```sh
    pip install -r requirements.txt
    ```

2. **Environment Variables**: Create a `.env` file to securely store your Discord bot token and any other sensitive information. The `.env` file should look like this:

    ```sh
    DISCORD_TOKEN=your_token_here
    ```

3. **Run the Bot**: You can start the bot by running the main script.

    ```sh
    python src/main.py
    ```

By following these steps, you'll be able to set up your development environment and contribute effectively to the project. Thank you for your interest in contributing!

## Installation

Clone the repository and install the dependencies:

```sh
git clone https://github.com/Badis213/Discord-Bot-UHM.git
cd Discord-Bot-UHM
pip install -r requirements.txt
