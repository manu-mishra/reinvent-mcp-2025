# re:Invent 2025 MCP Server

[![npm package](https://img.shields.io/npm/v/reinvent2025mcp?label=npm%20package)](https://www.npmjs.com/package/reinvent2025mcp)
[![pypi package](https://img.shields.io/pypi/v/re-invent-2025-mcp?label=pypi%20package)](https://pypi.org/project/re-invent-2025-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Comprehensive Model Context Protocol (MCP) server providing intelligent access to AWS re:Invent 2025 session catalog with 1,843 sessions, advanced search capabilities, and speaker discovery.**

---

## 🚀 **Quick Start for Claude Desktop Users**

**Get instant access to all 1,843 re:Invent 2025 sessions in Claude Desktop:**

### [📦 **Download Claude Extension**](https://github.com/manu-mishra/reinvent-mcp-2025/raw/main/claude/reinvent-2025-session-catalog-nodejs.mcpb)

**Installation**: Just drag & drop the `.mcpb` file into Claude Desktop Extensions → Click "Install" → Start exploring!

**Try asking Claude**: *"Find all AI sessions at re:Invent 2025"* or *"Show me sessions for developers about serverless"*

---

## 🌟 Overview

The re:Invent 2025 MCP Server transforms how professionals navigate AWS's flagship conference. With 1,843 sessions spanning 53 areas of interest and 19 industries, finding relevant content becomes an overwhelming challenge. This MCP server solves that problem by providing AI assistants with intelligent access to the complete session catalog, enabling personalized recommendations, strategic analysis, and data-driven conference planning.

Built on the [Model Context Protocol](https://modelcontextprotocol.io/), this server bridges the gap between conference content and actionable insights. Whether you're a developer seeking technical deep-dives, an executive planning strategic initiatives, or a sales professional researching customer opportunities, the server delivers precise, contextual recommendations that maximize your conference ROI.

### Real-World Impact

**For Technical Teams**: Discover hands-on workshops, certification-aligned content, and service-specific sessions that accelerate skill development and project success.

**For Business Leaders**: Access strategic frameworks, industry-specific insights, and quantified business outcomes ($3.7T markets, 70-90% efficiency gains) that inform decision-making and competitive positioning.

**For Sales & Partners**: Research customer industries, identify co-marketing opportunities, and extract compelling value propositions from 1,843 sessions of AWS innovation and customer success stories.

**For Event Organizers**: Analyze content gaps, optimize scheduling, track speaker participation, and understand audience segmentation across the world's largest cloud computing conference.

### What is Model Context Protocol (MCP)?

MCP is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It enables secure, controlled access to external data sources, tools, and services, allowing AI assistants to perform complex tasks with real-world information. This server leverages MCP to make conference navigation as intelligent as the AI systems AWS customers build on the platform.

### Why re:Invent 2025 Matters

AWS re:Invent isn't just a conference—it's the epicenter of cloud innovation, where breakthrough technologies like agentic AI, quantum computing, and autonomous systems are unveiled. With sessions covering everything from foundational concepts to distinguished-level expertise, re:Invent shapes the future of technology. This MCP server ensures you don't miss the sessions that matter most to your goals, whether that's technical mastery, business transformation, or competitive advantage.

## 🚀 Quick Start

### One-Click Installation (Claude Desktop)

**Download Claude Desktop Extension (.mcpb file)**:
- [📦 Download Extension](https://github.com/manu-mishra/reinvent-mcp-2025/raw/main/claude/reinvent-2025-session-catalog-nodejs.mcpb)

**Installation**: Drag and drop the `.mcpb` file into Claude Desktop Extensions → Click "Install"

### Command Line Installation

Install instantly with Node.js:

**Node.js**
```bash
npx reinvent2025mcp
```

### MCP Inspector (Testing)

Test the server with the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector npx reinvent2025mcp
```

### Integration with AI Assistants

Configure with popular MCP-compatible clients:

#### Claude Desktop

**Option 1: One-Click Installation (Recommended)**
Download and drag the `.mcpb` file from the Quick Start section above.

**Option 2: Manual Configuration**
Settings → Developer → Edit Config:

```json
{
  "mcpServers": {
    "reinvent-2025": {
      "command": "npx",
      "args": ["reinvent2025mcp"]
    }
  }
}
```

#### Amazon Q Developer (CLI)

```bash
q mcp add --name reinvent-2025 \
  --command npx \
  --args reinvent2025mcp
```

#### Amazon Q Developer (IDE)
Chat panel → Tools icon → Add MCP Server:
- **Name**: `reinvent-2025`
- **Command**: `npx`
- **Args**: `reinvent2025mcp`

#### Cline (VS Code)
MCP Servers icon → Add Server:

```json
{
  "name": "reinvent-2025",
  "command": "npx",
  "args": ["reinvent2025mcp"]
}
```

#### Continue.dev
`~/.continue/config.json`:

```json
{
  "mcpServers": [{
    "name": "reinvent-2025",
    "command": "npx",
    "args": ["reinvent2025mcp"]
  }]
}
```

#### Cursor IDE
Settings → MCP → Add Server or `.cursor/mcp.json`:

```json
{
  "servers": {
    "reinvent-2025": {
      "command": "npx",
      "args": ["reinvent2025mcp"]
    }
  }
}
```

#### VS Code (GitHub Copilot)
Extensions → @mcp → Install MCP extension, then configure in settings:

```json
{
  "mcp.servers": [{
    "name": "reinvent-2025",
    "command": "npx",
    "args": ["reinvent2025mcp"]
  }]
}
```

### Quick Setup Commands

**Test with MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector npx reinvent2025mcp
```

## ✨ Features

### 🔍 Intelligent Session Discovery
- **Universal Search**: Query across titles, abstracts, topics, and metadata
- **Empty Query Support**: List all 1,843 sessions with pagination
- **Fuzzy Matching**: Find relevant content even with partial or approximate terms

### 👥 Speaker Discovery  
- **Speaker Search**: Find speakers by name or company
- **Session Mapping**: View all sessions for any speaker
- **Professional Details**: Access speaker titles, companies, and roles

### 🎯 Advanced Filtering
- **13 Specialized Tools** for precise content discovery
- **Multi-dimensional Filtering**: By level, role, industry, topic, and more
- **Smart Categorization**: 53 areas of interest, 198 AWS services, 19 industries

### ⚡ Performance Optimized
- **Sub-second Startup**: Instant availability with MessagePack data format
- **Memory Efficient**: ~30MB footprint for complete dataset
- **Fast Queries**: <10ms response times for typical searches

## 🛠️ Available MCP Tools

### Core Discovery Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| `search_sessions` | Universal session search or complete listing | "Find all AI sessions" or "" for all sessions |
| `search_speakers` | Speaker discovery with session mapping | "Find speakers from AWS" or "" for all speakers |
| `get_session_details` | Complete session information | Get full details for session "AIM236-S" |
| `search_services` | AWS service-specific sessions | Find sessions covering "Amazon Bedrock" |

### Specialized Filters

| Tool | Categories | Count |
|------|------------|-------|
| `get_sessions_by_level` | Foundational → Distinguished (100-500) | 5 levels |
| `get_sessions_by_role` | Developer, Architect, Data Scientist, etc. | 19 roles |
| `get_sessions_by_industry` | Healthcare, Financial Services, Government, etc. | 19 industries |
| `get_sessions_by_topic` | AI, Security, Databases, Serverless, etc. | 18 topics |
| `get_sessions_by_area_of_interest` | Generative AI, DevOps, Cost Optimization, etc. | 53 areas |
| `get_sessions_by_segment` | Enterprise, Startup, Public Sector, etc. | 10 segments |
| `get_sessions_by_feature` | Hands-on, Interactive, Lecture-style, etc. | 4 formats |
| `list_categories` | Browse all available filter values | Dynamic discovery |

### Key Behaviors
- **Empty Query Magic**: `search_sessions("")` returns all 1,843 sessions
- **Speaker Discovery**: `search_speakers("")` returns all speakers (5 per page)
- **Nested Data**: Speakers include their complete session list
- **Pagination**: Cursor-based navigation for large result sets

## 📊 Dataset Overview

### Comprehensive Coverage
- **1,843 Sessions** across all re:Invent 2025 tracks
- **40+ Attributes** per session including metadata, speakers, and categorization
- **Real-time Accuracy** with official session catalog data

### Rich Categorization
- **53 Areas of Interest**: From Generative AI to Quantum Technologies
- **198 AWS Services**: Complete service coverage with session mapping  
- **19 Industries**: Vertical-specific content discovery
- **19 Job Roles**: Content tailored to professional functions
- **5 Difficulty Levels**: From foundational to distinguished expertise

### Data Quality
- **Cleaned Metadata**: Removed internal fields, normalized speaker data
- **Optimized Format**: MessagePack for 25% smaller size and faster loading
- **Structured Output**: Consistent JSON responses across all tools

## 🏗️ Architecture

### Dual Implementation
The Node.js implementation provides comprehensive functionality:

| Feature | Node.js | Status |
|---------|---------|--------|
| **MCP Tools** | 13 tools | ✅ Complete |
| **Data Format** | MessagePack | ✅ Optimized |
| **Performance** | <1s startup | ✅ Fast |
| **Tests** | 50 tests | ✅ Comprehensive |
| **Memory** | ~30MB | ✅ Efficient |

### Technical Stack
- **Protocol**: Model Context Protocol (MCP) v1.0
- **Data**: MessagePack binary format for optimal performance  
- **Architecture**: Simplified array-based processing
- **Transport**: Standard I/O (stdio) for universal compatibility

## 🎯 Use Cases

### Conference Experience Enhancement

#### **Role-Based Curation**
- **Developer Teams**: Find storage, database, and technical deep-dive sessions
- **Sales Professionals**: Discover partner programs and revenue growth strategies  
- **Executives**: Access strategic AI transformation and leadership content
- **Senior Leaders**: Locate organizational frameworks and decision models

#### **Industry-Specific Discovery**
- **Manufacturing & Industrial**: Asset lifecycle, predictive maintenance, HPC workflows
- **Energy & Utilities**: Renewable planning, industrial operations, compliance automation
- **Healthcare & Life Sciences**: Regulatory intelligence, quality management, R&D acceleration
- **Financial Services**: Risk management, compliance, customer experience transformation

#### **Learning & Development**
- **Certification Pathways**: Map sessions to AWS certification requirements
- **Skill Progression**: Build foundational → expert learning sequences
- **Team Training**: Bulk recommendations for entire departments
- **Prerequisites Mapping**: Identify required background knowledge

### Business Intelligence & Strategy

#### **Competitive Analysis**
- **Partner Ecosystem**: Track AWS partner involvement and strategic messaging
- **Technology Trends**: Forecast emerging vs mature technology adoption
- **Market Positioning**: Analyze AWS strategic priorities by session focus
- **Innovation Tracking**: Monitor new service announcements and capabilities

#### **Customer Research Integration**
- **Company Intelligence**: Research prospects' business units and pain points
- **Solution Mapping**: Align customer needs with relevant AWS sessions
- **Industry Vertical Analysis**: Match customer industries to conference content
- **ROI Benchmarking**: Extract quantified outcomes across use cases

#### **Event Planning & Operations**
- **Schedule Optimization**: Find non-conflicting sessions for multi-track attendance
- **Venue Planning**: Identify high-demand sessions requiring larger rooms
- **Content Gap Analysis**: Discover underrepresented topics or industries
- **Speaker Workload**: Track speaker participation across sessions

### Content Strategy & Marketing

#### **Thought Leadership**
- **Content Calendar**: Plan post-event content creation priorities
- **Audience Segmentation**: Develop detailed personas from session targeting
- **Campaign Messaging**: Extract key themes and value propositions
- **Innovation Labs**: Identify proof-of-concept and R&D opportunities

#### **Partnership Development**
- **Co-marketing**: Analyze joint session participation opportunities
- **Solution Integration**: Map complementary technology sessions
- **Market Expansion**: Plan geographic and vertical growth strategies
- **Customer References**: Identify success stories and case studies

### Compliance & Governance

#### **Regulatory Alignment**
- **Security Frameworks**: Map sessions to security certifications
- **Compliance Requirements**: Find sessions addressing specific regulations
- **Audit Preparation**: Locate compliance-focused recommendations
- **Risk Assessment**: Analyze security and governance session content

### AI-Powered Applications

#### **Intelligent Systems**
- **Recommendation Engines**: Build personalized session discovery systems
- **Conference Chatbots**: Power conversational event navigation
- **Learning Assistants**: Create adaptive learning path generators
- **Analytics Platforms**: Transform session data into business intelligence

## 📦 Package Information

### Node.js Package  
- **Name**: `reinvent2025mcp`
- **Registry**: [NPM](https://www.npmjs.com/package/reinvent2025mcp)
- **Runtime**: Node.js 18+
- **Dependencies**: `@modelcontextprotocol/sdk`, `@msgpack/msgpack`

## 🧪 Development

### Local Development

**Node.js**
```bash
git clone https://github.com/manu-mishra/reinvent-mcp-2025
cd reinvent-mcp-2025/npx
npm install
node src/index.js
```

### Testing
The implementation includes comprehensive test suites:

```bash
cd npx && npm test
```

### Data Pipeline
The project includes a complete data collection pipeline:

```bash
cd scrapper
python reinvent_scraper.py    # Collect session data
python data_processor.py      # Process and optimize
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Areas
- **New MCP Tools**: Additional session discovery capabilities
- **Data Enhancement**: Enriched metadata and categorization
- **Performance Optimization**: Query speed and memory improvements
- **Integration Examples**: Sample applications and use cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **GitHub Repository**: [manu-mishra/reinvent-mcp-2025](https://github.com/manu-mishra/reinvent-mcp-2025)
- **Model Context Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **AWS re:Invent 2025**: [reinvent.awsevents.com](https://reinvent.awsevents.com/)
- **Author**: [Manu Mishra](https://www.linkedin.com/in/manu-mishra/)

## 🙏 Acknowledgments

- **AWS re:Invent Team** for providing comprehensive session data
- **Anthropic** for developing the Model Context Protocol
- **MCP Community** for tools, examples, and best practices

---

<div align="center">

**Built with ❤️ for the AWS Community**

[⭐ Star this project](https://github.com/manu-mishra/reinvent-mcp-2025) • [🐛 Report Issues](https://github.com/manu-mishra/reinvent-mcp-2025/issues) • [💡 Request Features](https://github.com/manu-mishra/reinvent-mcp-2025/issues/new)

</div>
