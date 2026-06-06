import { apiRequest } from "./api";

export interface KnowledgeSearchResult {
  text: string;
  score: float;
  metadata: {
    guideline_type?: string;
    document_type?: string;
    section_code?: string;
    [key: string]: any;
  };
}

export interface KnowledgeSearchResponse {
  results: KnowledgeSearchResult[];
}

export const regulatoryService = {
  search: (query: string, documentType?: string, limit: number = 5) =>
    apiRequest<KnowledgeSearchResponse>("/knowledge/search", {
      method: "POST",
      body: { query, document_type: documentType, limit },
    }),
};
