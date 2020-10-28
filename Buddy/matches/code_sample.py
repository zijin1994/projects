if hobbies is not None:
    for hobby in hobbies:
        group = hobby.members.all()
        #there might be duplicate members in the list since one person could be in different hobby groups.
        #late after filtering all the people, we could count the existence of people to find the best matches.
        members.extend(group)
    #if user also gave ago info, try filter results with age range of +- 3.
    if age is not None:
        members = [person for person in members if person.age>=(age-3) and person.age<=(age+3)]
        #if user also gave location, try filter results with location.
        if location is not None:
            members = [person for person in members if person.location.name == location]
            #if user also gave school, try filter results with school.
            if school is not None:
                members = [person for person in members if person.education.name == school.name]
                #if user also gave nationality, try filter results with nationality.
                if nationality is not None:
                    members = [person for person in members if person.nationality.name == nationality]
            #if user provide hobbies, age, location, nationality.
            elif nationality is not None:
                members = [person for person in members if person.nationality.name == nationality]
        #if user provide hobbies, age, school.
        elif school is not None:
            members = [person for person in members if person.education.name == school.name]
            #if user provide hobbies, age, school, nationality.
            if nationality is not None:
                members = [person for person in members if person.nationality.name == nationality]

        #if user porvide hobbies, age, nationality.
        elif nationality is not None:
            members = [person for person in members if person.nationality.name == nationality]
    #if user provide hobbies, location.
    elif location is not None:
        members = [person for person in members if person.location.name == location]

        #if user provide hobbies, location, school.
        if school is not None:
            members = [person for person in members if person.education.name == school.name]

            #if user provide hobbies, location, school, nationality.
            if nationality is not None:
                members = [person for person in members if person.nationality.name == nationality]

        #if user porvide hobbies, location, nationality.
        elif nationality is not None:
            members = [person for person in members if person.nationality.name == nationality]
    #if user provide hobbies, school.
    elif school is not None:
        members = [person for person in members if person.education.name == school.name]
        #if user provide hobbies, school, nationality.
        if nationality is not None:
            members = [person for person in members if person.nationality.name == nationality]
    #if user provide hobbies, nationality.
    elif nationality is not None:
        members = [person for person in members if person.nationality.name == nationality]



#if user provide age.
elif age is not None:
    members = [person for person in members if person.age>=(age-3) and person.age<=(age+3)]
    #if user provide age, location.
    if location is not None:
        members = [person for person in members if person.location.name == location]
        #if user provide age, location, school.
        if school is not None:
            members = [person for person in members if person.education.name == school.name]

            #if user provide age, location, school, nationality.
            if nationality is not None:
                members = [person for person in members if person.nationality.name == nationality]

        #if user provide age, location, nationality.
        elif nationality is not None:
            members = [person for person in members if person.nationality.name == nationality]

    #if user provide age, school.
    elif school is not None:
        members = [person for person in members if person.education.name == school.name]

        #if user provide age, school, nationality.
        if nationality is not None:
            members = [person for person in members if person.nationality.name == nationality]


    #if user provide age, nationality.
    elif nationality is not None:
        members = [person for person in members if person.nationality.name == nationality]

#if user provide location.
elif location is not None:
    members = [person for person in members if person.location.name == location]

    #if user provide location, school.
    if school is not None:
        members = [person for person in members if person.education.name == school.name]

        #if user provide location, school, nationality.
        if nationality is not None:
            members = [person for person in members if person.nationality.name == nationality]

    #if user provide location, nationality.
    elif nationality is not None:
        members = [person for person in members if person.nationality.name == nationality]

#if user provide school.
elif school is not None:
    members = [person for person in members if person.education.name == school.name]
    #if user provide school, nationality.
    if nationality is not None:
        members = [person for person in members if person.nationality.name == nationality]

#if user provide nationality.
elif nationality is not None:
    members = [person for person in members if person.nationality.name == nationality]
