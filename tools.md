# MCP Server Tools for AWS re:Invent 2025

## Tool Summary

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `search_sessions` | Search sessions by keywords or list all sessions | query, limit, cursor | Minimal session info (code, title, abstract) |
| `search_services` | Find AWS services by name/abbreviation | query, limit, cursor | Service names with session counts |
| `get_session_details` | Get complete session information | session_code | Full session object with all metadata |
| `list_categories` | Browse available category values | category | Category values with counts/percentages |
| `get_sessions_by_service` | Find sessions for specific AWS service | service_name, limit, cursor | Minimal session info |
| `get_sessions_by_level` | Filter sessions by difficulty level | level, limit, cursor | Minimal session info |
| `get_sessions_by_role` | Find sessions for specific job functions | role, limit, cursor | Minimal session info |
| `get_sessions_by_industry` | Find sessions for industry verticals | industry, limit, cursor | Minimal session info |
| `get_sessions_by_segment` | Find sessions for business segments | segment, limit, cursor | Minimal session info |
| `get_sessions_by_feature` | Find sessions by format/feature type | feature, limit, cursor | Minimal session info |
| `get_sessions_by_topic` | Find sessions by technical domain | topic, limit, cursor | Minimal session info |
| `get_sessions_by_area_of_interest` | Find sessions by interest areas | area_of_interest, limit, cursor | Minimal session info |
| `search_speakers` | Search speakers by name or list all speakers | speaker_name, limit, cursor | Speaker details with nested sessions |

## Overview

This MCP server provides access to the complete AWS re:Invent 2025 session catalog with 1,843 sessions across comprehensive categorization dimensions. The server enables intelligent session discovery through fuzzy search, filtering, detailed metadata access, and speaker discovery.

## Key Features

### Empty Query Behavior
- **`search_sessions`**: Empty string returns all 1,843 sessions (paginated)
- **`search_speakers`**: Empty string returns all speakers (5 per page) with their sessions

### Speaker Discovery
The `search_speakers` tool returns speaker details with nested session information:
```json
{
  "speakers": [
    {
      "name": "John Doe",
      "jobTitle": "Senior Engineer",
      "company": "AWS",
      "role": "Speaker",
      "sessions": [
        {"code": "AIM236-S", "title": "AI Session Title"},
        {"code": "DVT222-S", "title": "Another Session"}
      ]
    }
  ],
  "total": 150,
  "hasMore": true,
  "nextCursor": "5"
}
```

## Dataset Attributes

**Areas of Interest (53 categories)**: Generative AI, Agentic AI, Innovation & Transformation, Cost Optimization, DevOps, Automation, Machine Learning, Serverless, Resilience, Management & Governance, Monitoring & Observability, Application Security, Data Protection, Containers, Event-Driven Architecture, Governance Risk & Compliance, Kubernetes, Lambda-Based Applications, SaaS, Business Intelligence, Global Infrastructure, Network & Infrastructure Security, Well-Architected Framework, DevSecOps, Disaster Response & Recovery, Threat Detection & Incident Response, Responsible AI, Training & Certification, Identity & Access Management, Customer Enablement, Open Data, Edge Computing, Culture of Security, Microsoft & .NET, Front-End Web & Mobile, Digital Sovereignty, Tech for Impact, VMware, Learning from Amazon, SAP, Internet of Things, Quantum Technologies, Sustainability, Blockchain, Threat Intelligence, Zero Trust, Oracle, Cryptography and Post-Quantum, Inclusion, Robotics, Privacy, Workforce Development

**Features (4 types)**: Interactive, Lecture-style, Hands-on, AWS Partners

**Industries (20 verticals)**: Financial Services, Software & Internet, Healthcare & Life Sciences, Manufacturing & Industrial, Retail & Consumer Goods, Government, Media & Entertainment, Advertising & Marketing, Automotive, Telecommunications, Energy & Utilities, Games, Travel & Hospitality, Professional Services, Education, Nonprofit, Aerospace & Satellite, Agriculture, Sports

**Levels (5 difficulty tiers)**: 
- 100 – Foundational (3.96%): Introductory content
- 200 – Intermediate (21.32%): Some prior knowledge assumed  
- 300 – Advanced (57.35%): Deep technical content, most common
- 400 – Expert (16.44%): Specialized implementations
- 500 – Distinguished (0.92%): Cutting-edge research

**Roles (19 job functions)**: Developer/Engineer, Solution/Systems Architect, IT Professional/Technical Manager, DevOps Engineer, IT Executive, Business Executive, Data Engineer, Data Scientist, Cloud Security Specialist, System Administrator, IT Administrator, Advisor/Consultant, Tech Explorer, Academic/Researcher, Entrepreneur (Founder/Co-Founder), Sales/Marketing, Student, Venture Capitalist, Press/Media Analyst

