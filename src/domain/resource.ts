import { invalid, valid, type Validation } from './validation';

/**
 * Recurso visual (S3.3; funciones 1 y 2 de la Fase 3): imagen cargada por la persona más el texto que el OCR detectó.
 * Reglas del documento de Fase 3: el original NUNCA se modifica; lo "detectado" por el OCR se distingue de lo
 * "validado por persona"; las palabras dudosas se marcan y nunca se completan por inferencia; un recurso NO es
 * automáticamente una Pieza creativa. Los recursos viven solo en IndexedDB y NO van en el respaldo JSON (las imágenes
 * no caben en el límite de 5 MB): la pantalla y los documentos lo dicen.
 *
 * SUPUESTOS de Claude (reversibles; el dueño dijo que formatos y tamaños los fija a mano): formatos PNG, JPEG y WebP;
 * máximo 5 MB y 25 millones de píxeles por imagen; hasta 200 recursos; umbral de confianza baja 60 (de 0 a 100).
 */
export const RESOURCE_LIMITS = {
  mimes: ['image/png', 'image/jpeg', 'image/webp'] as readonly string[],
  maxBytes: 5 * 1024 * 1024,
  maxPixels: 25_000_000,
  maxResources: 200,
  maxNameLength: 120,
  maxReviewedLength: 20_000,
  lowConfidence: 60,
  maxWords: 3_000,
} as const;

export const RESOURCE_ID = /^res_[A-Za-z0-9_-]{8,64}$/;
export const OCR_LANGS = 'spa+eng';

/** Palabra detectada. `uncertain` = confianza menor al umbral: no se corrige ni se completa. */
export interface OcrWord {
  readonly text: string;
  readonly confidence: number;
  readonly uncertain: boolean;
}

export interface OcrResult {
  readonly engine: string;
  readonly langs: string;
  readonly threshold: number;
  readonly ranAt: string;
  /** Texto tal como lo devolvió el motor (detectado, NO validado). */
  readonly text: string;
  readonly words: readonly OcrWord[];
}

export interface ResourceRecord {
  readonly id: string; // res_…
  readonly name: string;
  readonly mime: string;
  readonly size: number;
  readonly width: number;
  readonly height: number;
  readonly createdAt: string;
  readonly blob: Blob;
  readonly ocr?: OcrResult;
  /** Texto confirmado por una persona (puede diferir del detectado). Solo existe si alguien lo guardó. */
  readonly reviewedText?: string;
  readonly reviewedAt?: string;
}

const MB = (n: number) => `${String(Math.round((n / 1024 / 1024) * 10) / 10)} MB`;

export function validateResourceFile(file: {
  readonly name: string;
  readonly type: string;
  readonly size: number;
}): Validation<{ readonly name: string }> {
  if (!RESOURCE_LIMITS.mimes.includes(file.type))
    return invalid('Formato no admitido. Usa PNG, JPEG o WebP.');
  if (file.size <= 0) return invalid('El archivo está vacío.');
  if (file.size > RESOURCE_LIMITS.maxBytes)
    return invalid(
      `La imagen pesa ${MB(file.size)}; el máximo es ${MB(RESOURCE_LIMITS.maxBytes)}.`,
    );
  const name = [...file.name.trim()].slice(0, RESOURCE_LIMITS.maxNameLength).join('');
  return valid({ name: name.length > 0 ? name : 'Imagen sin nombre' });
}

export function validateDimensions(width: number, height: number): Validation<null> {
  if (
    !Number.isInteger(width) ||
    !Number.isInteger(height) ||
    width < 1 ||
    height < 1 ||
    width * height > RESOURCE_LIMITS.maxPixels
  )
    return invalid('La imagen no se pudo leer o tiene demasiados píxeles.');
  return valid(null);
}

