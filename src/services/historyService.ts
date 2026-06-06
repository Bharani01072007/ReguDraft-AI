import { apiRequest } from "./api";

export interface DocumentVersion {
  id: string;
  document_id: string;
  version_number: number;
  content_markdown: string;
  author_id?: string;
  change_summary?: string;
  is_approved: boolean;
  created_at: string;
}

export interface VersionDiff {
  version_id: string;
  compare_with_id: string;
  diff: string[];
}

export const historyService = {
  getVersions: (documentId: string) =>
    apiRequest<DocumentVersion[]>(`/history/${documentId}/versions`),
  
  getVersion: (versionId: string) =>
    apiRequest<DocumentVersion>(`/history/versions/${versionId}`),
  
  getDiff: (versionId: string, compareWithId: string) =>
    apiRequest<VersionDiff>(`/history/versions/${versionId}/diff?compare_with_id=${compareWithId}`),
};
