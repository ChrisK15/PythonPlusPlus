# Formats code
echo Running black!

poetry run black src/ tests/

echo Black completed!

# Formats imports
echo Running isort!

poetry run isort src/ tests/

echo Isort completed!