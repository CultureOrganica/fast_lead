/**
 * Widget UI components
 */

import type { WidgetConfig, WidgetState, LeadChannel } from './types';
import { getStyles } from './styles';
import { escapeHtml, generateId } from './utils';

export class WidgetUI {
  private config: WidgetConfig;
  private state: WidgetState;
  private container: HTMLDivElement | null = null;
  private button: HTMLButtonElement | null = null;
  private popup: HTMLDivElement | null = null;
  private styles: ReturnType<typeof getStyles>;

  constructor(config: WidgetConfig, state: WidgetState) {
    this.config = config;
    this.state = state;
    this.styles = getStyles(config.primaryColor);
  }

  /**
   * Initialize and render the widget
   */
  render(): void {
    // Inject animations
    this.injectStyles();

    // Create container
    this.container = document.createElement('div');
    this.container.id = 'fast-lead-widget';
    this.container.setAttribute('style', this.styles.container);

    // Create trigger button
    this.button = this.createButton();
    this.container.appendChild(this.button);

    // Append to body
    document.body.appendChild(this.container);
  }

  /**
   * Create trigger button
   */
  private createButton(): HTMLButtonElement {
    const button = document.createElement('button');
    button.id = 'fl-button';
    button.className = 'fl-button';
    button.setAttribute('style', this.styles.button);
    button.setAttribute('aria-label', 'Open contact form');
    button.innerHTML = '💬';

    // Hover effect
    button.addEventListener('mouseenter', () => {
      button.setAttribute('style', this.styles.button + this.styles.buttonHover);
    });

    button.addEventListener('mouseleave', () => {
      button.setAttribute('style', this.styles.button);
    });

    // Click handler
    button.addEventListener('click', () => {
      this.togglePopup();
    });

    return button;
  }

  /**
   * Toggle popup visibility
   */
  togglePopup(): void {
    if (this.state.isOpen) {
      this.closePopup();
    } else {
      this.openPopup();
    }
  }

  /**
   * Open popup
   */
  private openPopup(): void {
    this.state.isOpen = true;

    if (this.popup) {
      this.popup.style.display = 'block';
      return;
    }

    this.popup = this.createPopup();
    this.container?.appendChild(this.popup);
  }

  /**
   * Close popup
   */
  closePopup(): void {
    this.state.isOpen = false;
    if (this.popup) {
      this.popup.style.display = 'none';
    }
  }

  /**
   * Create popup form
   */
  private createPopup(): HTMLDivElement {
    const popup = document.createElement('div');
    popup.id = 'fl-popup';
    popup.className = 'fl-popup';
    popup.setAttribute('style', this.styles.popup);

    popup.innerHTML = `
      <div style="${this.styles.header}">
        <h3 style="${this.styles.headerTitle}">${escapeHtml(this.config.formTitle || 'Связаться с нами')}</h3>
        <button id="fl-close" style="${this.styles.closeButton}" aria-label="Close">×</button>
      </div>
      <form id="fl-form" style="${this.styles.form}">
        ${this.config.formDescription ? `<p style="${this.styles.description}">${escapeHtml(this.config.formDescription)}</p>` : ''}
        <div id="fl-error" style="display: none;"></div>
        <div id="fl-form-content"></div>
      </form>
    `;

    // Close button handler
    const closeBtn = popup.querySelector('#fl-close');
    closeBtn?.addEventListener('click', () => this.closePopup());

    // Render form content
    const formContent = popup.querySelector('#fl-form-content');
    if (formContent) {
      formContent.innerHTML = this.renderFormFields();
    }

    return popup;
  }

