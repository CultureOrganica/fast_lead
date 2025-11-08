/**
 * Widget configuration types
 */

export type LeadChannel =
  | 'web'
  | 'sms'
  | 'email'
  | 'vk'
  | 'telegram'
  | 'whatsapp'
  | 'instagram'
  | 'max';

export interface WidgetConfig {
  // Required
  apiUrl: string;
  tenantId: number;

  // Optional
  channel?: LeadChannel;
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  theme?: 'light' | 'dark';
  primaryColor?: string;

  // Customization
  buttonText?: string;
  formTitle?: string;
  formDescription?: string;
  successMessage?: string;
  errorMessage?: string;

  // Fields configuration
  fields?: {
    name?: boolean;
    phone?: boolean;
    email?: boolean;
    vkId?: boolean;
  };

  // Auto-collect
  collectUtm?: boolean;
  collectSource?: boolean;

  // Callbacks
  onSuccess?: (response: CreateLeadResponse) => void;
  onError?: (error: Error) => void;
}

export interface UTMParams {
  source?: string;
  medium?: string;
  campaign?: string;
  content?: string;
  term?: string;
}

export interface ConsentParams {
  gdpr: boolean;
  marketing: boolean;
}

export interface CreateLeadRequest {
  name: string;
  phone?: string;
  email?: string;
  vk_id?: string;
  channel: LeadChannel;
  source?: string;
  utm?: UTMParams;
  consent: ConsentParams;
  payload?: Record<string, any>;
}

export interface LeadResponse {
  id: number;
  name: string;
  phone?: string;
  email?: string;
  vk_id?: string;
  channel: LeadChannel;
  status: string;
  created_at: string;
  tenant_id: number;
}

export interface CreateLeadResponse {
  lead: LeadResponse;
  next_action?: string;
}

export interface WidgetState {
  isOpen: boolean;
  isLoading: boolean;
  isSubmitted: boolean;
  error?: string;
}
