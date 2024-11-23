import pandas as pd

def calculate_demographic_data(print_data=True):
    # Load data
    df = pd.read_csv("adult.data.csv", header=None, names=[
        "age", "workclass", "fnlwgt", "education", "education-num",
        "marital-status", "occupation", "relationship", "race",
        "sex", "capital-gain", "capital-loss", "hours-per-week",
        "native-country", "salary"
    ])
    
    # Ensure valid data types and clean rows
    df = df.dropna()  # Remove empty rows
    df["age"] = pd.to_numeric(df["age"], errors="coerce")  # Convert age to numeric
    df = df.dropna(subset=["age"])  # Drop rows where age couldn't be converted
    df["hours-per-week"] = pd.to_numeric(df["hours-per-week"], errors="coerce")  # Convert hours to numeric
    df = df.dropna(subset=["hours-per-week"])  # Drop rows with invalid hours

    # 1. How many people of each race are represented in this dataset?
    race_count = df["race"].value_counts()

    # 2. What is the average age of men?
    average_age_men = round(df[df["sex"] == "Male"]["age"].mean(), 1)

    # 3. What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df["education"] == "Bachelors").mean() * 100, 1)

    # 4. Percentage of people with advanced education (>50K)
    higher_education = df["education"].isin(["Bachelors", "Masters", "Doctorate"])
    higher_education_rich = round((df[higher_education & (df["salary"] == ">50K")].shape[0] / df[higher_education].shape[0]) * 100, 1)

    # 5. Percentage of people without advanced education (>50K)
    lower_education = ~higher_education
    lower_education_rich = round((df[lower_education & (df["salary"] == ">50K")].shape[0] / df[lower_education].shape[0]) * 100, 1)

    # 6. Minimum number of hours a person works per week
    min_work_hours = int(df["hours-per-week"].min())

    # 7. Percentage of people who work the minimum hours and earn >50K
    num_min_workers = df[df["hours-per-week"] == min_work_hours]
    if num_min_workers.shape[0] > 0:
        rich_percentage = round((num_min_workers[num_min_workers["salary"] == ">50K"].shape[0] / num_min_workers.shape[0]) * 100, 1)
    else:
        rich_percentage = 0

    # 8. Country with the highest percentage of people earning >50K
    country_earning = df[df["salary"] == ">50K"]["native-country"].value_counts()
    country_total = df["native-country"].value_counts()
    highest_earning_country_percentage = round((country_earning / country_total).max() * 100, 1)
    highest_earning_country = (country_earning / country_total).idxmax()

    # 9. Most popular occupation for those earning >50K in India
    india_occupation = df[(df["native-country"] == "India") & (df["salary"] == ">50K")]["occupation"]
    top_IN_occupation = india_occupation.value_counts().idxmax()

    # Print results if required
    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation
    }