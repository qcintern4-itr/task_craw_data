from craw_encounter import fetch_encounter_data
from process_data import process_encounter_data

def main():
    # print("Start fetching encounter data...")
    # fetch_encounter_data()
    # print("\nComplete!")

    print("\nStart processing data and creating Excel file...")
    process_encounter_data() 
    print("\nComplete!")

if __name__ == "__main__":
    main() 