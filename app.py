import numpy as np
import streamlit as st

st.title("Calculator")

st.write("---")

st.header("Basic Math Operations")

num1 = st.number_input("Enter the first number:", value=0.0)
num2 = st.number_input("Enter the second number:", value=0.0)

operation = st.selectbox(
    "Select an operation:",
    ["Addition", "Subtraction", "Multiplication", "Division"],
)

if st.button("Calculate Basic Math"):

  if operation == "Addition":
    result = np.add(num1, num2)
    st.success(f"Result: {num1} + {num2} = {result}")

  elif operation == "Subtraction":
    result = np.subtract(num1, num2)
    st.success(f"Result: {num1} - {num2} = {result}")

  elif operation == "Multiplication":
    result = np.multiply(num1, num2)
    st.success(f"Result: {num1} × {num2} = {result}")

  elif operation == "Division":

    if num2 == 0:
      st.error("Error: You cannot divide a number by zero.")
    else:
      result = np.divide(num1, num2)
      st.success(f"Result: {num1} ÷ {num2} = {result}")

st.write("---")
st.header("2. NumPy Array Statistics")
st.write(
    "NumPy is designed to work with arrays (lists of numbers). Try entering a"
    " few numbers below:"
)

user_input = st.text_input(
    "Enter numbers separated by commas:", "10, 20, 30, 40, 50"
)

if st.button("Calculate Stats"):
  try:

    raw_list = user_input.split(",")
    float_list = []
    for item in raw_list:
      float_list.append(float(item.strip()))

    my_array = np.array(float_list)

    st.write("Your NumPy Array:", my_array)

    st.metric("Total Sum", np.sum(my_array))
    st.metric("Average (Mean)", np.mean(my_array))
    st.metric("Highest Value", np.max(my_array))
    st.metric("Lowest Value", np.min(my_array))

  except ValueError:

    st.error(
        "Invalid input! Please make sure you only enter numbers separated by"
        " commas."
    )