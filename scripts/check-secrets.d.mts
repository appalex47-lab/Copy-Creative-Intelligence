export const APP_DIRS: readonly string[];
export const PATTERNS: readonly (readonly [string, RegExp])[];
export function scanText(text: string): string[];
export function scanTextWithLines(text: string): { line: number; problem: string }[];
export function scanTree(root?: string): { file: string; line?: number; problem: string }[];
export function listUninspectedArchives(root?: string): string[];
