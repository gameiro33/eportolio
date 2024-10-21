Setup your OpenAI API Key and .env file (OpenAI.com, N.D.):
1 - Head to your OpenAI account and create a new API Key
2 - Create a .env file in the same directory as the other files
3 - Add the following line to the .env file: OPENAI_API_KEY=<your_api_key>

In order to run the program:
1 - Head to the directorySearchAgent.py file
2 - Make sure that the directories for the Forensics and Archive folders exist and are correctly configured
3 - Make sure that there is at least a .txt or .sql file in your Forensics folder
4 - Run the program either through an IDE terminal or by navigating to the directory and typing "python directorySearchAgent.py"

In order to run the unit and integration tests, with coverage report:
1 - Make sure you have pytest installed
2 - On the IDE terminal, run "pytest --cov"
3 - To remove the warning, create a pyproject.toml file with the following code (De Andrade, E. S.,2024):

[tool.pytest.ini_options]
markers = [
    "integration: marks tests as integration tests",
]

References:
- OpenAI.com (N.D.) Developer Quickstart. Available from: https://platform.openai.com/docs/quickstart [Accessed: 10 October 2024]
- Pytest.org (N.D.) Pytest Documentation. Available from: https://docs.pytest.org/en/stable/contents.html [Accessed: 11 October 2024]
- De Andrade, E. S. (2024) Pytest Ignore Warnings. Available from: https://pytest-with-eric.com/configuration/pytest-ignore-warnings/#Understanding-Python-Warnings [Accessed: 12 October 2024]