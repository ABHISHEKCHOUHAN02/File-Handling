from data_reader import read_data
from Utilities.logger_config import get_logger

logger = get_logger(__name__)

def admin_kpi_dashboard():
    logger.info("Initiating Admin KPI dashboard")
    data = read_data()
    
    if not data:
        logger.warning("No attendance data available for KPI calculation.")
        print("No attendance data available.")
        return

    print("\n--- Admin Data Extraction (KPIs) ---")
    print("Filter by Date Range (leave both blank for All-Time)")
    start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
    end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
    
    filtered_data = data
    if start_date:
        filtered_data = [row for row in filtered_data if row.get("date") and row.get("date") >= start_date]
    if end_date:
        filtered_data = [row for row in filtered_data if row.get("date") and row.get("date") <= end_date]
        
    if start_date or end_date:
        if not filtered_data:
            print("No records found for the specified date range.")
            return
        print(f"Filtering KPIs from {start_date or 'Beginning'} to {end_date or 'Present'}")
    else:
        print("Displaying All-Time KPIs.")

    while True:
        print("\n--- KPI Menu ---")
        print("1. Total Attendance Records")
        print("2. Attendance Status Breakdown (Present, Absent, Leave, etc.)")
        print("3. Maximum Working Hours & Top Employee")
        print("4. Average Working Hours")
        print("5. View All KPIs")
        print("6. Return to Main Menu")
        
        choice = input("Select KPI to view (1-6): ").strip()
        
        # Calculate stats for filtered_data
        total_records = len(filtered_data)
        status_counts = {"Present": 0, "Absent": 0, "Leave": 0, "Half-Day": 0}
        max_working_hours = 0.0
        total_working_hours = 0.0
        valid_hours_count = 0
        top_employee = None
        
        for row in filtered_data:
            status = row.get("status", "")
            if status in status_counts:
                status_counts[status] += 1
                
            try:
                wh = float(row.get("working_hours", 0))
                if wh > 0:
                    total_working_hours += wh
                    valid_hours_count += 1
                    
                if wh > max_working_hours:
                    max_working_hours = wh
                    top_employee = row.get("employee_id")
            except ValueError:
                pass

        avg_working_hours = total_working_hours / valid_hours_count if valid_hours_count > 0 else 0.0

        if choice == '1':
            print(f"\nTotal Attendance Records: {total_records}")
        elif choice == '2':
            print("\nAttendance Status Breakdown:")
            print(f"  - Present:  {status_counts['Present']}")
            print(f"  - Absent:   {status_counts['Absent']}")
            print(f"  - Leave:    {status_counts['Leave']}")
            print(f"  - Half-Day: {status_counts['Half-Day']}")
        elif choice == '3':
            print(f"\nMaximum Working Hours: {max_working_hours:.2f} hrs (Employee ID: {top_employee or 'N/A'})")
        elif choice == '4':
            print(f"\nAverage Working Hours: {avg_working_hours:.2f} hrs")
        elif choice == '5':
            print("\n" + "-" * 40)
            print(f"Total Attendance Records: {total_records}")
            print(f"  - Present:  {status_counts['Present']}")
            print(f"  - Absent:   {status_counts['Absent']}")
            print(f"  - Leave:    {status_counts['Leave']}")
            print(f"  - Half-Day: {status_counts['Half-Day']}")
            print("-" * 40)
            print(f"Maximum Working Hours:   {max_working_hours:.2f} hrs (Employee: {top_employee or 'N/A'})")
            print(f"Average Working Hours:   {avg_working_hours:.2f} hrs")
            print("-" * 40)
        elif choice == '6':
            logger.info("Exiting Admin KPI Dashboard")
            break
        else:
            print("Invalid choice. Please select 1 through 6.")
