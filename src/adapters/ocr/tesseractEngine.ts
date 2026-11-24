import { flagWords, OCR_LANGS, RESOURCE_LIMITS } from '@/domain/resource';
import { fail, ok, type OcrEngine } from '@/services/contracts';

/** Versión del motor, para dejar constancia en cada resultado. */
export const OCR_ENGINE = 'tesseract.js 5.1.1';

/**
 * Motor OCR en el navegador (tesseract.js). TODO se sirve desde la propia app (public/ocr): worker, núcleo WASM y
 * datos de idioma; no hay CDN ni red externa, y tesseract no guarda caché propia (`cacheMethod: 'none'`).
 * Antes de reconocer se hace una copia ampliada EN MEMORIA (nunca se guarda ni reemplaza al original), porque el
 * texto pequeño de los banners se lee mejor con unos ~3200 px de ancho.
 */
export function createTesseractEngine(baseUrl: string = document.baseURI): OcrEngine {
  const at = (p: string) => new URL(`ocr/${p}`, baseUrl).href;
  return {
    async recognize(image, onProgress) {
      let bitmap: ImageBitmap | undefined;
      try {
        bitmap = await createImageBitmap(image);
        const scale = Math.min(4, Math.max(1, 3200 / bitmap.width));
        const w = Math.round(bitmap.width * scale);
        const h = Math.round(bitmap.height * scale);
        if (w * h > 36_000_000)
          return fail('validation_error', 'La imagen es demasiado grande para el OCR.');
        const canvas = document.createElement('canvas');
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext('2d');
        if (!ctx) return fail('unavailable', 'El navegador no pudo preparar la imagen.');
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, w, h);
        ctx.drawImage(bitmap, 0, 0, w, h);
        const { createWorker } = await import('tesseract.js');
        const worker = await createWorker(OCR_LANGS, 1, {
          workerPath: at('worker.min.js'),
          corePath: at('core'),
          langPath: at('lang'),
          workerBlobURL: false,
          cacheMethod: 'none',
          gzip: true,
          logger: (m: { progress: number }) => onProgress?.(m.progress),
        });
        try {
          await worker.setParameters({ tessedit_pageseg_mode: '11' as never });
          const { data } = await worker.recognize(canvas, {}, { text: true, blocks: true });
          const raw: { text: string; confidence: number }[] = [];
          for (const b of data.blocks ?? [])
            for (const p of b.paragraphs)
              for (const l of p.lines) for (const wd of l.words) raw.push(wd);
          return ok({
            text: data.text.trim(),
            words: flagWords(raw, RESOURCE_LIMITS.lowConfidence),
          });
        } finally {
          await worker.terminate();
        }
      } catch {
        return fail('unavailable', 'No se pudo ejecutar el OCR en este navegador.');
      } finally {
        bitmap?.close();
      }
    },
  };
}
