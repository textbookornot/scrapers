#######################################################################
#                              functions                              #
#######################################################################

def clean_string(dirty_string):
    return " ".join(dirty_string.split()).replace("\n", " ").replace("\t", "").strip()
