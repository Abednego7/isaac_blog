# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create uploads directory if it doesn't exist
mkdir -p uploads/posts