/**
 * API client for Fast Lead backend
 */

import type { CreateLeadRequest, CreateLeadResponse } from './types';

export class FastLeadAPI {
  private apiUrl: string;
  private tenantId: number;

  constructor(apiUrl: string, tenantId: number) {
    this.apiUrl = apiUrl.replace(/\/$/, ''); // Remove trailing slash
    this.tenantId = tenantId;
  }

  /**
   * Create a new lead
   */
  async createLead(data: CreateLeadRequest): Promise<CreateLeadResponse> {
    const url = `${this.apiUrl}/api/v1/leads`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Tenant-Id': String(this.tenantId),
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return response.json();
  }
}
