import pandas as pd

def list_columns(df):
    # TODO: return the list of column names in the dataframe
    return df.columns.tolist()

def get_stats(df, column):
    # TODO: return count, mean, max, min, sum for a numeric column
    stats = df[column].agg(["count", "mean", "max", "min", "sum"])
    return [int(stats["count"]), round(float(stats["mean"]), 2), stats["max"], stats["min"], stats["sum"]]

def filter_count(df, column, value):
    # TODO: return count and matching names for rows where column == value
    filtered_df = df[df[column] == value]
    cnt = len(filtered_df)
    names = filtered_df["Name"].tolist()
    return [cnt, names]

def call_tool(tool_name, arguments, df):
    # TODO: dispatch to the correct function via a name -> function mapping
    tools = {
        "list_columns": list_columns,
        "get_stats": get_stats,
        "filter_count": filter_count,
    }
    if tool_name in tools:
        return tools[tool_name](df, **arguments)
    else:
        return f"Tool {tool_name} not found."

if __name__ == "__main__":
    employee_data = {
        "Name": [
            "Rahul", "Lakshmi", "Manoj", "Divya", "Vikram", "Anita",
            "Karthik", "Deepa", "Suresh", "Kavya", "Sanjay", "Arun"
        ],
        "Department": [
            "Engineering", "Marketing", "Engineering", "Marketing", "Engineering", "Sales",
            "Marketing", "Engineering", "Sales", "Marketing", "Engineering", "Engineering"
        ],
        "Salary": [75500, 62000, 81000, 58000, 79500, 55000, 60500, 84000, 57000, 61000, 76000, 78000],
        "Experience (years)": [5, 4, 7, 3, 6, 4, 5, 8, 3, 4, 5, 6],
        "City": [
            "Hyderabad", "Pune", "Bangalore", "Delhi", "Hyderabad", "Mumbai",
            "Chennai", "Hyderabad", "Pune", "Bangalore", "Delhi", "Hyderabad"
        ],
    }
    df = pd.DataFrame(employee_data)
    count = call_tool("filter_count", {"column": "Department", "value": "Engineering"}, df)
    average_salary = call_tool("get_stats", {"column": "Salary"}, df[df["Department"] == "Engineering"])
    print(f"Count of employees in Engineering: {count[0]}, Names: {count[1]}, Average Salary: {average_salary[1]}")
    print(count)
    # Step 1: call_tool("filter_count", {"column": "Department", "value": "Engineering"}, df)
    # Step 2: use the filtered rows to call_tool("get_stats", {"column": "Salary"}, ...)
    # Step 3: print count, names, and average salary
