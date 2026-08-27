import pandas as pd
import numpy as np

def analyze_employee_data():
    print("=" * 60)
    print("        EMPLOYEE DATA ANALYSIS REPORT        ")
    print("=" * 60)

    # 1. Load Dataset
    url = "https://raw.githubusercontent.com/slidescope/Employee-Performance-Training-Data-Analysis-Power-BI-dashboard/main/employee_performance_dataset.csv"
    print(f"\n[1] Loading dataset from: {url}")
    df = pd.read_csv(url)

    print("\n--- Dataset Overview ---")
    print(f"Total Records (Rows): {df.shape[0]}")
    print(f"Total Attributes (Columns): {df.shape[1]}")
    print("\nFirst 5 Rows:")
    print(df.head())

    # 2. Look for Missing Values
    print("\n" + "=" * 60)
    print("[2] LOOKING FOR MISSING VALUES")
    print("=" * 60)
    missing_vals = df.isnull().sum()
    print("Missing values per column:")
    print(missing_vals)

    # 3. Fill Missing Values (Imputation Strategy)
    print("\n" + "=" * 60)
    print("[3] FILLING MISSING VALUES (IMPUTATION STRATEGY)")
    print("=" * 60)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'string']).columns

    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Filled missing in '{col}' with median: {median_val}")

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"Filled missing in '{col}' with mode: {mode_val}")

    print("Missing values check after imputation:")
    print(df.isnull().sum())

    # 4. Highest Salary
    print("\n" + "=" * 60)
    print("[4] HIGHEST SALARY ANALYSIS")
    print("=" * 60)
    max_salary = df["monthly_salary"].max()
    highest_paid_emp = df[df["monthly_salary"] == max_salary]
    print(f"Highest Monthly Salary: ${max_salary:,.2f}")
    print("\nEmployee(s) with Highest Salary:")
    print(highest_paid_emp[['id', 'age', 'department', 'job_level', 'years_experience', 'monthly_salary', 'performance_rating']].to_string(index=False))

    # 5. Average Salary
    print("\n" + "=" * 60)
    print("[5] AVERAGE SALARY ANALYSIS")
    print("=" * 60)
    avg_salary = df["monthly_salary"].mean()
    median_salary = df["monthly_salary"].median()
    print(f"Mean (Average) Monthly Salary: ${avg_salary:,.2f}")
    print(f"Median Monthly Salary:       ${median_salary:,.2f}")

    # 6. Department-wise Salary Analysis
    print("\n" + "=" * 60)
    print("[6] DEPARTMENT-WISE SALARY ANALYSIS")
    print("=" * 60)
    dept_salary_summary = df.groupby("department")["monthly_salary"].agg(
        Average_Salary='mean',
        Min_Salary='min',
        Max_Salary='max',
        Employee_Count='count'
    ).reset_index().sort_values(by="Average_Salary", ascending=False)
    
    print(dept_salary_summary.to_string(index=False))

    # 7. Employees with >5 Years Experience
    print("\n" + "=" * 60)
    print("[7] EMPLOYEES WITH > 5 YEARS EXPERIENCE")
    print("=" * 60)
    exp_gt_5 = df[df["years_experience"] > 5]
    pct_exp = (len(exp_gt_5) / len(df)) * 100
    print(f"Total employees with > 5 years experience: {len(exp_gt_5)} out of {len(df)} ({pct_exp:.1f}%)")
    print("\nSample records (>5 Years Experience):")
    print(exp_gt_5[['id', 'age', 'department', 'job_level', 'years_experience', 'monthly_salary']].head(10).to_string(index=False))

    # 8. Top Performers
    print("\n" + "=" * 60)
    print("[8] TOP PERFORMERS ANALYSIS")
    print("=" * 60)
    top_performers = df[df["performance_rating"].str.lower() == "excellent"]
    pct_top = (len(top_performers) / len(df)) * 100
    print(f"Total Top Performers ('Excellent' Rating): {len(top_performers)} ({pct_top:.1f}%)")
    
    perf_counts = df["performance_rating"].value_counts()
    print("\nOverall Performance Distribution:")
    print(perf_counts.to_string())

    print("\nSample Top Performers:")
    print(top_performers[['id', 'department', 'job_level', 'years_experience', 'monthly_salary', 'performance_rating']].head(10).to_string(index=False))

    # 9. Youngest and Oldest Employee
    print("\n" + "=" * 60)
    print("[9] YOUNGEST AND OLDEST EMPLOYEES")
    print("=" * 60)
    youngest_age = df["age"].min()
    oldest_age = df["age"].max()
    
    youngest_emps = df[df["age"] == youngest_age]
    oldest_emps = df[df["age"] == oldest_age]

    print(f"Youngest Age: {youngest_age} years")
    print(youngest_emps[['id', 'age', 'department', 'job_level', 'years_experience', 'monthly_salary']].to_string(index=False))

    print(f"\nOldest Age: {oldest_age} years")
    print(oldest_emps[['id', 'age', 'department', 'job_level', 'years_experience', 'monthly_salary']].to_string(index=False))

    # 10. Salary Distribution Summary Stats
    print("\n" + "=" * 60)
    print("[10] SALARY DISTRIBUTION SUMMARY")
    print("=" * 60)
    print(df["monthly_salary"].describe().to_string())

    print("\n[SUCCESS] Employee Data Analysis Completed Successfully!\n")

if __name__ == "__main__":
    analyze_employee_data()