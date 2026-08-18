export type ReviewIssue = { id: string; severity: 'P0' | 'P1' | 'P2'; title: string; sectionId: string; sectionTitle?: string; suggestion?: string };
export const reviewData = {
  conclusion: '有条件通过 · 3 项待处理',
  issues: [
    { id: 'PRD-001', severity: 'P1', title: '补充业务目标的量化口径', sectionId: '23-业务目标北极星指标--kr', sectionTitle: '2.3 业务目标（北极星指标 + KR）', suggestion: '明确统计周期、数据来源与负责人。' },
    { id: 'PRD-002', severity: 'P1', title: '补充异常流程的验收条件', sectionId: '42-页面功能详细设计', sectionTitle: '4.2 页面功能详细设计', suggestion: '覆盖失败、重试与权限不足场景。' },
    { id: 'PRD-003', severity: 'P2', title: '统一文档中的角色命名', sectionId: '22-用户角色', sectionTitle: '2.2 用户角色', suggestion: '避免“老师”和“教师”混用。' },
  ] as ReviewIssue[],
};
