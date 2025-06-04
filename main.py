from sunway_checkin import load_user_agents, load_users, checkin_user


def main():
    user_agents = load_user_agents()
    users = load_users()
    if not users:
        print("No users found. Please configure users.json or users.csv")
        return
    checkin_code = input("Please enter iCheckin Code (for all users): ").strip()
    for user in users:
        checkin_user(user, checkin_code, user_agents)


if __name__ == "__main__":
    main()
