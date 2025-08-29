def vacuum_world():
    # initializing goal_state
    # 0 indicates Clean and 1 indicates Dirty
    goal_state = {'A': '0', 'B': '0'}
    cost = 0

    # Inputs
    location_input = input("Enter Location of Vacuum (A or B): ")  # user_input of location vacuum is placed
    status_input = input("Enter status of " + location_input + " (0 for Clean, 1 for Dirty): ")  # status of current location
    status_input_complement = input("Enter status of the other room (0 for Clean, 1 for Dirty): ")

    print("\nInitial Location Condition:", goal_state)

    if location_input == 'A':
        print("Vacuum is placed in Location A")
        if status_input == '1':
            print("Location A is Dirty.")
            # suck the dirt and mark it as clean
            goal_state['A'] = '0'
            cost += 1
            print("COST for CLEANING A:", cost)
            print("Location A has been Cleaned.")
        else:
            print("Location A is already clean.")

        if status_input_complement == '1':
            print("Location B is Dirty.")
            print("Moving RIGHT to Location B...")
            cost += 1  # cost for moving right
            print("COST after moving RIGHT:", cost)
            # suck the dirt and mark it as clean
            goal_state['B'] = '0'
            cost += 1
            print("COST for SUCK:", cost)
            print("Location B has been Cleaned.")
        else:
            print("Location B is already clean. No action needed.")
            print("COST:", cost)

    else:  # location_input == 'B'
        print("Vacuum is placed in Location B")
        if status_input == '1':
            print("Location B is Dirty.")
            # suck the dirt and mark it as clean
            goal_state['B'] = '0'
            cost += 1
            print("COST for CLEANING B:", cost)
            print("Location B has been Cleaned.")
        else:
            print("Location B is already clean.")

        if status_input_complement == '1':
            print("Location A is Dirty.")
            print("Moving LEFT to Location A...")
            cost += 1  # cost for moving left
            print("COST after moving LEFT:", cost)
            # suck the dirt and mark it as clean
            goal_state['A'] = '0'
            cost += 1
            print("COST for SUCK:", cost)
            print("Location A has been Cleaned.")
        else:
            print("Location A is already clean. No action needed.")
            print("COST:", cost)

    # done cleaning
    print("\nGOAL STATE:", goal_state)
    print("Performance Measurement (Total Cost):", cost)


# Run function
vacuum_world()
