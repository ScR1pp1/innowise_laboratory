# Mini-Profile Generator Program

# User greeting
print("Hello! Welcome to Generator of mini-profiles!")

# Collect basic user information
user_name = input("Enter your full name: ")

# Get birth year and calculate age
birth_year = input("Enter your year of birth: ")
birth_year_int = int(birth_year)
current_age = 2025 - birth_year_int  # Calculate age based on current year

def generate_profile(age):
    """
    Determine life stage based on age
    Args:
        age (int): User's current age
    Returns:
        str: Life stage category
    """
    if age >= 0 and age <= 12:
        return "Child"
    elif age >= 13 and age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"
    else:
        return "Invalid age"

# Initialize empty list for hobbies collection
hobbies = []

# Collect hobbies in a loop until user types 'stop'
while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    
    # Exit condition - case insensitive check
    if hobby.lower() == "stop":
        break
    
    # Add valid hobby to the list
    hobbies.append(hobby)

# Determine user's life stage using the function
life_stage = generate_profile(current_age)

# Create user profile dictionary to store all collected data
user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies  # List of user's hobbies
}

# Display the formatted profile summary
print("\n---")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['stage']}")

# Check if hobbies list is empty and display appropriate message
if len(hobbies) == 0:
    print("You didn't mention any hobbies.")
else:
    # Display hobbies count and list each hobby with bullet points
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for hobby in hobbies:
        print(f"- {hobby}")
print("---")
