import pandas as pd

# Read the CSV file
data = pd.read_csv("students.csv")

print("Student Data:")
print(data)


# Find the topper
topper = data.loc[data["TotalMarks"].idxmax()]

print("\nTopper:")
print(topper["Name"])
print("Marks:", topper["TotalMarks"])


# Calculate average marks
average_marks = data["TotalMarks"].mean()

print("\nAverage Marks:")
print(average_marks)


# Cal percent
data["Percentage"] = (data["TotalMarks"] / data["MaxMarks"]) * 100

print("\nPercentage:")
print(data[["Name", "Percentage"]])


# 5. Assign grades
def assign_grade(percentage):

    if percentage >= 90:
        return "A+"

    elif percentage >= 80:
        return "A"

    elif percentage >= 70:
        return "B"

    elif percentage >= 60:
        return "C"

    elif percentage >= 50:
        return "D"

    else:
        return "F"


data["Grade"] = data["Percentage"].apply(assign_grade)

print("\nGrades:")
print(data[["Name", "Percentage", "Grade"]])


# 6. Find students with attendance below 75%
low_attendance = data[data["Attendance"] < 75]

print("\nStudents with attendance below 75%:")
print(low_attendance[["Name", "Attendance"]])


# 7. Depart average marks
department_average = data.groupby("Department")["TotalMarks"].mean()

print("\nDepartment-wise Average Marks:")
print(department_average)


# 8. final report
data.to_csv("student_performance_report.csv", index=False)

print("\nReport saved successfully!")