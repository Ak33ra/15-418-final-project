#!/bin/bash

# Script to export all .nsys-rep files to SQLite format

# Path to nsys executable
NSYS="/Applications/NVIDIA Nsight Systems.app/Contents/target-linux-x64/nsys"

# Check if nsys exists
if [ ! -f "$NSYS" ]; then
    echo "Error: nsys not found at $NSYS"
    echo "Please check your NVIDIA Nsight Systems installation"
    exit 1
fi

echo "Found nsys at: $NSYS"
echo ""
echo "Exporting all .nsys-rep files to SQLite format..."
echo "=================================================="
echo ""

# Counter for progress
count=0
total=$(find out/nsys -name "*.nsys-rep" | wc -l | tr -d ' ')

echo "Found $total .nsys-rep files to export"
echo ""

# Loop through all .nsys-rep files
for rep in out/nsys/*/*.nsys-rep; do
    if [ -f "$rep" ]; then
        count=$((count + 1))

        # Get directory and base filename
        dir=$(dirname "$rep")
        base=$(basename "$rep" .nsys-rep)
        output="$dir/$base.sqlite"

        echo "[$count/$total] Exporting: $rep"
        echo "         Output: $output"

        # Run the export
        "$NSYS" stats --report sqlite --output "$output" "$rep"

        if [ $? -eq 0 ]; then
            echo "         ✓ Success!"
        else
            echo "         ✗ Failed!"
        fi
        echo ""
    fi
done

echo "=================================================="
echo "Export complete! Exported $count files."
echo ""
echo "SQLite files are located in the same directories as .nsys-rep files"
echo "You can now run the nsys_analysis.ipynb notebook!"
