# Figma to iOS Code Generator

An automated pipeline that transforms Figma designs into structured iOS application code with MVVM architecture.

## Project Overview

This tool automates the iOS app development process by:

1. Extracting designs from Figma via the Figma API
2. Analyzing design elements (screens, colors, fonts, components)
3. Generating structured markdown specifications
4. Converting specifications to JSON format
5. Using AI agents to create Swift UIKit code with MVVM architecture
6. Assembling a complete iOS project with proper file structure
7. Adding CI/CD configuration and documentation

## Data Transformation Flow

![Data Transformation Flow](https://github.com/trongtin1495/code-generator/raw/main/data-transformation-flow.png)

The pipeline consists of two main phases:

- **Phase 1**: Figma processing (design extraction and analysis)
- **Phase 2**: Code generation (structure planning, code creation, project assembly)

## End-to-End Process Sequence

![End-to-End Process Sequence](https://github.com/trongtin1495/code-generator/raw/main/end-to-end-process.png)

This diagram shows the complete sequence of operations from Figma design to generated iOS project.

## Component Relationships

![Component Relationships](https://github.com/trongtin1495/code-generator/raw/main/component-relationships.png)

## Prerequisites

- Python 3.9+
- Figma account with access token
- OpenAI API key
- Anthropic API key (Claude)

## Installation

1. Clone the repository & navigate to project folder:

```bash
cd code-generator
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# On macOS/Linux
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:

```bash
touch .env
```

.env format provided

```
ANTHROPIC_API_KEY=<your_anthropic_api_key>
OPENAI_API_KEY=<your_openai_api_key>
FIGMA_ACCESS_TOKEN=<your_figma_access_token>
PROJECT_NAME=YourAppName
BASE_OUTPUT_PATH=./output
PROJECT_GENERATED_PATH=./output/generated-project
```

## Usage

Run the pipeline with a Figma file key:

```bash
python run_pipeline.py --figma-key <your_figma_file_key> [--output-dir <custom_output_directory>]
```

The Figma file key can be found in the URL of your Figma file:
`https://www.figma.com/file/<YOUR_FILE_KEY>/...`

### Output

The pipeline generates:

1. `output/figma_design.json`: Raw Figma API response
2. `output/summary_report.json`: Analyzed design elements
3. `output/figma_markdown.md`: Design specifications in markdown
4. `output/generated-project/`: Complete iOS project with Swift code

## Pipeline Components

### Core Modules

- **figma_fetcher.py**: Interfaces with Figma API to download design files
- **figma_analyzer.py**: Extracts design elements, colors, fonts, and components
- **markdown_generator.py**: Creates structured markdown specifications

### Agent Modules

- **spec_to_json_agent.py**: Converts markdown to structured JSON
- **ios_structure_planner_agent.py**: Plans iOS project structure
- **code_generator_agent.py**: Generates Swift code for screens
- **project_assembler_agent.py**: Writes files to disk in proper structure
- **ci_docs_agent.py**: Creates CI configuration and documentation

### Orchestration

- **run_pipeline.py**: Main entry point that executes the full pipeline
- **crew_runner.py**: Manages the AI agent workflow
- **dag_flow.py**: Creates a LangGraph DAG (Directed Acyclic Graph) for code generation

## Development

### Environment Setup

For development, you can use:

```bash
python -m pip install -e .
```

### Adding New Components

To extend the pipeline:

1. Add new agent files in the `agents/` directory
2. Update `dag_flow.py` to include new nodes in the graph
3. Modify `crew_runner.py` to integrate new workflow steps

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This project utilizes:

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [CrewAI](https://github.com/crewai/crewai)
- [Anthropic Claude](https://www.anthropic.com/)
- [OpenAI](https://openai.com/)
