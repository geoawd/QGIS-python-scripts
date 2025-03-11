import os
import subprocess
import sys
import datetime

def validate_directory(directory_path, output_log_path):
    """
    Run validate.py against each file in the specified directory and log the output.
    
    Args:
        directory_path: Path to the directory containing files to validate
        output_log_path: Path to the log file where results will be saved
    """
    # Check if directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    # Get current timestamp for the log header
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create/open the log file
    with open(output_log_path, 'w') as log_file:
        log_file.write(f"Validation Log - {timestamp}\n")
        log_file.write(f"Directory: {os.path.abspath(directory_path)}\n")
        log_file.write("=" * 60 + "\n\n")
        
        # Get all files in the directory
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        
        if not files:
            log_file.write("No files found in the directory.\n")
            print("No files found in the directory.")
            return
        
        # Process each file
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            log_file.write(f"Validating: {file_name}\n")
            print(f"Validating: {file_name}")
            
            try:
                # Run validate.py with the file as an argument
                result = subprocess.run(
                    ["python3", "validate.py", file_path], 
                    capture_output=True, 
                    text=True,
                    check=False
                )
                
                # Log the output
                log_file.write(f"Return code: {result.returncode}\n")
                log_file.write("STDOUT:\n")
                log_file.write(result.stdout if result.stdout else "No output\n")
                log_file.write("STDERR:\n")
                log_file.write(result.stderr if result.stderr else "No errors\n")
                log_file.write("-" * 60 + "\n\n")
                
            except Exception as e:
                log_file.write(f"Error executing validate.py: {str(e)}\n")
                log_file.write("-" * 60 + "\n\n")
                print(f"Error with {file_name}: {str(e)}")
        
        log_file.write("Validation completed.\n")
    
    print(f"Validation completed. Results saved to {output_log_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 validatefiles.py directory_path output_log_path")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    output_log_path = sys.argv[2]
    
    validate_directory(directory_path, output_log_path)
