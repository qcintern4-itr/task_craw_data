#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
from implement_file import read_last_values, save_to_excel
from process import process_patient_data

class Main:
    def __init__(self, _arguments):
        self.arguments = _arguments
        # self.OUTPUT_FOLDER = f'results/output_file_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
        self.OUTPUT_FOLDER = f'results/output_file_{datetime.now().strftime("%Y-%m-%d")}'

    def add_to_config(self, key, value):
        """Thêm giá trị vào config dictionary.
        
        Args:
            key: Khóa trong config
            value: Giá trị cần thêm, có thể là string hoặc list
            
        Ví dụ:
            add_to_config('-f', 'data.csv')  # Thêm string
            add_to_config('-i', ['tag1', 'tag2'])  # Thêm list
        """
        if key in self.config:
            if isinstance(value, str):
                self.config[key].append(value)
            else:
                self.config[key].extend(value)
        else:
            if isinstance(value, str):
                self.config[key] = [value]
            else:
                self.config[key] = value

    def build_config(self):
        """Xây dựng cấu hình từ các tham số dòng lệnh.
        
        Ví dụ:
            Nếu chạy: python main.py -f data.csv -n 20 -o output.xlsx -uc false -D 60
            Thì build_config sẽ tạo:
            {
                '-f': ['data.csv'],
                '-n': ['20'],
                '-o': ['output.xlsx'],
                '-uc': ['false'],
                '-D': ['60']
            }
        """
        self.config = {}
        if self.arguments.file:
            self.add_to_config('-f', self.arguments.file)
        if self.arguments.number:
            self.add_to_config('-n', str(self.arguments.number))
        if self.arguments.output:
            self.add_to_config('-o', self.arguments.output)
        if self.arguments.use_cache is not None:
            self.add_to_config('-uc', str(self.arguments.use_cache).lower())
        if self.arguments.from_date:
            self.add_to_config('--from', self.arguments.from_date)
        if self.arguments.to_date:
            self.add_to_config('--to', self.arguments.to_date)

    def __call__(self, *args, **kwargs):
        self.build_config()
        
        # Tạo thư mục output nếu chưa tồn tại
        if not os.path.exists(self.OUTPUT_FOLDER):
            os.makedirs(self.OUTPUT_FOLDER, exist_ok=True)
        
        try:
            # Read patient IDs from CSV
            values = read_last_values(self.arguments.file, self.arguments.number)
            
            if not values:
                print("\nNo patient IDs found in CSV file")
                return
            
            # Process patient data
            all_patient_data = process_patient_data(
                values, 
                self.arguments.use_cache,
                self.arguments.from_date,
                self.arguments.to_date,
            )
            
            # Save results
            if all_patient_data:
                # Tạo đường dẫn đầy đủ cho file output
                output_file = os.path.join(self.OUTPUT_FOLDER, self.arguments.output)
                save_to_excel(all_patient_data, output_file)
                print(f"\nOutput file saved to: {output_file}")
            else:
                print("\nNo patient data was collected")
                
        except Exception as e:
            print(f"\nUnexpected error in main: {str(e)}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Medical Records Data Processing Tool')
    
    # Required arguments
    parser.add_argument('-f', '--file', 
                       help='Input CSV file path',
                       required=True)
    
    # Optional arguments
    parser.add_argument('-n', '--number', 
                       type=int,
                       default=10,
                       help='Number of records to process (default: 10)')
    
    parser.add_argument('-o', '--output',
                       default='patient_data.xlsx',
                       help='Output Excel file name (default: patient_data.xlsx)')
    
    parser.add_argument('-uc', '--use-cache',
                       type=lambda x: x.lower() == 'true',
                       help='Use cache if available (true/false)')
    
    parser.add_argument('--from-date',
                       help='Start date in MM/DD/YYYY format')
    
    parser.add_argument('--to-date',
                       help='End date in MM/DD/YYYY format')
    
    return parser.parse_args()

if __name__ == '__main__':
    if os.path.basename(os.getcwd()) != 'task':
        raise Exception('Script must be executed in the `task` directory')
    
    arguments = parse_arguments()
    Main(arguments)()