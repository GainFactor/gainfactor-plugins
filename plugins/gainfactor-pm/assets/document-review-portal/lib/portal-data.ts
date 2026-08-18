export type ReviewSeverity = 'P0' | 'P1' | 'P2';

export type ReviewIssue = {
  id: string;
  severity: ReviewSeverity;
  title: string;
  sectionId: string;
  sectionTitle?: string;
  suggestion?: string;
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
  review: {
    conclusion: string;
    issues: ReviewIssue[];
  };
};

export type PortalData = {
  documents: Record<string, DocumentPortalEntry>;
};

export { portalData } from './portal-data.generated';
