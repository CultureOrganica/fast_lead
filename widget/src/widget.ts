/**
 * Fast Lead Widget - Main class
 */

import type {
  WidgetConfig,
  WidgetState,
  CreateLeadRequest,
  CreateLeadResponse,
} from './types';
import { FastLeadAPI } from './api';
import { WidgetUI } from './ui';
import {
  extractUTMParams,
  getSourceUrl,
  isValidEmail,
  isValidPhone,
  formatPhone,
} from './utils';

export class FastLeadWidget {
  private config: WidgetConfig;
  private state: WidgetState;
  private api: FastLeadAPI;
  private ui: WidgetUI;

  constructor(config: WidgetConfig) {
    // Validate required config
    if (!config.apiUrl) {
      throw new Error('FastLeadWidget: apiUrl is required');
    }
    if (!config.tenantId) {
      throw new Error('FastLeadWidget: tenantId is required');
    }

    // Set defaults
    this.config = {
      channel: 'web',
      position: 'bottom-right',
      theme: 'light',
      primaryColor: '#2563eb',
      collectUtm: true,
      collectSource: true,
      ...config,
    };

    // Initialize state
    this.state = {
      isOpen: false,
      isLoading: false,
      isSubmitted: false,
    };

    // Initialize API client
    this.api = new FastLeadAPI(this.config.apiUrl, this.config.tenantId);

    // Initialize UI
    this.ui = new WidgetUI(this.config, this.state);
  }

  /**
   * Initialize the widget
   */
  init(): void {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.render());
    } else {
      this.render();
    }
  }

  /**
   * Render the widget
   */
  private render(): void {
    this.ui.render();
    this.attachEventListeners();
  }

  /**
   * Attach event listeners
   */
  private attachEventListeners(): void {
    // Form submit handler
    const form = document.querySelector('#fl-form') as HTMLFormElement;
    if (form) {
      form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    // Input focus handlers for styling
    const inputs = document.querySelectorAll('#fl-form input');
    inputs.forEach((input) => {
      input.addEventListener('focus', (e) => {
        const target = e.target as HTMLInputElement;
        target.style.outline = 'none';
        target.style.borderColor = this.config.primaryColor || '#2563eb';
        target.style.boxShadow = `0 0 0 3px ${this.config.primaryColor || '#2563eb'}20`;
      });

      input.addEventListener('blur', (e) => {
        const target = e.target as HTMLInputElement;
        target.style.borderColor = '#d1d5db';
        target.style.boxShadow = 'none';
      });
    });
  }

  /**
   * Handle form submission
   */
  private async handleSubmit(e: Event): Promise<void> {
    e.preventDefault();

    // Clear previous errors
    this.ui.hideError();

    // Get form data
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);

    const name = formData.get('name') as string;
    const phone = formData.get('phone') as string;
    const email = formData.get('email') as string;
    const vkId = formData.get('vk_id') as string;
    const gdpr = formData.get('gdpr') === 'on';
    const marketing = formData.get('marketing') === 'on';

    // Validate
    if (!name || name.trim().length === 0) {
      this.ui.showError('Пожалуйста, введите ваше имя');
      return;
    }

    // Check that at least one contact method is provided
    if (!phone && !email && !vkId) {
      this.ui.showError('Пожалуйста, укажите хотя бы один способ связи');
      return;
    }

    // Validate email if provided
    if (email && !isValidEmail(email)) {
      this.ui.showError('Пожалуйста, введите корректный email');
      return;
    }

    // Validate phone if provided
    if (phone && !isValidPhone(phone)) {
      this.ui.showError('Пожалуйста, введите корректный номер телефона');
      return;
    }

    // Channel-specific validation
    if (this.config.channel === 'sms' && !phone) {
      this.ui.showError('Для SMS-канала необходим номер телефона');
      return;
    }

    if (this.config.channel === 'email' && !email) {
      this.ui.showError('Для Email-канала необходим адрес электронной почты');
      return;
    }

    if (this.config.channel === 'vk' && !vkId) {
      this.ui.showError('Для VK-канала необходим VK ID');
      return;
    }

    if (this.config.channel === 'whatsapp' && !marketing) {
      this.ui.showError(
        'Для WhatsApp необходимо согласие на маркетинговые сообщения'
      );
      return;
    }

    if (!gdpr) {
      this.ui.showError('Необходимо согласие на обработку персональных данных');
      return;
    }

    // Build request
    const request: CreateLeadRequest = {
      name: name.trim(),
      channel: this.config.channel!,
      consent: {
        gdpr,
        marketing,
      },
    };

    // Add contact methods
    if (phone) {
      request.phone = formatPhone(phone);
    }
    if (email) {
      request.email = email.trim();
    }
    if (vkId) {
      request.vk_id = vkId.trim();
    }

    // Add UTM parameters
    if (this.config.collectUtm) {
      const utm = extractUTMParams();
      if (utm) {
        request.utm = utm;
      }
    }

    // Add source URL
    if (this.config.collectSource) {
      request.source = getSourceUrl();
    }

    // Submit
    this.ui.showLoading();

    try {
      const response = await this.api.createLead(request);

      // Success
      this.ui.hideLoading();
      this.ui.showSuccess();

      // Call success callback if provided
      if (this.config.onSuccess) {
        this.config.onSuccess(response);
      }

      // Auto-close after 3 seconds
      setTimeout(() => {
        this.ui.closePopup();
      }, 3000);
    } catch (error) {
      // Error
      this.ui.hideLoading();

      const errorMessage =
        error instanceof Error
          ? error.message
          : this.config.errorMessage || 'Произошла ошибка. Попробуйте позже.';

      this.ui.showError(errorMessage);

      // Call error callback if provided
      if (this.config.onError && error instanceof Error) {
        this.config.onError(error);
      }
    }
  }

  /**
   * Open the widget popup
   */
  open(): void {
    this.ui.togglePopup();
  }

  /**
   * Close the widget popup
   */
  close(): void {
    this.ui.closePopup();
  }

  /**
   * Destroy the widget and clean up
   */
  destroy(): void {
    this.ui.destroy();
  }
}
