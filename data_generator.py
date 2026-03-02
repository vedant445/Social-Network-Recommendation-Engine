import random

first_names = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Sai", "Krishna",
    "Ishaan", "Rohan", "Kabir", "Vihaan",
    "Ananya", "Aadhya", "Diya", "Meera", "Ira",
    "Sara", "Riya", "Anika", "Tara", "Myra",
    "Aryan", "Dev", "Kunal", "Sneha", "Pooja"
]

last_names = [
    "Sharma", "Patel", "Verma", "Iyer", "Reddy",
    "Singh", "Gupta", "Nair", "Mehta", "Joshi",
    "Kapoor", "Malhotra", "Desai", "Kulkarni", "Chopra",
    "Agarwal", "Bansal", "Mishra", "Saxena"
]

cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Hyderabad"]
interests = ["AI", "ML", "Finance", "Gaming", "Sports", "Music", "Coding", "Blockchain"]
professions = ["Student", "Engineer", "Doctor", "Designer", "Trader", "Entrepreneur"]
skills = ["Python", "Java", "C++", "Data Analysis", "Machine Learning",
          "UI/UX", "Marketing", "Stock Trading", "Cloud"]
companies = ["TCS", "Infosys", "Google", "Microsoft", "Amazon", "Flipkart", "Startup"]
education = ["B.Tech", "MBA", "B.Sc", "M.Tech", "B.Com", "PhD"]
hobbies = ["Cricket", "Football", "Reading", "Traveling", "Photography", "Chess"]
languages = ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Kannada"]

def generate_random_name(existing_names):
    while True:
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        if name not in existing_names:
            return name

def generate_users(n=100, custom_name=None, custom_interests=None):
    users = {}
    existing_names = set()

    # Add custom user if provided
    if custom_name and custom_interests:
        users[custom_name] = {
            "age": random.randint(18, 40),
            "city": random.choice(cities),
            "interest": custom_interests[0] if isinstance(custom_interests, list) else custom_interests,
            "profession": random.choice(professions),
            "skills": random.sample(skills, 3),
            "company": random.choice(companies),
            "education": random.choice(education),
            "hobby": random.choice(hobbies),
            "language": random.choice(languages),
        }
        existing_names.add(custom_name)
        n -= 1  # Generate one less random user

    # Generate remaining random users
    for _ in range(n):
        name = generate_random_name(existing_names)
        existing_names.add(name)

        users[name] = {
            "age": random.randint(18, 40),
            "city": random.choice(cities),
            "interest": random.choice(interests),
            "profession": random.choice(professions),
            "skills": random.sample(skills, 3),
            "company": random.choice(companies),
            "education": random.choice(education),
            "hobby": random.choice(hobbies),
            "language": random.choice(languages),
        }

    return users

def get_user_input():
    """Get custom name and interests from user"""
    print("\n=== Setup Your Profile ===")
    
    # Get name
    name = input("Enter your name (or press Enter for random): ").strip()
    
    if not name:
        print("Using random name...")
        return None, None
    
    # Get interests
    print(f"\nAvailable interests: {', '.join(interests)}")
    interests_input = input("Enter your interests (comma-separated, e.g., Gaming,Coding): ").strip()
    
    if not interests_input:
        print("Using random interests...")
        return name, None
    
    custom_interests = [i.strip() for i in interests_input.split(",")]
    
    return name, custom_interests