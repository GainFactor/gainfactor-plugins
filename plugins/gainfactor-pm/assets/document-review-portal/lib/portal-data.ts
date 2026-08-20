export type ReviewSeverity = 'P0' | 'P1' | 'P2';
export type ReviewIssue = { id: string; severity: ReviewSeverity; title: string; sectionId: string; sectionTitle?: string; suggestion?: string };

type PortalModuleBase = { id: string; title?: string; description?: string };
export type PortalModule =
  | (PortalModuleBase & { type: 'metrics'; items: Array<{ label: string; value: string }> })
  | (PortalModuleBase & { type: 'cards'; items: Array<{
      title: string; eyebrow?: string; description?: string; quote?: string;
      image?: string; imageAlt?: string; fields?: Array<{ label: string; value: string }>;
    }> })
  | (PortalModuleBase & { type: 'steps'; items: Array<{ title?: string; content: string }> })
  | (PortalModuleBase & { type: 'callout'; content: string; tone?: 'info' | 'success' | 'warning' });

export type PortalPresentation = {
  schemaVersion: 1;
  layout: 'document' | 'report' | 'reference';
  modules: PortalModule[];
};

export type DocumentPortalEntry = {
  sourceSlug: string;
  group: 'product-requirements' | 'technical-design' | 'quality-delivery' | 'other';
  documentType: string;
  collection: string;
  version: string;
  status: string;
  owner: string;
  updated: string;
  presentation?: PortalPresentation;
  review: { conclusion: string; issues: ReviewIssue[] };
};

export type PortalData = { documents: Record<string, DocumentPortalEntry> };
export { portalData } from './portal-data.generated';
