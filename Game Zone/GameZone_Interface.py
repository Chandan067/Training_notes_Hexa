from GameZone_DB_Creation import connect_db, create_tables
MEMBERSHIP_HOURS = {'daily': 5, 'monthly': 60, 'yearly': 300}

def add_game():
    name = input("Enter game name: ")
    gtype = input("Enter game type (e.g., Sports, Racing): ")
    charge = float(input("Enter charge per hour: "))
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO games (name, type, charge_per_hour) VALUES (%s, %s, %s)", (name, gtype, charge))
        conn.commit()
        conn.close()
        print("Game added successfully.")

def register_member():
    name = input("Enter member name: ")
    mtype = input("Enter membership type (daily/monthly/yearly): ").lower()
    hours = MEMBERSHIP_HOURS.get(mtype, 0)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (name, membership_type, hours_left) VALUES (%s, %s, %s)", (name, mtype, hours))
        conn.commit()
        conn.close()
        print("Member registered successfully with", hours, "hours.")

def log_gameplay():
    member_name = input("Enter member name: ")
    game_name = input("Enter game name: ")
    hours = int(input("Enter hours to play: "))
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id, hours_left FROM members WHERE name = %s", (member_name,))
    member = cursor.fetchone()
    if not member:
        print("Member not found.")
        return
    mid, hrs_left = member
    if hrs_left < hours:
        print("Insufficient hours to play.")
        return
    cursor.execute("SELECT id, charge_per_hour FROM games WHERE name = %s", (game_name,))
    game = cursor.fetchone()
    if not game:
        print("Game not found.")
        return
    gid, charge = game
    cursor.execute("INSERT INTO gameplays (member_id, game_id, hours_played) VALUES (%s, %s, %s)", (mid, gid, hours))
    cursor.execute("UPDATE members SET hours_left = hours_left - %s, hours_spent = hours_spent + %s WHERE id = %s", (hours, hours, mid))
    conn.commit()
    conn.close()
    print(f"Gameplay logged. Total charge: ₹{hours * charge:.2f}")


def report_games():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_members():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_members_by_type():
    conn = connect_db()
    cursor = conn.cursor()
    for mtype in ['daily', 'monthly', 'yearly']:
        print(f"\n{mtype.capitalize()} Members:")
        cursor.execute("SELECT * FROM members WHERE membership_type = %s", (mtype,))
        for row in cursor.fetchall():
            print(row)
    conn.close()

def report_member_hours():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, membership_type, hours_left FROM members")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_monthly_member_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members WHERE membership_type = 'monthly'")
    print("Monthly Members Count:", cursor.fetchone()[0])
    conn.close()

def report_game_players():
    game = input("Enter game name: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT member_id) FROM gameplays gp JOIN games g ON gp.game_id = g.id WHERE g.name = %s", (game,))
    print("Players count:", cursor.fetchone()[0])
    conn.close()

def report_game_hours():
    game = input("Enter game name: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(hours_played) FROM gameplays gp JOIN games g ON gp.game_id = g.id WHERE g.name = %s", (game,))
    print("Total hours played:", cursor.fetchone()[0])
    conn.close()

def report_most_played_game():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT g.name, SUM(gp.hours_played) AS total FROM gameplays gp JOIN games g ON gp.game_id = g.id GROUP BY gp.game_id ORDER BY total DESC LIMIT 1")
    print("Most played game:", cursor.fetchone())
    conn.close()

def report_low_hour_members():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE hours_left < 10")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_members_multiple_games():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT member_id FROM gameplays GROUP BY member_id HAVING COUNT(DISTINCT game_id) > 2")
    for row in cursor.fetchall():
        print("Member ID:", row[0])
    conn.close()

def report_hours_by_membership():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT membership_type, SUM(hours_left) FROM members GROUP BY membership_type")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_income():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(g.charge_per_hour * gp.hours_played) FROM gameplays gp JOIN games g ON gp.game_id = g.id")
    print("Total Income: ₹", cursor.fetchone()[0])
    conn.close()

def report_most_active_member():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, hours_spent FROM members ORDER BY hours_spent DESC LIMIT 1")
    print("Most active member:", cursor.fetchone())
    conn.close()

def report_top_3_games():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT g.name, SUM(gp.hours_played) as total FROM gameplays gp JOIN games g ON gp.game_id = g.id GROUP BY gp.game_id ORDER BY total DESC LIMIT 3")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_hours_per_member_game():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT m.name, g.name, SUM(gp.hours_played) FROM gameplays gp JOIN members m ON gp.member_id = m.id JOIN games g ON gp.game_id = g.id GROUP BY m.name, g.name")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_members_above_75_percent():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, hours_spent, (hours_spent + hours_left) AS total, ROUND((hours_spent / (hours_spent + hours_left)) * 100, 2) AS used_percent FROM members HAVING used_percent > 75")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_detailed_member_summary():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT m.name, m.membership_type, COUNT(DISTINCT gp.game_id), SUM(gp.hours_played), m.hours_left FROM members m LEFT JOIN gameplays gp ON m.id = gp.member_id GROUP BY m.id")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def report_never_played():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT m.name FROM members m LEFT JOIN gameplays gp ON m.id = gp.member_id WHERE gp.id IS NULL")
    for row in cursor.fetchall():
        print(row)
    conn.close()


def menu():
    create_tables()
    while True:
        print("\n===== GamingZone Menu =====")
        print("1. Add Game")
        print("2. Register Member")
        print("3. Log Gameplay")
        print("4. Reports")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_game()
        elif choice == '2':
            register_member()
        elif choice == '3':
            log_gameplay()
        elif choice == '4':
            print("\n--- Reports ---")
            print("1. List All Games")
            print("2. List All Members")
            print("3. List Members by Type")
            print("4. Member Hours Summary")
            print("5. Monthly Member Count")
            print("6. Players per Game")
            print("7. Hours per Game")
            print("8. Most Played Game")
            print("9. Members with <10 Hours Left")
            print("10. Members with >2 Games")
            print("11. Hours by Membership Type")
            print("12. Total Income from Games")
            print("13. Most Active Member")
            print("14. Top 3 Most Played Games")
            print("15. Hours Played Per Member/Game")
            print("16. Members Used >75% Hours")
            print("17. Member Summary Report")
            print("18. Members Never Played")
            rchoice = input("Enter report number or 'b' to go back: ")

            reports = [
                report_games, report_members, report_members_by_type, report_member_hours,
                report_monthly_member_count, report_game_players, report_game_hours, report_most_played_game,
                report_low_hour_members, report_members_multiple_games, report_hours_by_membership,
                report_income, report_most_active_member, report_top_3_games,
                report_hours_per_member_game, report_members_above_75_percent,
                report_detailed_member_summary, report_never_played
            ]

            if rchoice.lower() == 'b':
                continue
            elif rchoice.isdigit() and 1 <= int(rchoice) <= 18:
                reports[int(rchoice) - 1]()
            else:
                print("Invalid option.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()