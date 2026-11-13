# BookCircle — Book Social Platform

A modular social networking web application built with **Django 5.1** where readers can catalog books, track reading shelves, share reviews and quotes, and connect with fellow readers.

## Architecture & Apps
- **`accounts`**: Custom email-based authentication (`CustomUser`), automatic user profiles (`Profile`), avatar uploads, and author verification status.
- **`books`**: Catalog of `Book`, `Author`, and `Genre` with search/genre filtering and personal `ReadingShelf` tracking (`Want to Read`, `Currently Reading`, `Finished`).
- **`posts`**: Social feed supporting book reviews, quotes, reading thoughts, star ratings (1–5), and photo uploads.
- **`interactions`**: Social engagement features including `Like`, `Comment`, `Follow` (with self-follow validation), reader discovery, and public profiles.

## Setup & Local Execution

1. **Activate virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt