if __name__ == '__main__':
    print("Run the main.py file instead of this one.")
    exit(1)

from pprint import pprint
from os import path

root_dir = path.abspath(path.dirname(__file__))
backend_dir = path.join(root_dir, "backend")
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]


def stripe(fn):
    fstripes = []
    f = open(fn, 'rb').read()

    # Split the file into stripes of length 64 / 64 bytes.
    for i in range(0, len(f), 64):
        fstripes.append(f[i:i + 64])
    return fstripes


# Copilot did this one, but I'm not sure how it works, yet.
# def parity(blocks):
# Calculate the parity
#    parity = []
#    for i in range(len(stripes)):
#        parity.append(sum(map(ord, stripes[i])) % 2)
#    return parity


def write_chunk(chunk, du):
    # Write chunk data to the backend.
    # Name each chunk in this format: "AA", "AB", "AC", etc.
    for a in alphabet:
        for b in alphabet:
            for c in alphabet:
                for d in alphabet:
                    for i in range(du):
                        drive_num = i + 1
                        fp = path.join(backend_dir, "DRIVE-" + str(drive_num), a + b + c + d)
                        if not path.exists(fp):
                            with open(fp, 'wb') as f:
                                f.write(chunk)
                                return True
    return False


def r0(fnl, du):
    stripes = []
    for fn in fnl:
        stripes.append(stripe(fn))

    for i in range(len(stripes)):
        for j in range(len(stripes[i])):
            write_chunk(stripes[i][j], du)
    return True


def r1(fnl):
    return True


def r2(fnl):
    return True


def r3(fnl):
    return True


def r4(fnl):
    return True


def r5(fnl):
    return True


def r6(fnl):
    return True


def r01(fnl):
    return True


def r03(fnl):
    return True


def r10(fnl):
    return True


def r50(fnl):
    return True


def r60(fnl):
    return True


def r100(fnl):
    return True