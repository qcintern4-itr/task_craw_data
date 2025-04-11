import pandas as pd

def format_header(header):
    return header.upper().replace('_', ' ')

def process_encounter_data(csv_file="encounter_data.csv", excel_file="encounter_data.xlsx"):
    try:
        df = pd.read_csv(csv_file)
        df.columns = [format_header(col) for col in df.columns]
        
        # Tạo ExcelWriter object để có thể format
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Ghi DataFrame vào Excel
            df.to_excel(writer, index=False, sheet_name='Encounter Data')
            
            # Lấy workbook và worksheet để format
            workbook = writer.book
            worksheet = writer.sheets['Encounter Data']
            
            # Format các cột
            for idx, col in enumerate(df.columns):
                # Tìm độ rộng tối đa cho mỗi cột
                max_length = max(
                    df[col].astype(str).apply(len).max(),  
                    len(str(col)) 
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
                
                # Format header
                header_cell = worksheet.cell(row=1, column=idx + 1)
                header_cell.font = workbook.create_font(bold=True)
                
            print(f"Đã xử lý và lưu dữ liệu vào file {excel_file}")
            
    except FileNotFoundError:
        print(f"Không tìm thấy file CSV: {csv_file}")
    except Exception as e:
        print(f"Lỗi khi xử lý dữ liệu: {str(e)}")

