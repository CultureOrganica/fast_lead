/**
 * Widget styles - using inline styles to avoid conflicts with host site
 */

export const getStyles = (primaryColor: string = '#2563eb') => ({
  // Widget container (hidden by default)
  container: `
    position: fixed;
    z-index: 999999;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    font-size: 14px;
    line-height: 1.5;
  `,

  // Trigger button
  button: `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 30px;
    background-color: ${primaryColor};
    color: white;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    transition: all 0.3s ease;
    z-index: 999999;
  `,

  buttonHover: `
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  `,

  // Widget popup
  popup: `
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 360px;
    max-width: calc(100vw - 40px);
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    z-index: 999999;
    animation: slideUp 0.3s ease;
  `,

  // Header
  header: `
    background-color: ${primaryColor};
    color: white;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  `,

  headerTitle: `
    margin: 0;
    font-size: 18px;
    font-weight: 600;
  `,

  closeButton: `
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    padding: 0;
    line-height: 1;
    opacity: 0.8;
    transition: opacity 0.2s;
  `,

  closeButtonHover: `
    opacity: 1;
  `,

  // Form
  form: `
    padding: 20px;
  `,

  description: `
    margin: 0 0 16px 0;
    color: #6b7280;
    font-size: 14px;
  `,

  fieldGroup: `
    margin-bottom: 16px;
  `,

  label: `
    display: block;
    margin-bottom: 6px;
    font-weight: 500;
    color: #374151;
    font-size: 14px;
  `,

  input: `
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    font-family: inherit;
    transition: border-color 0.2s;
    box-sizing: border-box;
  `,

  inputFocus: `
    outline: none;
    border-color: ${primaryColor};
    box-shadow: 0 0 0 3px ${primaryColor}20;
  `,

  inputError: `
    border-color: #ef4444;
  `,

  checkbox: `
    margin-right: 8px;
    cursor: pointer;
  `,

  checkboxLabel: `
    display: flex;
    align-items: flex-start;
    font-size: 13px;
    color: #6b7280;
    cursor: pointer;
  `,

  submitButton: `
    width: 100%;
    padding: 12px;
    background-color: ${primaryColor};
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 8px;
  `,

  submitButtonHover: `
    opacity: 0.9;
    transform: translateY(-1px);
  `,

  submitButtonDisabled: `
    opacity: 0.5;
    cursor: not-allowed;
  `,

  // Messages
  errorMessage: `
    background-color: #fee2e2;
    color: #dc2626;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 16px;
    font-size: 14px;
  `,

  successMessage: `
    background-color: #d1fae5;
    color: #059669;
    padding: 20px;
    text-align: center;
    font-size: 14px;
  `,

  // Loading spinner
  spinner: `
    border: 3px solid #f3f4f6;
    border-top: 3px solid ${primaryColor};
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 0.8s linear infinite;
    margin: 0 auto;
  `,

  // Animations (injected as <style> tag)
  animations: `
    @keyframes slideUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    @media (max-width: 480px) {
      .fl-popup {
        bottom: 0 !important;
        right: 0 !important;
        left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        border-radius: 12px 12px 0 0 !important;
      }

      .fl-button {
        bottom: 10px !important;
        right: 10px !important;
      }
    }
  `,
});
