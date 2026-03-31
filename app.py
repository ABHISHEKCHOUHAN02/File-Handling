import sys
import os
from pathlib import Path

# Ensure Auth package is importable
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from Auth.user_registration import register_user
from Auth.login_service import login_user

def main():
   
    print("   WELCOME TO THE EMPLOYEE SYSTEM       ")
   
    
    while True:
        print("\nAvailable Actions: login, register , exit")
        command = input("Enter command: ").strip().lower()
        
        if command == 'register':
            register_user()
        elif command == 'login':
            login_user()
        elif command == 'exit':
            print("Exiting application. Goodbye! 👋")
            break
        elif command == '':
            continue
        else:
            print(f"Unknown command: '{command}'. Please use 'login', 'register', or 'exit'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated. Goodbye!")
        sys.exit(0)
