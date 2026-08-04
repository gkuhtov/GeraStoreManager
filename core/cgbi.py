import struct
import zlib


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def convert_cgbi(input_file, output_file):
    with open(input_file, "rb") as f:
        data = f.read()

    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("Файл не является PNG")

    pos = 8
    chunks = []
    idat_data = b""
    width = None
    height = None
    color_type = None
    bit_depth = None
    cgbi = False

    while pos < len(data):

        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        chunk_data = data[pos + 8:pos + 8 + length]

        pos += 12 + length

        if chunk_type == b"CgBI":
            cgbi = True
            continue

        if chunk_type == b"IHDR":

            width, height, bit_depth, color_type, compression, filt, interlace = struct.unpack(
                ">IIBBBBB",
                chunk_data
            )

            chunks.append(
                (chunk_type, chunk_data)
            )

        elif chunk_type == b"IDAT":

            idat_data += chunk_data

        elif chunk_type == b"IEND":

            chunks.append(
                (chunk_type, chunk_data)
            )

        else:

            chunks.append(
                (chunk_type, chunk_data)
            )

    if not cgbi:
        raise ValueError("Это обычный PNG, CgBI не найден")

    if bit_depth != 8:
        raise ValueError(
            f"Неподдерживаемая глубина цвета: {bit_depth}"
        )

    if color_type not in (2, 6):
        raise ValueError(
            f"Неподдерживаемый тип цвета: {color_type}"
        )

    channels = 4 if color_type == 6 else 3
    row_size = width * channels

    raw = zlib.decompress(
        idat_data,
        -15
    )

    expected = height * (row_size + 1)

    if len(raw) != expected:
        raise ValueError(
            f"Неверный размер данных: {len(raw)}, ожидалось {expected}"
        )

    output_raw = bytearray()

    previous = bytearray(row_size)

    pos = 0

    for y in range(height):

        filter_type = raw[pos]
        pos += 1

        row = bytearray(
            raw[pos:pos + row_size]
        )

        pos += row_size

        recon = bytearray(row_size)

        for x in range(row_size):

            left = (
                recon[x - channels]
                if x >= channels
                else 0
            )

            up = previous[x]

            up_left = (
                previous[x - channels]
                if x >= channels
                else 0
            )

            value = row[x]

            if filter_type == 0:
                result = value

            elif filter_type == 1:
                result = value + left

            elif filter_type == 2:
                result = value + up

            elif filter_type == 3:
                result = value + ((left + up) // 2)

            elif filter_type == 4:

                p = left + up - up_left

                pa = abs(p - left)
                pb = abs(p - up)
                pc = abs(p - up_left)

                if pa <= pb and pa <= pc:
                    predictor = left
                elif pb <= pc:
                    predictor = up
                else:
                    predictor = up_left

                result = value + predictor

            else:
                raise ValueError(
                    f"Неизвестный PNG filter: {filter_type}"
                )

            recon[x] = result & 255

        # CgBI хранит RGB как BGR.
        for x in range(0, row_size, channels):

            recon[x], recon[x + 2] = (
                recon[x + 2],
                recon[x]
            )

        output_raw.append(0)
        output_raw.extend(recon)

        previous = recon

    compressed = zlib.compress(
        bytes(output_raw),
        9
    )

    def make_chunk(chunk_type, chunk_data):

        crc = zlib.crc32(
            chunk_type + chunk_data
        ) & 0xffffffff

        return (
            struct.pack(">I", len(chunk_data))
            + chunk_type
            + chunk_data
            + struct.pack(">I", crc)
        )

    result = bytearray(PNG_SIGNATURE)

    ihdr = struct.pack(
        ">IIBBBBB",
        width,
        height,
        bit_depth,
        color_type,
        0,
        0,
        0
    )

    result.extend(
        make_chunk(
            b"IHDR",
            ihdr
        )
    )

    result.extend(
        make_chunk(
            b"IDAT",
            compressed
        )
    )

    result.extend(
        make_chunk(
            b"IEND",
            b""
        )
    )

    with open(output_file, "wb") as f:
        f.write(result)

    return {
        "width": width,
        "height": height,
        "output": output_file
    }
