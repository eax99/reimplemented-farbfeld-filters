# naïvely scale up a farbfeld image to double size
# 2024-07-17 EK
import sys
import os

def duplicate_pixel_row(pixel_bytes):
    return b"".join(pixel_bytes[i+0:i+8] + pixel_bytes[i+0:i+8]
                for i in range(0, len(pixel_bytes), 8))

#with os.fdopen(sys.stdin.fileno(), "rb") as stdin:
#    with os.fdopen(sys.stdout.fileno(), "wb") as stdout:
        # check header signature
magic = sys.stdin.buffer.read(8)
if magic != b'farbfeld':
    raise Exception('Input is not a Farbfeld image')
# read the rest of the header
input_width_bytes = sys.stdin.buffer.read(4)
input_height_bytes = sys.stdin.buffer.read(4)
if input_height_bytes == None:
    raise Exception('Input ended before header end')
input_width = int.from_bytes(input_width_bytes, byteorder='big')
input_height = int.from_bytes(input_height_bytes, byteorder='big')
if input_width >= 2**31 or input_height >= 2**31:
    raise Exception('Image is too big to scale further')
output_width = input_width * 2
output_height = input_height * 2
#print(input_width, "x", input_height, "->", output_width, "x", output_height, file=sys.stderr)
# write out the output header
header_out = (b'farbfeld' +
    output_width.to_bytes(4, byteorder='big') +
    output_height.to_bytes(4, byteorder='big'))
#print(header_out, file=sys.stderr)
sys.stdout.buffer.write(header_out)
# start processing pixels, one input line at a time
for input_row_number in range(input_height):
    input_row = sys.stdin.buffer.read(input_width * 8)
    output_row = duplicate_pixel_row(input_row)
    sys.stdout.buffer.write(output_row + output_row)
    sys.stdout.buffer.flush()


