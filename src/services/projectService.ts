import { apiRequest } from "./api";

export interface Project {
  id: string;
  name: string;
  description?: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
}

export interface DocumentResponse {
  id: string;
  project_id: string;
  name: string;
  type: string;
  status: "DRAFT" | "IN_REVIEW" | "APPROVED" | "EXPORTED";
  current_version_id?: string;
  created_at: string;
  updated_at: string;
}

export const projectService = {
  list: () => apiRequest<Project[]>("/projects/"),
  create: (data: ProjectCreate) => apiRequest<Project>("/projects/", { method: "POST", body: data }),
  get: (id: string) => apiRequest<Project>(`/projects/${id}`),
  delete: (id: string) => apiRequest<void>(`/projects/${id}`, { method: "DELETE" }),
  createDocument: (projectId: string, data: { name: string; type: string }) =>
    apiRequest<DocumentResponse>(`/projects/${projectId}/documents`, { method: "POST", body: data }),
};
