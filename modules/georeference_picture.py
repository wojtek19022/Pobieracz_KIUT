import subprocess


def georeference_picture(input_picture, output_picture):
    command = (
        f"gdal_translate -of JPEG -a_srs EPSG:4326 {input_picture} {output_picture}"
    )
    process = subprocess.Popen(
        ['bash', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Georeferencing failed with error: {stderr.decode()}")
    return output_picture
