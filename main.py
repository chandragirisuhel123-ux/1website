import os
from app import create_app

app = create_app()

# 👇 THIS LINE IS IMPORTANT FOR GUNICORN
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
