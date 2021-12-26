

def has_group(user,group):
    return user.groups.filter(name=group).exists()

def has_permisions(user):
    pass
    