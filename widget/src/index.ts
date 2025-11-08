/**
 * Fast Lead Widget - Main entry point
 */

import { FastLeadWidget } from './widget';
import type { WidgetConfig } from './types';

// Export types and main class
export { FastLeadWidget };
export type * from './types';

// Global initialization function
declare global {
  interface Window {
    FastLeadWidget: typeof FastLeadWidget;
    fastLeadWidget?: FastLeadWidget;
  }
}

// Auto-initialize if config is provided in window
if (typeof window !== 'undefined') {
  // Expose class globally
  window.FastLeadWidget = FastLeadWidget;

  // Auto-init if config exists
  const config = (window as any).FAST_LEAD_CONFIG as WidgetConfig | undefined;
  if (config) {
    const widget = new FastLeadWidget(config);
    widget.init();
    window.fastLeadWidget = widget;
  }
}
