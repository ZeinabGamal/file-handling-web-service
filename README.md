# Web Service for File Handling

## Overview

This Django web service is designed to handle text file uploads and perform various operations on the uploaded files. The functionalities include:

1. **File Upload:** Upload and store text files.
2. **Retrieve One Random Line:** Fetch a random line from a specific uploaded file in `text/plain`, `application/json`, or `application/xml` format.
3. **Retrieve Random Line Backwards:** Get a random line from a specific uploaded file.
4. **Longest 100 Lines:** Retrieve the 100 longest lines from all uploaded files.
5. **Longest 20 Lines of One File:** Fetch the 20 longest lines from a specific uploaded file.

## Technologies

- **Backend Framework:** Django
- **API Framework:** Django REST Framework
- **Database:** SQLite (configurable to PostgreSQL/MySQL)
- **File Storage:** Local file system (configurable to cloud storage)

## Project Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>

2. **Navigate to the Project Directory**
   ```bash
   cd <project-directory>


3. **Create and Activate a Virtual Environment**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

5. **Apply Migrations**
   ```bash
   python manage.py migrate

6. **Run the Development Server**
   ```bash
   python manage.py runserver


## API Endpoints

### File Upload
- **Endpoint:** `/upload/`
- **Method:** `POST`
- **Description:** Upload a text file. Only .txt files are accepted. If a file with the same name already exists, the upload will be rejected, and you will be prompted to change the file name. Overwriting existing files is not allowed.

### Retrieve One Random Line
- **Endpoint:** `/random-line/<str:file_name>/`
- **Method:** `GET`
- **Description:**  Retrieve a random line from the specified file. If the file name does not include the .txt extension, it will be added automatically. Handles responses in text/plain, application/json, or application/xml format based on Accept header.
- **Accept Headers:** `text/plain`, `application/json`, `application/xml`

### Retrieve Random Line Backwards
- **Endpoint:** `random-line-backwards/<str:file_name>/`
- **Method:** `GET`
- **Description:** Retrieve a random line from the specified file, reversed. If the file name does not include the .txt extension, it will be added automatically. Handles responses in text/plain, application/json, or application/xml format based on Accept header.
- **Accept Headers:** `text/plain`, `application/json`, `application/xml`

### Longest 100 Lines
- **Endpoint:** `/longest-lines/`
- **Method:** `GET`
- **Description:** Retrieve the 100 longest lines from all uploaded files.
- **Accept Headers:** `text/plain`, `application/json`, `application/xml`

### Longest 20 Lines of One File
- **Endpoint:** `/longest-lines/<str:file_name>/`
- **Method:** `GET`
- **Description:** Retrieve the 20 longest lines from the specified file. If the file name does not include the .txt extension, it will be added automatically.
- **Accept Headers:** `text/plain`, `application/json`, `application/xml`

## Architectural Design

### Models
- **UploadedFile**
  - `file`: FileField
  - `uploaded_at`: DateTimeField

### Serializers
- **UploadedFileSerializer**
  - Serializes the `UploadedFile` model.

### Views
- **FileUploadView:** Handles file uploads.
- **RandomLineView:** Returns a random line from the latest uploaded file.
- **RandomLineBackwardsView:** Returns a random line backwards.
- **Longest100LinesView:** Returns the 100 longest lines from all files.
- **Longest20LinesView:** Returns the 20 longest lines from a specific file.

### URLs
- `/upload/`
- `/random-line/<str:file_name>/`
- `/random-line-backwards/<str:file_name>/`
- `/100-longest-lines/`
- `/20-longest-lines-in-file/<str:file_name>/`


# Test Cases

## 1. File Upload

### Test Case 1.1: Valid File Upload

- **Description:** Test uploading a valid text file.
- **Steps:**
  1. Send a POST request to `/upload/` with a text file.
- **Expected Result:** Status `201 Created`.

### Test Case 1.2: Invalid File Upload

- **Description:** Test uploading a non-text file.
- **Steps:**
  1. Send a POST request to `/upload/` with a non-text file.
- **Expected Result:** Status `400 Bad Request`.

### Test Case 1.3: File Name Conflict

- **Description:** Test uploading a file with a name that already exists.
- **Steps:**
  1. Send a POST request to `/upload/` with a text file that has the same name as an existing file.
- **Expected Result:** Status `400 Bad Request` with a message indicating that the file already exists and prompting to choose a different name.

## 2. Retrieve One Random Line

### Test Case 2.1: Retrieve Random Line in `text/plain` Format

- **Description:** Retrieve a random line in `text/plain`.
- **Steps:**
  1. Send a GET request to `/random-line/<str:file_name>/` with `Accept: text/plain`.
- **Expected Result:** Status `200 OK`.

### Test Case 2.2: Retrieve Random Line in `application/json` Format

- **Description:** Retrieve a random line in `application/json`.
- **Steps:**
  1. Send a GET request to `/random-line/<str:file_name>/` with `Accept: application/json`.
- **Expected Result:** Status `200 OK`.

### Test Case 2.3: Retrieve Random Line in `application/xml` Format

- **Description:** Retrieve a random line in `application/xml`.
- **Steps:**
  1. Send a GET request to `/random-line/<str/file_name>/` with `Accept: application/xml`.
- **Expected Result:** Status `200 OK`.

### Test Case 2.4: No Files Uploaded

- **Description:** Test with no uploaded files.
- **Steps:**
  1. Send a GET request to `/random-line/<str/file_name>/`.
- **Expected Result:** Status `404 Not Found`.

## 3. Retrieve Random Line Backwards

### Test Case 3.1: Retrieve Random Line Backwards in `text/plain` Format

- **Description:** Retrieve a random line backwards in `text/plain`.
- **Steps:**
  1. Send a GET request to `/random-line-backwards/<str/file_name>/` with `Accept: text/plain`.
- **Expected Result:** Status `200 OK`.

### Test Case 3.2: Retrieve Random Line Backwards in `application/json` Format

- **Description:** Retrieve a random line backwards in `application/json`.
- **Steps:**
  1. Send a GET request to `/random-line-backwards/<str/file_name>/` with `Accept: application/json`.
- **Expected Result:** Status `200 OK`.

### Test Case 3.3: Retrieve Random Line Backwards in `application/xml` Format

- **Description:** Retrieve a random line backwards in `application/xml`.
- **Steps:**
  1. Send a GET request to `/random-line-backwards/<str/file_name>/` with `Accept: application/xml`.
- **Expected Result:** Status `200 OK`.

### Test Case 3.4: No Files Uploaded

- **Description:** Test with no uploaded files.
- **Steps:**
  1. Send a GET request to `/random-line-backwards/<str/file_name>/`.
- **Expected Result:** Status `404 Not Found`.

## 4. Retrieve Longest 100 Lines

### Test Case 4.1: Retrieve Longest 100 Lines in `text/plain` Format

- **Description:** Retrieve the 100 longest lines in `text/plain`.
- **Steps:**
  1. Send a GET request to `/100-longest-lines/` with `Accept: text/plain`.
- **Expected Result:** Status `200 OK`.

### Test Case 4.2: Retrieve Longest 100 Lines in `application/json` Format

- **Description:** Retrieve the 100 longest lines in `application/json`.
- **Steps:**
  1. Send a GET request to `/100-longest-lines/` with `Accept: application/json`.
- **Expected Result:** Status `200 OK`.

### Test Case 4.3: Retrieve Longest 100 Lines in `application/xml` Format

- **Description:** Retrieve the 100 longest lines in `application/xml`.
- **Steps:**
  1. Send a GET request to `/100-longest-lines/` with `Accept: application/xml`.
- **Expected Result:** Status `200 OK`.

### Test Case 4.4: No Files Uploaded

- **Description:** Test with no uploaded files.
- **Steps:**
  1. Send a GET request to `/100-longest-lines/`.
- **Expected Result:** Status `404 Not Found`.

## 5. Retrieve Longest 20 Lines of One File

### Test Case 5.1: Retrieve Longest 20 Lines in `text/plain` Format

- **Description:** Retrieve the 20 longest lines from a specific file in `text/plain`.
- **Steps:**
  1. Send a GET request to `/20-longest-lines-in-file/<str/file_name>/` with `Accept: text/plain`.
- **Expected Result:** Status `200 OK`.

### Test Case 5.2: Retrieve Longest 20 Lines in `application/json` Format

- **Description:** Retrieve the 20 longest lines from a specific file in `application/json`.
- **Steps:**
  1. Send a GET request to `/20-longest-lines-in-file/<str/file_name>/` with `Accept: application/json`.
- **Expected Result:** Status `200 OK`.

### Test Case 5.3: Retrieve Longest 20 Lines in `application/xml` Format

- **Description:** Retrieve the 20 longest lines from a specific file in `application/xml`.
- **Steps:**
  1. Send a GET request to `/20-longest-lines-in-file/<str/file_name>/` with `Accept: application/xml`.
- **Expected Result:** Status `200 OK`.

### Test Case 5.4: File Not Found

- **Description:** Test retrieving the longest 20 lines from a non-existent file.
- **Steps:**
  1. Send a GET request to `/20-longest-lines-in-file/<str/file_name>/`.
- **Expected Result:** Status `404 Not Found` with an error message indicating the file does not exist.
