# Overview

MedEvidence is an AI-powered medical search application that helps healthcare professionals find evidence-based medical literature. The application combines parallel.ai search capabilities with OpenAI's language models to provide comprehensive medical literature search with intelligent summaries and credibility assessments. It serves as a clone of OpenEvidence, focusing on delivering peer-reviewed medical content with clinical context and professional-grade search functionality.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-rendered architecture with Flask templates and Bootstrap 5 for responsive design. The frontend consists of:

- **Template Structure**: Base template with inheritance pattern for consistent layout and navigation
- **UI Framework**: Bootstrap 5 with custom medical-themed CSS variables and styling
- **Interactive Elements**: Vanilla JavaScript for search enhancements, form validation, and UI interactions
- **Design System**: Medical-themed color palette with consistent spacing, typography, and component styling

## Backend Architecture
Built on Flask with a service-oriented architecture pattern:

- **Main Application**: Flask app with route handlers for search functionality and page rendering
- **Service Layer**: Separated business logic into dedicated service classes for external API integrations
- **Error Handling**: Comprehensive logging and user-friendly error messages with flash messaging
- **Session Management**: Flask sessions with configurable secret key for user state management

## Search Processing Pipeline
The application implements a multi-stage search enhancement process:

1. **Query Enhancement**: Medical context is added to user queries to improve search relevance
2. **Parallel Search**: Multiple targeted queries are executed against parallel.ai's medical literature database
3. **AI Enhancement**: OpenAI processes search results to generate medical summaries and credibility scores
4. **Result Presentation**: Enhanced results are formatted with clinical context and professional medical language

## Configuration Management
Environment-based configuration for API keys and sensitive data:

- **API Keys**: Stored in environment variables for both OpenAI and Parallel.ai services
- **Session Security**: Configurable session secret key with fallback default
- **Logging**: Debug-level logging configured for development and troubleshooting

# External Dependencies

## AI and Search Services
- **OpenAI API**: Used for medical content summarization and credibility assessment with GPT-5 model
- **Parallel.ai Search API**: Primary search engine for accessing peer-reviewed medical literature and clinical studies

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Feather Icons**: Lightweight icon library for consistent iconography throughout the interface

## Python Framework and Libraries
- **Flask**: Web framework for routing, templating, and request handling
- **OpenAI Python Client**: Official client library for OpenAI API integration
- **Requests**: HTTP library for making API calls to parallel.ai search service

## Development and Deployment
- **Python Logging**: Built-in logging module for debugging and monitoring
- **Environment Variables**: Used for configuration management and API key security