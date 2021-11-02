import time
import os
import turtle
from PIL import Image


# Set variables
users = int(input("Utenti: "))
desks = int(input("Desks: "))
days = (int(input("Giorni al lavoro: ")), int(input("Giorni a casa: ")))
total_days = sum(days)
save_images = input("Salvare le immagini (Attualmente non funzionante su windows)? Si/No:") in ["Si", "SI", "si", "sI"]

# Find possible combination for the first user
possible_first_user = {}

for n in range(2**total_days):
    r = [0, 2**total_days]  # Range available
    v = []

    for x in range(total_days):  # Try each number in the range
        # Find the half in the range
        half = r[0]+(r[1]-r[0])/2

        # Decide whether it's an office or an home day
        # And re-set the range limiters
        if n <= half-1:
            if v.count(1) == days[0]:
                break

            r[1] = half
            v.append(1)
        else:
            if v.count(0) == days[1]:
                break

            r[0] = half
            v.append(0)

    # Exclude every impossible combination
    if len(v) == total_days:
        possible_first_user[n] = v

# Add all the users
for k_opt, option in possible_first_user.items():
    timetable = {0: option}

    for user in range(1, users):
        day_scores = {}

        # Sum the desk usage for each day
        for n in range(total_days):
            day_scores[n] = 0
            for t in timetable.values():
                if t[n] == 1:
                    day_scores[n] += 1

        # Remove days where the maximum desk limit has been reached
        day_scores = {k: v for k, v in day_scores.items() if v < desks}
        assert len(day_scores)

        # Sort the days based on the amount of desks used (ascending order)
        sorted_day_scores = dict(
            sorted(day_scores.items(), key=lambda item: item[1])
        )

        # Find the lowest value and the days with that value
        lowest_value = None
        lowest_days = []
        for k, v in sorted_day_scores.items():
            if lowest_value is None or v < lowest_value:
                lowest_value = v
                lowest_days = [k]
            elif v == lowest_value:
                lowest_days.append(k)

        if len(lowest_days) < days[0]:
            # Find how many days are missing and what days can be used
            missing_days = days[0] - len(lowest_days)
            remaining_days = [
                k for k in sorted_day_scores.keys() if k not in lowest_days
            ]

            assert len(remaining_days) >= missing_days

            # Add the first N days needed
            for k in remaining_days[:missing_days]:
                lowest_days.append(k)

        elif len(lowest_days) > days[0]:
            # Reduce the number of used day to the one we really need
            lowest_days = lowest_days[:days[0]]

        user_timetable = [
            1 if x in lowest_days else 0 for x in range(0, total_days)
        ]
        timetable[user] = user_timetable

    print(
        "COMBINAZIONE N°{}\n   L M M G V\n{}"
        .format(
            k_opt,
            '\n'.join(
                "U{} {}".format(
                    k,
                    " ".join(str(x) for x in v)
                ) for k, v in timetable.items()
            )
        )
    )

    # Draw
    s = turtle.getscreen()
    t = turtle.Turtle()
    t.pen(pensize=10, speed=12)

    # Move the pen to correct position
    t.penup()
    t.rt(-90)
    t.fd(400)
    t.rt(90)
    t.fd(-400)

    # Write week days
    t.rt(-90)
    t.fd(80)
    t.rt(90)

    letters = ["L", "M", "M", "G", "V", "S", "D"]
    for letter in letters[:total_days]:
        t.write(letter, font=("Calibri", 40, "bold"))
        t.fd(90)

    t.fd(-90*len(letters[:total_days]))
    t.rt(90)
    t.fd(80)
    t.rt(-90)

    # Write user days
    t.fd(-120)
    t.rt(90)

    for user in range(users):
        t.write(f"U{user}", font=("Calibri", 40, "bold"))
        t.fd(100)

    t.fd(-100*users)
    t.rt(-90)
    t.fd(120)

    # Minor adjustments
    t.rt(-90)
    t.fd(10)
    t.rt(90)
    t.fd(20)

    for user in timetable.values():
        for day in user:
            if day:
                t.begin_fill()

            t.pendown()
            t.circle(20)
            t.penup()

            if day:
                t.end_fill()

            t.fd(100)

        t.rt(180)
        t.fd(100*len(user))
        t.rt(-90)
        t.fd(100)
        t.rt(-90)

    # Create folder
    if save_images:
        folder_path = f"timetables/{users}-{desks}-{days[0]}-{days[1]}/"
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        # Save image
        path = f"{folder_path}/{k_opt}.ps"
        turtle.getscreen().getcanvas().postscript(file=path)

        # Convert to png
        img = Image.open(path)
        img.save(path.replace(".ps", ".png"))
        os.remove(path)

    time.sleep(3)
    t.clear()