**Segments (11 business types)**: Enterprise, Developer Community, Independent Software Vendor, Digital Native Business, Small & Medium Business, Startup, Partner Enablement, Public Sector, New to AWS, Senior Leaders

**Services (198 AWS services)**: Top services by session count - Amazon Bedrock (19.64%), Amazon EC2 (7.76%), Amazon SageMaker (5.91%), Amazon EKS (5.37%), Amazon SageMaker AI (5.32%), Amazon S3 (5.15%), AWS Lambda (4.23%), Amazon CloudWatch (3.53%), Amazon Q Developer (3.15%), Amazon Q (2.77%), Amazon Nova (2.71%), Amazon ECS (2.6%), plus 186 additional services

**Topics (18 technical domains)**: Artificial Intelligence, Migration & Modernization, Architecture, Cloud Operations, Security & Identity, Developer Tools, Serverless & Containers, Industry Solutions, Analytics, Business Applications, Compute, Databases, Storage, Application Integration, Networking & Content Delivery, Hybrid Cloud & Multicloud, Open Source, End-User Computing

## Tool Definitions

### 1. search_sessions
**Description**: Fuzzy search across all session content (title, abstract, topics, services, etc.)
**Use when**: User asks about specific technologies, concepts, or keywords
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "search_sessions",
  "description": "Fuzzy search across all session content (title, abstract, topics, services, etc.)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search keywords for fuzzy matching across session content"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["query"]
  }
}
```

### 2. search_services  
**Description**: Find AWS services by name/abbreviation from 198 available services
**Use when**: User wants to discover services or needs exact service names

```json
{
  "name": "search_services",
  "description": "Find AWS services by name/abbreviation from 198 available services",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search keywords for fuzzy matching AWS service names"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 50
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["query"]
  }
}
```

### 3. get_session_details
**Description**: Get complete session information by session code
**Use when**: User has specific session code or wants full details including speakers

```json
{
  "name": "get_session_details",
  "description": "Get complete session information by session code",
  "inputSchema": {
    "type": "object",
    "properties": {
      "session_code": {
        "type": "string",
        "description": "Session code (e.g., 'DVT222-S')",
        "pattern": "^[A-Z]{3}[0-9]{3}(-[A-Z])?$"
      }
    },
    "required": ["session_code"]
  }
}
```

### 4. list_categories
**Description**: Browse available values in any category with distribution stats
**Use when**: User wants to explore options or see session distribution

```json
{
  "name": "list_categories",
  "description": "Browse available values in any category with distribution stats",
  "inputSchema": {
    "type": "object",
    "properties": {
      "category": {
        "type": "string",
        "enum": ["topics", "services", "industries", "roles", "levels", "segments", "areas_of_interest", "features", "types"],
        "description": "Category type to list"
      }
    },
    "required": ["category"]
  }
}
```

### 5. get_sessions_by_service
**Description**: Find all sessions for a specific AWS service
**Use when**: User wants comprehensive coverage of one service
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_service",
  "description": "Find all sessions for a specific AWS service",
  "inputSchema": {
    "type": "object",
    "properties": {
      "service_name": {
        "type": "string",
        "description": "AWS service name (exact match required)"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["service_name"]
  }
}
```

