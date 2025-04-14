import csv

def read_last_values(file_path, num_values=2):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            # Skip header row
            next(csv_reader)
            
            # Get last value from each row
            values = []
            for i, row in enumerate(csv_reader):
                if i >= num_values:  
                    break
                if row:  
                    values.append(row[-1])  
            
            # Print values
            print("\nPrint values (id-patientid):")
            for value in values:
                print(value)
            
            return values
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {str(e)}")
