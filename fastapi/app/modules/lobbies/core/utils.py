from nanoid import generate

def generate_lobby_code():
    alphabet = 'ACDEFGHJKLMNPQRTUVWXY34679'
    return generate(alphabet, size=6)
