# URL Shortener Project

This project is a URL shortener service built with FastAPI and MySQL.

## Running the Project Locally

### Prerequisites
- Python 3.12 or higher
- Poetry for dependency management
- MySQL server running locally

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/devankitjuneja/url-shortner.git
   cd url-shortner
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

4. Set up the `.env` file with the following content:
   ```properties
   DB_USER=root
   DB_PASSWORD=secret
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=url_shortner
   ```

5. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn src.url_shortner.app:app --host 0.0.0.0 --port 8000
   ```

6. Access the application at `http://localhost:8000`.

## Running the Project with Docker (Recommended)

### Prerequisites
- Docker installed on your system

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/devankitjuneja/url-shortner.git
   cd url-shortner
   ```

2. Build and run the Docker containers:
   ```bash
   docker compose up
   ```

3. Access the application at `http://localhost:8000`.

### Notes
- The `docker-compose.yml` file automatically sets up the FastAPI server and MySQL database.
- Environment variables are mentioned in the `docker-compose.yml` file itself.
- You can use the API via the `/docs` endpoint for interactive documentation.

## API Endpoints
- **POST /shorten**: Create a new short URL.
- **GET /shorten/{short_code}**: Retrieve the original URL.
- **PUT /shorten/{short_code}**: Update an existing short URL.
- **DELETE /shorten/{short_code}**: Delete a short URL.
- **GET /shorten/{short_code}/stats**: Get statistics for a short URL.

Refer to the code for detailed request and response formats.