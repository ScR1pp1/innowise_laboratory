# User greeting
print("Hello!\nWelcome to Generator of mini-profiles!")

# Request for user's name
user_name = input("Enter your full name: ")

# Request for birth year and convert it in int
birth_year = input("Enter your year of birth: ")
birth_year_int = int(birth_year)

# Calculating age
current_age = 2025 - birth_year_int

def generate_profile(age):
    if age >= 0 and age <= 12:
        return "Child"
    elif age >= 13 and age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"
    else:
        return "Invalid age"

# Create empty list for hobbies
hobbies = []
# Infinitive loop
while True:
    hobby = input("Enter favourite hobby or stop entering with 'stop': ")

    if hobby.lower() == "stop":
        break

    hobbies.append(hobby)

life_stage = generate_profile(current_age)

user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies
}
print("\n---")
print(f"Profile summary: \nName: {user_profile['name']}\nAge: {user_profile['age']}\nLife stage: {user_profile['stage']}")

if len(hobbies) == 0:
    print("You did not specify any hobbies")
else:
    print(f"Your favourite {len(hobbies)} hobbies: ")
    for hobby in hobbies:
        print(f"- {hobby}")
print("---\n")
