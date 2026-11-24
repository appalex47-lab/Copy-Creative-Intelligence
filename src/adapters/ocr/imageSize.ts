/** Lee el ancho y alto de una imagen sin modificarla. `null` si el navegador no la puede decodificar. */
export async function readImageSize(
  blob: Blob,
): Promise<{ readonly width: number; readonly height: number } | null> {
  try {
    const bmp = await createImageBitmap(blob);
    const size = { width: bmp.width, height: bmp.height };
    bmp.close();
    return size;
  } catch {
    return null;
  }
}
