export type ReviewSeverity = 'P0' | 'P1' | 'P2';

export type ReviewIssue = {
  id: string;
  severity: ReviewSeverity;
  title: string;
  sectionId: string;
  sectionTitle?: string;
  suggestion?: string;
};

export const reviewData = {
  conclusion: '尚未生成评审结果',
  issues: [] as ReviewIssue[],
};
