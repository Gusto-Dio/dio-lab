# Memory Index — biztech-uipath-rpa

- [Diário de processo](process_diary.md) — como trabalhamos, tipos de tarefa, padrões de diagnóstico, ferramentas, retrospectivas e backlog de melhorias (V1/V2/C1 como prioridade)

- [Work state — PRs, in-progress, pendências](work_state.md) — 4 PRs abertas: #2741/#2699 (BT-72272 CoveredCal, merge #2741 primeiro); #2742/#2743 (BT-72297 BCBS IL/TX, prioridade 1); BT-73075 PR #2733 aguardando review; PR #2726 aguardando review
- [BT-72272 — CoveredCal Terminations](project_bt72272_coveredcal_terminations.md) — PRs #2741 (Gusto_Benefits lib 1.550.8) + #2699 (processo 6.0.5) aguardando review; Staging validado 2 tx (incl. multi-policy-year StepForPolicyYear)
- [BT-72297 — BCBS TX/IL GroupSubmissions MemberLevel](work_state.md) — PRs #2742 (IL v2.1.2, 5 tx) + #2743 (TX v2.1.3, 1 tx) abertas com branches separadas; Staging publicado; portalPlan regex bug + dep add skip corrigidos
- [Hackathon — BenOps RCA Agent](project_hackathon_rca_agent.md) — agente Python autônomo, Benefits Hackathon junho 2026; spec+pitch+arch+demo em github.com/Gusto-Dio/dio-lab/benops-rca-agent/
- [dio-lab — workspace pessoal](reference_dio_lab.md) — repo privado Gusto-Dio/dio-lab para brainstorms, specs e experimentos
- [BT-73075 — UHC SAMx Renewal Modern](project_bt73075_uhc_samx_renewal.md) — seletor 'X' close icon quebrado em 5 lugares (3 arquivos), portal mudou de SAMX→SamxOne SSO, shadow com Oscar; PR #2733 aberta
- [XAML edit skill protocol](feedback_xaml_skill_protocol.md) — invocar uipath:uipath-rpa antes de qualquer edit em .xaml, sem exceção
- [BenOps RPA resources](reference_benops_resources.md) — Notion (pasta RPA BenOps), GitHub skills repo (Gusto-Dio/benops-rpa-skills), Google Doc tab
- [Contatos prioritários](reference_contacts.md) — Slack IDs de Sri, Oscar, Ahsen, Harinath + canal do time
- [Skills publicadas](reference_benops_resources.md) — benops-rpa-setup + benops-ticket-investigation no repo Gusto-Dio/benops-rpa-skills
- [Visão agente autônomo](project_autonomous_agent_vision.md) — roadmap em 5 fases, arquitetura de tiers de risco, métricas de maturidade
- [uip rpa pack — requisitos](feedback_uip_rpa_pack.md) — caminho absoluto + project.uiproj + description obrigatório; --skip-analyze para warnings pré-existentes
- [Orchestrator API — quirks](feedback_orchestrator_api.md) — header X-UIPATH-OrganizationUnitId (numérico); releases em folder 48382 (Benefits); uploads em 946022 (Benefits/CarrierAutomation); AddQueueItem via UiPathODataSvc.AddQueueItem
- [Anthem — estabilidade pendente](project_anthem_stability_todo.md) — waits de carregamento entre páginas; retomar após merge das PRs
- [PR workflow](feedback_pr_workflow.md) — Diogenes sempre aprova PRs manualmente; nunca oferecer para aprovar
- [Validar antes de implementar](feedback_validate_before_implement.md) — apresentar tese ao usuário e aguardar confirmação antes de qualquer implementação
- [Publicar biblioteca no Orchestrator](feedback_orchestrator_library_publish.md) — usar REST API via Invoke-RestMethod (não CLI nem Python/urllib — Cloudflare bloqueia); folder 48382 para releases, 946022 para packages
- [Buildkite — branch atrás do develop](feedback_buildkite_branch_behind_develop.md) — fazer merge do develop antes de PR; git diff usa origin/develop..HEAD e inclui processos não relacionados se branch estiver atrás
- [Skills biztech-rpa-skills-bundle](reference_benops_skills_bundle.md) — /benops-triage-agent, /uipath-migration-repair, /uipath-test-cases-from-ticket instaladas em 2026-05-19
