def fretboard(s):

    def order(s):
        s = s.lower()
        notes = 'abcdefg'
        noteind = notes.find(s)
        reorder = str(notes[noteind:] + notes[:noteind] + s)
        return reorder

    if not isinstance(s, str):
        raise TypeError ('Must be a guitar string!')
    if s not in 'edgbaEDGBA':
        raise Exception('Please choose e,a,d,g or b!')

    frets = 0

    for t in order(s):
        if t in 'be':
            frets += 1
        if t in 'acfdg':
            frets += 2
        print(frets)