/** Marca como dudosas las palabras con confianza menor al umbral. No altera el texto de ninguna. */
export function flagWords(
  raw: readonly { readonly text: string; readonly confidence: number }[],
  threshold: number = RESOURCE_LIMITS.lowConfidence,
): readonly OcrWord[] {
  const out: OcrWord[] = [];
  for (const w of raw) {
    const text = w.text.trim();
    if (text.length === 0) continue;
    const confidence = Math.min(100, Math.max(0, Math.round(w.confidence)));
    out.push({ text, confidence, uncertain: confidence < threshold });
    if (out.length >= RESOURCE_LIMITS.maxWords) break;
  }
  return out;
}

export const countUncertain = (words: readonly OcrWord[]): number =>
  words.filter((w) => w.uncertain).length;

export const compareResourcesNewestFirst = (a: ResourceRecord, b: ResourceRecord): number =>
  a.createdAt < b.createdAt ? 1 : a.createdAt > b.createdAt ? -1 : a.id < b.id ? 1 : -1;

const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));

function validateOcr(raw: unknown): Validation<OcrResult> {
  const bad = invalid<OcrResult>('El resultado del OCR no es válido.');
  if (
    !isObject(raw) ||
    typeof raw['engine'] !== 'string' ||
    typeof raw['langs'] !== 'string' ||
    typeof raw['threshold'] !== 'number' ||
    !isIso(raw['ranAt']) ||
    typeof raw['text'] !== 'string' ||
    raw['text'].length > 100_000 ||
    !Array.isArray(raw['words']) ||
    raw['words'].length > RESOURCE_LIMITS.maxWords
  )
    return bad;
  const words: OcrWord[] = [];
  for (const w of raw['words'] as unknown[]) {
    if (
      !isObject(w) ||
      typeof w['text'] !== 'string' ||
      typeof w['confidence'] !== 'number' ||
      typeof w['uncertain'] !== 'boolean'
    )
      return bad;
    words.push({ text: w['text'], confidence: w['confidence'], uncertain: w['uncertain'] });
  }
  return valid({
    engine: raw['engine'],
    langs: raw['langs'],
    threshold: raw['threshold'],
    ranAt: raw['ranAt'],
    text: raw['text'],
    words,
  });
}

export function validateResourceRecord(raw: unknown): Validation<ResourceRecord> {
  const bad = invalid<ResourceRecord>('El recurso guardado no es válido.');
  if (!isObject(raw)) return bad;
  const id = raw['id'];
  const name = raw['name'];
  if (typeof id !== 'string' || !RESOURCE_ID.test(id)) return bad;
  if (
    typeof name !== 'string' ||
    name.length === 0 ||
    [...name].length > RESOURCE_LIMITS.maxNameLength
  )
    return bad;
  if (typeof raw['mime'] !== 'string' || !RESOURCE_LIMITS.mimes.includes(raw['mime'])) return bad;
  const size = raw['size'];
  if (
    typeof size !== 'number' ||
    !Number.isInteger(size) ||
    size < 1 ||
    size > RESOURCE_LIMITS.maxBytes
  )
    return bad;
  const w = raw['width'];
  const h = raw['height'];
  if (typeof w !== 'number' || typeof h !== 'number' || !validateDimensions(w, h).ok) return bad;
  if (!isIso(raw['createdAt']) || !(raw['blob'] instanceof Blob)) return bad;
  let ocr: OcrResult | undefined;
  if (raw['ocr'] !== undefined) {
    const o = validateOcr(raw['ocr']);
    if (!o.ok) return bad;
    ocr = o.value;
  }
  const rt = raw['reviewedText'];
  if (rt !== undefined && (typeof rt !== 'string' || rt.length > RESOURCE_LIMITS.maxReviewedLength))
    return bad;
  if ((rt === undefined) !== (raw['reviewedAt'] === undefined)) return bad;
  if (raw['reviewedAt'] !== undefined && !isIso(raw['reviewedAt'])) return bad;
  return valid({
    id,
    name,
    mime: raw['mime'],
    size,
    width: w,
    height: h,
    createdAt: raw['createdAt'],
    blob: raw['blob'],
    ...(ocr ? { ocr } : {}),
    ...(typeof rt === 'string'
      ? { reviewedText: rt, reviewedAt: raw['reviewedAt'] as string }
      : {}),
  });
}
