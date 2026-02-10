> WEB FRONTEND LIVE LINK : https://cepv-visualizer.onrender.com/

> DESKTOP APP EXE FILE : https://drive.google.com/file/d/1603yFZSnbDfFOPfP0M2fZQkt469dVgdG/view?usp=sharing 
(DESKTOP APP READY TO RUN)

> BACKEND IS DEPLOYED ON RENDER (COLD START) : https://cepv-chemical-equipment-parameter.onrender.com 
PLEASE WAIT IF LOADING............... THANK YOU


CEPV – Chemical Equipment Parameter Visualizer

CEPV is a full-stack data analytics and visualization platform built for analyzing chemical equipment datasets using CSV files.
It provides web and desktop interfaces backed by a Django REST API, enabling users to upload datasets, visualize trends, generate reports, and manage historical analyses.

> -- Key Features
> ------> Core Functionality

Upload CSV files with chemical equipment parameters

Automatic data validation & preprocessing

Statistical summaries (averages, counts, distributions)

Interactive analytics charts

CSV preview (first 10 rows)

PDF report generation

Dataset history with re-analysis support

> --------> Web Application (React)

Modern, responsive UI built with React + Tailwind CSS

Secure authentication (login & signup)

Dashboard for upload, analytics, and reports

History page to revisit previous datasets

Clean, professional UI inspired by enterprise dashboards

> --------> Desktop Application (PyQt5)

Native cross-platform desktop app (Windows focus)

Same functionality as web dashboard

CSV upload, analytics charts (Matplotlib), previews, and PDF export

Works with deployed backend or local backend

Can be packaged into a standalone .exe

> --------> Backend (Django REST Framework)

RESTful API built with Django + DRF

Token-based authentication

CSV parsing & validation

Data aggregation and analytics

PDF generation using ReportLab

Database-agnostic (SQLite locally, PostgreSQL in production)

CORS-enabled for web & desktop clients

> --------> Tech Stack
> Frontend (Web)
React
Tailwind CSS
Axios

> Desktop
Python
PyQt5
Matplotlib
Requests

> Backend
Django
Django REST Framework
PostgreSQL / SQLite
Pandas
ReportLab
