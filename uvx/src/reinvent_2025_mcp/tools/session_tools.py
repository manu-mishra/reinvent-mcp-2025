import json
from mcp.types import Tool
from reinvent_2025_mcp.services.session_service import SessionService

def create_session_tools(sessions):
    service = SessionService(sessions)
    
    return {
        "search_sessions": {
            "name": "search_sessions",
            "description": "Search sessions by keywords or get all sessions. Use empty string to list all 1,843 sessions. Searches across title, abstract, topics, services, industries, roles, and areas of interest.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keywords for fuzzy matching. Use empty string \"\" to return all sessions."},
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["query"]
            },
            "handler": lambda args: service.search_sessions(args.get("query"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "search_services": {
            "name": "search_services", 
            "description": "Find AWS services by name/abbreviation from 198 available services",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keywords for fuzzy matching AWS service names"},
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 50},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["query"]
            },
            "handler": lambda args: service.search_services(args.get("query"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_session_details": {
            "name": "get_session_details",
            "description": "Get complete session information including speakers, abstract, topics, services, and all metadata. Use session codes from search results (e.g., 'AIM236-S', 'DVT222-S').", 
            "inputSchema": {
                "type": "object",
                "properties": {
                    "session_code": {"type": "string", "description": "Session code (e.g., \"DVT222-S\")", "pattern": "^[A-Z]{3}[0-9]{3}(-[A-Z])?$"}
                },
                "required": ["session_code"]
            },
            "handler": lambda args: service.get_session_details(args.get("session_code"))
        },
        
        "list_categories": {
            "name": "list_categories",
            "description": "Browse available values in any category with distribution stats. Use this to discover all supported values for topics, services, industries, roles, levels, segments, areas_of_interest, features, or types before using other filter tools.",
            "inputSchema": {
                "type": "object", 
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["topics", "services", "industries", "roles", "levels", "segments", "areas_of_interest", "features", "types"],
                        "description": "Category type to list - returns all available values with session counts and percentages"
                    }
                },
                "required": ["category"]
            },
            "handler": lambda args: service.list_categories(args.get("category"))
        },
        
        "get_sessions_by_service": {
            "name": "get_sessions_by_service",
            "description": "Find all sessions for a specific AWS service",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "service_name": {"type": "string", "description": "AWS service name (exact match required)"},
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["service_name"]
            },
            "handler": lambda args: service.get_sessions_by_service(args.get("service_name"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_sessions_by_level": {
            "name": "get_sessions_by_level", 
            "description": "Filter sessions by difficulty level. Supported levels: 100 (Foundational), 200 (Intermediate), 300 (Advanced), 400 (Expert), 500 (Distinguished)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "enum": ["100", "200", "300", "400", "500"],
                        "description": "Session difficulty level: 100–Foundational, 200–Intermediate, 300–Advanced, 400–Expert, 500–Distinguished"
                    },
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["level"]
            },
            "handler": lambda args: service.get_sessions_by_level(args.get("level"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_sessions_by_role": {
            "name": "get_sessions_by_role",
            "description": "Find sessions targeted at specific job functions. Supported roles: Developer / Engineer, Solution / Systems Architect, IT Professional / Technical Manager, DevOps Engineer, IT Executive, Business Executive, Data Engineer, Data Scientist, Cloud Security Specialist, System Administrator, IT Administrator, Advisor / Consultant, Tech Explorer, Academic / Researcher, Entrepreneur (Founder/Co-Founder), Sales / Marketing, Student, Venture Capitalist, Press / Media Analyst.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "enum": ["Developer / Engineer", "Solution / Systems Architect", "IT Professional / Technical Manager", "DevOps Engineer", "IT Executive", "Business Executive", "Data Engineer", "Data Scientist", "Cloud Security Specialist", "System Administrator", "IT Administrator", "Advisor / Consultant", "Tech Explorer", "Academic / Researcher", "Entrepreneur (Founder/Co-Founder)", "Sales / Marketing", "Student", "Venture Capitalist", "Press / Media Analyst"],
                        "description": "Target job function - use list_categories with \"roles\" to see all available options"
                    },
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["role"]
            },
            "handler": lambda args: service.get_sessions_by_role(args.get("role"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_sessions_by_industry": {
            "name": "get_sessions_by_industry",
            "description": "Find sessions relevant to specific industry verticals. Supported industries: Financial Services, Software & Internet, Healthcare & Life Sciences, Manufacturing & Industrial, Retail & Consumer Goods, Government, Media & Entertainment, Advertising & Marketing, Automotive, Telecommunications, Energy & Utilities, Games, Travel & Hospitality, Professional Services, Education, Nonprofit, Aerospace & Satellite, Agriculture, Sports.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "industry": {
                        "type": "string", 
                        "enum": ["Financial Services", "Software & Internet", "Healthcare & Life Sciences", "Manufacturing & Industrial", "Retail & Consumer Goods", "Government", "Media & Entertainment", "Advertising & Marketing", "Automotive", "Telecommunications", "Energy & Utilities", "Games", "Travel & Hospitality", "Professional Services", "Education", "Nonprofit", "Aerospace & Satellite", "Agriculture", "Sports"],
                        "description": "Industry vertical - use list_categories with \"industries\" to see all available options"
                    },
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["industry"]
            },
            "handler": lambda args: service.get_sessions_by_industry(args.get("industry"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_sessions_by_segment": {
            "name": "get_sessions_by_segment",
            "description": "Find sessions for specific business segments. Supported segments: Enterprise, Developer Community, Independent Software Vendor, Digital Native Business, Small & Medium Business, Startup, Partner Enablement, Public Sector, New to AWS, Senior Leaders.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "segment": {
                        "type": "string",
                        "enum": ["Enterprise", "Developer Community", "Independent Software Vendor", "Digital Native Business", "Small & Medium Business", "Startup", "Partner Enablement", "Public Sector", "New to AWS", "Senior Leaders"],
                        "description": "Business segment - use list_categories with \"segments\" to see all available options"
                    },
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["segment"]
            },
            "handler": lambda args: service.get_sessions_by_segment(args.get("segment"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_sessions_by_feature": {
            "name": "get_sessions_by_feature",
            "description": "Find sessions by format/feature type. Supported features: Interactive, Lecture-style, Hands-on, AWS Partners",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "feature": {
                        "type": "string",
                        "enum": ["Interactive", "Lecture-style", "Hands-on", "AWS Partners"],
                        "description": "Session format/feature type - use list_categories with \"features\" to see all available options"
                    },
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["feature"]
            },
            "handler": lambda args: service.get_sessions_by_feature(args.get("feature"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_sessions_by_topic": {
            "name": "get_sessions_by_topic",
            "description": "Find sessions by technical domain. Supported topics: Artificial Intelligence, Migration & Modernization, Architecture, Cloud Operations, Security & Identity, Developer Tools, Serverless & Containers, Industry Solutions, Analytics, Business Applications, Compute, Databases, Storage, Application Integration, Networking & Content Delivery, Hybrid Cloud & Multicloud, Open Source, End-User Computing.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "enum": ["Artificial Intelligence", "Migration & Modernization", "Architecture", "Cloud Operations", "Security & Identity", "Developer Tools", "Serverless & Containers", "Industry Solutions", "Analytics", "Business Applications", "Compute", "Databases", "Storage", "Application Integration", "Networking & Content Delivery", "Hybrid Cloud & Multicloud", "Open Source", "End-User Computing"],
                        "description": "Technical domain - use list_categories with \"topics\" to see all available options"
                    },
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["topic"]
            },
            "handler": lambda args: service.get_sessions_by_topic(args.get("topic"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "get_sessions_by_area_of_interest": {
            "name": "get_sessions_by_area_of_interest",
            "description": "Find sessions by specific interest areas. All 53 supported areas: Generative AI, Agentic AI, Innovation & Transformation, Cost Optimization, DevOps, Automation, Machine Learning, Serverless, Resilience, Management & Governance, Monitoring & Observability, Application Security, Data Protection, Containers, Event-Driven Architecture, Governance Risk & Compliance, Kubernetes, Lambda-Based Applications, SaaS, Business Intelligence, Global Infrastructure, Network & Infrastructure Security, Well-Architected Framework, DevSecOps, Disaster Response & Recovery, Threat Detection & Incident Response, Responsible AI, Training & Certification, Identity & Access Management, Customer Enablement, Open Data, Edge Computing, Culture of Security, Microsoft & .NET, Front-End Web & Mobile, Digital Sovereignty, Tech for Impact, VMware, Learning from Amazon, SAP, Internet of Things, Quantum Technologies, Sustainability, Blockchain, Threat Intelligence, Zero Trust, Oracle, Cryptography and Post-Quantum, Inclusion, Robotics, Privacy, Workforce Development.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "area_of_interest": {
                        "type": "string",
                        "enum": ["Generative AI", "Agentic AI", "Innovation & Transformation", "Cost Optimization", "DevOps", "Automation", "Machine Learning", "Serverless", "Resilience", "Management & Governance", "Monitoring & Observability", "Application Security", "Data Protection", "Containers", "Event-Driven Architecture", "Governance, Risk & Compliance", "Kubernetes", "Lambda-Based Applications", "SaaS", "Business Intelligence", "Global Infrastructure", "Network & Infrastructure Security", "Well-Architected Framework", "DevSecOps", "Disaster Response & Recovery", "Threat Detection & Incident Response", "Responsible AI", "Training & Certification", "Identity & Access Management", "Customer Enablement", "Open Data", "Edge Computing", "Culture of Security", "Microsoft & .NET", "Front-End Web & Mobile", "Digital Sovereignty", "Tech for Impact", "VMware", "Learning from Amazon", "SAP", "Internet of Things", "Quantum Technologies", "Sustainability", "Blockchain", "Threat Intelligence", "Zero Trust", "Oracle", "Cryptography and Post-Quantum", "Inclusion", "Robotics", "Privacy", "Workforce Development"],
                        "description": "Area of interest - use list_categories with \"areas_of_interest\" to see all available options"
                    },
                    "limit": {"type": "number", "description": "Number of results per page", "default": 20, "minimum": 1, "maximum": 100},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["area_of_interest"]
            },
            "handler": lambda args: service.get_sessions_by_area_of_interest(args.get("area_of_interest"), args.get("limit", 20), args.get("cursor", 0))
        },
        
        "search_speakers": {
            "name": "search_speakers",
            "description": "Search speakers by name or get all speakers. Returns speaker details with their sessions. Use empty string to list all speakers (5 per page).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "speaker_name": {"type": "string", "description": "Speaker name for search. Use empty string \"\" to return all speakers."},
                    "limit": {"type": "number", "description": "Number of speakers per page", "default": 5, "minimum": 1, "maximum": 20},
                    "cursor": {"type": "string", "description": "Pagination cursor for next page"}
                },
                "required": ["speaker_name"]
            },
            "handler": lambda args: service.search_speakers(args.get("speaker_name"), args.get("limit", 5), args.get("cursor", 0))
        }
    }
