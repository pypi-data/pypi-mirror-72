import click
import qrcode

def get_error_correction(error_correction):
    if error_correction in [0, 1, 2, 3]: # defined values are [0, 1, 2, 3], so we just accept it.
        return error_correction
    if error_correction == "7":
        return qrcode.constants.ERROR_CORRECT_L
    elif error_correction == "15":
        return qrcode.constants.ERROR_CORRECT_M
    elif error_correction == "25":
        return qrcode.constants.ERROR_CORRECT_Q
    else:
        return qrcode.constants.ERROR_CORRECT_H

def gen(output, message, version=None, error_correction=30, box_size=10, border=4, fill_color="black", back_color="white"):
    error_correction = get_error_correction(error_correction)
    gen = qrcode.QRCode(version=version, error_correction=error_correction, box_size=box_size, border=border)
    gen.add_data(message)
    img = gen.make_image(fill_color=fill_color, back_color=back_color)
    img.save(output)
    return img

@click.command()
@click.option("-o", "--output", help="Output file name.", required=True)
@click.option("-v", "--version", type=int, help="An integer from 1 to 40 that controls the size of the QR Code. The smallest, version 1, is a 21x21 matrix. Default to None, means making the code to determine the size automatically.")
@click.option("-c", "--error-correction", type=click.Choice(["7", "15", "25", "30"]), default="30", help="controls the error correction used for the QR Code. Default to 30.")
@click.option("-s", "--box-size", type=int, default=10, help="controls how many pixels each 'box' of the QR code is. Default to 10.")
@click.option("-b", "--border", type=int, default=4, help="controls how many boxes thick the border should be (the default is 4, which is the minimum according to the specs).")
@click.option("-f", "--fill-color", default="black", help="Named color or #RGB color accepted. Default to named color 'black'.")
@click.option("-b", "--back-color", default="white", help="Named color or #RGB color accepted. Default to named color 'white'.")
@click.argument("message", nargs=1, required=True)
def main(output, message, version, error_correction, box_size, border, fill_color, back_color):
    gen(output, message, version, error_correction, box_size, border, fill_color, back_color)


if __name__ == "__main__":
    main()
