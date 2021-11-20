import asyncio
import time

# Set variables
# users = int(input("Utenti: "))
# desks = int(input("Desks: "))
# days = (int(input("Giorni al lavoro: ")), int(input("Giorni a casa: ")))
# total_days = sum(days)

users, desks, days, total_days = 5, 3, (3, 2), 5
total_timetables = 0


async def main():
    # Find possible combination for the first user
    combinations = []

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
            combinations.append(v)

    tasks = []
    for combination in combinations:
        timetable = {0: combination}
        tasks.append(
            asyncio.create_task(fill(users, days, total_days, timetable, combinations))
        )

    await asyncio.wait(tasks)
    print(total_timetables)


async def fill(users: int, days: tuple, total_days: int, timetable: dict, combinations: dict):
    global total_timetables

    # Find missing user to fill
    for n in range(0, users):
        if n not in timetable:
            missing_user = n
            break
    else:
        missing_user = None

    if missing_user:
        tasks = []

        # Start a new fill for each combination found
        for combination in combinations:
            # Create new combination
            new_timetable = {**timetable, n: combination}

            # Verify that doesn't break requirements
            for day in range(0, total_days):
                occupied = 0
                for user in range(0, users):
                    try:
                        user_occupied = new_timetable[user][day]
                    except KeyError:
                        pass
                    else:
                        occupied += user_occupied

                if occupied > days[0]:
                    break

            else:
                tasks.append(
                    asyncio.create_task(fill(users, days, total_days, new_timetable, combinations))
                )

        await asyncio.gather(*tasks)

    else:
        total_timetables += 1


start = time.perf_counter()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
end = time.perf_counter()

print(f"Tempo: {round(end - start, 2)}s")
