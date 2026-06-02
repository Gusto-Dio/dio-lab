# Memory Index — biztech-uipath-rpa

## Lifecycle rule
Ticket aberto → tem `project_*.md`. Ticket fechado → deletar o project file; mover qualquer pendência para `work_state.md` backlog.

---

## Estado do trabalho

- [Work state — PRs, in-progress, pendências](work_state.md) — PRs abertas: #2699 (BT-72272 CoveredCal), #2733 (BT-73075 UHC SamX), #2726 (BT-72891 CoveredCal NHE), #2744 (BT-72297 BCBS TX); pendências e backlog técnico

---

## Tickets ativos

- [BT-73075 — UHC SAMx Renewal Modern](project_bt73075_uhc_samx_renewal.md) — seletor 'X' close icon fix; PR #2733 aberta; shadow com Oscar
- [Hackathon — BenOps RCA Agent](project_hackathon_rca_agent.md) — agente Python autônomo, Benefits Hackathon junho 2026

---

## Como trabalhamos

- [Diário de processo](process_diary.md) — fluxo padrão de ticket, regras não-negociáveis, padrões de diagnóstico, ferramentas, Orchestrator IDs, retrospectivas e backlog de melhorias

---

## Regras comportamentais

- [Criação de tickets Jira](feedback_ticket_creation.md) — usar canal Slack C01CBJW8M16 com formato padrão; nunca criar direto via API
- [XAML edit protocol](feedback_xaml_skill_protocol.md) — invocar uipath:uipath-rpa antes de qualquer edit em .xaml, sem exceção
- [PR workflow](feedback_pr_workflow.md) — PR description/title sempre em inglês; nunca oferecer para aprovar PRs
- [Buildkite — branch atrás do develop](feedback_buildkite_branch_behind_develop.md) — merge develop antes de PR; git diff usa origin/develop..HEAD
- [Validar antes de implementar](feedback_validate_before_implement.md) — apresentar tese e aguardar confirmação antes de qualquer implementação
- [Orchestrator API quirks](feedback_orchestrator_api.md) — header X-UIPATH-OrganizationUnitId; folder IDs; endpoints confirmados
- [Publicar lib no Orchestrator](feedback_orchestrator_library_publish.md) — Invoke-RestMethod (Cloudflare bloqueia Python/urllib)
- [uip rpa pack](feedback_uip_rpa_pack.md) — caminho absoluto + project.uiproj + description; --skip-analyze para warnings pré-existentes

---

## Referências

- [BenOps RPA resources](reference_benops_resources.md) — Notion, GitHub skills repo (Gusto-Dio/benops-rpa-skills), Google Doc
- [Skills bundle instalado](reference_benops_skills_bundle.md) — /benops-triage-agent, /uipath-migration-repair, /uipath-test-cases-from-ticket
- [Contatos prioritários](reference_contacts.md) — Slack IDs de Sri, Oscar, Ahsen, Harinath + canal C0ANAPHL1NE
- [dio-lab workspace](reference_dio_lab.md) — repo Gusto-Dio/dio-lab para brainstorms, specs e backup de memória
- [Notion workspace docs](https://github.com/Gusto-Dio/dio-lab/tree/main/notion-workspace) — IDs, databases, skills, histórico do Hub BenOps e continuidade de sessão (`notion-workspace/` no dio-lab)

---

## Visão de longo prazo

- [Agente autônomo BenOps](project_autonomous_agent_vision.md) — roadmap 5 fases, arquitetura de tiers de risco
