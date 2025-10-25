# Project Refactoring: Migrating to MongoDB Cloud & Deploying to Vercel

## Objective
Refactor the application to store data in an external MongoDB Cloud database and deploy successfully to Vercel cloud platform.

## Steps Taken

### 1. MongoDB Account Setup
- Created a MongoDB Cloud account
- Set up a new cluster in MongoDB Atlas
- Created a new database and collection
- Generated connection string with proper credentials

### 2. Code Implementation
- Provided the MongoDB API connection details to GitHub Copilot in VS Code
- AI assistant generated the database connection code
- Implemented MongoDB data models and schemas
- Updated CRUD operations to work with MongoDB
- Used AI assistance for dependencies installation

<!-- 这里加一个空行，确保后续内容正常显示 -->

### 3. Vercel Deployment Setup
- Created a Vercel account and connected GitHub repository
- Configured project settings for deployment
- Set up environment variables in Vercel dashboard
- Resolved build failures related to missing environment variables
- Used AI assistance to properly configure deployment settings

## Challenges Faced

### 1. Missing Dependencies Error
- **Problem**: Application failed to start due to missing MongoDB driver
- **Error Message**: `Cannot find module 'mongodb'` or similar
- **Root Cause**: MongoDB package not installed in project dependencies

### 2. Connection Issues
- **Problem**: Initial connection failures to MongoDB Cloud
- **Possible Causes**:
  - Incorrect connection string
  - IP not whitelisted in MongoDB Atlas
  - Network connectivity issues

### 3. Vercel Build Failures
- **Problem**: Deployment failed due to missing environment variables
- **Error Message**: Build process failing during environment configuration
- **Root Cause**: MongoDB connection string and other secrets not configured in Vercel
- **Solution**: Used AI guidance to properly set up environment variables in Vercel dashboard

## Solutions Implemented

### 1. Dependency Resolution
- Asked AI assistant for correct installation commands
- Verified package.json included required dependencies
- Ran `npm install` to install missing packages

### 2. Connection Troubleshooting
- Double-checked connection string format
- Added IP address to MongoDB Atlas whitelist
- Implemented proper error handling for connection issues

### 3. Vercel Environment Configuration
- Added all required environment variables in Vercel project settings
- Configured MongoDB connection string as secret variable
- Set up proper build commands and output directory
- Verified environment variables were accessible during build process