import os

def compare_expression(control_file, cte_file):
    print("Control File Path:", os.path.abspath(control_file))
    print("CTE File Path:", os.path.abspath(cte_file))

    if not os.path.exists(control_file):
        print(f"Error: Control file '{control_file}' not found.")
    if not os.path.exists(cte_file):
        print(f"Error: CTE file '{cte_file}' not found.")
