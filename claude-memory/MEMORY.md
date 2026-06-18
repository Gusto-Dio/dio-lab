# Memory Index — biztech-uipath-rpa

## Lifecycle rule
Ticket aberto → tem `project_*.md`. Ticket fechado → deletar o project file; mover qualquer pendência para `work_state.md` backlog.

---

## Estado do trabalho

- [Work state — PRs, in-progress, pendências](work_state.md) — PRs abertas: #2803 (BT-73633), #2804 (BT-73683), #2799 (BT-73387), #2798 (BT-73415), #2796 (BT-73457), #2733 (BT-73075), #2726 (BT-72891)

---

## Tickets ativos

- [BT-73371 — Anthem_GroupSubmissions_MemberLevel Legacy→Modern migration](project_bt73371_anthem_groupsub_migration.md) — build passa; próximo: rename projeto (rm Legacy, mv Modern), update project.json/Config.json, PR
- [BT-73457 — Guardian PacketCollection Gmail IMAP fix](project_bt73457_guardian_imap.md) — PR #2796 aberta (v1.20.6, NCheckState portal error); aguardando merge + monitoramento Prod
- [BT-73415 — BSCA GroupSubmissions MemberLevel Edit Subscriber fix](project_bt73415_bsca_member_roster.md) — PR #2798 aberta (v6.2.8, NClick HardwareEvents + NCheckState); aguardando aprovação
- [BT-73387 — BSCA_NewHireEnrollment Screenshot errada + mensagem vaga](project_bt73387_bsca_nhe_screenshot.md) — branch criada; logs Prod analisados (EnterCoverage "navigationUnsuccesful" = provável Portal exception); Phase 5 (código) pendente para 2026-06-16
- [BT-73075 — UHC SAMx Renewal Modern](project_bt73075_uhc_samx_renewal.md) — seletor 'X' close icon fix; PR #2733 aberta; shadow com Oscar
- [BT-73427 — UHC_SamX_Renewal_Modern Eligibility Audit check](work_state.md) — fix planejado em SearchForGroup.xaml; bloqueado aguardando Carrier Order ID da Bri para capturar seletor
- [BT-73633 — BCBS_TX_GroupSubmissions_NewPlan duplicate portal applications on retry](project_bt73633_bcbs_tx_duplicate_retry.md) — PR #2803 aberta; v2.0.11 + Gusto_Benefits 1.551.1; aguardando aprovação
- [BT-73683 — BCBS_IL_MemberUpdates assembly load failure](project_bt73683_bcbs_il_memberupdates.md) — PR #2804 aberta; Gusto_Benefits 1.551.0→1.551.1; aguardando aprovação
- [BT-73296 — BCBS_TX_GroupSubmissions_NewPlan invalid access code](work_state.md) — aberto 2026-06-03; 100% fault 26 dias; diagnóstico completo; Oscar ack
- [Hackathon — BenOps RCA Agent](project_hackathon_rca_agent.md) — agente Python autônomo, Benefits Hackathon junho 2026

---

## Como trabalhamos

- [Diário de processo](process_diary.md) — fluxo padrão de ticket, regras não-negociáveis, padrões de diagnóstico, ferramentas, Orchestrator IDs, retrospectivas e backlog de melhorias

---

## Regras comportamentais

- [Criação de tickets Jira](feedback_ticket_creation.md) — usar canal Slack C01CBJW8M16 com formato padrão; nunca criar direto via API
- [Formatação negrito em tickets Slack](feedback_slack_ticket_bold_format.md) — usar `**texto**` (não `*texto*`) para negrito via slack_send_message tool
- [Formato de replies Slack](feedback_slack_reply_format.md) — replies em thread: texto corrido, sem bold/backticks/exclamação; formatação estruturada só para abertura de tickets
- [Assinatura em commits](feedback_commit_signature.md) — nunca incluir Co-Authored-By do Claude nas mensagens de commit
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
- [dio-lab workspace](reference_dio_lab.md) — repo Gusto-Dio/dio-lab; inclui `notion/runbooks.md` com 8 runbooks prontos para importar no Notion
- [Notion workspace docs](https://github.com/Gusto-Dio/dio-lab/tree/main/notion-workspace) — IDs, databases, skills, histórico do Hub BenOps e continuidade de sessão (`notion-workspace/` no dio-lab)

---

## Visão de longo prazo

- [Agente autônomo BenOps](project_autonomous_agent_vision.md) — roadmap 5 fases, arquitetura de tiers de risco
