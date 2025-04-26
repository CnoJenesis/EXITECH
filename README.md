# EXITECH - Exit Management System

A web application for managing student exits in a school environment using RFID.

## Deployment Instructions for Vercel

### Prerequisites

1. A GitHub account
2. A Vercel account (sign up at https://vercel.com)
3. MySQL database (You can use PlanetScale, AWS RDS, or any MySQL-compatible database service)

### Steps to Deploy

1. Push this repository to GitHub:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/exitech.git
   git push -u origin main
   ```

2. Log in to your Vercel account and import your GitHub repository.

3. Configure environment variables:
   - In the Vercel dashboard, go to your project settings.
   - Navigate to the "Environment Variables" section.
   - Add the following environment variables with your database credentials:
     - `MYSQL_HOST`
     - `MYSQL_USER`
     - `MYSQL_PASSWORD`
     - `MYSQL_DB`
     - `SECRET_KEY`

4. Deploy your application.

5. Note: Socket.IO functionality will be limited in serverless environments. For full real-time functionality, consider using a traditional hosting service like Heroku, DigitalOcean, or Railway.

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`

## Features

- RFID-based student exit tracking
- Real-time monitoring of student exits
- Administrative dashboard
- Comprehensive student management
- Class schedule management 