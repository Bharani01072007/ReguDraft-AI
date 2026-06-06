import { apiRequest } from "./api";
import { DocumentResponse } from "./projectService";

export interface DocumentVersionResponse {
  id: string;
  document_id: string;
  version_number: number;
  content_markdown: string;
  change_summary?: string;
  is_approved: boolean;
  created_at: string;
}

export interface ComplianceIssue {
  severity: "WARNING" | "ERROR" | "INFO";
  section: string;
  message: string;
}

export interface ComplianceSuggestion {
  section: string;
  message: string;
}

export interface ComplianceReportResponse {
  compliance_score: number;
  issues: ComplianceIssue[];
  suggestions: ComplianceSuggestion[];
}

export interface DocumentDetailResponse {
  id: string;
  project_id: string;
  name: string;
  type: string;
  status: string;
  current_version?: DocumentVersionResponse;
  compliance_report?: ComplianceReportResponse;
}

export interface UploadedFileResponse {
  id: string;
  project_id: string;
  document_id?: string;
  file_name: string;
  file_url: string;
  file_type: string;
  file_size: number;
  created_at: string;
}

export interface ExportResponse {
  export_id: string;
  version_id: string;
  format: string;
  file_url: string;
  created_at: string;
}

export const draftService = {
  create: (projectId: string, data: { name: string; type: string }) =>
    apiRequest<DocumentResponse>(`/projects/${projectId}/documents`, { method: "POST", body: data }),

  uploadFile: (projectId: string, documentId: string | undefined, file: File) => {
    const formData = new FormData();
    formData.append("project_id", projectId);
    if (documentId) {
      formData.append("document_id", documentId);
    }
    formData.append("file", file);
    return apiRequest<UploadedFileResponse>("/documents/upload-file", {
      method: "POST",
      body: formData,
    });
  },

  generate: (documentId: string, rawInputs?: Record<string, any>) =>
    apiRequest<{
      document_id: string;
      version_id: string;
      status: string;
      compliance_score: number;
      message: string;
    }>(`/documents/${documentId}/generate`, { 
      method: "POST", 
      body: rawInputs ? { raw_inputs: rawInputs } : undefined 
    }),

  getById: (documentId: string) =>
    apiRequest<DocumentDetailResponse>(`/documents/${documentId}`),

  submitReview: (
    documentId: string,
    data: { action: "APPROVE" | "REJECT" | "EDIT"; edited_content?: string; comments?: string[] }
  ) =>
    apiRequest<{
      document_id: string;
      status: string;
      exports?: Record<string, string>;
      message: string;
    }>(`/documents/${documentId}/submit-review`, { method: "POST", body: data }),

  refine: (data: { content: string; action: "IMPROVE" | "SUMMARIZE" | "EXPAND" }) =>
    apiRequest<{ refined_content: string }>("/documents/refine", { method: "POST", body: data }),

  exportVersion: (versionId: string, format: string, themeTemplate: string = "modern_branded") =>
    apiRequest<ExportResponse>(`/exports/versions/${versionId}/export`, {
      method: "POST",
      body: { format, theme_template: themeTemplate },
    }),

  delete: (documentId: string) =>
    apiRequest<void>(`/documents/${documentId}`, { method: "DELETE" }),
};

export type Draft = DocumentResponse;