  /**
   * Render form fields based on configuration
   */
  private renderFormFields(): string {
    const fields = this.config.fields || {
      name: true,
      phone: true,
      email: true,
    };

    let html = '';

    // Name field
    if (fields.name !== false) {
      html += `
        <div style="${this.styles.fieldGroup}">
          <label for="fl-name" style="${this.styles.label}">Имя *</label>
          <input
            type="text"
            id="fl-name"
            name="name"
            required
            placeholder="Ваше имя"
            style="${this.styles.input}"
          />
        </div>
      `;
    }

    // Phone field
    if (fields.phone !== false) {
      html += `
        <div style="${this.styles.fieldGroup}">
          <label for="fl-phone" style="${this.styles.label}">Телефон ${this.config.channel === 'sms' ? '*' : ''}</label>
          <input
            type="tel"
            id="fl-phone"
            name="phone"
            ${this.config.channel === 'sms' ? 'required' : ''}
            placeholder="+7 (999) 123-45-67"
            style="${this.styles.input}"
          />
        </div>
      `;
    }

    // Email field
    if (fields.email !== false) {
      html += `
        <div style="${this.styles.fieldGroup}">
          <label for="fl-email" style="${this.styles.label}">Email ${this.config.channel === 'email' ? '*' : ''}</label>
          <input
            type="email"
            id="fl-email"
            name="email"
            ${this.config.channel === 'email' ? 'required' : ''}
            placeholder="your@email.com"
            style="${this.styles.input}"
          />
        </div>
      `;
    }

    // VK ID field
    if (fields.vkId) {
      html += `
        <div style="${this.styles.fieldGroup}">
          <label for="fl-vk-id" style="${this.styles.label}">VK ID ${this.config.channel === 'vk' ? '*' : ''}</label>
          <input
            type="text"
            id="fl-vk-id"
            name="vk_id"
            ${this.config.channel === 'vk' ? 'required' : ''}
            placeholder="vk.com/yourid"
            style="${this.styles.input}"
          />
        </div>
      `;
    }

    // Consent checkboxes
    html += `
      <div style="${this.styles.fieldGroup}">
        <label style="${this.styles.checkboxLabel}">
          <input type="checkbox" id="fl-gdpr" name="gdpr" required style="${this.styles.checkbox}" />
          <span>Я согласен на обработку персональных данных *</span>
        </label>
      </div>
      <div style="${this.styles.fieldGroup}">
        <label style="${this.styles.checkboxLabel}">
          <input type="checkbox" id="fl-marketing" name="marketing" style="${this.styles.checkbox}" />
          <span>Я согласен на получение маркетинговых сообщений</span>
        </label>
      </div>
    `;

    // Submit button
    html += `
      <button
        type="submit"
        id="fl-submit"
        style="${this.styles.submitButton}"
      >
        ${escapeHtml(this.config.buttonText || 'Отправить')}
      </button>
    `;

    return html;
  }

  /**
   * Show loading state
   */
  showLoading(): void {
    this.state.isLoading = true;
    const submitBtn = document.querySelector('#fl-submit') as HTMLButtonElement;
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.setAttribute('style', this.styles.submitButton + this.styles.submitButtonDisabled);
      submitBtn.innerHTML = `<div style="${this.styles.spinner}"></div>`;
    }
  }

  /**
   * Hide loading state
   */
  hideLoading(): void {
    this.state.isLoading = false;
    const submitBtn = document.querySelector('#fl-submit') as HTMLButtonElement;
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.setAttribute('style', this.styles.submitButton);
      submitBtn.textContent = this.config.buttonText || 'Отправить';
    }
  }

  /**
   * Show error message
   */
  showError(message: string): void {
    this.state.error = message;
    const errorDiv = document.querySelector('#fl-error');
    if (errorDiv) {
      errorDiv.setAttribute('style', this.styles.errorMessage);
      errorDiv.textContent = message;
    }
  }

  /**
   * Hide error message
   */
  hideError(): void {
    this.state.error = undefined;
    const errorDiv = document.querySelector('#fl-error');
    if (errorDiv) {
      errorDiv.setAttribute('style', 'display: none;');
      errorDiv.textContent = '';
    }
  }

  /**
   * Show success message
   */
  showSuccess(): void {
    this.state.isSubmitted = true;
    const formContent = document.querySelector('#fl-form-content');
    if (formContent) {
      formContent.innerHTML = `
        <div style="${this.styles.successMessage}">
          ✓ ${escapeHtml(this.config.successMessage || 'Спасибо! Мы свяжемся с вами в ближайшее время.')}
        </div>
      `;
    }
  }

  /**
   * Inject CSS animations
   */
  private injectStyles(): void {
    const styleId = 'fl-styles';
    if (document.getElementById(styleId)) return;

    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = this.styles.animations;
    document.head.appendChild(style);
  }

  /**
   * Clean up and remove widget from DOM
   */
  destroy(): void {
    this.container?.remove();
    const styles = document.getElementById('fl-styles');
    styles?.remove();
  }
}
