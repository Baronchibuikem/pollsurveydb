
def filter_votes(instance):
    """ 
    Custom function to filter related voters ids 
    And return list of voters username on a poll 

    """
    voter_list = []

    for voter_id in instance:
        for voters_name in voter_id.values():
            if voters_name is None:
                continue
            else:
                voter_list.append(voters_name)

    return voter_list
