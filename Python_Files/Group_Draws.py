import pandas as pd
import random


def GD4(i, n, df):
    a = df.iloc[[i, i + n, i + (2 * n), i + (3 * n)], :]
    a = a.set_index([pd.Index([0, 1, 2, 3]), ])
    return a


def GD5(i, n, df):
    a = df.iloc[[i, i + n, i + (2 * n), i + (3 * n), i + (4 * n)], :]
    a = a.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    return a


def GD6(i, n, df):
    a = df.iloc[[i, i + n, i + (2 * n), i + (3 * n), i + (4 * n), i + (5 * n)], :]
    a = a.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
    return a


def WorldCupDraw(df):
    complete1, complete2, complete3 = 0, 0, 0

    df = df.reset_index(drop=True)

    grp = ["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H"]

    # r refers to the elements of grp i.e r(0) corresponds to Group A
    r = [0, 1, 2, 3, 4, 5, 6, 7]

    for p in range(4):

        # The first 8 teams (pot 1) can just be distributed into the 8 groups
        if p == 0:
            for i in range(8):
                grp[i] = df.iloc[i:i + 1, :]

        # Drawing pot 2
        if p == 1:

            r = [0, 1, 2, 3, 4, 5, 6, 7]

            print(complete1)

            # This loop tries to draw all the teams without breaking the constraints
            # While loop keeps trying until it has been successful
            while complete1 == 0:

                try:

                    # Resetting r for re-drawing the group
                    r2 = r

                    # For each of the 8 groups
                    for i in range(8):

                        # Selecting the next team to be drawn, reading the confederation of that team
                        nt = df.iloc[i + 8:i + 9, :]
                        nt_con = df.loc[i + 8, "Confederation"]

                        # Resetting j and s1 for re-drawing the team
                        j = 0
                        s1 = 0

                        # While loop continues team has been placed into a group
                        while s1 == 0:

                            # Setting n equal to the jth element of r2. This means each time j increases we try to
                            # draw the team into the next group available that hasn't been tried before
                            n = r2[j]

                            # Checking list of confederations already in the group
                            con = grp[n]["Confederation"].tolist()
                            x = con.count(nt_con)

                            # Rule as for whether team can be placed in group, if it can s1 changes, we exit the while
                            # loop and move onto the next team
                            if (nt_con == "UEFA" and x < 2) or x == 0:
                                grp[n] = grp[n].append(nt, ignore_index=True)
                                s1 = 1

                                # If we place the 8th team then we have placed every team and can move onto the next pot
                                if i == 7:
                                    complete1 = 1
                                    break

                                # Remove the group from the list of r so we don't place more than one team from this
                                # pot into a group
                                del r2[j]

                            # If we fail to place the team, increase j
                            else:
                                j = j + 1
                    break

                # If the a team cannot be placed in any group we randomise the order of groups and draw the group
                # again until the rules are satisfied
                except:

                    if complete1 == 0:
                        print("\nAren't you cheeky, please enter a number...")

                        # Re-shuffling r to randomise order of groups do draw into
                        r = [0, 1, 2, 3, 4, 5, 6, 7]
                        random.shuffle(r)

                        # Removing teams from this pot that we drew in the failed attempt
                        for i in range(8):
                            grp[i] = grp[i].head(1)

                    continue

        # We repeat the process for pot 2 with pot 3 and pot 4 below
        if p == 2:

            r = [0, 1, 2, 3, 4, 5, 6, 7]

            while complete2 == 0:

                try:

                    r3 = r

                    for i in range(8):

                        nt = df.iloc[i + 16:i + 17, :]
                        nt_con = df.loc[i + 16, "Confederation"]

                        j = 0
                        s2 = 0

                        while s2 == 0:

                            n = r3[j]

                            con = grp[n]["Confederation"].tolist()
                            x = con.count(nt_con)

                            if (nt_con == "UEFA" and x < 2) or x == 0:
                                grp[n] = grp[n].append(nt, ignore_index=True)
                                s2 = 1

                                if i == 7:
                                    complete = 1
                                    break

                                del r3[j]

                            # Otherwise
                            else:
                                j = j + 1
                    break


                except:

                    if complete2 == 0:
                        print("\nAren't you cheeky, please enter a number...")

                        r = [0, 1, 2, 3, 4, 5, 6, 7]
                        random.shuffle(r)

                        for i in range(8):
                            grp[i] = grp[i].head(2)

                    continue

        if p == 3:

            r = [0, 1, 2, 3, 4, 5, 6, 7]

            while complete3 == 0:

                try:

                    r4 = r

                    for i in range(8):

                        nt = df.iloc[i + 24:i + 25, :]
                        nt_con = df.loc[i + 24, "Confederation"]

                        j = 0
                        s3 = 0

                        while s3 == 0:

                            n = r4[j]

                            con = grp[n]["Confederation"].tolist()
                            x = con.count(nt_con)

                            if (nt_con == "UEFA" and x < 2) or x == 0:
                                grp[n] = grp[n].append(nt, ignore_index=True)
                                s3 = 1

                                if i == 7:
                                    complete3 = 1
                                    break

                                del r4[j]

                            # Otherwise
                            else:
                                j = j + 1
                    break


                except:

                    if complete3 == 0:
                        print("\nAren't you cheeky, please enter a number...")

                        r = [0, 1, 2, 3, 4, 5, 6, 7]
                        random.shuffle(r)

                        for i in range(8):
                            grp[i] = grp[i].head(3)

                    continue

    for c in range(8):
        print(grp[c])

    return (grp)
