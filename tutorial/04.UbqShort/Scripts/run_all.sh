for script in 1ubq*.py; do
  echo "Running $script..."
  python "$script"

  echo "Finished $script. Waiting a few seconds..."
  sleep 15
done

echo "All scripts completed."
