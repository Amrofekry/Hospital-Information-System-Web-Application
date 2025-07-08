#!/usr/bin/env python3
"""
Static site generator for Flask application
Converts the Flask app to static HTML files for deployment
"""

import os
import shutil
from flask import Flask
from app import app

def build_static_site():
    """Generate static HTML files from Flask routes"""
    
    # Create build directory
    build_dir = 'dist'
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    # Copy static files
    if os.path.exists('static'):
        shutil.copytree('static', os.path.join(build_dir, 'static'))
    
    # Create a simple index.html for static deployment
    with app.app_context():
        # Generate basic HTML structure
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OM AL-MASRYEN Hospital</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">
                <h1>OM AL-MASRYEN</h1>
            </div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="container">
            <div class="welcome-section">
                <h1>Welcome to OM AL-MASRYEN</h1>
                <p>An advanced healthcare management platform for patients and doctors.</p>
                <div class="action-buttons">
                    <a href="#services" class="btn secondary-btn">Our Services</a>
                </div>
            </div>

            <div class="features-section" id="services">
                <h2>Our Services</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">📋</div>
                        <h3>Patient Registration</h3>
                        <p>Register as a new patient and manage your medical information.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🔐</div>
                        <h3>Secure Login</h3>
                        <p>Access your information securely as a patient or doctor.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">👤</div>
                        <h3>Profile Management</h3>
                        <p>View and manage your personal and medical information.</p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="footer-container">
            <div class="footer-column">
                <h3>Find Care</h3>
                <p class="clickable">Find a Doctor</p>
                <p class="clickable">Find a Location</p>
                <p class="clickable">Immediate Care</p>
                <p class="clickable">Emergency Care</p>
                <p class="clickable">Make an Appointment</p>
                <p class="clickable">Medical Services</p>
            </div>

            <div class="footer-column">
                <h3>Patient Resources</h3>
                <p class="clickable">Prepare for Your Visit</p>
                <p class="clickable">Visitor Guidelines</p>
                <p class="clickable">Patient Education</p>
                <p class="clickable">Billing & Insurance</p>
                <p class="clickable">Price Transparency</p>
                <p class="clickable">Support & Information</p>
            </div>

            <div class="footer-column">
                <h3>Discover OM AL-MASRYEN</h3>
                <p class="clickable">About OM AL-MASRYEN</p>
                <p class="clickable">Departments</p>
                <p class="clickable">Patient Stories</p>
                <p class="clickable">For Healthcare Professionals</p>
                <p class="clickable">Inclusive Excellence</p>
                <p class="clickable">Contact Media Team</p>
            </div>

            <div class="footer-column">
                <h3>Get Involved</h3>
                <p class="clickable">Donate to OM AL-MASRYEN</p>
                <p class="clickable">Work at OM AL-MASRYEN</p>
                <p class="clickable">Volunteer for OM AL-MASRYEN</p>
                <p class="clickable">Read our Publications</p>
                <p class="clickable">Your Feedback</p>
                <p class="clickable">Contact Us</p>
            </div>
        </div>

        <div class="footer-bottom">
            <p>&copy; 2025 OM AL-MASRYEN | HIPAA Notice | Privacy Notice | Nondiscrimination | Report Misconduct | We listen. We care.</p>
        </div>
    </footer>
</body>
</html>'''
        
        # Write index.html
        with open(os.path.join(build_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"Static site built successfully in '{build_dir}' directory")

if __name__ == '__main__':
    build_static_site()