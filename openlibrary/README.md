<<<<<<< HEAD
# Open Library Management System

[![Version](https://img.shields.io/badge/version-19.0.1.0.0-blue.svg)](https://odoo.com)
[![License](https://img.shields.io/badge/license-LGPL--3-blue.svg)](LICENSE)
[![Odoo](https://img.shields.io/badge/Odoo-19.0-purple.svg)](https://odoo.com)

Complete library management solution for Odoo 19 Community and Enterprise editions.

## 📋 Overview

Open Library is a comprehensive library management module that helps libraries, educational institutions, and organizations manage their book collections, members, and lending operations efficiently. The module provides a complete workflow from book acquisition to member management and lending tracking.

## ✨ Key Features

### 📚 Book Management
- **Multi-Library Support**: Manage multiple library branches from a single installation
- **Multi-Repository Support**: Organize books across different repositories within each library
- **Book Editions**: Track different editions, publishers, and publication dates
- **Author Management**: Maintain author biographies, nationalities, and birth/death dates
- **Publisher Management**: Keep track of publishers and their information
- **Tags & Genres**: Categorize books using customizable tags
- **Book Copies**: Manage individual book copies with unique codes

### 👥 Member Management
- **Member Registration**: Register library members with personal information
- **Membership Management**: Track memberships across multiple libraries
- **Member Status**: Active, inactive, or suspended member statuses
- **Contact Integration**: Seamless integration with Odoo's partner system

### 🔄 Lending Operations
- **Book Lending**: Simple and intuitive book borrowing process
- **Due Date Calculation**: Automatic due date calculation based on member's allowed days
- **Return Processing**: Easy book return 
- **Late Management**: Configurable late thresholds (warning, suspicious, dangerous)
- **Lending History**: Complete historical record of all transactions
- **Status Tracking**: Real-time status updates (Lent, Delay, Suspicious, Dangerous)

### 📊 Views & Dashboards
- **List View**: Tabular view for quick browsing
- **Kanban View**: Visual card-based view for book status
- **Calendar View**: Visual representation of lending periods
- **Form View**: Detailed forms for data entry
- **Search Filters**: Advanced search and filtering capabilities

### 🔧 Technical Features
- **Multi-Company Support**: Full compatibility with Odoo's multi-company architecture
- **Security Groups**: Granular access control with user groups
- **Activity Tracking**: Integration with Odoo's mail and activity mixin
- **Reporting**: Comprehensive reports and statistics
- **Configurable Settings**: System parameters for late fee thresholds

## 🚀 Installation

### Prerequisites
- Odoo 19.0 (Community or Enterprise)
- Python 3.10 or higher

### Installation Steps

1. **Copy the module to your addons directory**
   ```bash
   cp -r openlibrary /path/to/odoo/addons/
