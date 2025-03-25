# Navigate to the script directory
cd "$(dirname "$0")"

# Check if virtual environment is already active
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo "🔄 Activating virtual environment..."
  source venv/bin/activate

fi

# Run the tool
python main.py