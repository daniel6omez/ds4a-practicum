# DS4A Practicum Project Structure, Documents and Artifact Templates

This is a general project directory structure for Team Data Science Process based on TDSP by Microsoft. It also contains templates for various documents that are recommended as part of executing a data science project when using TDSP.

For more information and tools check [Team Data Science Process (TDSP)](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/overview) and [tools](https://github.com/Azure/Azure-TDSP-Utilities) for productive data science.

## Recommended environment

- IDE: [Visual Studio Code](https://code.visualstudio.com/Download)
- Extensions: [Visual Studio Code Marketplace](https://marketplace.visualstudio.com/VSCode)
- DevOps: [GitHub](https://github.com/)
- Virtualization: [Docker](https://www.docker.com/)
- Cloud: [AWS](https://aws.amazon.com/)

## Setting up the environment

1. Install [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview)
2. Install the next extensions:

   - [Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
   - [Visual Studio IntelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)
   - [Docker for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
   - [Live Share Extension Pack](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare-pack)

3. Take your time with this tutorial ["Getting Started with Python in VS Code"](https://code.visualstudio.com/docs/python/python-tutorial)
4. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and clone the repository

```
git clone https://github.com/daniel6omez/ds4a-practicum.git
```

5. Open the project with Visual Studio Code

```
cd ds4a-practicum
code .
```

6. Create and activate virtual environment

**Mac**

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

**Windows**

```
python3 -m venv .venv
.venv/bin/activate
pip install --upgrade pip
```

7. Install Jupyter notebook

```
pip install jupyter
```

7. [Working with Jupyter Notebooks in Visual Studio Code](https://code.visualstudio.com/docs/python/jupyter-support)

**NOTE:** In this directory structure, the **Sample_Data folder is NOT supposed to contain LARGE raw or processed data**. It is only supposed to contain **small and sample** data sets, which could be used to test the code.

**NOTE:** To store **LARGE raw or processed data** SQL (PostgreSQL) or NoSQL (MongoDB) is preferred.

The two documents under backend/docs/project, namely the [CHARTER](./backend/docs/project/CHARTER.md) and [EXIT_REPORT](./backend/docs/project/EXIT_REPORT.md) are particularly important to consider. They help to define the project at the start of an engagement, and provide a final report to the customer or client.

**NOTE:** In some projects, e.g. short term proof of concept (PoC) or proof of value (PoV) engagements, it can be relatively time consuming to create and all the recommended documents and artifacts. In that case, at least the Charter and Exit Report should be created and delivered to the customer or client. As necessary, organizations may modify certain sections of the documents. But it is strongly recommended that the content of the documents be maintained, as they provide important information about the project and deliverables.
