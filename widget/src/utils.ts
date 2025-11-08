/**
 * Utility functions for widget
 */

import type { UTMParams } from './types';

/**
 * Extract UTM parameters from URL
 */
export function extractUTMParams(): UTMParams | undefined {
  if (typeof window === 'undefined') return undefined;

  const params = new URLSearchParams(window.location.search);
  const utm: UTMParams = {};

  const utmSource = params.get('utm_source');
  const utmMedium = params.get('utm_medium');
  const utmCampaign = params.get('utm_campaign');
  const utmContent = params.get('utm_content');
  const utmTerm = params.get('utm_term');

  if (utmSource) utm.source = utmSource;
  if (utmMedium) utm.medium = utmMedium;
  if (utmCampaign) utm.campaign = utmCampaign;
  if (utmContent) utm.content = utmContent;
  if (utmTerm) utm.term = utmTerm;

  return Object.keys(utm).length > 0 ? utm : undefined;
}

/**
 * Get source URL (current page)
 */
export function getSourceUrl(): string {
  if (typeof window === 'undefined') return '';
  return window.location.href;
}

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate phone format (Russian format)
 */
export function isValidPhone(phone: string): boolean {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');

  // Russian phone numbers: +7XXXXXXXXXX (11 digits) or 8XXXXXXXXXX
  return cleaned.length === 11 && (cleaned[0] === '7' || cleaned[0] === '8');
}

/**
 * Format phone number to E.164 format (+7XXXXXXXXXX)
 */
export function formatPhone(phone: string): string {
  const cleaned = phone.replace(/\D/g, '');

  // Convert 8XXXXXXXXXX to 7XXXXXXXXXX
  if (cleaned[0] === '8' && cleaned.length === 11) {
    return '+7' + cleaned.slice(1);
  }

  // Add + if not present
  if (cleaned[0] === '7' && cleaned.length === 11) {
    return '+' + cleaned;
  }

  return phone;
}

/**
 * Escape HTML to prevent XSS
 */
export function escapeHtml(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Generate unique ID
 */
export function generateId(): string {
  return `fl-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
