from app import app
import os

# Get the port from environment variables or use the default port 5000
PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
