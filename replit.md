# Replit.md

## Overview

This is a Discord bot application built with discord.py that facilitates YouTube video submissions with categorization. The bot provides an interactive interface where users can submit YouTube video links through Discord slash commands and modals, then categorize their submissions using dropdown menus. The application focuses on organizing content submissions into predefined categories: Large Streamer Content, IRL Content, and Reactions/Gameplay.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py Library**: Uses the modern discord.py library with application commands (slash commands) and UI components
- **Command System**: Implements both traditional prefix commands (`!`) and modern slash commands using `app_commands`
- **Intents Configuration**: Configured with default intents plus message content intent for comprehensive Discord API access

### User Interface Design
- **Modal-Based Input**: Uses Discord's native Modal UI component for YouTube link submission, providing a clean form-like interface
- **Interactive Selection**: Implements View-based dropdown menus for category selection, enhancing user experience over text-based commands
- **Ephemeral Responses**: Uses ephemeral messages for private user interactions during the submission process

### Data Flow Architecture
- **Two-Step Submission Process**: 
  1. YouTube link collection via modal
  2. Category selection via dropdown menu
- **Temporary Data Storage**: Passes YouTube link data between UI components using constructor parameters
- **Embedded Messaging**: Uses Discord embeds for structured and visually appealing message presentation

### Category System
- **Predefined Categories**: Three fixed content categories with associated emojis for visual identification
- **Value Mapping**: Uses simple letter codes (a, b, c) mapped to descriptive category names for efficient data handling

## External Dependencies

### Core Dependencies
- **discord.py**: Primary Discord API wrapper library for bot functionality
- **Discord API**: External service for all bot interactions, message handling, and UI components

### Discord Features Utilized
- **Application Commands**: Modern slash command system
- **UI Components**: Modals, Views, Select menus, and TextInput components
- **Message Embeds**: Rich message formatting and presentation
- **Ephemeral Messages**: Private user interactions

Note: The current implementation appears to be incomplete, as the category selection handler is cut off and there's no visible completion of the submission workflow or data persistence mechanism.