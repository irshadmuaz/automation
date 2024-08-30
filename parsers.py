# Parses the copied vitals and medications from excel sheet
# take = 3 for medical, 1 for vitals
def parse_records(med, take):
    try:
        lst = eval(med)
        format = []
        for r in lst:
            format.append(' '.join(r[:len(r)-take]))
        return '\n'.join(format)
    except:
        return 'error'

def parse_name(name):
    return ' '.join(name.split(' ')[:-1])