### 6. get_sessions_by_level
**Description**: Filter sessions by difficulty (100-Foundational to 500-Distinguished)
**Use when**: User wants skill-appropriate content
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_level",
  "description": "Filter sessions by difficulty level",
  "inputSchema": {
    "type": "object",
    "properties": {
      "level": {
        "type": "string",
        "enum": ["100", "200", "300", "400", "500"],
        "description": "Session difficulty level: 100-Foundational, 200-Intermediate, 300-Advanced, 400-Expert, 500-Distinguished"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["level"]
  }
}
```

### 7. get_sessions_by_role
**Description**: Find sessions targeted at specific job functions
**Use when**: User wants role-appropriate content
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_role",
  "description": "Find sessions targeted at specific job functions",
  "inputSchema": {
    "type": "object",
    "properties": {
      "role": {
        "type": "string",
        "enum": ["Developer / Engineer", "Solution / Systems Architect", "IT Professional / Technical Manager", "DevOps Engineer", "IT Executive", "Business Executive", "Data Engineer", "Data Scientist", "Cloud Security Specialist", "System Administrator", "IT Administrator", "Advisor / Consultant", "Tech Explorer", "Academic / Researcher", "Entrepreneur (Founder/Co-Founder)", "Sales / Marketing", "Student", "Venture Capitalist", "Press / Media Analyst"],
        "description": "Target job function"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["role"]
  }
}
```

### 8. get_sessions_by_industry
**Description**: Find sessions relevant to specific industry verticals
**Use when**: User wants industry-specific content
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_industry",
  "description": "Find sessions relevant to specific industry verticals",
  "inputSchema": {
    "type": "object",
    "properties": {
      "industry": {
        "type": "string",
        "enum": ["Financial Services", "Software & Internet", "Healthcare & Life Sciences", "Manufacturing & Industrial", "Retail & Consumer Goods", "Government", "Media & Entertainment", "Advertising & Marketing", "Automotive", "Telecommunications", "Energy & Utilities", "Games", "Travel & Hospitality", "Professional Services", "Education", "Nonprofit", "Aerospace & Satellite", "Agriculture", "Sports"],
        "description": "Industry vertical"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["industry"]
  }
}
```

### 9. get_sessions_by_segment
**Description**: Find sessions for specific business segments
**Use when**: User wants segment-appropriate content
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_segment",
  "description": "Find sessions for specific business segments",
  "inputSchema": {
    "type": "object",
    "properties": {
      "segment": {
        "type": "string",
        "enum": ["Enterprise", "Developer Community", "Independent Software Vendor", "Digital Native Business", "Small & Medium Business", "Startup", "Partner Enablement", "Public Sector", "New to AWS", "Senior Leaders"],
        "description": "Business segment"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["segment"]
  }
}
```

### 10. get_sessions_by_feature
**Description**: Find sessions by format/feature type
**Use when**: User wants specific session formats
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_feature",
  "description": "Find sessions by format/feature type",
  "inputSchema": {
    "type": "object",
    "properties": {
      "feature": {
        "type": "string",
        "enum": ["Interactive", "Lecture-style", "Hands-on", "AWS Partners"],
        "description": "Session format/feature type"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["feature"]
  }
}
```

### 11. get_sessions_by_topic
**Description**: Find sessions by technical domain
**Use when**: User wants content in specific technical areas
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_topic",
  "description": "Find sessions by technical domain",
  "inputSchema": {
    "type": "object",
    "properties": {
      "topic": {
        "type": "string",
        "enum": ["Artificial Intelligence", "Migration & Modernization", "Architecture", "Cloud Operations", "Security & Identity", "Developer Tools", "Serverless & Containers", "Industry Solutions", "Analytics", "Business Applications", "Compute", "Databases", "Storage", "Application Integration", "Networking & Content Delivery", "Hybrid Cloud & Multicloud", "Open Source", "End-User Computing"],
        "description": "Technical domain"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["topic"]
  }
}
```

### 12. get_sessions_by_area_of_interest
**Description**: Find sessions by specific interest areas
**Use when**: User wants content in specialized interest areas
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "get_sessions_by_area_of_interest",
  "description": "Find sessions by specific interest areas",
  "inputSchema": {
    "type": "object",
    "properties": {
      "area_of_interest": {
        "type": "string",
        "enum": ["Generative AI", "Agentic AI", "Innovation & Transformation", "Cost Optimization", "DevOps", "Automation", "Machine Learning", "Serverless", "Resilience", "Management & Governance", "Monitoring & Observability", "Application Security", "Data Protection", "Containers", "Event-Driven Architecture", "Governance, Risk & Compliance", "Kubernetes", "Lambda-Based Applications", "SaaS", "Business Intelligence", "Global Infrastructure", "Network & Infrastructure Security", "Well-Architected Framework", "DevSecOps", "Disaster Response & Recovery", "Threat Detection & Incident Response", "Responsible AI", "Training & Certification", "Identity & Access Management", "Customer Enablement", "Open Data", "Edge Computing", "Culture of Security", "Microsoft & .NET", "Front-End Web & Mobile", "Digital Sovereignty", "Tech for Impact", "VMware", "Learning from Amazon", "SAP", "Internet of Things", "Quantum Technologies", "Sustainability", "Blockchain", "Threat Intelligence", "Zero Trust", "Oracle", "Cryptography and Post-Quantum", "Inclusion", "Robotics", "Privacy", "Workforce Development"],
        "description": "Area of interest"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["area_of_interest"]
  }
}
```

### 13. search_sessions_by_speaker
**Description**: Find sessions by speaker name using fuzzy matching
**Use when**: User wants to find sessions by specific speakers or presenters
**Returns**: Minimal session info (code, title, abstract) - use get_session_details for full info

```json
{
  "name": "search_sessions_by_speaker",
  "description": "Find sessions by speaker name using fuzzy matching",
  "inputSchema": {
    "type": "object",
    "properties": {
      "speaker_name": {
        "type": "string",
        "description": "Speaker name or partial name for fuzzy matching"
      },
      "limit": {
        "type": "number",
        "description": "Number of results per page",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      },
      "cursor": {
        "type": "string",
        "description": "Pagination cursor for next page"
      }
    },
    "required": ["speaker_name"]
  }
}
```
