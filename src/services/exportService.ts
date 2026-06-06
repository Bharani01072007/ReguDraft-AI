import { apiRequest } from "./api";

export type ExportFormat = "pdf" | "docx" | "txt" | "markdown";

export const exportService = {
  exportDocument: (draftId: string, format: ExportFormat) =>
    apiRequest<{ downloadUrl: string }>("/export-document", {
      method: "POST",
      body: { draftId, format },
    }),
};
