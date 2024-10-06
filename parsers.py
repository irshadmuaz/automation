# Parses the copied vitals and medications from excel sheet
# take = 3 for medical, 1 for vitals
def parse_records(med, take, header=None):
    try:
        lst = eval(med)
        format = []
        for r in lst:
            format.append(' '.join(r[:len(r)-take]))
        if header:
            format[0] = header
        return '\n'.join(format)
    except:
        return ''

def parse_name(name):
    splits = name.split(' ')
    if len(splits) > 2:
        splits.pop()
    return ' '.join(splits)

def to_consider(val):
    return to_consider in ('f','n')