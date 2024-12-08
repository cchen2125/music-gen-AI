class Protection: 
    # Sterne accounts
    accounts = open("accounts.txt")
    sterne_names = []
    sterne_pwords = []
    for line in accounts:
        parts = line.strip().split(',')
        if len(parts) == 2:  # Ensure there are exactly two parts
            sterne_names.append(parts[0])
            sterne_pwords.append(parts[1])
    
 

